#!/usr/bin/env python3
"""Channel coverage audit from committed analytics (no YouTube API calls).

Writes ``data/reports/audit-YYYY-WW.md`` (brand) or ``audit-YYYY-WW{suffix}.md`` when
``ANALYTICS_REPORT_SUFFIX`` is set (e.g. ``-personal`` for the personal workflow).

Uses the same classification as ``scripts/correlate.py`` (imported dynamically).
``ANALYTICS_JSON_PATH`` selects the analytics file (default ``data/analytics.json``).
``ANALYTICS_CHANNEL`` may be ``brand`` or ``personal``; if unset, personal is inferred
when the analytics filename contains ``personal``.

Run from repo root: ``python scripts/audit_channel.py``
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

from agent.log_generation import video_id_index  # noqa: E402

REPORTS_DIR = _REPO_ROOT / "data" / "reports"


def _iso_week_file_suffix() -> str:
    """YYYY-Www for report filename (calendar ISO week)."""
    now = datetime.now(timezone.utc)
    y, w, _ = now.isocalendar()
    return f"{y}-W{w:02d}"


def _analytics_json_path() -> Path:
    rel = os.environ.get("ANALYTICS_JSON_PATH", "data/analytics.json").strip() or "data/analytics.json"
    p = Path(rel)
    return p if p.is_absolute() else _REPO_ROOT / p


def resolve_youtube_identity() -> str:
    """Which YouTube channel this analytics file belongs to (brand vs personal)."""
    raw = os.environ.get("ANALYTICS_CHANNEL", "").strip().lower()
    if raw in ("brand", "personal"):
        return raw
    name = _analytics_json_path().name.lower()
    if "personal" in name:
        return "personal"
    return "brand"


def _audit_report_filename_suffix() -> str:
    return os.environ.get("ANALYTICS_REPORT_SUFFIX", "").strip()


def _ledger_row_identity(row: dict) -> str | None:
    """Return brand / personal when known; else None (legacy or ambiguous workflow)."""
    ch = row.get("channel")
    if ch in ("brand", "personal"):
        return ch
    wf = row.get("workflow") or ""
    if "Personal" in wf:
        return "personal"
    if "Brand" in wf:
        return "brand"
    return None


def _ledger_join_stats(videos: list, identity: str) -> tuple[int, int, float, int, float]:
    """Return (n_videos, any_ledger_hits, pct_any, aligned_hits, pct_aligned)."""
    gen_by_vid = video_id_index()
    n = 0
    any_hit = 0
    aligned = 0
    for v in videos:
        vid = v.get("video_id")
        if not vid:
            continue
        n += 1
        row = gen_by_vid.get(vid)
        if not row:
            continue
        any_hit += 1
        if _ledger_row_identity(row) == identity:
            aligned += 1
    pct_any = (100.0 * any_hit / n) if n else 0.0
    pct_aligned = (100.0 * aligned / n) if n else 0.0
    return n, any_hit, pct_any, aligned, pct_aligned


def write_audit_report() -> Path:
    analytics_path = _analytics_json_path()
    identity = resolve_youtube_identity()

    data = load_analytics()
    if not data:
        raise SystemExit(f"No analytics data — expected JSON at {analytics_path}")

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

    n_vid, n_ledger_any, pct_any, n_ledger_aligned, pct_aligned = _ledger_join_stats(videos, identity)

    week = _iso_week_file_suffix()
    suffix = _audit_report_filename_suffix()
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = REPORTS_DIR / f"audit-{week}{suffix}.md"

    analytics_display = str(analytics_path.relative_to(_REPO_ROOT))

    mood_section_title = "## Mood preset coverage"
    mood_note = ""
    if identity == "brand":
        mood_note = " *(brand SEO line: 14 presets)*"

    lines = [
        f"# Channel coverage audit ({week})",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"**YouTube identity (this run):** `{identity}`",
        f"**Analytics file:** `{analytics_display}`",
        f"Analytics `fetched_at`: {fetched_at}",
        f"Analytics window: `{dr.get('start', '')}` → `{dr.get('end', '')}`",
        "",
        "## Overview",
        "",
        f"- **Videos in analytics:** {len(videos)}",
        f"- **generations.json join (any ledger row):** {n_ledger_any} / {n_vid} ({pct_any:.1f}%)",
        f"- **generations.json join (identity-aligned):** {n_ledger_aligned} / {n_vid} ({pct_aligned:.1f}%)",
        "  - *Identity-aligned uses optional ledger `channel`, else infers from `workflow` (e.g. `Content Factory (Brand)`). Rows with neither still count only toward “any”.*",
        "  - *Historic uploads may lack rows until logged by the upload pipeline.*",
        "",
        f"{mood_section_title}{mood_note}",
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
    lines.append("*Produced by `scripts/audit_channel.py` (Analytics Agent or Analytics Agent Personal).*")
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
    scope = "personal" if "personal" in markdown_path.name.lower() else "brand"
    with open(gs, "a", encoding="utf-8") as f:
        f.write(f"\n## Channel coverage audit ({scope})\n\n")
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
