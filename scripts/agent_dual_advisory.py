#!/usr/bin/env python3
"""Dual advisory v0: Gemini (API) + GGUF on the workflow runner (default Qwen2.5-1.5B Instruct q4).

Both run **in parallel** (threads) after deterministic ``run-next``. **Gemini** sees the full
file bundle; **runner GGUF** uses a **lean** bundle (``run-next`` **without** the human cross-lane
section + compact JSON + short reports + **coverage_summary** from correlate + two analytics slices)
so small ``n_ctx`` still fits and the small model does not blend brand vs personal numbers.
Advisory only — not ``run_intent`` / ``batch_generate``.

Outputs (per lane ``brand`` | ``personal``):

- ``data/reports/agent-insight-YYYY-WW-{lane}-gemini.md``
- ``data/reports/agent-insight-YYYY-WW-{lane}-runner.md`` (GGUF; CPU on GitHub-hosted runners)

  pip install llama-cpp-python   # runner path only; Gemini uses stdlib + REST
  GEMINI_API_KEY=... python scripts/agent_dual_advisory.py --lane brand --week 2026-W16
  GEMINI_API_KEY_PERSONAL=... python scripts/agent_dual_advisory.py --lane personal --week 2026-W16

**Gemini rate limits (optional env):** ``GEMINI_MIN_INTERVAL_SEC`` (default ``6``) — minimum
seconds between completed Gemini HTTP calls in this process (reduces 429s when re-running locally).
``GEMINI_MAX_RETRIES`` (default ``5``) — retries on HTTP 429 / 503 with backoff and
``Retry-After`` when the API sends it. Set interval ``0`` to disable spacing only.
``GEMINI_429_MIN_SLEEP_SEC`` (default ``0``) — floor on **retry** sleep after 429/503 (e.g. ``20`` under **~5 RPM** free-tier caps so retries do not stack in the same minute).

**Default REST model** when ``GEMINI_MODEL`` is unset: ``gemini-2.5-flash`` (not 2.0). Override per project via env / Actions **Variable** ``GEMINI_MODEL`` if you need another tier.

**Runner output:** ``MAX_RUNNER_TOKENS`` (default ``1536``) — GGUF ``max_tokens``; raise if logs show ``finish_reason=length`` and markdown is cut off.

**Gemini output:** ``GEMINI_MAX_OUTPUT_TOKENS`` (default ``4096``). For **2.5** models, ``thinkingConfig.thinkingBudget`` defaults to **0** so hidden reasoning does not eat the whole budget (see [Gemini thinking](https://ai.google.dev/gemini-api/docs/thinking)); set ``GEMINI_THINKING_BUDGET=omit`` to omit that block for older model ids.

**CI log prefixes:** ``[runner-advisory]`` (GGUF), ``[gemini-advisory]`` (REST usage / ``finishReason`` / prose size).

Week label: ISO calendar (same as ``audit_channel`` / ``run_next_report``).
"""

from __future__ import annotations

import argparse
import json
import os
import random
import shutil
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
REPORTS = _REPO / "data" / "reports"
DATA = _REPO / "data"

_DEFAULT_GEMINI = "gemini-2.5-flash"
MAX_CONTEXT_GEMINI = 24_000
# Runner GGUF: small n_ctx; char→token ratio ~3–4 for EN/JSON — keep prompt+context safely under n_ctx.
RUNNER_BUNDLE_MAX_CHARS = 5200
# Default output cap (was 512; logs showed finish_reason=length mid-markdown). Override: ``MAX_RUNNER_TOKENS`` env.
_DEFAULT_MAX_RUNNER_TOKENS = 1536
_LLAMA_N_CTX = 4096

# ``run_next_report.py`` appends a cross-lane section for humans; strip it from runner CONTEXT only
# (``build_bundle`` for Gemini still includes the full run-next file).
_RUN_NEXT_CROSS_READ_HEADER = {
    "personal": "## Brand lane (cross-read only)",
    "brand": "## Personal lane (context only)",
}
_RUN_NEXT_PRODUCTION_HOOKS = "## Production hooks (manual)"


