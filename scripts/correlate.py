#!/usr/bin/env python3
"""
ML Correlation Script - Phase 2 Analytics Agent

Analyzes video performance data to find patterns and generate suggestions.
No neural nets - just simple statistics that work with small datasets.

NOTE: This is STATISTICS, not ML. No model learning weights, no predictions.
Real ML comes in Phase 4 when we have 100+ videos.

Output:
- data/suggestions.json (machine-readable)
- stdout (human-readable, captured by workflow for Step Summary)
"""
import json
import os
import sys
from collections import defaultdict
from datetime import datetime
import math

# Allow importing agent when run as script from repo root
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from agent.log_generation import video_id_index

# Paths
ANALYTICS_PATH = "data/analytics.json"
SUGGESTIONS_PATH = "data/suggestions.json"
GENERATIONS_PATH = "data/generations.json"

# Statistical thresholds (per AGENT.md spec)
MIN_SAMPLE_SIZE = 5  # Actionable requires n >= 5
MIN_GROUP_VIEWS = 200  # Actionable requires group_views >= 200
MIN_VIEWS_FOR_RETENTION = 20  # Exclude videos with < 20 views from retention analysis
MIN_DELTA_THRESHOLD = 2.0  # Minimum % points (retention) to suggest action
# Mean watch minutes per video (eligible: views>=MIN_VIEWS_FOR_RETENTION) vs channel mean
MIN_DELTA_WATCH_MINUTES = 1.0


def load_analytics():
    """Load analytics data."""
    if not os.path.exists(ANALYTICS_PATH):
        print("❌ No analytics data found")
        return None
    with open(ANALYTICS_PATH) as f:
        return json.load(f)


def parse_video_type_from_title(title):
    """Extract type/mood from video title only (fallback)."""
    t = title.lower()

    # Art-creator videos
    if title.startswith("Ambient "):
        parts = title.split("|")
        if len(parts) >= 3:
            art_period = parts[0].replace("Ambient ", "").strip()
            music_style = parts[2].replace("Evolving", "").replace("Soundscape", "").strip()
            return {"category": "art-creator", "art_period": art_period, "music_style": music_style}
        return {"category": "art-creator", "art_period": "unknown", "music_style": "unknown"}

    # Mood-based videos — 'study' before 'focus' so titles with both map to study
    mood_keywords = [
        ('lofi', 'lofi_study'), ('piano', 'piano_relax'), ('ocean', 'ocean_waves'),
        ('rain', 'rain_sleep'), ('fire', 'fireplace'), ('forest', 'forest_morning'),
        ('sleep', 'sleep'), ('chill', 'chill'),
        ('study', 'study'),
        ('focus', 'deep_focus'),
        ('energiz', 'energize'), ('trance', 'trance'),
        ('strength', 'warrior'), ('warrior', 'warrior'), ('ceremon', 'ceremony'),
    ]

    for kw, mood in mood_keywords:
        if kw in t:
            return {"category": "mood", "mood": mood}

    return {"category": "other", "mood": "unknown"}


def classify_from_ledger_row(row: dict, title: str) -> dict:
    """Prefer params + mood from data/generations.json join."""
    params = row.get("params") or {}
    ap = params.get("art_period")
    ms = params.get("music_style")
    if ap or ms:
        return {
            "category": "art-creator",
            "art_period": ap or "unknown",
            "music_style": ms or "unknown",
        }
    mood = row.get("mood")
    if mood:
        return {"category": "mood", "mood": mood}
    return parse_video_type_from_title(title)


def parse_video_type(title, video_id=None, gen_by_video_id=None):
    """Resolve category using generations.json when video_id matches, else title parse."""
    if video_id and gen_by_video_id and video_id in gen_by_video_id:
        return classify_from_ledger_row(gen_by_video_id[video_id], title)
    return parse_video_type_from_title(title)


