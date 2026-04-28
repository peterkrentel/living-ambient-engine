#!/usr/bin/env python3
"""Validate ``agent-insight-*-runner.md`` channel totals against ``analytics*.json``.

Mirrors the sums fed into the runner CONTEXT (``_analytics_channel_totals_from_videos`` in
``agent_dual_advisory.py``): sum of ``metrics.views``, sum of ``metrics.watch_time_minutes``,
and count of videos with views > 0.

Requires those three integers to appear as distinct digit-tokens in the markdown slice from
``## What I reviewed`` through the line before ``## Insights`` (same grounding window the
runner script uses before injection).

Skip (exit 0): runner file documents LLM skip (no GGUF). Fail: missing sections, inference
error body, or totals not quoted.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parent.parent


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
    if not ana_path.is_file():
        return None
    try:
        data = json.loads(ana_path.read_text(encoding="utf-8", errors="replace"))
    except (json.JSONDecodeError, OSError, TypeError):
        return None
    videos = data.get("videos") or []
    return _analytics_channel_totals_from_videos(videos)


def _int_in_text_as_token(text: str, n: int) -> bool:
    """True if ``n`` appears with digit boundaries; commas ignored (``4,224`` matches ``4224``)."""
    t = text.replace(",", "")
    return re.search(rf"(?<!\d){re.escape(str(n))}(?!\d)", t) is not None


def _prose_quotes_channel_totals(slice_text: str, totals: tuple[int, int, int]) -> bool:
    sv, sw, cv = totals
    return (
        _int_in_text_as_token(slice_text, sv)
        and _int_in_text_as_token(slice_text, sw)
        and _int_in_text_as_token(slice_text, cv)
    )


def _slice_wir_through_before_insights(prose: str) -> str:
    """Body from ``## What I reviewed`` through just before ``## Insights``."""
    a = prose.find("## What I reviewed")
    b = prose.find("## Insights")
    if a == -1 or b == -1 or b <= a:
        return ""
    return prose[a:b]


def validate_runner_advisory(
    *, runner_text: str, totals: tuple[int, int, int]
) -> list[str]:
    errs: list[str] = []
    t = runner_text or ""
    if "_Runner LLM skipped_" in t or "_Runner LLM skipped:" in t:
        return ["SKIP: runner GGUF not executed; no totals contract to validate"]

    if "## Inference error" in t[:1200]:
        return ["runner markdown contains ## Inference error — fix CONTEXT or re-run dual advisory"]

    sl = _slice_wir_through_before_insights(t)
    if not sl.strip():
        errs.append("missing ## What I reviewed … ## Insights slice (required headings)")
    elif not _prose_quotes_channel_totals(sl, totals):
        sv, sw, cv = totals
        errs.append(
            "channel totals not all present as digit-tokens in What I reviewed+Summary slice "
            f"(expected views={sv}, watch_minutes={sw}, videos_with_views={cv}); "
            "re-run dual advisory or check analytics JSON vs runner prose"
        )
    return errs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Validate agent-insight runner markdown vs analytics JSON totals")
    ap.add_argument("--lane", choices=("brand", "personal"), required=True)
    ap.add_argument("--week", required=True, help="ISO week label e.g. 2026-W18")
    ap.add_argument("--reports-dir", type=Path, default=_REPO_ROOT / "data" / "reports")
    ap.add_argument("--analytics", type=Path, default=None, help="Override analytics JSON path")
    args = ap.parse_args(argv)

    reports: Path = args.reports_dir
    suffix = f"{args.week}-{args.lane}-runner.md"
    runner_path = reports / f"agent-insight-{suffix}"
    ana_path = args.analytics
    if ana_path is None:
        ana_path = (
            _REPO_ROOT / "data" / "analytics_personal.json"
            if args.lane == "personal"
            else _REPO_ROOT / "data" / "analytics.json"
        )

    if not runner_path.is_file():
        print(f"ERROR: runner advisory missing: {runner_path}", file=sys.stderr)
        return 2

    totals = _analytics_channel_totals_from_file(ana_path)
    if totals is None:
        print(f"ERROR: could not read analytics totals from: {ana_path}", file=sys.stderr)
        return 2

    text = runner_path.read_text(encoding="utf-8", errors="replace")
    errs = validate_runner_advisory(runner_text=text, totals=totals)
    if errs and errs[0].startswith("SKIP:"):
        print(errs[0])
        return 0
    if errs:
        print(f"runner advisory validation failed lane={args.lane} week={args.week}:", file=sys.stderr)
        for e in errs:
            print(f"- {e}", file=sys.stderr)
        return 1
    print(f"runner advisory validation OK lane={args.lane} week={args.week} totals={totals}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