def max_runner_tokens() -> int:
    """Effective GGUF ``max_tokens``; clamped so prompt + generation stays under ``n_ctx``."""
    raw = (os.environ.get("MAX_RUNNER_TOKENS") or "").strip()
    if raw:
        try:
            return max(128, min(3072, int(raw)))
        except ValueError:
            pass
    return _DEFAULT_MAX_RUNNER_TOKENS


# Backward-compatible name for docs/tests (effective cap is ``max_runner_tokens()``).
MAX_RUNNER_TOKENS = _DEFAULT_MAX_RUNNER_TOKENS
DEFAULT_GGUF = Path.home() / ".cache" / "living-agent" / "qwen2.5-1.5b-instruct-q4_k_m.gguf"


def _runner_log(msg: str) -> None:
    """Lines show in GitHub Actions job logs for the non-cloud path."""
    print(f"[runner-advisory] {msg}", flush=True)


def _gemini_log(msg: str) -> None:
    """Gemini REST path — same job logs as ``[runner-advisory]``, distinct prefix."""
    print(f"[gemini-advisory] {msg}", flush=True)


def _log_gemini_response(
    raw: dict,
    prose: str,
    *,
    lane: str,
    week: str,
    prompt_chars: int,
    context_chars: int,
) -> None:
    """One place for usage / finishReason logging after ``generateContent`` (diagnose short files)."""
    _gemini_log(f"lane={lane} week={week}")
    mid = _gemini_model()
    mv = raw.get("modelVersion") or "(missing)"
    _gemini_log(
        f"REST model_id={mid!r} response.modelVersion={mv!r} "
        f"prompt_chars={prompt_chars} context_chars={context_chars}"
    )

    um = raw.get("usageMetadata")
    if isinstance(um, dict):
        bits = [f"{k}={um[k]}" for k in ("promptTokenCount", "candidatesTokenCount", "totalTokenCount", "thoughtsTokenCount") if k in um]
        _gemini_log("usageMetadata: " + (", ".join(bits) if bits else str(um)[:240]))
    else:
        _gemini_log("usageMetadata: (missing)")

    cands = raw.get("candidates")
    if isinstance(cands, list) and cands and isinstance(cands[0], dict):
        fr = cands[0].get("finishReason", "(missing)")
        _gemini_log(f"candidates[0].finishReason={fr!r} prose_chars={len(prose)}")
        fru = str(fr).upper()
        if fru in ("MAX_TOKENS", "OTHER", "FINISHREASON_UNSPECIFIED", "UNSPECIFIED", "MALFORMED_FUNCTION_CALL"):
            _gemini_log(
                "note: finishReason may indicate truncation or tool-shape issues — "
                "consider raising generationConfig.maxOutputTokens or changing GEMINI_MODEL"
            )
    else:
        _gemini_log("candidates: (missing or empty)")

    pfb = raw.get("promptFeedback")
    if isinstance(pfb, dict) and pfb.get("blockReason"):
        _gemini_log(f"promptFeedback.blockReason={pfb.get('blockReason')!r}")

    if "##" not in prose and len(prose) < 800:
        _gemini_log(
            "note: prose is short or has no '##' section headings — possible early stop or "
            "reasoning/thought tokens using output budget (see thoughtsTokenCount if present)"
        )


DEFAULT_GGUF_URL = (
    "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/"
    "qwen2.5-1.5b-instruct-q4_k_m.gguf"
)

# Qwen2.5 ChatML specials (HF tokenizer 151644 / 151645). Built with concat so literals are never mangled.
_QWEN_IM_START = "<|" + "im_start" + "|>"
_QWEN_IM_END = "<|" + "im_end" + "|>"


def iso_week_suffix(utc_now: datetime | None = None) -> str:
    """YYYY-Www for filenames (calendar ISO week), matching ``run_next_report``."""
    now = utc_now or datetime.now(timezone.utc)
    y, w, _ = now.isocalendar()
    return f"{y}-W{w:02d}"


