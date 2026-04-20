#!/usr/bin/env python3
"""Dual advisory v0: Gemini (API) + small GGUF on the workflow runner (e.g. Qwen2.5-0.5B).

Both run **in parallel** (threads) after deterministic ``run-next``. Same fixed bundle as
Phase 6 — advisory only, not ``run_intent`` / ``batch_generate``.

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
MAX_CONTEXT_RUNNER = 12_000
MAX_RUNNER_TOKENS = 384
DEFAULT_GGUF = Path.home() / ".cache" / "living-agent" / "qwen2.5-0.5b-instruct-q4_k_m.gguf"
DEFAULT_GGUF_URL = (
    "https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/"
    "qwen2.5-0.5b-instruct-q4_k_m.gguf"
)


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
        "Use ONLY the CONTEXT below. If the planner blocked or data is thin, say so plainly.\n"
        "Output GitHub-flavored markdown with sections: ## Summary, ## Risks / caveats, "
        "## Experiments or packaging ideas (bullets).\n"
        "Do not invent statistics; quote approximate values only if present in CONTEXT.\n\n"
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
        return
    url = _gguf_url()
    print(f"Downloading GGUF → {path} …")
    req = urllib.request.Request(url, headers={"User-Agent": "living-ambient-engine-agent-dual/1"})
    with urllib.request.urlopen(req, timeout=900) as resp, path.open("wb") as out:
        shutil.copyfileobj(resp, out, length=1024 * 1024)


def write_runner_gguf(lane: str, week: str, bundle: str) -> Path:
    out = REPORTS / f"agent-insight-{week}-{lane}-runner.md"
    out.parent.mkdir(parents=True, exist_ok=True)

    try:
        from llama_cpp import Llama  # noqa: WPS433
    except ImportError:
        out.write_text(
            _header_runner(lane, week)
            + "_Runner LLM skipped:_ `llama-cpp-python` not installed (e.g. `pip install llama-cpp-python`).\n",
            encoding="utf-8",
        )
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
        print(f"Runner GGUF download failed: {e}; wrote {out}")
        return out

    prompt = (
        "[INST]You are a compact advisor for a YouTube ambient channel. Use only CONTEXT. "
        "Output markdown: ## Summary, ## Risks, ## Ideas (bullets). Under 350 words.[/INST]\n"
        f"CONTEXT:\n{bundle[:MAX_CONTEXT_RUNNER]}"
    )
    try:
        llm = Llama(
            model_path=str(gguf),
            n_ctx=2048,
            n_threads=int(os.environ.get("AGENT_LLAMA_THREADS", "4")),
            n_gpu_layers=0,
            verbose=False,
        )
        result = llm(
            prompt,
            max_tokens=MAX_RUNNER_TOKENS,
            temperature=0.25,
            stop=["</s>", "[INST]"],
        )
        text = (result["choices"][0]["text"] or "").strip() or "(empty runner response)"
    except Exception as e:  # noqa: BLE001 — advisory path; always write markdown
        text = f"## Inference error\n\n`{type(e).__name__}`: {e}\n"

    out.write_text(_header_runner(lane, week) + text + "\n", encoding="utf-8")
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
    bundle = build_bundle(args.lane, week)

    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = {
            pool.submit(write_gemini, args.lane, week, bundle): "gemini",
            pool.submit(write_runner_gguf, args.lane, week, bundle): "runner",
        }
        for fut in as_completed(futures):
            fut.result()


if __name__ == "__main__":
    main()