def calculate_correlations(videos):
    """Calculate performance correlations by category."""
    # Group videos by different dimensions
    by_mood = defaultdict(list)
    by_art_period = defaultdict(list)
    by_music_style = defaultdict(list)
    by_category = defaultdict(list)

    gen_by_video_id = {}
    if os.path.exists(GENERATIONS_PATH):
        try:
            gen_by_video_id = video_id_index()
        except (json.JSONDecodeError, OSError):
            gen_by_video_id = {}

    for v in videos:
        metrics = v["metrics"]
        retention = metrics.get("average_view_percentage", 0)
        views = metrics.get("views", 0)
        watch_minutes = float(metrics.get("watch_time_minutes") or 0)

        video_type = parse_video_type(
            v["title"],
            video_id=v.get("video_id"),
            gen_by_video_id=gen_by_video_id,
        )
        category = video_type["category"]
        
        data = {
            "retention": retention,
            "watch_minutes": watch_minutes,
            "views": views,
            "title": v["title"],
        }
        by_category[category].append(data)
        
        if category == "mood":
            by_mood[video_type["mood"]].append(data)
        elif category == "art-creator":
            by_art_period[video_type["art_period"]].append(data)
            by_music_style[video_type["music_style"]].append(data)
    
    return by_mood, by_art_period, by_music_style, by_category


def calc_stats(videos, value_key="retention"):
    """Calculate average and std dev of a metric for videos with sufficient views.

    Per AGENT.md spec: exclude views < 20 from analysis.
    value_key: "retention" (avg % viewed) or "watch_minutes" (total minutes in window).
    Returns: (avg, std_dev, eligible_count, group_views)
    """
    # Filter to videos with >= MIN_VIEWS_FOR_RETENTION views (spec: exclude views < 20)
    eligible = [v for v in videos if v["views"] >= MIN_VIEWS_FOR_RETENTION]
    if not eligible:
        return 0, 0, 0, 0  # avg, std_dev, count, group_views

    values = [v[value_key] for v in eligible]
    group_views = sum(v["views"] for v in eligible)
    avg = sum(values) / len(values)

    # Calculate standard deviation
    if len(values) > 1:
        variance = sum((x - avg) ** 2 for x in values) / (len(values) - 1)
        std_dev = math.sqrt(variance)
    else:
        std_dev = 0

    return avg, std_dev, len(values), group_views


def generate_coverage_report(by_mood, by_art_period, by_music_style):
    """Generate coverage report showing ALL produced combinations (including 0 views)."""
    # Define full parameter space
    ALL_ART_PERIODS = ["cave_art", "ancient", "medieval", "renaissance", "baroque",
                       "impressionist", "modern", "contemporary", "future"]
    ALL_MUSIC_STYLES = ["gnawa", "taiko", "gamelan", "burundi", "kuku",
                        "candomble", "bamboula", "heartbeat", "none"]
    ALL_MOODS = ["deep_focus", "sleep", "chill", "study", "energize", "trance",
                 "ceremony", "warrior", "rain_sleep", "fireplace", "ocean_waves",
                 "lofi_study", "piano_relax", "forest_morning"]

    coverage = {
        "moods": {},
        "art_periods": {},
        "music_styles": {},
        "art_music_combos": {}
    }

    # Track moods (total count, not just with views)
    for mood in ALL_MOODS:
        total = len(by_mood.get(mood, []))
        with_views = len([v for v in by_mood.get(mood, []) if v["views"] > 0])
        coverage["moods"][mood] = {"total": total, "with_views": with_views}

    # Track art periods
    for period in ALL_ART_PERIODS:
        total = len(by_art_period.get(period, []))
        with_views = len([v for v in by_art_period.get(period, []) if v["views"] > 0])
        coverage["art_periods"][period] = {"total": total, "with_views": with_views}

    # Track music styles
    for style in ALL_MUSIC_STYLES:
        total = len(by_music_style.get(style, []))
        with_views = len([v for v in by_music_style.get(style, []) if v["views"] > 0])
        coverage["music_styles"][style] = {"total": total, "with_views": with_views}

    # Track art×music combinations (81 combinations = 9×9)
    for period in ALL_ART_PERIODS:
        for style in ALL_MUSIC_STYLES:
            combo_key = f"{period}+{style}"
            # Find videos matching this combo
            period_videos = by_art_period.get(period, [])
            # Cross-reference with music style by title
            combo_videos = []
            for v in period_videos:
                # Check if this video also has this music style
                for mv in by_music_style.get(style, []):
                    if v["title"] == mv["title"]:
                        combo_videos.append(v)
                        break
            total = len(combo_videos)
            with_views = len([v for v in combo_videos if v["views"] > 0])
            coverage["art_music_combos"][combo_key] = {"total": total, "with_views": with_views}

    return coverage