def _read(path: Path, cap: int) -> str:
    if not path.exists():
        rel = path.relative_to(_REPO) if path.is_relative_to(_REPO) else path
        return f"(missing: {rel})"
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) > cap:
        return text[:cap] + f"\n\n… truncated ({len(text)} chars total)"
    return text


def _strip_run_next_cross_lane_section(body: str, lane: str) -> str:
    """Drop ``run-next`` cross-lane block so runner GGUF stays single-lane (matches ``run_next_report.py`` headings)."""
    if lane not in _RUN_NEXT_CROSS_READ_HEADER:
        return body
    start_h = _RUN_NEXT_CROSS_READ_HEADER[lane]
    i0 = body.find(start_h)
    if i0 == -1:
        return body
    i1 = body.find(_RUN_NEXT_PRODUCTION_HOOKS, i0 + len(start_h))
    if i1 == -1:
        return body
    return body[:i0].rstrip() + "\n\n" + body[i1:].lstrip()


def build_bundle(lane: str, week: str) -> str:
    parts: list[str] = []
    if lane == "personal":
        paths = [
            REPORTS / f"{week}-personal.md",
            REPORTS / f"run-next-{week}-personal.md",
            REPORTS / "run-intent-blocked-personal.md",
            DATA / "suggestions_personal.json",
            DATA / "analytics_personal.json",
        ]
    else:
        paths = [
            REPORTS / f"{week}.md",
            REPORTS / f"run-next-{week}.md",
            REPORTS / "run-intent-blocked.md",
            DATA / "suggestions.json",
            DATA / "analytics.json",
        ]
    for p in paths:
        parts.append(f"### {p.as_posix()}\n\n{_read(p, 8000)}")
    return "\n\n".join(parts)


def _dim_coverage_stats(block: object) -> dict[str, int]:
    """One correlate ``coverage`` sub-map → tiny counts (no per-label explosion)."""
    if not isinstance(block, dict):
        return {"labels": 0, "produced_at_least_one": 0, "produced_zero_views": 0}
    labels = produced = zero_views = 0
    for v in block.values():
        if not isinstance(v, dict):
            continue
        labels += 1
        t = int(v.get("total") or 0)
        w = int(v.get("with_views") or 0)
        if t > 0:
            produced += 1
        if t > 0 and w == 0:
            zero_views += 1
    return {
        "labels": labels,
        "produced_at_least_one": produced,
        "produced_zero_views": zero_views,
    }


def _compact_suggestions(path: Path, max_chars: int = 3400) -> str:
    """Correlate JSON without huge ``coverage`` grids — top rows + stats + coverage_summary."""
    if not path.exists():
        rel = path.relative_to(_REPO) if path.is_relative_to(_REPO) else path
        return f"(missing: {rel})"
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError:
        return _read(path, 1200)
    slim: dict[str, object] = {
        "generated_at": data.get("generated_at"),
        "overall_avg_retention": data.get("overall_avg_retention"),
        "overall_avg_watch_minutes_per_video": data.get("overall_avg_watch_minutes_per_video"),
        "videos_analyzed": data.get("videos_analyzed"),
        "videos_with_views": data.get("videos_with_views"),
        "suggestions": (data.get("suggestions") or [])[:25],
    }
    cov = data.get("coverage")
    if isinstance(cov, dict):
        slim["coverage_summary"] = {
            "moods": _dim_coverage_stats(cov.get("moods")),
            "art_periods": _dim_coverage_stats(cov.get("art_periods")),
            "music_styles": _dim_coverage_stats(cov.get("music_styles")),
            "art_music_combos": _dim_coverage_stats(cov.get("art_music_combos")),
        }
    text = json.dumps(slim, indent=2, ensure_ascii=False)
    if len(text) > max_chars:
        return text[: max_chars - 40] + "\n… truncated suggestions json\n"
    return text


