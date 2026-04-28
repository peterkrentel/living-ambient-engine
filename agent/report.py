#!/usr/bin/env python3
"""Generate performance reports.

Creates weekly performance reports correlating generation parameters
with YouTube Analytics data.

**Inputs:** ``ANALYTICS_JSON_PATH`` (default ``data/analytics.json``). For the
personal experiment, set ``ANALYTICS_JSON_PATH=data/analytics_personal.json``,
``ANALYTICS_CHANNEL=personal``, and ``ANALYTICS_REPORT_SUFFIX=-personal`` so
reports are clearly scoped and filenames do not collide with brand.

Spec: docs/spec/AGENT.md
Contract: docs/spec/contracts/agent-youtube.md
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


DATA_DIR = Path("data")
REPORTS_DIR = DATA_DIR / "reports"
GENERATIONS_FILE = DATA_DIR / "generations.json"
DEFAULT_ANALYTICS_JSON = str(DATA_DIR / "analytics.json")


def analytics_json_path() -> Path:
    return Path(os.environ.get("ANALYTICS_JSON_PATH", DEFAULT_ANALYTICS_JSON))


def report_filename_suffix() -> str:
    """Suffix before ``.md`` (e.g. ``-personal`` → ``2026-W16-personal.md``)."""
    return os.environ.get("ANALYTICS_REPORT_SUFFIX", "").strip()


def is_personal_report_scope() -> bool:
    return os.environ.get("ANALYTICS_CHANNEL", "").strip().lower() == "personal"


def _md_table_cell(value: Any, *, max_chars: int = 40) -> str:
    """Make a value safe inside a pipe-markdown table cell (GitHub-flavored).

    YouTube titles often contain ``|`` as a separator; unescaped pipes break
    column alignment. Newlines would break the table row.
    """
    s = "" if value is None else str(value)
    s = s.replace("\r\n", "\n").replace("\r", "\n").replace("\n", " ").replace("|", "\u00b7")
    s = " ".join(s.split()).strip()
    if max_chars > 0 and len(s) > max_chars:
        s = s[:max_chars].rstrip()
    return s


def load_generations() -> Dict[str, Any]:
    """Load generations data."""
    if GENERATIONS_FILE.exists():
        with open(GENERATIONS_FILE, "r") as f:
            return json.load(f)
    return {"videos": []}


def load_analytics() -> Dict[str, Any]:
    """Load analytics data from ``analytics_json_path()``."""
    path = analytics_json_path()
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return {"videos": []}


def parse_mood_from_title(title: str) -> Optional[str]:
    """Extract mood from video title.

    Titles are structured like:
    - "Deep Focus | 5 Minutes | ..." -> deep_focus
    - "Ambient Baroque | ..." -> (art-creator, no mood)
    - "Rain Sleep | ..." -> rain_sleep
    """
    if not title:
        return None

    # Known mood keywords (from moods.yaml)
    mood_patterns = {
        "deep focus": "deep_focus",
        "rain sleep": "rain_sleep",
        "ocean waves": "ocean_waves",
        "fireplace": "fireplace",
        "forest morning": "forest_morning",
        "sleep": "sleep",
        "chill": "chill",
        "study": "study",
        "energize": "energize",
        "lofi study": "lofi_study",
        "piano relax": "piano_relax",
        "warrior": "warrior",
        "ceremony": "ceremony",
        "trance": "trance",
    }

    title_lower = title.lower()
    for pattern, mood in mood_patterns.items():
        if pattern in title_lower:
            return mood

    # Art-creator titles start with "Ambient" but don't have moods
    if title_lower.startswith("ambient"):
        return "art_creator"

    return None


def correlate_data() -> List[Dict[str, Any]]:
    """Get video data from analytics (fetch_all stores video metadata).

    Since fetch_all() now stores title/description/published_at directly
    in analytics.json, we can work without generations.json.
    """
    analytics = load_analytics()

    # Try generations.json first for richer data (if available)
    generations = load_generations()
    gen_by_id = {v["video_id"]: v for v in generations.get("videos", []) if v.get("video_id")}

    correlated = []
    for video in analytics.get("videos", []):
        vid = video.get("video_id")
        if not vid:
            continue

        # Skip deleted/private videos (shouldn't be in data, but filter just in case)
        title = video.get("title", "")
        if title in ("Deleted video", "Private video", ""):
            continue

        # If we have generation data, use it
        gen = gen_by_id.get(vid, {})

        # Parse mood from title if not in generation data
        title = video.get("title") or gen.get("metadata", {}).get("title", "")
        mood = gen.get("mood") or parse_mood_from_title(title)

        entry = {
            "video_id": vid,
            "title": title,
            "workflow": gen.get("workflow"),
            "mood": mood,
            "duration_seconds": gen.get("duration_seconds"),
            "params": gen.get("params", {}),
            "metadata": {"title": title, "description": video.get("description", "")},
            "generated_at": gen.get("generated_at") or video.get("published_at"),
            "metrics": video.get("metrics", {}),
        }
        correlated.append(entry)

    return correlated


def generate_report(data: List[Dict[str, Any]], week: Optional[str] = None) -> str:
    """Generate a markdown performance report.
    
    Args:
        data: Correlated generation + analytics data
        week: Week identifier (YYYY-WW format), defaults to current week
    
    Returns:
        Markdown report content
    """
    if week is None:
        now = datetime.now(timezone.utc)
        week = f"{now.year}-W{now.isocalendar()[1]:02d}"

    raw = load_analytics()
    dr = raw.get("date_range") or {}
    w_start, w_end = dr.get("start"), dr.get("end")
    if w_start and w_end:
        window_bullet = (
            f"- **Analytics window:** `{w_start}` → `{w_end}` "
            f"(YouTube Analytics API range for metrics below. "
            f"In Studio, pick the **same** custom dates when comparing totals — "
            f"not e.g. “Last 28 days” unless `fetch_analytics` used `--days 28`.)"
        )
    else:
        window_bullet = "- **Analytics window:** _(missing — re-run `fetch_analytics`)_"

    if is_personal_report_scope():
        title = f"# Personal channel — Analytics Report ({week})"
        scope_lines = [
            "",
            "> **Channel scope:** Personal YouTube only. Data file: `data/analytics_personal.json`. "
            "Brand metrics live in `data/analytics.json` (main Analytics Agent workflow).",
            "",
        ]
    else:
        title = f"# Analytics Report - {week}"
        scope_lines = [""]

    lines = [
        title,
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
    ]
    lines.extend(scope_lines)
    lines.extend(
        [
            "## Summary",
            "",
            window_bullet,
            f"- **Total videos tracked:** {len(data)}",
            f"- **Videos with analytics:** {sum(1 for d in data if d.get('metrics'))}",
            "",
        ]
    )
    
    # Calculate totals
    total_views = sum(d.get("metrics", {}).get("views", 0) for d in data)
    total_watch_time = sum(d.get("metrics", {}).get("watch_time_minutes", 0) for d in data)
    total_subs = sum(d.get("metrics", {}).get("subscribers_gained", 0) for d in data)
    
    lines.extend([
        "## Totals",
        "",
        f"- **Total views:** {total_views:,}",
        f"- **Total watch time:** {total_watch_time:,.0f} minutes",
        f"- **Subscribers gained:** {total_subs}",
        "",
    ])
    
    # Top performers by retention
    with_retention = [d for d in data if d.get("metrics", {}).get("average_view_percentage")]
    if with_retention:
        top_retention = sorted(
            with_retention,
            key=lambda x: x["metrics"]["average_view_percentage"],
            reverse=True
        )[:5]
        
        lines.extend([
            "## Top 5 by Retention",
            "",
            "| Video | Mood | Retention % | Views |",
            "|-------|------|-------------|-------|",
        ])
        for v in top_retention:
            title = _md_table_cell(
                v.get("title") or v.get("metadata", {}).get("title") or v["video_id"],
                max_chars=40,
            )
            mood = _md_table_cell(v.get("mood", "N/A"), max_chars=64)
            ret = v["metrics"]["average_view_percentage"]
            views = v["metrics"].get("views", 0)
            lines.append(f"| {title} | {mood} | {ret:.1f}% | {views:,} |")
        lines.append("")
    
    # Top performers by views
    with_views = [d for d in data if d.get("metrics", {}).get("views")]
    if with_views:
        top_views = sorted(with_views, key=lambda x: x["metrics"]["views"], reverse=True)[:5]
        
        lines.extend([
            "## Top 5 by Views",
            "",
            "| Video | Mood | Views | Watch Time (min) |",
            "|-------|------|-------|------------------|",
        ])
        for v in top_views:
            title = _md_table_cell(
                v.get("title") or v.get("metadata", {}).get("title") or v["video_id"],
                max_chars=40,
            )
            mood = _md_table_cell(v.get("mood", "N/A"), max_chars=64)
            views = v["metrics"]["views"]
            wt = v["metrics"].get("watch_time_minutes", 0)
            lines.append(f"| {title} | {mood} | {views:,} | {wt:,.0f} |")
        lines.append("")
    
    # Breakdown by mood
    mood_stats: Dict[str, Dict[str, float]] = {}
    for d in data:
        mood = d.get("mood") or "unknown"
        if mood not in mood_stats:
            mood_stats[mood] = {"count": 0, "views": 0, "retention_sum": 0, "retention_count": 0}
        mood_stats[mood]["count"] += 1
        mood_stats[mood]["views"] += d.get("metrics", {}).get("views", 0)
        ret = d.get("metrics", {}).get("average_view_percentage")
        if ret:
            mood_stats[mood]["retention_sum"] += ret
            mood_stats[mood]["retention_count"] += 1

    if mood_stats:
        lines.extend([
            "## Performance by Mood",
            "",
            "| Mood | Videos | Total Views | Avg Retention |",
            "|------|--------|-------------|---------------|",
        ])
        for mood, stats in sorted(mood_stats.items(), key=lambda x: x[1]["views"], reverse=True):
            avg_ret = stats["retention_sum"] / stats["retention_count"] if stats["retention_count"] > 0 else 0
            mood_cell = _md_table_cell(mood, max_chars=64)
            lines.append(f"| {mood_cell} | {stats['count']} | {stats['views']:,} | {avg_ret:.1f}% |")
        lines.append("")

    if is_personal_report_scope():
        next_steps = [
            "## Next steps (personal)",
            "",
            "1. Compare retention and watch time vs brand weekly reports when cross-analyzing.",
            "2. Double down on topics and lengths that cluster with watch time; deprioritize low performers.",
            "3. Optional: extend the personal fetcher (CTR, impressions) per docs/PERSONAL_ANALYTICS.md.",
            "",
        ]
    else:
        next_steps = [
            "## Next Steps",
            "",
            "1. Review top performers - what parameters correlate with success?",
            "2. Review low performers - what should be adjusted?",
            "3. Update moods.yaml based on learnings",
            "",
        ]

    lines.extend(next_steps)
    lines.extend(
        [
            "---",
            "",
            "*Report generated by Analytics Agent - docs/spec/AGENT.md*",
        ]
    )

    return "\n".join(lines)


def save_report(content: str, week: Optional[str] = None) -> Path:
    """Save report to file."""
    if week is None:
        now = datetime.now(timezone.utc)
        week = f"{now.year}-W{now.isocalendar()[1]:02d}"

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    suffix = report_filename_suffix()
    report_path = REPORTS_DIR / f"{week}{suffix}.md"

    with open(report_path, "w") as f:
        f.write(content)

    return report_path


def main():
    """CLI entry point - generate weekly report.

    Works directly from analytics.json (populated by fetch_all).
    No generations.json required.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Generate analytics report")
    parser.add_argument("--week", help="Week identifier (YYYY-WW format)")
    args = parser.parse_args()

    print("📊 Generating performance report...")

    data = correlate_data()

    if not data:
        ap = analytics_json_path()
        print(f"⚠️ No data to report ({ap} is empty — run fetch_analytics first)")
        return

    content = generate_report(data, args.week)
    report_path = save_report(content, args.week)

    print(f"✅ Report saved to {report_path}")
    print("")
    print(content)


if __name__ == "__main__":
    main()

