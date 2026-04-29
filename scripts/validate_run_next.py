#!/usr/bin/env python3
"""Validate deterministic `run-next` markdown against JSON inputs.

Checks **headline snapshot** bullets (retention %, watch min/video, videos with views / analyzed) and
the **Correlate bundle ``generated_at``** line against ``suggestions*.json`` so the committed
``run-next`` file cannot drift from the correlate bundle that produced it.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class RunNextSnapshot:
    overall_avg_retention: float | None
    overall_avg_watch_minutes_per_video: float | None
    videos_with_views: int | None
    videos_analyzed: int | None
    correlate_generated_at: str | None


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _parse_int(s: str) -> int | None:
    try:
        return int(s)
    except Exception:
        return None


def _parse_float(s: str) -> float | None:
    try:
        return float(s)
    except Exception:
        return None


def parse_run_next_snapshot(md: str) -> RunNextSnapshot:
    """Extract headline snapshot values from run-next markdown."""
    t = md or ""
    m_ret = re.search(r"^\s*-\s+\*\*Overall avg retention:\*\*\s+([0-9]+(?:\.[0-9]+)?)%\s*$", t, re.M)
    m_oaw = re.search(
        r"^\s*-\s+\*\*Overall avg watch min / video \(window\):\*\*\s+([0-9]+(?:\.[0-9]+)?)\s*$",
        t,
        re.M,
    )
    m_videos = re.search(
        r"^\s*-\s+\*\*Videos analyzed:\*\*\s+(\d+)\s+with views\s+/\s+(\d+)\s+total\s*$",
        t,
        re.M,
    )
    return RunNextSnapshot(
        overall_avg_retention=_parse_float(m_ret.group(1)) if m_ret else None,
        overall_avg_watch_minutes_per_video=_parse_float(m_oaw.group(1)) if m_oaw else None,
        videos_with_views=_parse_int(m_videos.group(1)) if m_videos else None,
        videos_analyzed=_parse_int(m_videos.group(2)) if m_videos else None,
        correlate_generated_at=parse_correlate_generated_at_line(t),
    )


def parse_suggestions_snapshot(data: dict) -> RunNextSnapshot:
    """Extract the same snapshot values from suggestions JSON."""
    gen = data.get("generated_at")
    gen_s = str(gen).strip() if gen is not None else None
    return RunNextSnapshot(
        overall_avg_retention=_parse_float(str(data.get("overall_avg_retention"))) if data.get("overall_avg_retention") is not None else None,
        overall_avg_watch_minutes_per_video=_parse_float(str(data.get("overall_avg_watch_minutes_per_video")))
        if data.get("overall_avg_watch_minutes_per_video") is not None
        else None,
        videos_with_views=_parse_int(str(data.get("videos_with_views"))) if data.get("videos_with_views") is not None else None,
        videos_analyzed=_parse_int(str(data.get("videos_analyzed"))) if data.get("videos_analyzed") is not None else None,
        correlate_generated_at=gen_s,
    )


def _float_close(a: float | None, b: float | None, tol: float = 1e-3) -> bool:
    if a is None or b is None:
        return a is b
    return abs(a - b) <= tol


def _normalize_generated_at(s: str) -> str:
    """Loosen Z vs +00:00 and whitespace for correlate timestamp comparison."""
    t = (s or "").strip()
    if t.endswith("Z"):
        t = t[:-1] + "+00:00"
    return t


def parse_correlate_generated_at_line(md: str) -> str | None:
    """Value after ``**Correlate bundle `generated_at`:**`` if present."""
    m = re.search(
        r"^\*\*Correlate bundle `generated_at`:\*\*\s*(.+?)\s*$",
        md or "",
        re.M,
    )
    return m.group(1).strip() if m else None


def validate_run_next(*, run_next_text: str, suggestions_data: dict) -> list[str]:
    """Return a list of human-readable errors (empty means OK)."""
    errs: list[str] = []
    md = parse_run_next_snapshot(run_next_text)
    js = parse_suggestions_snapshot(suggestions_data)

    if md.correlate_generated_at is None:
        errs.append("run-next missing line: **Correlate bundle `generated_at`:** …")
    elif not js.correlate_generated_at:
        errs.append("suggestions JSON missing: generated_at (run-next cites correlate bundle timestamp)")
    elif _normalize_generated_at(md.correlate_generated_at) != _normalize_generated_at(js.correlate_generated_at):
        errs.append(
            "generated_at mismatch: run-next correlate line vs suggestions.json "
            f"({md.correlate_generated_at!r} vs {js.correlate_generated_at!r})"
        )

    if md.overall_avg_retention is None:
        errs.append("run-next snapshot missing: overall_avg_retention")
    elif js.overall_avg_retention is None:
        errs.append("suggestions JSON missing: overall_avg_retention")
    elif not _float_close(md.overall_avg_retention, js.overall_avg_retention, tol=1e-3):
        errs.append(
            f"overall_avg_retention mismatch: run-next={md.overall_avg_retention} vs suggestions={js.overall_avg_retention}"
        )

    # Watch-min snapshot is optional in some bundles; validate only if present in either.
    if md.overall_avg_watch_minutes_per_video is not None or js.overall_avg_watch_minutes_per_video is not None:
        if md.overall_avg_watch_minutes_per_video is None:
            errs.append("run-next snapshot missing: overall_avg_watch_minutes_per_video")
        elif js.overall_avg_watch_minutes_per_video is None:
            errs.append("suggestions JSON missing: overall_avg_watch_minutes_per_video")
        elif not _float_close(md.overall_avg_watch_minutes_per_video, js.overall_avg_watch_minutes_per_video, tol=1e-3):
            errs.append(
                "overall_avg_watch_minutes_per_video mismatch: "
                f"run-next={md.overall_avg_watch_minutes_per_video} vs suggestions={js.overall_avg_watch_minutes_per_video}"
            )

    if md.videos_with_views is None or md.videos_analyzed is None:
        errs.append("run-next snapshot missing: videos analyzed line (with views / total)")
    else:
        if js.videos_with_views is None:
            errs.append("suggestions JSON missing: videos_with_views")
        elif md.videos_with_views != js.videos_with_views:
            errs.append(f"videos_with_views mismatch: run-next={md.videos_with_views} vs suggestions={js.videos_with_views}")
        if js.videos_analyzed is None:
            errs.append("suggestions JSON missing: videos_analyzed")
        elif md.videos_analyzed != js.videos_analyzed:
            errs.append(f"videos_analyzed mismatch: run-next={md.videos_analyzed} vs suggestions={js.videos_analyzed}")

    return errs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Validate run-next markdown snapshot vs suggestions JSON")
    ap.add_argument("--lane", choices=("brand", "personal"), required=True)
    ap.add_argument("--week", required=True, help="ISO week label e.g. 2026-W18")
    ap.add_argument("--reports-dir", default=str(_REPO_ROOT / "data" / "reports"))
    ap.add_argument("--suggestions", required=True, help="Path to suggestions*.json used by correlate")
    args = ap.parse_args(argv)

    reports = Path(args.reports_dir)
    sug_path = Path(args.suggestions)
    run_next_path = reports / (f"run-next-{args.week}-personal.md" if args.lane == "personal" else f"run-next-{args.week}.md")

    if not run_next_path.exists():
        print(f"ERROR: run-next file missing: {run_next_path}")
        return 2
    if not sug_path.exists():
        print(f"ERROR: suggestions JSON missing: {sug_path}")
        return 2

    try:
        sug = json.loads(_read_text(sug_path))
    except json.JSONDecodeError as e:
        print(f"ERROR: suggestions JSON unreadable: {sug_path} ({e})")
        return 2

    errs = validate_run_next(run_next_text=_read_text(run_next_path), suggestions_data=sug)
    if errs:
        print(f"run-next validation failed for lane={args.lane} week={args.week}:")
        for e in errs:
            print(f"- {e}")
        return 1
    print(f"run-next validation OK for lane={args.lane} week={args.week}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