def _compact_analytics(path: Path, max_chars: int = 2400) -> str:
    """Top videos by views + by retention (small rows; analytics JSON is huge on disk)."""
    if not path.exists():
        rel = path.relative_to(_REPO) if path.is_relative_to(_REPO) else path
        return f"(missing: {rel})"
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError:
        return _read(path, 800)
    videos = data.get("videos") or []

    def _views(v: dict) -> int:
        m = v.get("metrics") or {}
        return int(m.get("views") or 0)

    def _avg_pct(v: dict) -> float:
        m = v.get("metrics") or {}
        try:
            return float(m.get("average_view_percentage") or 0.0)
        except (TypeError, ValueError):
            return 0.0

    def _row(v: dict) -> dict:
        m = v.get("metrics") or {}
        return {
            "title": ((v.get("title") or "")[:90]),
            "views": m.get("views"),
            "avg_pct": m.get("average_view_percentage"),
            "watch_min": m.get("watch_time_minutes"),
        }

    top_views = sorted(videos, key=_views, reverse=True)[:12]
    min_views = 2
    qualified = [v for v in videos if _views(v) >= min_views]
    top_ret = sorted(qualified, key=_avg_pct, reverse=True)[:8]
    slim = {
        "fetched_at": data.get("fetched_at"),
        "n_videos": len(videos),
        "top_by_views": [_row(v) for v in top_views],
        "top_by_avg_view_pct_min_views_2": [_row(v) for v in top_ret],
    }
    text = json.dumps(slim, ensure_ascii=False, separators=(",", ":"))
    if len(text) > max_chars:
        return text[: max_chars - 30] + "…"
    return text


def build_runner_bundle(lane: str, week: str) -> str:
    """Lean context for small GGUF: run-next (single-lane) + compact JSON + short prose (fits ``n_ctx``)."""
    if lane == "personal":
        weekly = REPORTS / f"{week}-personal.md"
        run_next = REPORTS / f"run-next-{week}-personal.md"
        blocked = REPORTS / "run-intent-blocked-personal.md"
        sug_path = DATA / "suggestions_personal.json"
        ana_path = DATA / "analytics_personal.json"
        scope_note = (
            "**Advisory lane:** `personal` only — CONTEXT uses `*-personal.md`, "
            "`suggestions_personal.json`, `analytics_personal.json`. "
            "Do not cite brand-channel totals; cross-lane excerpts are omitted here."
        )
    else:
        weekly = REPORTS / f"{week}.md"
        run_next = REPORTS / f"run-next-{week}.md"
        blocked = REPORTS / "run-intent-blocked.md"
        sug_path = DATA / "suggestions.json"
        ana_path = DATA / "analytics.json"
        scope_note = (
            "**Advisory lane:** `brand` only — CONTEXT uses `YYYY-WW.md` (brand), "
            "`suggestions.json`, `analytics.json`. "
            "Do not cite personal-channel totals; cross-lane excerpts are omitted here."
        )

    run_next_body = _strip_run_next_cross_lane_section(_read(run_next, 4500), lane)

    parts = [
        "### runner scope\n\n" + scope_note,
        "### run-next (priority)\n\n" + run_next_body,
        "### weekly report\n\n" + _read(weekly, 2800),
        "### run-intent blocked\n\n" + _read(blocked, 1200),
        "### suggestions (compact)\n\n" + _compact_suggestions(sug_path),
        "### analytics (compact top videos + retention slice)\n\n" + _compact_analytics(ana_path),
    ]
    text = "\n\n".join(parts)
    if len(text) > RUNNER_BUNDLE_MAX_CHARS:
        return text[: RUNNER_BUNDLE_MAX_CHARS - 40] + "\n… hard-capped for runner ctx\n"
    return text


def _header_gemini(lane: str, week: str) -> str:
    return _header("Gemini (API)", lane, week)


def _header_runner(lane: str, week: str) -> str:
    return _header("Runner GGUF (CPU)", lane, week)


def _header(title: str, lane: str, week: str) -> str:
    return "\n".join(
        [
            f"# Agent advisory — {title} ({lane}, {week})",
            "",
            "> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. "
            "Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.",
            "",
            "---",
            "",
        ]
    )


def _gemini_model() -> str:
    return (os.environ.get("GEMINI_MODEL") or _DEFAULT_GEMINI).strip() or _DEFAULT_GEMINI


