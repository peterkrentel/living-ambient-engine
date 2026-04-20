#!/usr/bin/env python3
"""Dual advisory v0: Gemini (API) + GGUF on the workflow runner (default Qwen2.5-1.5B Instruct q4).

Both run **in parallel** (threads) after deterministic ``run-next``. **Gemini** sees the full
file bundle; **runner GGUF** uses a **lean** bundle (run-next + compact JSON + short reports)
so small ``n_ctx`` fits. Advisory only — not ``run_intent`` / ``batch_generate``.

Outputs (per lane ``brand`` | ``personal``):

- ``data/reports/agent-insight-YYYY-WW-{lane}-gemini.md``
- ``data/reports/agent-insight-YYYY-WW-{lane}-runner.md`` (GGUF; CPU on GitHub-hosted runners)

  pip install llama-cpp-python   # runner path only; Gemini uses stdlib + REST
  GEMINI_API_KEY=... python scripts/agent_dual_advisory.py --lane brand --week 2026-W16

Week label: ISO calendar (same as ``audit_channel`` / ``run_next_report``).
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
REPORTS = _REPO / "data" / "reports"
DATA = _REPO / "data"

_DEFAULT_GEMINI = "gemini-2.0-flash"
MAX_CONTEXT_GEMINI = 24_000
# Runner GGUF: small n_ctx; char→token ratio ~3–4 for EN/JSON — keep prompt+context safely under n_ctx.
RUNNER_BUNDLE_MAX_CHARS = 4200
MAX_RUNNER_TOKENS = 512
_LLAMA_N_CTX = 4096
DEFAULT_GGUF = Path.home() / ".cache" / "living-agent" / "qwen2.5-1.5b-instruct-q4_k_m.gguf"


def _runner_log(msg: str) -> None:
    """Lines show in GitHub Actions job logs for the non-cloud path."""
    print(f"[runner-advisory] {msg}", flush=True)


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


def _compact_suggestions(path: Path, max_chars: int = 2200) -> str:
    """Correlate JSON without huge ``coverage`` grids — keeps top suggestion rows + headline stats."""
    if not path.exists():
        rel = path.relative_to(_REPO) if path.is_relative_to(_REPO) else path
        return f"(missing: {rel})"
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError:
        return _read(path, 1200)
    slim = {
        "generated_at": data.get("generated_at"),
        "overall_avg_retention": data.get("overall_avg_retention"),
        "overall_avg_watch_minutes_per_video": data.get("overall_avg_watch_minutes_per_video"),
        "videos_analyzed": data.get("videos_analyzed"),
        "videos_with_views": data.get("videos_with_views"),
        "suggestions": (data.get("suggestions") or [])[:15],
    }
    text = json.dumps(slim, indent=2, ensure_ascii=False)
    if len(text) > max_chars:
        return text[: max_chars - 40] + "\n… truncated suggestions json\n"
    return text


def _compact_analytics(path: Path, max_chars: int = 1600) -> str:
    """Top videos by views only (no descriptions) — analytics JSON is huge on disk."""
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

    top = sorted(videos, key=_views, reverse=True)[:10]
    rows: list[dict] = []
    for v in top:
        m = v.get("metrics") or {}
        rows.append(
            {
                "title": ((v.get("title") or "")[:90]),
                "views": m.get("views"),
                "avg_pct": m.get("average_view_percentage"),
                "watch_min": m.get("watch_time_minutes"),
            }
        )
    slim = {"fetched_at": data.get("fetched_at"), "n_videos": len(videos), "top_by_views": rows}
    text = json.dumps(slim, ensure_ascii=False, separators=(",", ":"))
    if len(text) > max_chars:
        return text[: max_chars - 30] + "…"
    return text


def build_runner_bundle(lane: str, week: str) -> str:
    """Lean context for small GGUF: run-next + compact JSON + short prose (fits ``n_ctx``)."""
    if lane == "personal":
        weekly = REPORTS / f"{week}-personal.md"
        run_next = REPORTS / f"run-next-{week}-personal.md"
        blocked = REPORTS / "run-intent-blocked-personal.md"
        sug_path = DATA / "suggestions_personal.json"
        ana_path = DATA / "analytics_personal.json"
    else:
        weekly = REPORTS / f"{week}.md"
        run_next = REPORTS / f"run-next-{week}.md"
        blocked = REPORTS / "run-intent-blocked.md"
        sug_path = DATA / "suggestions.json"
        ana_path = DATA / "analytics.json"

    parts = [
        "### run-next (priority)\n\n" + _read(run_next, 3800),
        "### weekly report\n\n" + _read(weekly, 2200),
        "### run-intent blocked\n\n" + _read(blocked, 1200),
        "### suggestions (compact)\n\n" + _compact_suggestions(sug_path),
        "### analytics (compact top videos)\n\n" + _compact_analytics(ana_path),
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


def write_gemini(lane: str, week: str, bundle: str) -> Path:
    out = REPORTS / f"agent-insight-{week}-{lane}-gemini.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        out.write_text(
            _header_gemini(lane, week)
            + "_Gemini skipped:_ set repository secret `GEMINI_API_KEY` to enable API calls.\n",
            encoding="utf-8",
        )
        print(f"Wrote {out} (Gemini skipped, no API key)")
        return out

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
        f"## CONTEXT\n\n{bundle[:MAX_CONTEXT_GEMINI]}"
    )
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.35, "maxOutputTokens": 1024},
    }
    url = f"{_gemini_url()}?key={key}"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")[:4000]
        text = _header_gemini(lane, week) + f"## API error\n\n```\n{e.code}\n{err_body}\n```\n"
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
        "Respond AS IF you finished reading that bundle, then give concise interpretation.\n"
        "Required shape (GitHub-flavored markdown, under ~450 words, no outer ``` fences):\n"
        "## What I reviewed — 2–3 sentences naming the kinds of inputs (e.g. run-next, suggestions excerpt, weekly report).\n"
        "## Insights — numbered 1–5. Each: one short paragraph. Prefer mood/style/packaging angles when CONTEXT supports them. "
        "If an item is not directly supported, start that paragraph with **Speculative:**.\n"
        "## Risks — short bullets (thin data, confounders, contradictions in CONTEXT).\n"
        "## Next tries — bullets (concrete experiments; no invented metrics).\n"
        "Do not paste large tables; at most one tiny 3-row markdown table if essential. "
        "Numbers must match CONTEXT; never fabricate counts."
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
    _runner_log(
        f"llama: n_ctx={_LLAMA_N_CTX} max_output_tokens={MAX_RUNNER_TOKENS} "
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
            max_tokens=MAX_RUNNER_TOKENS,
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