def generate_suggestions(
    by_mood,
    by_art_period,
    by_music_style,
    by_category,
    overall_avg,
    *,
    metric_kind="retention",
):
    """Generate actionable suggestions based on correlations.

    metric_kind:
      - "retention": average_view_percentage among videos with views>=20 (quality per play)
      - "watch_minutes": watch_time_minutes per video, same eligibility (growth / minutes)

    Actionability gates (per AGENT.md spec):
    - Actionable: n >= 5 AND group_views >= 200
    - Exploratory: n >= 3 (but fails actionable)
    - Ignore: n < 3 (too noisy)
    """
    if metric_kind == "retention":
        value_key = "retention"
        metric_id = "average_view_percentage"
        min_delta = MIN_DELTA_THRESHOLD
    else:
        value_key = "watch_minutes"
        metric_id = "watch_time_minutes"
        min_delta = MIN_DELTA_WATCH_MINUTES

    def _fmt_delta(delta: float) -> str:
        if metric_kind == "retention":
            return f"{delta:+.1f}%"
        return f"{delta:+.1f} min"

    suggestions = []

    # Analyze moods - include ALL videos, show total count alongside eligible count
    all_stats = []
    for mood, videos in by_mood.items():
        avg, std_dev, eligible_count, group_views = calc_stats(videos, value_key=value_key)
        total_count = len(videos)  # Total including 0 views
        delta = avg - overall_avg if eligible_count > 0 else 0
        all_stats.append({
            "type": "mood",
            "name": mood,
            "avg": avg,
            "delta": delta,
            "count": eligible_count,
            "total": total_count,
            "group_views": group_views,
            "std_dev": std_dev,
            "metric": metric_id,
        })

    # Analyze art periods - include ALL videos
    for period, videos in by_art_period.items():
        avg, std_dev, eligible_count, group_views = calc_stats(videos, value_key=value_key)
        total_count = len(videos)
        delta = avg - overall_avg if eligible_count > 0 else 0
        all_stats.append({
            "type": "art_period",
            "name": period,
            "avg": avg,
            "delta": delta,
            "count": eligible_count,
            "total": total_count,
            "group_views": group_views,
            "std_dev": std_dev,
            "metric": metric_id,
        })

    # Analyze music styles - include ALL videos
    for style, videos in by_music_style.items():
        avg, std_dev, eligible_count, group_views = calc_stats(videos, value_key=value_key)
        total_count = len(videos)
        delta = avg - overall_avg if eligible_count > 0 else 0
        all_stats.append({
            "type": "music_style",
            "name": style,
            "avg": avg,
            "delta": delta,
            "count": eligible_count,
            "total": total_count,
            "group_views": group_views,
            "std_dev": std_dev,
            "metric": metric_id,
        })

    # Sort by delta (best performers first)
    all_stats.sort(key=lambda x: x["delta"], reverse=True)

    # Generate suggestions with proper actionability gates
    for stat in all_stats[:5]:  # Top 5
        if stat["delta"] > min_delta:
            # Apply actionability gates per AGENT.md spec
            is_actionable = stat["count"] >= MIN_SAMPLE_SIZE and stat["group_views"] >= MIN_GROUP_VIEWS
            is_exploratory = stat["count"] >= 3 and not is_actionable

            if stat["count"] < 3:
                continue  # Ignore: too noisy, don't report

            if is_actionable:
                confidence = "high" if stat["count"] >= 10 else "medium"
                note = f"(n={stat['count']}, views={stat['group_views']})"
            else:  # exploratory
                confidence = "low"
                note = f"(n={stat['count']}, views={stat['group_views']}, exploratory)"

            suggestions.append({
                "action": "increase",
                "type": stat["type"],
                "name": stat["name"],
                "reason": f"{_fmt_delta(stat['delta'])} vs channel avg {note}",
                "confidence": confidence,
                "actionable": is_actionable,
                "sample_size": stat["count"],
                "group_views": stat["group_views"],
                "metric": metric_id,
            })

    for stat in all_stats[-3:]:  # Bottom 3
        if stat["delta"] < -min_delta:
            # Apply actionability gates per AGENT.md spec
            is_actionable = stat["count"] >= MIN_SAMPLE_SIZE and stat["group_views"] >= MIN_GROUP_VIEWS
            is_exploratory = stat["count"] >= 3 and not is_actionable

            if stat["count"] < 3:
                continue  # Ignore: too noisy, don't report

            if is_actionable:
                confidence = "high" if stat["count"] >= 10 else "medium"
                note = f"(n={stat['count']}, views={stat['group_views']})"
            else:  # exploratory
                confidence = "low"
                note = f"(n={stat['count']}, views={stat['group_views']}, exploratory)"

            suggestions.append({
                "action": "reduce",
                "type": stat["type"],
                "name": stat["name"],
                "reason": f"{_fmt_delta(stat['delta'])} vs channel avg {note}",
                "confidence": confidence,
                "actionable": is_actionable,
                "sample_size": stat["count"],
                "group_views": stat["group_views"],
                "metric": metric_id,
            })

    return suggestions, all_stats