def _gemini_url() -> str:
    m = _gemini_model()
    return f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent"


_DEFAULT_GEMINI_MAX_OUTPUT = 4096


def _gemini_max_output_tokens() -> int:
    """Cap on visible + internal tokens for ``generateContent`` (raise if prose truncates)."""
    raw = (os.environ.get("GEMINI_MAX_OUTPUT_TOKENS") or "").strip()
    if not raw:
        return _DEFAULT_GEMINI_MAX_OUTPUT
    try:
        return max(256, min(8192, int(raw)))
    except ValueError:
        return _DEFAULT_GEMINI_MAX_OUTPUT


def _gemini_thinking_config() -> dict | None:
    """Return ``thinkingConfig`` dict for the REST payload, or ``None`` to omit.

    Gemini **2.5** can use a large hidden thinking budget; ``thinkingBudget=0`` disables it
    so ``maxOutputTokens`` remains available for markdown. Older ids (e.g. 2.0) omit this key.
    Set ``GEMINI_THINKING_BUDGET=omit`` to never send ``thinkingConfig``.
    """
    if (os.environ.get("GEMINI_THINKING_BUDGET") or "").strip().lower() in ("omit", "none"):
        return None
    if "2.5" not in _gemini_model().lower():
        return None
    raw = (os.environ.get("GEMINI_THINKING_BUDGET") or "0").strip()
    try:
        n = int(raw)
    except ValueError:
        n = 0
    return {"thinkingBudget": n}


_gemini_spacing_lock = threading.Lock()
_gemini_last_http_end = 0.0


def _gemini_min_interval_sec() -> float:
    raw = (os.environ.get("GEMINI_MIN_INTERVAL_SEC") or "").strip()
    if not raw:
        return 6.0
    try:
        return max(0.0, float(raw))
    except ValueError:
        return 6.0


def _gemini_max_retries() -> int:
    raw = (os.environ.get("GEMINI_MAX_RETRIES") or "").strip()
    if not raw:
        return 5
    try:
        return max(0, int(raw))
    except ValueError:
        return 5


def _gemini_429_min_sleep_sec() -> float:
    """Minimum seconds to sleep before retrying after HTTP 429 / 503 (free-tier RPM safety)."""
    raw = (os.environ.get("GEMINI_429_MIN_SLEEP_SEC") or "").strip()
    if not raw:
        return 0.0
    try:
        return max(0.0, float(raw))
    except ValueError:
        return 0.0


def _wait_gemini_spacing() -> None:
    """Space out Gemini calls in this process (free-tier RPM / burst)."""
    interval = _gemini_min_interval_sec()
    if interval <= 0:
        return
    global _gemini_last_http_end
    with _gemini_spacing_lock:
        now = time.monotonic()
        wait_s = _gemini_last_http_end + interval - now
    if wait_s > 0:
        time.sleep(wait_s)


def _mark_gemini_http_done() -> None:
    global _gemini_last_http_end
    with _gemini_spacing_lock:
        _gemini_last_http_end = time.monotonic()


def _retry_after_seconds(err: urllib.error.HTTPError) -> float | None:
    if err.headers is None:
        return None
    h = err.headers.get("Retry-After")
    if not h:
        return None
    try:
        return max(0.0, float(h))
    except ValueError:
        return None


class GeminiHttpError(Exception):
    """Non-retryable Gemini REST failure or exhausted 429/503 retries."""

    def __init__(self, code: int, body: str):
        self.code = code
        self.body = body
        super().__init__(f"Gemini HTTP {code}")


