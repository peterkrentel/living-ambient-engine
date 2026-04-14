#!/usr/bin/env python3
"""Channel coverage audit from committed analytics (no YouTube API calls).

Writes data/reports/audit-YYYY-WW.md and optionally appends to GITHUB_STEP_SUMMARY.
Uses the same classification as scripts/correlate.py (imported dynamically).

Run from repo root: python scripts/audit_channel.py
"""
from __future__ import annotations

import importlib.util
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

# Load correlate as a module (scripts/ is not a package)
_CORRELATE_PATH = _REPO_ROOT / "scripts" / "correlate.py"
_spec = importlib.util.spec_from_file_location("correlate", _CORRELATE_PATH)
_corr = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_corr)

load_analytics = _corr.load_analytics
calculate_correlations = _corr.calculate_correlations
generate_coverage_report = _corr.generate_coverage_report

from agent.log_generation import load_generations  # noqa: E402

REPORTS_DIR = _REPO_ROOT / "data" / "reports"
ANALYTICS_PATH = _REPO_ROOT / "data" / "analytics.json"


def _iso_week_file_suffix() -> str:
    """YYYY-Www for report filename (calendar ISO week)."""
    now = datetime.now(timezone.utc)
    y, w, _ = now.isocalendar()
    return f"{y}-W{w:02d}"


def _ledger_join_stats(videos: list) -> tuple[int, int, float]:
    """Return (analytics_count, with_ledger_row, pct)."""
    data = load_generations()
    rows = data.get("videos") or []
    ledger_ids = {r.get("video_id") for r in rows if r.get("video_id")}
    n = 0
    hit = 0
    for v in videos:
        vid = v.get("video_id")
        if not vid:
            continue
        n += 1
        if vid in ledger_ids:
            hit += 1
    pct = (100.0 * hit / n) if n else 0.0
    return n, hit, pct


def write_audit_report() -> Path:
    data = load_analytics()
    if not data:
        raise SystemExit("No analytics data — run fetch_analytics first")

    videos = data.get("videos") or []
    fetched_at = data.get("fetched_at", "")
    dr = data.get("date_range") or {}

    by_mood, by_art, by_music, by_cat = calculate_correlations(videos)
    coverage = generate_coverage_report(by_mood, by_art, by_music)

    moods_cov = coverage.get("moods") or {}
    missing_moods = [m for m, s in moods_cov.items() if s.get("total", 0) == 0]

    combos = coverage.get("art_music_combos") or {}
    missing_combos = [k for k, s in combos.items() if s.get("total", 0) == 0]
    present_combos = len(combos) - len(missing_combos)

    n_vid, n_ledger, pct_ledger = _ledger_join_stats(videos)

    week = _iso_week_file_suffix()
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = REPORTS_DIR / f"audit-{week}.md"

    lines = [
        f"# Channel coverage audit ({week})",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Analytics `fetched_at`: {fetched_at}",
        f"Analytics window: `{dr.get('start', '')}` → `{dr.get('end', '')}`",
        "",
        "## Overview",
        "",
        f"- **Videos in analytics.json:** {len(videos)}",
        f"- **generations.json join:** {n_ledger} / {n_vid} video_ids with a ledger row ({pct_ledger:.1f}%)",
        "  - *Historic uploads may lack rows until logged by current upload pipeline.*",
        "",
        "## 14 mood presets (brand SEO line)",
        "",
        "| Mood | Videos | With views |",
        "|------|--------|------------|",
    ]
    for mood in sorted(moods_cov.keys()):
        s = moods_cov[mood]
        lines.append(f"| `{mood}` | {s.get('total', 0)} | {s.get('with_views', 0)} |")

    lines.extend(
        [
            "",
            f"**Missing presets (0 videos):** {', '.join(f'`{m}`' for m in missing_moods) or 'none — all 14 present'}",
            "",
            "## Art × music grid (9×9)",
            "",
            f"- **Combos with ≥1 video:** {present_combos} / 81",
            f"- **Combos with 0 videos:** {len(missing_combos)}",
            "",
        ]
    )
    if missing_combos and len(missing_combos) <= 40:
        lines.append("Missing: " + ", ".join(f"`{c}`" for c in sorted(missing_combos)))
    elif missing_combos:
        lines.append(f"*(Too many to list; {len(missing_combos)} missing.)*")

    lines.extend(
        [
            "",
            "## Category counts",
            "",
            "| Category | Videos |",
            "|----------|--------|",
        ]
    )
    for cat, rows in sorted(by_cat.items()):
        lines.append(f"| {cat} | {len(rows)} |")

    lines.append("")
    lines.append("---")
    lines.append("*Produced by `scripts/audit_channel.py` in the Analytics Agent workflow.*")
    lines.append("")

    text = "\n".join(lines)
    out_path.write_text(text, encoding="utf-8")
    print(f"✅ Wrote {out_path.relative_to(_REPO_ROOT)}")
    return out_path


def append_step_summary(markdown_path: Path) -> None:
    gs = os.environ.get("GITHUB_STEP_SUMMARY")
    if not gs:
        return
    body = markdown_path.read_text(encoding="utf-8")
    with open(gs, "a", encoding="utf-8") as f:
        f.write("\n## Channel coverage audit\n\n")
        # Keep summary readable (full file is in repo)
        for line in body.splitlines()[:120]:
            f.write(line + "\n")
        if len(body.splitlines()) > 120:
            f.write("\n*(Truncated — see full report in `data/reports/`.)*\n")


def main() -> None:
    os.chdir(_REPO_ROOT)
    path = write_audit_report()
    append_step_summary(path)


if __name__ == "__main__":
    main()
