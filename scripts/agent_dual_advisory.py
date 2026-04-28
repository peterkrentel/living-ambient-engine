#!/usr/bin/env python3
"""Dual advisory v0: Gemini (API) + GGUF on the workflow runner (default Qwen2.5-1.5B Instruct q4).

Both run **in parallel** (threads) after deterministic ``run-next``. **Gemini** sees the full
file bundle; **runner GGUF** uses a **lean** bundle: **deterministic facts** JSON, a **trimmed
run-next** (snapshot digest + actionable tail, cross-lane stripped in the tail), compact JSON,
short weekly/blocked caps, **coverage_summary** + compact analytics slices — so small ``n_ctx``
fits and the small model does not blend brand vs personal numbers.
Advisory only — not ``run_intent`` / ``batch_generate``.

Outputs (per lane ``brand`` | ``personal``):

- ``data/reports/agent-insight-YYYY-WW-{lane}-gemini.md``
- ``data/reports/agent-insight-YYYY-WW-{lane}-runner.md`` (GGUF; CPU on GitHub-hosted runners)

**Human compare (read order + rubric):** ``docs/spec/DUAL_ADVISORY_COMPARE.md``.

  pip install llama-cpp-python   # runner path only; Gemini uses stdlib + REST
  GEMINI_API_KEY=... python scripts/agent_dual_advisory.py --lane brand --week 2026-W16
  GEMINI_API_KEY_PERSONAL=... python scripts/agent_dual_advisory.py --lane personal --week 2026-W16

**Gemini rate limits (optional env):** ``GEMINI_MIN_INTERVAL_SEC`` (default ``6``) — minimum
seconds between completed Gemini HTTP calls in this process (reduces 429s when re-running locally).
``GEMINI_MAX_RETRIES`` (default ``5``) — retries on HTTP 429 / 503 with backoff and
``Retry-After`` when the API sends it. Set interval ``0`` to disable spacing only.
``GEMINI_429_MIN_SLEEP_SEC`` (default ``0``) — floor on **retry** sleep after 429/503 (e.g. ``20`` under **~5 RPM** free-tier caps so retries do not stack in the same minute).

**Default REST model** when ``GEMINI_MODEL`` is unset: ``gemini-2.5-flash`` (not 2.0). Override per project via env / Actions **Variable** ``GEMINI_MODEL`` if you need another tier.

**Runner output:** ``MAX_RUNNER_TOKENS`` (default ``1536``, ceiling **6144**) — GGUF ``max_tokens`` request; after
``Llama`` loads, the script **clamps** to ``n_ctx - tokenize(prompt) - margin`` so prompt + generation fit. If logs
still show ``finish_reason=length``, raise the env cap or shorten system/CONTEXT; if you see ``runner_output_cap_clamped``,
raise ``AGENT_LLAMA_N_CTX`` or trim the bundle.

**Runner bundle (env, optional):** ``RUNNER_BUNDLE_MAX_CHARS`` (default ``5200``) — hard cap on lean CONTEXT chars. ``AGENT_LLAMA_N_CTX`` (default ``4096``, clamp 2048–8192) — llama.cpp context. ``AGENT_RUNNER_TEMPERATURE`` (default ``0.15``) — GGUF sampling; lower = less repetitive prose.
**Runner debug logs (optional):** set ``AGENT_RUNNER_VERBOSE=1`` (or ``true`` / ``yes``) for extra ``[runner-advisory]`` lines: per-part bundle sizes, run-next digest/tail lengths, prompt/section sizes, completion preview, markdown heading counts, and how many lines sanitize dropped.

**Gemini output:** ``GEMINI_MAX_OUTPUT_TOKENS`` (default ``4096``). For **2.5** models, ``thinkingConfig.thinkingBudget`` defaults to **0** so hidden reasoning does not eat the whole budget (see [Gemini thinking](https://ai.google.dev/gemini-api/docs/thinking)); set ``GEMINI_THINKING_BUDGET=omit`` to omit that block for older model ids.

**CI log prefixes:** ``[runner-advisory]`` (GGUF), ``[gemini-advisory]`` (REST usage / ``finishReason`` / prose size).

Week label: ISO calendar (same as ``audit_channel`` / ``run_next_report``).
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
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
_DEFAULT_RUNNER_BUNDLE_MAX_CHARS = 5200
# Default output cap (was 512; logs showed finish_reason=length mid-markdown). Override: ``MAX_RUNNER_TOKENS`` env.
_DEFAULT_MAX_RUNNER_TOKENS = 1536
# Upper bound for env ``MAX_RUNNER_TOKENS`` (actual generation may be lower — see ``_runner_effective_max_tokens``).
_RUNNER_MAX_OUTPUT_TOKENS_CEILING = 6144
# llama.cpp slack: BOS/special + completion buffer (keep prompt + max_tokens strictly under ``n_ctx``).
_RUNNER_N_CTX_GENERATION_MARGIN = 24
_DEFAULT_LLAMA_N_CTX = 4096
_DEFAULT_RUNNER_TEMPERATURE = 0.15

# ``run_next_report.py`` appends a cross-lane section for humans; strip it from runner CONTEXT only
# (``build_bundle`` for Gemini still includes the full run-next file).
_RUN_NEXT_CROSS_READ_HEADER = {
    "personal": "## Brand lane (cross-read only)",
    "brand": "## Personal lane (context only)",
}
_RUN_NEXT_PRODUCTION_HOOKS = "## Production hooks (manual)"


def max_runner_tokens() -> int:
    """Requested GGUF ``max_tokens`` upper bound from env (before ``n_ctx`` tokenize clamp in ``write_runner_gguf``)."""
    raw = (os.environ.get("MAX_RUNNER_TOKENS") or "").strip()
    if raw:
        try:
            return max(128, min(_RUNNER_MAX_OUTPUT_TOKENS_CEILING, int(raw)))
        except ValueError:
            pass
    return _DEFAULT_MAX_RUNNER_TOKENS


def _runner_effective_max_tokens(llm: object, *, prompt: str, n_ctx_eff: int, requested: int) -> int:
    """Clamp ``max_tokens`` so ``tokenize(prompt) + generation + margin`` fits ``n_ctx``."""
    margin = _RUNNER_N_CTX_GENERATION_MARGIN
    try:
        tokenize = getattr(llm, "tokenize", None)
        if not callable(tokenize):
            return requested
        ids = tokenize(prompt.encode("utf-8"))  # type: ignore[operator]
        n_prompt = len(ids)
    except Exception:  # noqa: BLE001 — advisory path; fall back to requested
        _runner_log("runner_tokenize: failed; using MAX_RUNNER_TOKENS without n_ctx clamp")
        return requested
    room = n_ctx_eff - n_prompt - margin
    effective = min(requested, max(1, room))
    if room < 64:
        _runner_log(
            f"runner_ctx_warn: prompt_tokens={n_prompt} n_ctx={n_ctx_eff} margin={margin} "
            f"room={room} effective_max_tokens={effective}"
        )
    if effective < requested:
        _runner_log(
            f"runner_output_cap_clamped: requested={requested} effective={effective} "
            f"prompt_tokens={n_prompt} n_ctx={n_ctx_eff} margin={margin}"
        )
    return max(1, effective)


# Backward-compatible name for docs/tests (effective cap is ``max_runner_tokens()``).
MAX_RUNNER_TOKENS = _DEFAULT_MAX_RUNNER_TOKENS
DEFAULT_GGUF = Path.home() / ".cache" / "living-agent" / "qwen2.5-1.5b-instruct-q4_k_m.gguf"


def runner_bundle_max_chars() -> int:
    """Lean CONTEXT cap (chars). Override: ``RUNNER_BUNDLE_MAX_CHARS``."""
    raw = (os.environ.get("RUNNER_BUNDLE_MAX_CHARS") or "").strip()
    if raw:
        try:
            return max(3000, min(14_000, int(raw)))
        except ValueError:
            pass
    return _DEFAULT_RUNNER_BUNDLE_MAX_CHARS


def llama_n_ctx() -> int:
    """llama.cpp ``n_ctx``. Override: ``AGENT_LLAMA_N_CTX`` (2048–8192)."""
    raw = (os.environ.get("AGENT_LLAMA_N_CTX") or "").strip()
    if raw:
        try:
            return max(2048, min(8192, int(raw)))
        except ValueError:
            pass
    return _DEFAULT_LLAMA_N_CTX


def runner_temperature() -> float:
    """GGUF sampling temperature. Override: ``AGENT_RUNNER_TEMPERATURE``."""
    raw = (os.environ.get("AGENT_RUNNER_TEMPERATURE") or "").strip()
    if raw:
        try:
            return max(0.0, min(0.9, float(raw)))
        except ValueError:
            pass
    return _DEFAULT_RUNNER_TEMPERATURE


def runner_verbose_logs() -> bool:
    """Extra ``[runner-advisory]`` detail for CI/local tuning. Override: ``AGENT_RUNNER_VERBOSE``."""
    v = (os.environ.get("AGENT_RUNNER_VERBOSE") or "").strip().lower()
    return v in ("1", "true", "yes", "on", "debug")


# Backward-compatible alias (prefer ``runner_bundle_max_chars()``).
RUNNER_BUNDLE_MAX_CHARS = _DEFAULT_RUNNER_BUNDLE_MAX_CHARS


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


def _analytics_channel_totals_from_videos(videos: object) -> tuple[int, int, int]:
    """Sum views / watch minutes / count-with-views from an analytics ``videos`` list."""
    tot_views = 0
    tot_watch_min = 0
    with_views = 0
    if not isinstance(videos, list):
        return (0, 0, 0)
    for v in videos:
        if not isinstance(v, dict):
            continue
        m = v.get("metrics") or {}
        try:
            vi = int(m.get("views") or 0)
        except (TypeError, ValueError):
            vi = 0
        try:
            wm = int(m.get("watch_time_minutes") or 0)
        except (TypeError, ValueError):
            wm = 0
        tot_views += vi
        tot_watch_min += wm
        if vi > 0:
            with_views += 1
    return (tot_views, tot_watch_min, with_views)


def _analytics_channel_totals_from_file(ana_path: Path) -> tuple[int, int, int] | None:
    """Return ``(sum_views_all_videos, sum_watch_time_minutes_all_videos, count_videos_with_views_gt_0)``."""
    if not ana_path.exists():
        return None
    try:
        data = json.loads(ana_path.read_text(encoding="utf-8", errors="replace"))
    except (json.JSONDecodeError, OSError, TypeError):
        return None
    videos = data.get("videos") or []
    return _analytics_channel_totals_from_videos(videos)


def _runner_facts_block(ana_path: Path, sug_path: Path) -> str:
    """Small deterministic JSON so the small GGUF can cite channel totals without inventing them."""
    ana_rel = ana_path.relative_to(_REPO) if ana_path.is_relative_to(_REPO) else ana_path
    sug_rel = sug_path.relative_to(_REPO) if sug_path.is_relative_to(_REPO) else sug_path
    ana_facts: dict[str, object] = {"analytics_path": str(ana_rel)}
    if ana_path.exists():
        try:
            data = json.loads(ana_path.read_text(encoding="utf-8", errors="replace"))
            videos = data.get("videos") or []
            tot_views, tot_watch_min, with_views = _analytics_channel_totals_from_videos(videos)
            ana_facts.update(
                {
                    "date_range": data.get("date_range"),
                    "fetched_at": data.get("fetched_at"),
                    "n_videos_in_snapshot": len(videos),
                    "sum_views_all_videos": tot_views,
                    "sum_watch_time_minutes_all_videos": tot_watch_min,
                    "count_videos_with_views_gt_0": with_views,
                }
            )
        except (json.JSONDecodeError, OSError, TypeError) as e:
            ana_facts["parse_error"] = str(e)
    else:
        ana_facts["missing"] = True

    sug_facts: dict[str, object] = {"suggestions_path": str(sug_rel)}
    if sug_path.exists():
        try:
            s = json.loads(sug_path.read_text(encoding="utf-8", errors="replace"))
            sug_facts.update(
                {
                    "videos_analyzed": s.get("videos_analyzed"),
                    "videos_with_views": s.get("videos_with_views"),
                    "overall_avg_retention": s.get("overall_avg_retention"),
                    "overall_avg_watch_minutes_per_video": s.get("overall_avg_watch_minutes_per_video"),
                }
            )
        except (json.JSONDecodeError, OSError, TypeError) as e:
            sug_facts["parse_error"] = str(e)
    else:
        sug_facts["missing"] = True

    payload = {"analytics_totals": ana_facts, "suggestions_headline": sug_facts}
    body = json.dumps(payload, indent=2, ensure_ascii=False)
    if len(body) > 2200:
        body = body[:2180] + "\n… truncated\n"
    return (
        "### deterministic facts (computed by script)\n\n"
        "For **channel-wide** views and watch minutes, copy **only** the numbers inside "
        "`analytics_totals` below. If weekly prose or run-next disagrees, **trust this JSON**.\n\n"
        f"```json\n{body}\n```\n"
    )


def _runner_run_next_for_qwen(run_next: Path, lane: str) -> str:
    """Smaller run-next CONTEXT: snapshot extract + tail from Actionable onward (cross-lane stripped).

    Avoids feeding Qwen near-duplicate full run-next plus long weekly tables.
    """
    if not run_next.exists():
        rel = run_next.relative_to(_REPO) if run_next.is_relative_to(_REPO) else run_next
        _runner_log(f"run_next_for_qwen: missing file lane={lane} path={rel}")
        return f"### run-next (trimmed)\n\n(missing: {rel})\n"
    raw = run_next.read_text(encoding="utf-8", errors="replace")
    body = _strip_run_next_cross_lane_section(raw, lane)
    snap_h = "## Brand snapshot (this run)" if lane == "brand" else "## Personal snapshot (this run)"
    ev_h = "## Evidence (paths)"
    i0 = body.find(snap_h)
    i1 = body.find(ev_h)
    if i0 != -1 and i1 != -1 and i1 > i0:
        digest = body[i0:i1].strip()
        cap_d = 900
        if len(digest) > cap_d:
            digest = digest[:cap_d] + "\n…\n"
    else:
        digest = "(snapshot section not found)"

    act_h = "## Actionable"
    start_tail = body.find(act_h)
    if start_tail != -1:
        tail = body[start_tail:].strip()
        # Tail can still include the human cross-lane block (e.g. personal pointers on brand run-next).
        cross = _RUN_NEXT_CROSS_READ_HEADER.get("personal" if lane == "brand" else "brand", "")
        if cross and cross in tail:
            i0 = tail.find(cross)
            i1 = tail.find(_RUN_NEXT_PRODUCTION_HOOKS, i0 + len(cross)) if i0 != -1 else -1
            if i0 != -1 and i1 != -1:
                tail = (tail[:i0].rstrip() + "\n\n" + tail[i1:].lstrip()).strip()
        cap_t = 2400
        if len(tail) > cap_t:
            tail = tail[:cap_t] + "\n… truncated run-next tail\n"
    else:
        tail = "(no ## Actionable section found)"

    block = (
        "### run-next digest (snapshot only)\n\n"
        "Use this block for headline snapshot metrics; do not re-derive them.\n\n"
        f"{digest}\n\n"
        "### run-next tail (actionable → end)\n\n"
        f"{tail}\n"
    )
    _runner_log(
        f"run_next_for_qwen: lane={lane} digest_chars={len(digest)} tail_chars={len(tail)} "
        f"digest_ok={digest != '(snapshot section not found)'} actionable_ok={tail != '(no ## Actionable section found)'}"
    )
    if runner_verbose_logs():
        _runner_log(f"run_next_for_qwen verbose: digest_preview={digest[:240]!r}")
        _runner_log(f"run_next_for_qwen verbose: tail_head={tail[:320]!r}")
    return block


def _runner_int_in_text_as_token(text: str, n: int) -> bool:
    """True if integer ``n`` appears with digit boundaries (avoids ``46`` inside ``146``).

    Thousands separators (commas) are ignored so ``4,224`` matches ``4224``.
    """
    t = text.replace(",", "")
    return re.search(rf"(?<!\d){re.escape(str(n))}(?!\d)", t) is not None


def _sanitize_runner_prose(
    text: str, channel_totals: tuple[int, int, int] | None = None
) -> tuple[str, int]:
    """Remove tautology lines small models emit (e.g. same % compared to itself via 'slightly higher than').

    Lines that also carry **several distinct numeric facts** (e.g. channel views + minutes + counts plus a
    redundant retention comparison) are **kept** — dropping the whole line would remove grounding totals.

    When ``channel_totals`` is set, lines that mention **any** of those three integers (same token rules as
    grounding) are never dropped — so a line with only ``46`` plus a duplicated ``22.33`` tautology is kept.

    Returns ``(cleaned_text, lines_removed)``.
    """
    out: list[str] = []
    removed = 0
    for line in text.splitlines():
        low = line.lower()
        if "slightly higher" in low or "slightly lower" in low:
            decimals = re.findall(r"\d+\.\d+", line)
            nums = re.findall(r"\d+\.\d+|\d+", line)
            vals: list[float] = []
            for n in nums:
                try:
                    vals.append(float(n))
                except ValueError:
                    continue
            uniq_vals = {round(v, 5) for v in vals}
            # Tautology-only lines repeat one number (e.g. 24.67 vs 24.67). Summary lines often mix
            # channel totals (755, 4224, 46) with one bad comparison — do not strip the entire line.
            if len(uniq_vals) >= 3:
                out.append(line)
                continue
            if channel_totals is not None:
                sv, sw, cv = channel_totals
                if (
                    _runner_int_in_text_as_token(line, sv)
                    or _runner_int_in_text_as_token(line, sw)
                    or _runner_int_in_text_as_token(line, cv)
                ):
                    out.append(line)
                    continue
            if len(decimals) >= 2 and len(set(decimals)) == 1:
                removed += 1
                continue
            if len(vals) >= 2 and len(uniq_vals) == 1:
                removed += 1
                continue
        out.append(line)
    return "\n".join(out), removed


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

    facts = _runner_facts_block(ana_path, sug_path)
    run_next_trimmed = _runner_run_next_for_qwen(run_next, lane)
    weekly_body = _read(weekly, 1800)
    blocked_body = _read(blocked, 900)
    sug_compact = _compact_suggestions(sug_path)
    ana_compact = _compact_analytics(ana_path)

    labels = (
        "runner_scope",
        "deterministic_facts",
        "run_next_digest_tail",
        "weekly",
        "blocked",
        "suggestions_compact",
        "analytics_compact",
    )
    parts = [
        "### runner scope\n\n" + scope_note,
        facts,
        run_next_trimmed,
        "### weekly report\n\n" + weekly_body,
        "### run-intent blocked\n\n" + blocked_body,
        "### suggestions (compact)\n\n" + sug_compact,
        "### analytics (compact top videos + retention slice)\n\n" + ana_compact,
    ]
    text = "\n\n".join(parts)
    cap = runner_bundle_max_chars()
    hard_capped = len(text) > cap
    if hard_capped:
        text = text[: cap - 40] + "\n… hard-capped for runner ctx\n"
    sizes = ", ".join(f"{lb}={len(p)}" for lb, p in zip(labels, parts))
    _runner_log(
        f"build_runner_bundle: lane={lane} week={week} total_chars={len(text)} cap={cap} "
        f"hard_capped={hard_capped} ({sizes})"
    )
    if runner_verbose_logs():
        for lb, p in zip(labels, parts):
            head = p.replace("\n", "\\n")[:200]
            _runner_log(f"build_runner_bundle verbose part {lb}: chars={len(p)} head={head!r}")
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


def _runner_log_output_shape(prose: str) -> None:
    """Log markdown heading patterns in model output (tuning ``###`` vs ``##`` drift)."""
    lines = prose.splitlines()
    n_h2 = n_h3 = n_h1 = 0
    for line in lines:
        t = line.lstrip()
        if t.startswith("# ") and not t.startswith("##"):
            n_h1 += 1
        elif t.startswith("## ") and not t.startswith("###"):
            n_h2 += 1
        elif t.startswith("### "):
            n_h3 += 1
    first = lines[0][:160] if lines else ""
    _runner_log(
        f"runner_output_shape: lines={len(lines)} h1={n_h1} h2={n_h2} h3={n_h3} "
        f"first_line={first!r}"
    )
    if runner_verbose_logs() and prose:
        prev = min(700, len(prose))
        _runner_log(f"runner_output_shape verbose: prose_head={prose[:prev]!r}")


def _runner_output_is_instruction_scaffold_echo(prose: str) -> bool:
    """First line copies a long system-prompt rule line (common 1.5B failure).

    If the model uses the old long \"## What I reviewed — **exactly 3** …\" line but then
    real ``-`` bullets, treat as OK (see tests).
    """
    raw_lines = (prose or "").splitlines()
    nonempty = [ln.strip() for ln in raw_lines if ln.strip()]
    if not nonempty:
        return False
    first = nonempty[0]
    if first.startswith("## Summary — **2–3** sentences only"):
        return True
    if first.startswith("## Insights — numbered **1–5**"):
        return True
    if first.startswith("## What I reviewed — **exactly 3** short bullets"):
        for ln in raw_lines[1:10]:
            if ln.lstrip().startswith(("-", "*")):
                return False
        return True
    return False


def _runner_output_is_system_rubric_echo(prose: str) -> bool:
    """Detect outputs that paste the system prompt's rubric sentences verbatim.

    Newer prompts include plain-English rubric lines like "Three short `-` bullets:" under headings.
    If the model outputs those rubric lines instead of actual bullets/sentences, treat as template echo.
    """
    t = (prose or "").strip()
    if not t:
        return True
    needles = (
        "Three short `-` bullets:",
        "**2–3** sentences: main story from metrics",
        "Numbered **1–5**.",
        "**2–4** short `-` bullets",
        "**2–5** `-` bullets:",
        "Do not paste large tables;",
    )
    hits = sum(1 for n in needles if n in t)
    if hits >= 2:
        return True
    # One rubric line is still bad if there is no real filled content.
    has_any_bullet = any(ln.lstrip().startswith(("-", "*")) for ln in t.splitlines())
    has_any_numbered = any(re.match(r"^\s*\d+\.\s+", ln) for ln in t.splitlines())
    if hits >= 1 and (not has_any_bullet) and (not has_any_numbered):
        return True
    return False


# Runner advisory body must use these ``##`` headings in order (first heading in output = first here).
_RUNNER_REQUIRED_H2_ORDER = (
    "## What I reviewed",
    "## Summary",
    "## Insights",
    "## Risks",
    "## Next tries",
)
# Titles that may appear as erroneous ``###`` (CONTEXT uses ``###``; small models mirror it).
_RUNNER_H3_PROMOTABLE_TITLES = (
    "What I reviewed",
    "Summary",
    "Insights",
    "Risks",
    "Next tries",
)


def _runner_rest_allows_h3_promotion_to_h2(rest: str, title: str) -> bool:
    """True if ``rest`` after ``###`` is exactly ``title`` or ``title`` + allowed continuation (not e.g. ``Summary of``)."""
    if rest == title:
        return True
    if not rest.startswith(title):
        return False
    suffix = rest[len(title) :].lstrip()
    if not suffix:
        return True
    fc = suffix[0]
    # markdown / list / numbering — not a bogus word continuation like ``Summary of``
    return fc in (":", "—", "-", "*", "\u2013", "\u2014") or fc.isdigit()


def _runner_normalize_known_h3_heads_to_h2(prose: str) -> tuple[str, bool]:
    """Promote ``###`` → ``##`` only for the five required section titles (CI drift from CONTEXT)."""
    changed = False
    out_lines: list[str] = []
    for line in (prose or "").splitlines():
        s = line.lstrip()
        indent = line[: len(line) - len(s)]
        if s.startswith("### ") and not s.startswith("####"):
            rest = s[4:].lstrip()
            for title in _RUNNER_H3_PROMOTABLE_TITLES:
                if _runner_rest_allows_h3_promotion_to_h2(rest, title):
                    line = f"{indent}## {rest}"
                    changed = True
                    break
        out_lines.append(line)
    return "\n".join(out_lines), changed


def _runner_line_matches_h2(s: str, head: str) -> bool:
    """True if stripped line is ``head`` or ``head`` plus title suffix (not ``###``)."""
    if not s.startswith("## ") or s.startswith("###"):
        return False
    if not s.startswith(head):
        return False
    if len(s) == len(head):
        return True
    nxt = s[len(head)]
    # space, colon, hyphen, en dash, em dash — not a third `#`
    return nxt in (" \t:#-—\u2013\u2014") and nxt != "#"


def _runner_output_schema_valid(prose: str) -> bool:
    """True if prose has required ``##`` section headings in order (each starts a line, not ``###``)."""
    t = (prose or "").strip()
    if not t:
        return False
    if t.startswith("## Inference error"):
        return True
    lines = t.splitlines()
    min_line = -1
    for head in _RUNNER_REQUIRED_H2_ORDER:
        found_at = None
        for i, raw in enumerate(lines):
            if i <= min_line:
                continue
            s = raw.lstrip()
            if _runner_line_matches_h2(s, head):
                found_at = i
                break
        if found_at is None:
            return False
        min_line = found_at
    return True


def _runner_schema_failure_label(prose: str) -> str:
    """Short log label for the first required heading not found in order (``ok`` if valid)."""
    if _runner_output_schema_valid(prose):
        return "ok"
    lines = (prose or "").strip().splitlines()
    min_line = -1
    for head in _RUNNER_REQUIRED_H2_ORDER:
        found_at = None
        for i, raw in enumerate(lines):
            if i <= min_line:
                continue
            s = raw.lstrip()
            if _runner_line_matches_h2(s, head):
                found_at = i
                break
        if found_at is None:
            return f"missing:{head}"
        min_line = found_at
    return "ok"


def _strip_wir_placeholder_bullets(text: str) -> tuple[str, int]:
    """Remove rubric-echo bullets under ``## What I reviewed`` (keep totals line with ``:`` + digits).

    Small models often paste the instruction template literally; stripping keeps the committed
    file readable without weakening grounding (totals line is preserved).
    """
    if not text or text.startswith("## Inference error"):
        return text, 0
    lines = text.splitlines()
    wir = "## What I reviewed"
    summ = "## Summary"
    try:
        i_wir = next(i for i, ln in enumerate(lines) if ln.lstrip().startswith(wir))
        i_sum = next(i for i, ln in enumerate(lines) if i > i_wir and ln.lstrip().startswith(summ))
    except StopIteration:
        return text, 0
    removed = 0
    out_mid: list[str] = []
    for idx in range(i_wir + 1, i_sum):
        ln = lines[idx]
        stripped = ln.strip()
        low = stripped.lower()
        if stripped == "- deterministic facts (computed by script)":
            removed += 1
            continue
        if stripped == "- run-next digest + tail":
            removed += 1
            continue
        if "one other context" in low:
            removed += 1
            continue
        out_mid.append(ln)
    if removed == 0:
        return text, 0
    new_lines = lines[: i_wir + 1] + out_mid + lines[i_sum:]
    body = "\n".join(new_lines)
    if text.endswith("\n") and not body.endswith("\n"):
        body += "\n"
    return body, removed


def _runner_analytics_path_for_lane(lane: str) -> Path:
    if lane == "personal":
        return DATA / "analytics_personal.json"
    return DATA / "analytics.json"


def _runner_slice_wir_summary(prose: str) -> str:
    """Body from ``## What I reviewed`` through just before ``## Insights`` (for grounding checks)."""
    a = prose.find("## What I reviewed")
    b = prose.find("## Insights")
    if a == -1 or b == -1 or b <= a:
        return ""
    return prose[a:b]


def _runner_prose_quotes_channel_totals(slice_text: str, totals: tuple[int, int, int]) -> bool:
    """Require all three analytics channel totals to appear verbatim in WIR+Summary slice."""
    sv, sw, cv = totals
    return (
        _runner_int_in_text_as_token(slice_text, sv)
        and _runner_int_in_text_as_token(slice_text, sw)
        and _runner_int_in_text_as_token(slice_text, cv)
    )


def _runner_grounding_slice_ok(prose: str, totals: tuple[int, int, int]) -> bool:
    """True if ``## What I reviewed`` … ``## Summary`` slice exists and quotes all three channel totals."""
    sl = _runner_slice_wir_summary(prose)
    if not (sl or "").strip():
        return False
    return _runner_prose_quotes_channel_totals(sl, totals)


def _runner_inject_channel_totals_into_wir_summary(
    prose: str, totals: tuple[int, int, int]
) -> tuple[str, bool]:
    """Ensure channel totals appear in ``## What I reviewed`` and ``## Summary``.

    Small models can ignore grounding instructions even when we spoon-feed the integers. When schema is valid,
    it is safer to inject the deterministic totals in the two required sections and keep the rest of the prose.

    Returns ``(new_prose, changed)``.
    """
    if not prose or prose.startswith("## Inference error"):
        return prose, False
    if not _runner_output_schema_valid(prose):
        return prose, False

    sv, sw, cv = totals
    lines = prose.splitlines()
    wir = "## What I reviewed"
    summ = "## Summary"
    insights = "## Insights"

    try:
        i_wir = next(i for i, ln in enumerate(lines) if ln.lstrip().startswith(wir))
        i_sum = next(i for i, ln in enumerate(lines) if i > i_wir and ln.lstrip().startswith(summ))
        i_ins = next(i for i, ln in enumerate(lines) if i > i_sum and ln.lstrip().startswith(insights))
    except StopIteration:
        return prose, False

    changed = False

    # Inject a deterministic-facts bullet into What I reviewed if needed.
    wir_block = "\n".join(lines[i_wir:i_sum])
    if not (
        _runner_int_in_text_as_token(wir_block, sv)
        and _runner_int_in_text_as_token(wir_block, sw)
        and _runner_int_in_text_as_token(wir_block, cv)
    ):
        bullet = (
            f"- deterministic facts (computed by script): {sv} views, {sw} watch minutes, "
            f"{cv} videos with views\n"
        )
        insert_at = i_sum
        # Keep bullets near the top of WIR; insert after the heading line if that seems cleaner.
        if i_wir + 1 < i_sum and not lines[i_wir + 1].lstrip().startswith(("-", "*")):
            insert_at = i_wir + 1
        lines.insert(insert_at, bullet.rstrip("\n"))
        # Adjust indices after insertion if it occurred before Summary.
        if insert_at <= i_sum:
            i_sum += 1
            i_ins += 1
        changed = True

    # Inject a totals sentence into Summary if needed.
    sum_block = "\n".join(lines[i_sum:i_ins])
    if not (
        _runner_int_in_text_as_token(sum_block, sv)
        and _runner_int_in_text_as_token(sum_block, sw)
        and _runner_int_in_text_as_token(sum_block, cv)
    ):
        sent = f"Channel totals: {sv} views, {sw} watch minutes, {cv} videos with views.\n"
        insert_at = i_sum + 1
        lines.insert(insert_at, sent.rstrip("\n"))
        changed = True

    return "\n".join(lines), changed


def _runner_insights_section(prose: str) -> str:
    a = prose.find("## Insights")
    b = prose.find("## Risks")
    if a == -1 or b == -1 or b <= a:
        return ""
    return prose[a:b]


def _runner_insight_item_starts(line_stripped: str) -> bool:
    if re.match(r"^\d+\.\s+", line_stripped):
        return True
    return bool(re.match(r"^\*{1,2}\d+\.\*{1,2}\s+", line_stripped))


def _runner_insights_numbered_bodies(prose: str) -> list[str]:
    """Split ``## Insights`` into one string per leading ``1.`` / ``2.`` / … item."""
    body = _runner_insights_section(prose)
    if not body:
        return []
    items: list[str] = []
    buf: list[str] = []
    started = False
    for line in body.splitlines()[1:]:
        stripped = line.strip()
        if _runner_insight_item_starts(stripped):
            if buf:
                items.append("\n".join(buf).strip())
            buf = [line]
            started = True
        elif started:
            buf.append(line)
    if buf:
        items.append("\n".join(buf).strip())
    return items


def _runner_insight_norm(blob: str) -> str:
    t = (blob or "").strip()
    t = re.sub(r"^\d+\.\s+", "", t)
    t = re.sub(r"^\*{1,2}\d+\.\*{1,2}\s+", "", t)
    t = re.sub(r"\s+", " ", t.lower()).strip()
    return t[:220]


def _runner_insights_nonduplicate(prose: str) -> bool:
    """Reject obvious copy-paste duplicates among numbered insights (needs ≥4 items)."""
    items = _runner_insights_numbered_bodies(prose)
    if len(items) < 4:
        return True
    norms = [_runner_insight_norm(x) for x in items]
    return len(norms) == len(set(norms))


def _runner_output_is_context_dump(prose: str) -> bool:
    """Detect outputs that paste run-next / machine bundle instead of synthesizing."""
    t = prose or ""
    markers = (
        "Produced by `scripts/run_next_report.py`",
        "### Personal snapshot (this run)",
        "### Brand snapshot (this run)",
        "## Actionable (correlate gates passed)",
        "### run-next tail (actionable",
    )
    return any(m in t for m in markers)


def _runner_output_is_template_echo(prose: str) -> bool:
    """Detect runner outputs that simply repeat the instructions (no filled content)."""
    t = (prose or "").strip()
    if not t:
        return True
    if _runner_output_is_instruction_scaffold_echo(prose):
        return True
    if _runner_output_is_system_rubric_echo(prose):
        return True
    # Strong signature: the model repeats the exact instruction scaffolding.
    needle = "## What I reviewed — **exactly 3** short bullets"
    if needle not in t:
        return False
    # If it contains the other instruction lines and no actual bullets/numbers, treat as echo.
    has_other = "## Next tries — **2–5** bullets" in t and "## Risks — **2–4** short bullets" in t
    has_bullets = any(line.lstrip().startswith(("-", "*")) for line in t.splitlines())
    has_numbers = any(ch.isdigit() for ch in t)
    # The template includes digits (2–5, etc). We require bullets or something beyond the header lines.
    return bool(has_other) and (not has_bullets) and has_numbers and len(t.splitlines()) <= 20


def _runner_retry_system_prefix() -> str:
    return (
        "Do NOT repeat the instructions. Write an actual advisory using only CONTEXT. "
        "If you cannot comply, write '## Inference error' and one sentence why.\n"
    )


def _runner_retry_skeleton() -> str:
    """Fill-in template for the retry path (small models follow this better than rule prose)."""
    return (
        "Fill the markdown below using ONLY numbers/labels found in CONTEXT. "
        "Do not repeat these instructions.\n"
        "**Forbidden:** pasting run-next tables or CONTEXT headings such as "
        "'### Personal snapshot', '## Actionable (correlate gates passed)', or the "
        "'Produced by scripts/run_next_report.py' footer — synthesize in your own words.\n\n"
        "## What I reviewed\n"
        "- deterministic facts (computed by script)\n"
        "- run-next digest + tail\n"
        "- one other CONTEXT section you used\n\n"
        "## Summary\n"
        "(2–3 sentences)\n\n"
        "## Insights\n"
        "1. ...\n"
        "2. ...\n"
        "3. ...\n\n"
        "## Risks\n"
        "- ...\n"
        "- ...\n\n"
        "## Next tries\n"
        "- ...\n"
        "- ...\n"
    )


def _runner_schema_retry_system() -> str:
    """Short system prompt for the one-shot schema completion retry (after primary output too short / wrong)."""
    return (
        "You are a compact advisor for a YouTube ambient music channel. Use ONLY the CONTEXT below. "
        "Do not repeat these instructions.\n"
        "The user message is a **fill-in template**: it already lists the five required `##` headings. "
        "**Keep every one of those five `##` lines** (two `#` only — not `###`) in the **same order**. "
        "Replace placeholders with real prose from CONTEXT.\n"
        "In **## What I reviewed** and **## Summary**, copy **sum_views_all_videos**, "
        "**sum_watch_time_minutes_all_videos**, and **count_videos_with_views_gt_0** from deterministic "
        "facts JSON **verbatim** (same digits).\n"
        "Never paste run-next snapshot/actionable blocks or the `run_next_report.py` footer.\n"
        "Do not output `## Inference error` unless CONTEXT is unusable."
    )


def _runner_grounding_retry_system() -> str:
    """Short system prompt for the one-shot grounding retry (totals missing from WIR+Summary)."""
    return (
        "You are a compact advisor for a YouTube ambient music channel. Use ONLY the CONTEXT in the user message. "
        "The user lists three integers that MUST appear as digit tokens in both **## What I reviewed** "
        "and **## Summary** (exact values). Output a complete advisory: five `##` sections in order — "
        "**## What I reviewed**, **## Summary**, **## Insights**, **## Risks**, **## Next tries** — "
        "two `#` characters per heading, not `###`. "
        "Do not paste run-next snapshot/actionable blocks or the `run_next_report.py` footer."
    )


def _runner_grounding_retry_user(*, draft: str, totals: tuple[int, int, int], ctx_used: str) -> str:
    sv, sw, cv = totals
    return (
        f"REQUIRED verbatim integers (each must appear in ## What I reviewed AND ## Summary): "
        f"{sv}, {sw}, {cv}\n\n"
        f"Previous draft (rewrite into a valid full advisory):\n\n{draft}\n\n"
        f"CONTEXT:\n{ctx_used}"
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

    ctx_used = bundle[: runner_bundle_max_chars()]
    ch_totals = _analytics_channel_totals_from_file(_runner_analytics_path_for_lane(lane))
    _runner_log(
        f"runner_prompt_budget: ctx_used_chars={len(ctx_used)} bundle_in_chars={len(bundle)} "
        f"runner_bundle_max_chars={runner_bundle_max_chars()} verbose={runner_verbose_logs()}"
    )
    system = (
        "You are a compact advisor for a YouTube ambient music channel. "
        "You ONLY see the user CONTEXT (markdown + JSON excerpts from this repo’s analytics run). "
        "You did NOT call YouTube or the internet.\n"
        "The section **deterministic facts (computed by script)** has JSON built by Python: "
        "for **sum_views_all_videos**, **sum_watch_time_minutes_all_videos**, and **count_videos_with_views_gt_0**, "
        "you MUST copy those integers exactly when you mention channel totals. Never invent different totals.\n"
        "In **## What I reviewed**, the deterministic-facts bullet must include those **three integers** verbatim. "
        "In **## Summary**, the prose must also include the **same three integers** at least once each (no rounding, "
        "no recomputing from per-video rows).\n"
        "In **## Insights**, each numbered item must be **distinct** — do not reuse the same titles/stats "
        "in another numbered item.\n"
        "Treat the rest of CONTEXT as evidence too, but if prose disagrees with that JSON, **follow the JSON**.\n"
        "Do not reference files you did not read here; do not answer with pointers only (e.g. “see run-next”) — "
        "synthesize takeaways in your own words.\n"
        "**Forbidden in your output:** copying run-next machine text — no "
        "'### Personal snapshot', '### Brand snapshot', '## Actionable (correlate gates passed)', "
        "'### run-next tail', or the footer line mentioning `run_next_report.py`. "
        "Those exist only inside CONTEXT; your job is a short human advisory, not a paste.\n"
        "Required shape (GitHub-flavored markdown, use `##` section headings only; stay concise; "
        "no outer ``` fences). Do **not** begin your answer by repeating these rule lines verbatim.\n"
        "**Critical:** Your reply body MUST use exactly these five headings as the **first** markdown "
        "headings in your answer, in this **exact order** — each on its own line starting with `## ` "
        "(**exactly two** `#` characters, then a space — **not** `###` three hashes). CONTEXT uses `###` "
        "for its own blocks; your advisory sections must still use `##` only. "
        "Headings in order: `## What I reviewed`, `## Summary`, `## Insights`, `## Risks`, `## Next tries`. "
        "Do not put `### …` section titles before `## What I reviewed`.\n"
        "## What I reviewed\n"
        "Use **2–4** short `-` bullets naming which CONTEXT parts you actually used, in plain words "
        "(e.g. **Channel totals JSON**, **run-next snapshot + actionable tail**, **weekly report excerpt**). "
        "Do **not** paste rubric placeholders as bullets: never use the literal line "
        "`- deterministic facts (computed by script)` with nothing after it, never "
        "`- run-next digest + tail` alone, and never the phrase **one other CONTEXT**. "
        "One bullet **must** include the three channel integers with a colon (same as Summary). "
        "No pasted tables.\n"
        "## Summary\n"
        "**2–3** sentences: main story from metrics (thin data is OK to name).\n"
        "## Insights\n"
        "Numbered **1–5**. Each item: **at most 2 sentences**. "
        "Each item must name at least one **concrete** label from CONTEXT: a **mood**, **music_style**, **art_period**, "
        "or a **video title** from analytics compact / run-next tail — not generic praise like 'well-received'.\n"
        "Use **at least three distinct numeric facts** across the five items (prefer deterministic JSON for channel totals). "
        "Every number must appear verbatim in CONTEXT (no invented totals).\n"
        "**Forbidden:** saying a metric is 'higher', 'lower', or 'slightly higher/lower than' **the same numeric value** "
        "(e.g. '24.67% is slightly higher than 24.67%'). **Forbidden:** comparing a count to itself.\n"
        "If an item is not directly supported, start that paragraph with **Speculative:**.\n"
        "Do **not** repeat the same bullet twice; do **not** reuse the same sentence in multiple insights.\n"
        "## Risks\n"
        "**2–4** short `-` bullets (thin data, confounders); **do not** duplicate the same risk sentence.\n"
        "## Next tries\n"
        "**2–5** `-` bullets: concrete experiments tied to moods/styles named in CONTEXT.\n"
        "Do not paste large tables; at most one tiny 3-row markdown table if essential. "
        "If a metric is missing from CONTEXT, say **Not in CONTEXT** instead of guessing."
    )
    user = (
        "Your reply must include **all five** section headings in order, each its own line starting "
        "with exactly `## ` (two `#` characters, not `###`): "
        "`## What I reviewed`, `## Summary`, `## Insights`, `## Risks`, `## Next tries`. "
        "Do not stop after three sections.\n\n"
        f"CONTEXT:\n{ctx_used}"
    )
    prompt = _qwen25_chat_prompt(system=system, user=user)
    prompt_chars = len(prompt)
    sys_chars = len(system)
    usr_chars = len(user)
    est_prompt_tokens = max(1, int(prompt_chars / 3.5))
    n_threads = int(os.environ.get("AGENT_LLAMA_THREADS", "4"))
    _runner_log(
        f"context: bundle_chars={len(ctx_used)} prompt_chars={prompt_chars} "
        f"system_chars={sys_chars} user_chars={usr_chars} "
        f"est_input_tokens≈{est_prompt_tokens} (rough; model tokenizer may differ)"
    )
    if runner_verbose_logs():
        sh = system.replace("\n", "\\n")[:500]
        uh = user.replace("\n", "\\n")[:500]
        _runner_log(f"runner_prompt verbose system_head={sh!r}")
        _runner_log(f"runner_prompt verbose user_head={uh!r}")
    cap_requested = max_runner_tokens()
    n_ctx_eff = llama_n_ctx()
    temp = runner_temperature()

    llm = None
    try:
        t0 = time.perf_counter()
        llm = Llama(
            model_path=str(gguf),
            n_ctx=n_ctx_eff,
            n_threads=n_threads,
            n_gpu_layers=0,
            verbose=False,
        )
        t_load = time.perf_counter()
        _runner_log(f"model load wall_s={t_load - t0:.2f}s")
        cap_eff = _runner_effective_max_tokens(
            llm, prompt=prompt, n_ctx_eff=n_ctx_eff, requested=cap_requested
        )
        _runner_log(
            f"llama: n_ctx={n_ctx_eff} max_output_tokens_requested={cap_requested} "
            f"max_output_tokens_effective={cap_eff} n_threads={n_threads} n_gpu_layers=0 temperature={temp}"
        )
        result = llm(
            prompt,
            max_tokens=cap_eff,
            temperature=temp,
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
        _runner_log_output_shape(text)
    except Exception as e:  # noqa: BLE001 — advisory path; always write markdown
        text = f"## Inference error\n\n`{type(e).__name__}`: {e}\n"
        _runner_log(f"inference error: {type(e).__name__}: {e}")

    if not text.startswith("## Inference error"):
        before_san = text
        text, san_removed = _sanitize_runner_prose(text, ch_totals)
        _runner_log(
            f"sanitize: tautology_lines_removed={san_removed} "
            f"chars_before_after={len(before_san)}->{len(text)}"
        )

    # Guardrail: small models echo instructions or paste run-next CONTEXT verbatim.
    if llm is not None and (
        _runner_output_is_template_echo(text) or _runner_output_is_context_dump(text)
    ):
        _runner_log("runner_guardrail: detected template-echo or context-dump; retrying once")
        try:
            retry_system = (
                "You are a compact advisor for a YouTube ambient music channel. "
                "Use ONLY the provided CONTEXT. Do not repeat instructions. "
                "Never paste run-next snapshot/actionable headings or the run_next_report.py footer. "
                "Output MUST use `## What I reviewed`, `## Summary`, `## Insights`, `## Risks`, "
                "`## Next tries` as lines (in that order) before any other `##` headings — "
                "exactly two `#` characters per heading, not `###`."
            )
            retry_user = _runner_retry_skeleton() + "\n\nCONTEXT:\n" + ctx_used
            retry_prompt = _qwen25_chat_prompt(system=retry_system, user=retry_user)
            retry_temp = min(temp, 0.1)
            cap_retry = _runner_effective_max_tokens(
                llm, prompt=retry_prompt, n_ctx_eff=n_ctx_eff, requested=cap_requested
            )
            result2 = llm(
                retry_prompt,
                max_tokens=cap_retry,
                temperature=retry_temp,
                stop=[_QWEN_IM_END, _QWEN_IM_START],
            )
            choice2 = (result2.get("choices") or [{}])[0]
            text2 = (choice2.get("text") or "").strip()
            fr2 = choice2.get("finish_reason")
            _runner_log(
                f"runner_guardrail retry: output_chars={len(text2)} finish_reason={fr2!r} temperature={retry_temp}"
            )
            _runner_log_output_shape(text2)
            if text2 and not text2.startswith("## Inference error"):
                before_san2 = text2
                text2, san_removed2 = _sanitize_runner_prose(text2, ch_totals)
                _runner_log(
                    f"sanitize(retry): tautology_lines_removed={san_removed2} "
                    f"chars_before_after={len(before_san2)}->{len(text2)}"
                )
            if (
                text2
                and not _runner_output_is_template_echo(text2)
                and not _runner_output_is_context_dump(text2)
            ):
                text = text2
            else:
                text = (
                    "## Inference error\n\n"
                    "Runner repeated instructions or pasted run-next / CONTEXT machine text "
                    "instead of a synthesized advisory.\n"
                )
        except Exception as e:  # noqa: BLE001 — guardrail; keep workflow running
            _runner_log(f"runner_guardrail retry failed: {type(e).__name__}: {e}")
            text = "## Inference error\n\nRunner guardrail retry failed.\n"

    if not text.startswith("## Inference error"):
        text_norm, norm_changed = _runner_normalize_known_h3_heads_to_h2(text)
        if norm_changed:
            _runner_log("runner_heading_normalize: promoted ### → ## for known advisory section titles")
            text = text_norm
        if not _runner_output_schema_valid(text):
            _runner_log(
                f"runner_schema_reject: missing or out-of-order required ## sections "
                f"(first_issue={_runner_schema_failure_label(text)!r})"
            )
            if llm is not None:
                _runner_log("runner_schema_retry: one completion with fill-in template")
                try:
                    schema_user = _runner_retry_skeleton() + "\n\nCONTEXT:\n" + ctx_used
                    schema_prompt = _qwen25_chat_prompt(
                        system=_runner_schema_retry_system(), user=schema_user
                    )
                    schema_temp = min(temp, 0.1)
                    cap_schema = _runner_effective_max_tokens(
                        llm, prompt=schema_prompt, n_ctx_eff=n_ctx_eff, requested=cap_requested
                    )
                    result_s = llm(
                        schema_prompt,
                        max_tokens=cap_schema,
                        temperature=schema_temp,
                        stop=[_QWEN_IM_END, _QWEN_IM_START],
                    )
                    choice_s = (result_s.get("choices") or [{}])[0]
                    text_s = (choice_s.get("text") or "").strip()
                    fr_s = choice_s.get("finish_reason")
                    _runner_log(
                        f"runner_schema_retry: output_chars={len(text_s)} finish_reason={fr_s!r} "
                        f"temperature={schema_temp}"
                    )
                    _runner_log_output_shape(text_s)
                    if text_s and not text_s.startswith("## Inference error"):
                        text_s, san_rs = _sanitize_runner_prose(text_s, ch_totals)
                        _runner_log(
                            f"sanitize(schema_retry): tautology_lines_removed={san_rs} "
                            f"chars_after={len(text_s)}"
                        )
                    text_s, norm_s = _runner_normalize_known_h3_heads_to_h2(text_s)
                    if norm_s:
                        _runner_log(
                            "runner_heading_normalize(schema_retry): promoted ### → ## "
                            "for known advisory section titles"
                        )
                    if (
                        text_s
                        and not text_s.startswith("## Inference error")
                        and not _runner_output_is_template_echo(text_s)
                        and not _runner_output_is_context_dump(text_s)
                        and _runner_output_schema_valid(text_s)
                    ):
                        text = text_s
                        _runner_log("runner_schema_retry: accepted")
                    else:
                        _runner_log(
                            "runner_schema_retry: rejected "
                            f"(schema_ok={_runner_output_schema_valid(text_s)}, "
                            f"first_issue={_runner_schema_failure_label(text_s)!r})"
                        )
                except Exception as e:  # noqa: BLE001
                    _runner_log(f"runner_schema_retry failed: {type(e).__name__}: {e}")
            if not _runner_output_schema_valid(text):
                text = (
                    "## Inference error\n\n"
                    "Runner output did not include required `##` sections in order: "
                    "## What I reviewed → ## Summary → ## Insights → ## Risks → ## Next tries.\n"
                )

    if not text.startswith("## Inference error"):
        if ch_totals is not None:
            if not _runner_grounding_slice_ok(text, ch_totals):
                sl = _runner_slice_wir_summary(text)
                sv, sw, cv = ch_totals
                _runner_log(
                    "runner_grounding_reject: channel totals not quoted verbatim in "
                    "## What I reviewed + ## Summary slice "
                    f"slice_len={len(sl)} has_sv={bool(sl and _runner_int_in_text_as_token(sl, sv))} "
                    f"has_sw={bool(sl and _runner_int_in_text_as_token(sl, sw))} "
                    f"has_cv={bool(sl and _runner_int_in_text_as_token(sl, cv))}"
                )
                if llm is not None:
                    _runner_log("runner_grounding_retry: one completion")
                    try:
                        gr_sys = _runner_grounding_retry_system()
                        gr_user = _runner_grounding_retry_user(
                            draft=text, totals=ch_totals, ctx_used=ctx_used
                        )
                        gr_prompt = _qwen25_chat_prompt(system=gr_sys, user=gr_user)
                        gr_temp = min(temp, 0.1)
                        cap_gr = _runner_effective_max_tokens(
                            llm, prompt=gr_prompt, n_ctx_eff=n_ctx_eff, requested=cap_requested
                        )
                        res_gr = llm(
                            gr_prompt,
                            max_tokens=cap_gr,
                            temperature=gr_temp,
                            stop=[_QWEN_IM_END, _QWEN_IM_START],
                        )
                        ch_gr = (res_gr.get("choices") or [{}])[0]
                        text_gr = (ch_gr.get("text") or "").strip()
                        fr_gr = ch_gr.get("finish_reason")
                        _runner_log(
                            f"runner_grounding_retry: output_chars={len(text_gr)} "
                            f"finish_reason={fr_gr!r} temperature={gr_temp}"
                        )
                        if text_gr and not text_gr.startswith("## Inference error"):
                            text_gr, san_gr = _sanitize_runner_prose(text_gr, ch_totals)
                            _runner_log(
                                f"sanitize(grounding_retry): tautology_lines_removed={san_gr} "
                                f"chars_after={len(text_gr)}"
                            )
                        text_gr, norm_gr = _runner_normalize_known_h3_heads_to_h2(text_gr)
                        if norm_gr:
                            _runner_log(
                                "runner_heading_normalize(grounding_retry): promoted ### → ## "
                                "for known advisory section titles"
                            )
                        gr_ok = (
                            text_gr
                            and not text_gr.startswith("## Inference error")
                            and not _runner_output_is_template_echo(text_gr)
                            and not _runner_output_is_context_dump(text_gr)
                            and _runner_output_schema_valid(text_gr)
                            and _runner_grounding_slice_ok(text_gr, ch_totals)
                            and _runner_insights_nonduplicate(text_gr)
                        )
                        if gr_ok:
                            text = text_gr
                            _runner_log("runner_grounding_retry: accepted")
                        else:
                            _runner_log(
                                "runner_grounding_retry: rejected "
                                f"(schema_ok={_runner_output_schema_valid(text_gr)}, "
                                f"grounding_ok={_runner_grounding_slice_ok(text_gr, ch_totals) if text_gr else False}, "
                                f"dedup_ok={_runner_insights_nonduplicate(text_gr) if text_gr else False})"
                            )
                    except Exception as e:  # noqa: BLE001
                        _runner_log(f"runner_grounding_retry failed: {type(e).__name__}: {e}")
            # Deterministic injection: if schema is valid but grounding still fails, insert totals in WIR+Summary.
            if not text.startswith("## Inference error") and not _runner_grounding_slice_ok(text, ch_totals):
                text_inj, inj_changed = _runner_inject_channel_totals_into_wir_summary(text, ch_totals)
                if inj_changed:
                    _runner_log("runner_grounding_inject: inserted deterministic totals into WIR+Summary")
                    text = text_inj
            if not text.startswith("## Inference error") and not _runner_grounding_slice_ok(
                text, ch_totals
            ):
                text = (
                    "## Inference error\n\n"
                    "Runner output must quote **sum_views_all_videos**, **sum_watch_time_minutes_all_videos**, "
                    "and **count_videos_with_views_gt_0** from deterministic JSON verbatim in "
                    "## What I reviewed and/or ## Summary.\n"
                )
            elif not text.startswith("## Inference error") and not _runner_insights_nonduplicate(text):
                _runner_log("runner_insights_dedup_reject: duplicate numbered insights")
                text = (
                    "## Inference error\n\n"
                    "Runner output repeated the same insight text for multiple numbered items.\n"
                )

    if not text.startswith("## Inference error"):
        text, strip_n = _strip_wir_placeholder_bullets(text)
        if strip_n:
            _runner_log(f"runner_wir_strip: removed_placeholder_lines={strip_n}")

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