def _gemini_generate_json(url: str, payload: dict) -> dict:
    """POST generateContent; retries 429/503. Caller should call _wait_gemini_spacing() once first."""
    data = json.dumps(payload).encode("utf-8")
    max_retries = _gemini_max_retries()
    for attempt in range(max_retries + 1):
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                raw = json.loads(resp.read().decode("utf-8"))
            _mark_gemini_http_done()
            return raw
        except urllib.error.HTTPError as e:
            _mark_gemini_http_done()
            body = e.read().decode("utf-8", errors="replace")[:4000]
            if e.code not in (429, 503) or attempt >= max_retries:
                raise GeminiHttpError(e.code, body) from e
            ra = _retry_after_seconds(e)
            base = min(120.0, (2.0**attempt) + random.uniform(0, 0.5))
            floor = _gemini_429_min_sleep_sec()
            sleep_s = max(ra or 0.0, base, floor)
            print(
                f"Gemini HTTP {e.code}; sleeping {sleep_s:.1f}s then retry "
                f"({attempt + 1}/{max_retries + 1} attempts)",
                flush=True,
            )
            time.sleep(sleep_s)
        except OSError:
            _mark_gemini_http_done()
            raise


def _gemini_api_key(lane: str) -> str:
    """Brand: ``GEMINI_API_KEY``. Personal: that or ``GEMINI_API_KEY_PERSONAL`` (personal analytics CI)."""
    generic = os.environ.get("GEMINI_API_KEY", "").strip()
    if lane == "personal":
        return generic or os.environ.get("GEMINI_API_KEY_PERSONAL", "").strip()
    return generic


def write_gemini(lane: str, week: str, bundle: str) -> Path:
    out = REPORTS / f"agent-insight-{week}-{lane}-gemini.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    key = _gemini_api_key(lane)
    if not key:
        hint = (
            "set repository secret `GEMINI_API_KEY_PERSONAL` (personal workflow) or env `GEMINI_API_KEY`."
            if lane == "personal"
            else "set repository secret `GEMINI_API_KEY` (brand workflow) or env `GEMINI_API_KEY`."
        )
        out.write_text(
            _header_gemini(lane, week) + f"_Gemini skipped:_ {hint}\n",
            encoding="utf-8",
        )
        print(f"Wrote {out} (Gemini skipped, no API key)")
        return out

    ctx_used = bundle[:MAX_CONTEXT_GEMINI]
    prompt = (
        "You are a metrics-aware creative advisor for a YouTube ambient music channel.\n"
        "You ONLY read the CONTEXT block below (committed repo files / excerpts from the analytics pipeline). "
        "You did NOT query YouTube live.\n"
        "Start with 2–3 sentences: confirm you reviewed that bundle and what you will do in this answer.\n"
        "Then use ONLY that CONTEXT. If the planner blocked or data is thin, say so plainly.\n"
        "Output GitHub-flavored markdown with: ## What I reviewed, ## Summary, ## Risks / caveats, "
        "## Insights (numbered 1–5: one paragraph each; tie mood/style when CONTEXT supports it; "
        "prefix **Speculative:** when not directly supported), ## Experiments or packaging ideas (bullets).\n"
        "Do not invent statistics; quote approximate values only if present in CONTEXT.\n"
        "Avoid large duplicate tables unless CONTEXT has no prose summary.\n\n"
        f"## CONTEXT\n\n{ctx_used}"
    )
    gen_cfg: dict = {"temperature": 0.35, "maxOutputTokens": _gemini_max_output_tokens()}
    th = _gemini_thinking_config()
    if th is not None:
        gen_cfg["thinkingConfig"] = th
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": gen_cfg,
    }
    url = f"{_gemini_url()}?key={key}"
    _wait_gemini_spacing()
    try:
        raw = _gemini_generate_json(url, payload)
    except GeminiHttpError as e:
        text = _header_gemini(lane, week) + f"## API error\n\n```\n{e.code}\n{e.body}\n```\n"
        out.write_text(text, encoding="utf-8")
        print(f"Gemini HTTP {e.code}; wrote {out}")
        return out
    except OSError as e:
        text = _header_gemini(lane, week) + f"## Request failed\n\n`{type(e).__name__}`: {e}\n"
        out.write_text(text, encoding="utf-8")
        print(f"Gemini error: {e}; wrote {out}")
        return out

    try:
        parts = raw["candidates"][0]["content"]["parts"]
        prose = "".join(p.get("text", "") for p in parts).strip() or "(empty model response)"
    except (KeyError, IndexError, TypeError):
        prose = f"```json\n{json.dumps(raw, indent=2)[:8000]}\n```"
        _gemini_log("could not parse candidates[0].content.parts — writing raw JSON excerpt to report")

    _log_gemini_response(
        raw if isinstance(raw, dict) else {},
        prose,
        lane=lane,
        week=week,
        prompt_chars=len(prompt),
        context_chars=len(ctx_used),
    )

    out.write_text(_header_gemini(lane, week) + prose + "\n", encoding="utf-8")
    print(f"Wrote {out} (Gemini)")
    return out