def get_metric(video, key, default=0):
    """Safely get a metric value, handling empty metrics dicts."""
    return video.get("metrics", {}).get(key, default)


def main():
    data = load_analytics()
    if not data:
        return

    videos = data["videos"]
    with_views = [v for v in videos if get_metric(v, "views") > 0]

    # Get correlations (includes ALL videos, even 0 views)
    by_mood, by_art_period, by_music_style, by_category = calculate_correlations(videos)

    # Generate coverage report (what's produced vs what's remaining)
    coverage = generate_coverage_report(by_mood, by_art_period, by_music_style)

    # Channel averages (videos with any views in window — same pool for both metrics)
    if len(with_views) >= 1:
        overall_avg = sum(get_metric(v, "average_view_percentage") for v in with_views) / len(
            with_views
        )
        overall_avg_watch = sum(
            float(get_metric(v, "watch_time_minutes") or 0) for v in with_views
        ) / len(with_views)
    else:
        overall_avg = 0.0
        overall_avg_watch = 0.0

    # Retention (% viewed) — quality per play; watch minutes — growth / total attention in window
    suggestions_r, all_stats = generate_suggestions(
        by_mood,
        by_art_period,
        by_music_style,
        by_category,
        overall_avg,
        metric_kind="retention",
    )
    suggestions_w, all_stats_watch = generate_suggestions(
        by_mood,
        by_art_period,
        by_music_style,
        by_category,
        overall_avg_watch,
        metric_kind="watch_minutes",
    )
    suggestions = suggestions_r + suggestions_w

    # Save to JSON (includes coverage data)
    output = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "overall_avg_retention": round(overall_avg, 2),
        "overall_avg_watch_minutes_per_video": round(overall_avg_watch, 3),
        "videos_analyzed": len(videos),
        "videos_with_views": len(with_views),
        "coverage": coverage,
        "suggestions": suggestions,
        "all_stats": all_stats,
        "all_stats_watch_time": all_stats_watch,
    }

    os.makedirs(os.path.dirname(SUGGESTIONS_PATH), exist_ok=True)
    with open(SUGGESTIONS_PATH, "w") as f:
        json.dump(output, f, indent=2)

    # Print human-readable output (for Step Summary)
    print("=" * 60)
    print("🤖 ML CORRELATION ANALYSIS")
    print("=" * 60)
    print(f"\n📊 Data: {len(videos)} videos, {len(with_views)} with views")
    print(f"📈 Overall avg retention: {overall_avg:.1f}% (avg % of video watched)")
    print(
        f"⏱️  Overall avg watch minutes (per video, in date window): {overall_avg_watch:.2f}"
    )

    # === COVERAGE REPORT ===
    print("\n" + "=" * 60)
    print("📦 EXPERIMENT COVERAGE (produced vs remaining)")
    print("=" * 60)

    # Moods coverage
    moods_data = coverage["moods"]
    moods_produced = [m for m, d in moods_data.items() if d["total"] > 0]
    moods_missing = [m for m, d in moods_data.items() if d["total"] == 0]
    print(f"\n🎭 MOODS: {len(moods_produced)}/14 produced")
    if moods_missing:
        print(f"   Missing: {', '.join(moods_missing)}")
    for mood, d in sorted(moods_data.items(), key=lambda x: x[1]["total"], reverse=True):
        if d["total"] > 0:
            print(f"   ✅ {mood}: {d['total']} total, {d['with_views']} with views")

    # Art periods coverage
    art_data = coverage["art_periods"]
    art_produced = [p for p, d in art_data.items() if d["total"] > 0]
    art_missing = [p for p, d in art_data.items() if d["total"] == 0]
    print(f"\n🎨 ART PERIODS: {len(art_produced)}/9 produced")
    if art_missing:
        print(f"   Missing: {', '.join(art_missing)}")
    for period, d in sorted(art_data.items(), key=lambda x: x[1]["total"], reverse=True):
        if d["total"] > 0:
            print(f"   ✅ {period}: {d['total']} total, {d['with_views']} with views")

    # Music styles coverage
    music_data = coverage["music_styles"]
    music_produced = [s for s, d in music_data.items() if d["total"] > 0]
    music_missing = [s for s, d in music_data.items() if d["total"] == 0]
    print(f"\n🎵 MUSIC STYLES: {len(music_produced)}/9 produced")
    if music_missing:
        print(f"   Missing: {', '.join(music_missing)}")
    for style, d in sorted(music_data.items(), key=lambda x: x[1]["total"], reverse=True):
        if d["total"] > 0:
            print(f"   ✅ {style}: {d['total']} total, {d['with_views']} with views")

    # Art×Music combos coverage
    combo_data = coverage["art_music_combos"]
    combos_produced = [c for c, d in combo_data.items() if d["total"] > 0]
    combos_missing = [c for c, d in combo_data.items() if d["total"] == 0]
    print(f"\n🔀 ART×MUSIC COMBOS: {len(combos_produced)}/81 produced ({len(combos_missing)} remaining)")
    if combos_missing and len(combos_missing) <= 20:
        print(f"   Missing: {', '.join(combos_missing[:20])}")
    elif combos_missing:
        print(f"   Missing (first 20): {', '.join(combos_missing[:20])}...")

    # === SUGGESTIONS ===
    print("\n" + "=" * 60)
    print("💡 SUGGESTIONS (by metric)")
    print("=" * 60)
    print(f"   (Actionable: n>={MIN_SAMPLE_SIZE} AND views>={MIN_GROUP_VIEWS})")
    print(
        f"   (Eligible videos: >={MIN_VIEWS_FOR_RETENTION} views; retention in %, watch in min)"
    )

    def _print_bucket(title, subset):
        actionable_b = [s for s in subset if s.get("actionable", False)]
        exploratory_b = [s for s in subset if not s.get("actionable", False)]
        print(f"\n--- {title} ---")
        if not subset:
            print("   ⚠️ No strong patterns for this metric")
            return
        if actionable_b:
            print("   🎯 ACTIONABLE:")
            for s in actionable_b:
                icon = "⬆️" if s["action"] == "increase" else "⬇️"
                print(f"   {icon} {s['action'].upper()}: {s['name']} ({s['type']})")
                print(f"      {s['reason']}")
        if exploratory_b:
            print("   🔍 EXPLORATORY:")
            for s in exploratory_b:
                icon = "⬆️" if s["action"] == "increase" else "⬇️"
                print(f"   {icon} {s['action'].upper()}: {s['name']} ({s['type']})")
                print(f"      {s['reason']}")

    _print_bucket("Average % viewed (retention)", suggestions_r)
    _print_bucket("Watch minutes in window (growth signal)", suggestions_w)

    # === PERFORMANCE STATS ===
    print("\n" + "=" * 60)
    print("📋 TOP GROUPS — retention % (videos with 20+ views only)")
    print("=" * 60)
    print(f"\n{'Type':<12} {'Name':<18} {'Avg%':>6} {'Delta':>7} {'n':>4} {'GrpViews':>8} {'Total':>5}")
    print("-" * 70)
    for s in all_stats[:15]:  # Top 15
        total = s.get("total", s["count"])
        grp_views = s.get("group_views", 0)
        print(
            f"{s['type']:<12} {s['name']:<18} {s['avg']:>5.1f}% {s['delta']:>+6.1f}% "
            f"{s['count']:>4} {grp_views:>8} {total:>5}"
        )

    print("\n" + "=" * 60)
    print("📋 TOP GROUPS — watch minutes per video (same eligibility)")
    print("=" * 60)
    print(f"\n{'Type':<12} {'Name':<18} {'AvgMin':>7} {'Delta':>8} {'n':>4} {'GrpViews':>8} {'Total':>5}")
    print("-" * 70)
    for s in all_stats_watch[:15]:
        total = s.get("total", s["count"])
        grp_views = s.get("group_views", 0)
        print(
            f"{s['type']:<12} {s['name']:<18} {s['avg']:>7.2f} {s['delta']:>+7.2f}m "
            f"{s['count']:>4} {grp_views:>8} {total:>5}"
        )

    # Add warning about sample sizes
    low_sample = [s for s in all_stats if s["count"] < MIN_SAMPLE_SIZE]
    if low_sample:
        print(
            f"\n⚠️  {len(low_sample)} groups have n<{MIN_SAMPLE_SIZE} eligible videos (need more data)"
        )

    print(f"\n✅ Suggestions saved to {SUGGESTIONS_PATH}")


if __name__ == "__main__":
    main()

