#!/usr/bin/env python3
"""Generate performance reports.

Creates weekly performance reports correlating generation parameters
with YouTube Analytics data.

Spec: docs/spec/AGENT.md
Contract: docs/spec/contracts/agent-youtube.md
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


DATA_DIR = Path("data")
REPORTS_DIR = DATA_DIR / "reports"
GENERATIONS_FILE = DATA_DIR / "generations.json"
ANALYTICS_FILE = DATA_DIR / "analytics.json"


def load_generations() -> Dict[str, Any]:
    """Load generations data."""
    if GENERATIONS_FILE.exists():
        with open(GENERATIONS_FILE, "r") as f:
            return json.load(f)
    return {"videos": []}


def load_analytics() -> Dict[str, Any]:
    """Load analytics data."""
    if ANALYTICS_FILE.exists():
        with open(ANALYTICS_FILE, "r") as f:
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
    
    lines = [
        f"# Analytics Report - {week}",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Summary",
        "",
        f"- **Total videos tracked:** {len(data)}",
        f"- **Videos with analytics:** {sum(1 for d in data if d.get('metrics'))}",
        "",
    ]
    
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
            title = (v.get("title") or v.get("metadata", {}).get("title") or v["video_id"])[:40]
            mood = v.get("mood", "N/A")
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
            title = (v.get("title") or v.get("metadata", {}).get("title") or v["video_id"])[:40]
            mood = v.get("mood", "N/A")
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
            lines.append(f"| {mood} | {stats['count']} | {stats['views']:,} | {avg_ret:.1f}% |")
        lines.append("")

    lines.extend([
        "## Next Steps",
        "",
        "1. Review top performers - what parameters correlate with success?",
        "2. Review low performers - what should be adjusted?",
        "3. Update moods.yaml based on learnings",
        "",
        "---",
        "",
        "*Report generated by Analytics Agent - docs/spec/AGENT.md*",
    ])

    return "\n".join(lines)


def save_report(content: str, week: Optional[str] = None) -> Path:
    """Save report to file."""
    if week is None:
        now = datetime.now(timezone.utc)
        week = f"{now.year}-W{now.isocalendar()[1]:02d}"

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / f"{week}.md"

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
        print("⚠️ No data to report (analytics.json is empty - run fetch_analytics first)")
        return

    content = generate_report(data, args.week)
    report_path = save_report(content, args.week)

    print(f"✅ Report saved to {report_path}")
    print("")
    print(content)


if __name__ == "__main__":
    main()