def _gguf_url() -> str:
    return (os.environ.get("AGENT_GGUF_URL") or DEFAULT_GGUF_URL).strip() or DEFAULT_GGUF_URL


def _ensure_gguf(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.stat().st_size > 1_000_000:
        mb = path.stat().st_size / (1024 * 1024)
        _runner_log(f"GGUF present: {path} ({mb:.1f} MiB)")
        return
    url = _gguf_url()
    _runner_log(f"Downloading GGUF → {path} (url tail: …{url[-60:]})")
    req = urllib.request.Request(url, headers={"User-Agent": "living-ambient-engine-agent-dual/1"})
    with urllib.request.urlopen(req, timeout=900) as resp, path.open("wb") as out:
        shutil.copyfileobj(resp, out, length=1024 * 1024)
    mb = path.stat().st_size / (1024 * 1024)
    _runner_log(f"Download complete ({mb:.1f} MiB)")


def _qwen25_chat_prompt(*, system: str, user: str) -> str:
    """ChatML shape for Qwen2.x Instruct GGUFs (not Llama ``[INST]`` — wrong template → empty output)."""
    s, e = _QWEN_IM_START, _QWEN_IM_END
    return (
        f"{s}system\n{system.strip()}{e}\n"
        f"{s}user\n{user.strip()}{e}\n"
        f"{s}assistant\n"
    )


def write_runner_gguf(lane: str, week: str, bundle: str) -> Path:
    out = REPORTS / f"agent-insight-{week}-{lane}-runner.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    _runner_log(f"lane={lane} week={week} (non-cloud GGUF path)")

    try:
        from llama_cpp import Llama  # noqa: WPS433
    except ImportError:
        out.write_text(
            _header_runner(lane, week)
            + "_Runner LLM skipped:_ `llama-cpp-python` not installed (e.g. `pip install llama-cpp-python`).\n",
            encoding="utf-8",
        )
        _runner_log("skip: llama_cpp import failed")
        print(f"Wrote {out} (runner skipped, no llama_cpp)")
        return out

    gguf = Path(os.environ.get("AGENT_GGUF_PATH", str(DEFAULT_GGUF))).expanduser()
    try:
        _ensure_gguf(gguf)
    except OSError as e:
        out.write_text(
            _header_runner(lane, week) + f"## Model download failed\n\n`{type(e).__name__}`: {e}\n",
            encoding="utf-8",
        )
        _runner_log(f"download failed: {type(e).__name__}: {e}")
        print(f"Runner GGUF download failed: {e}; wrote {out}")
        return out

    ctx_used = bundle[:RUNNER_BUNDLE_MAX_CHARS]
    system = (
        "You are a compact advisor for a YouTube ambient music channel. "
        "You ONLY see the user CONTEXT (markdown + JSON excerpts from this repo’s analytics run). "
        "You did NOT call YouTube or the internet.\n"
        "Treat CONTEXT as the sole evidence. Do not reference files you did not read here; "
        "do not answer with pointers only (e.g. “see run-next”) — synthesize takeaways in your own words.\n"
        "Required shape (GitHub-flavored markdown, stay concise—complete sections beat padding, no outer ``` fences):\n"
        "## What I reviewed — 2–3 bullets naming concrete CONTEXT blocks "
        "(e.g. run-next, weekly report, suggestions JSON incl. coverage_summary if present, analytics compact).\n"
        "## Summary — 2–4 sentences: the main story the metrics tell (thin data is OK to name explicitly).\n"
        "## Insights — numbered 1–5. Each: one short paragraph. "
        "Use **at least three distinct numeric facts** copied from CONTEXT (counts, %, averages, views) across these items; "
        "every number must appear verbatim in CONTEXT (no rounding invented, no new totals). "
        "Prefer mood / art_period / music_style / packaging angles when CONTEXT supports them. "
        "If an item is not directly supported, start that paragraph with **Speculative:**.\n"
        "## Risks — short bullets (thin data, confounders, contradictions inside CONTEXT).\n"
        "## Next tries — bullets: concrete experiments grounded in what CONTEXT shows; no invented KPIs.\n"
        "Do not paste large tables; at most one tiny 3-row markdown table if essential. "
        "If a metric is missing from CONTEXT, say **Not in CONTEXT** instead of guessing."
    )
    user = f"CONTEXT:\n{ctx_used}"
    prompt = _qwen25_chat_prompt(system=system, user=user)
    prompt_chars = len(prompt)
    est_prompt_tokens = max(1, int(prompt_chars / 3.5))
    n_threads = int(os.environ.get("AGENT_LLAMA_THREADS", "4"))
    _runner_log(
        f"context: bundle_chars={len(ctx_used)} prompt_chars≈{prompt_chars} "
        f"est_input_tokens≈{est_prompt_tokens} (rough; model tokenizer may differ)"
    )
    cap = max_runner_tokens()
    _runner_log(
        f"llama: n_ctx={_LLAMA_N_CTX} max_output_tokens={cap} "
        f"n_threads={n_threads} n_gpu_layers=0"
    )

    try:
        t0 = time.perf_counter()
        llm = Llama(
            model_path=str(gguf),
            n_ctx=_LLAMA_N_CTX,
            n_threads=n_threads,
            n_gpu_layers=0,
            verbose=False,
        )
        t_load = time.perf_counter()
        _runner_log(f"model load wall_s={t_load - t0:.2f}s")
        result = llm(
            prompt,
            max_tokens=cap,
            temperature=0.25,
            # Qwen2.5: stop at turn end and next role header (not Llama ``[/INST]`` / ``</s>``).
            stop=[_QWEN_IM_END, _QWEN_IM_START],
        )
        t_done = time.perf_counter()
        choice = (result.get("choices") or [{}])[0]
        text = (choice.get("text") or "").strip()
        fr = choice.get("finish_reason")
        if not text:
            _runner_log(f"empty completion finish_reason={fr!r} choice_keys={list(choice.keys())}")
            text = "(empty runner response)"
        elif fr == "length":
            _runner_log(
                "finish_reason=length: hit max_tokens — output may be truncated mid-sentence; "
                "raise MAX_RUNNER_TOKENS env or shorten the runner system prompt / CONTEXT cap"
            )
        _runner_log(
            f"inference wall_s={t_done - t_load:.2f}s total_since_start_s={t_done - t0:.2f}s "
            f"output_chars={len(text)} finish_reason={fr!r}"
        )
    except Exception as e:  # noqa: BLE001 — advisory path; always write markdown
        text = f"## Inference error\n\n`{type(e).__name__}`: {e}\n"
        _runner_log(f"inference error: {type(e).__name__}: {e}")

    out.write_text(_header_runner(lane, week) + text + "\n", encoding="utf-8")
    _runner_log(f"wrote {out.relative_to(_REPO) if out.is_relative_to(_REPO) else out}")
    print(f"Wrote {out} (runner GGUF)")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Dual LLM advisory: Gemini + runner GGUF (v0)")
    ap.add_argument("--lane", choices=("brand", "personal"), required=True)
    ap.add_argument(
        "--week",
        default="",
        help="ISO week label e.g. 2026-W16 (default: current UTC week)",
    )
    args = ap.parse_args()
    week = args.week.strip() or iso_week_suffix()
    bundle_gemini = build_bundle(args.lane, week)
    bundle_runner = build_runner_bundle(args.lane, week)

    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = {
            pool.submit(write_gemini, args.lane, week, bundle_gemini): "gemini",
            pool.submit(write_runner_gguf, args.lane, week, bundle_runner): "runner",
        }
        for fut in as_completed(futures):
            fut.result()


if __name__ == "__main__":
    main()
