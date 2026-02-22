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
from collections import defaultdict
from datetime import datetime
import math

# Paths
ANALYTICS_PATH = "data/analytics.json"
SUGGESTIONS_PATH = "data/suggestions.json"

# Statistical thresholds
MIN_SAMPLE_SIZE = 3  # Ignore groups with fewer videos (reduces noise)
MIN_DELTA_THRESHOLD = 2.0  # Minimum % difference to suggest action


def load_analytics():
    """Load analytics data."""
    if not os.path.exists(ANALYTICS_PATH):
        print("❌ No analytics data found")
        return None
    with open(ANALYTICS_PATH) as f:
        return json.load(f)


def parse_video_type(title):
    """Extract type/mood from video title."""
    t = title.lower()
    
    # Art-creator videos
    if title.startswith("Ambient "):
        # Extract art_period and music_style
        parts = title.split("|")
        if len(parts) >= 3:
            art_period = parts[0].replace("Ambient ", "").strip()
            music_style = parts[2].replace("Evolving", "").replace("Soundscape", "").strip()
            return {"category": "art-creator", "art_period": art_period, "music_style": music_style}
        return {"category": "art-creator", "art_period": "unknown", "music_style": "unknown"}
    
    # Mood-based videos
    mood_keywords = [
        ('lofi', 'lofi_study'), ('piano', 'piano_relax'), ('ocean', 'ocean_waves'),
        ('rain', 'rain_sleep'), ('fire', 'fireplace'), ('forest', 'forest_morning'),
        ('focus', 'deep_focus'), ('sleep', 'sleep'), ('chill', 'chill'),
        ('study', 'study'), ('energiz', 'energize'), ('trance', 'trance'),
        ('strength', 'warrior'), ('warrior', 'warrior'), ('ceremon', 'ceremony')
    ]
    
    for kw, mood in mood_keywords:
        if kw in t:
            return {"category": "mood", "mood": mood}
    
    return {"category": "other", "mood": "unknown"}


def calculate_correlations(videos):
    """Calculate performance correlations by category."""
    # Group videos by different dimensions
    by_mood = defaultdict(list)
    by_art_period = defaultdict(list)
    by_music_style = defaultdict(list)
    by_category = defaultdict(list)
    
    for v in videos:
        metrics = v["metrics"]
        retention = metrics.get("average_view_percentage", 0)
        views = metrics.get("views", 0)
        
        video_type = parse_video_type(v["title"])
        category = video_type["category"]
        
        data = {"retention": retention, "views": views, "title": v["title"]}
        by_category[category].append(data)
        
        if category == "mood":
            by_mood[video_type["mood"]].append(data)
        elif category == "art-creator":
            by_art_period[video_type["art_period"]].append(data)
            by_music_style[video_type["music_style"]].append(data)
    
    return by_mood, by_art_period, by_music_style, by_category


def calc_stats(videos, metric="retention"):
    """Calculate average and std dev of a metric for videos with views."""
    with_views = [v for v in videos if v["views"] > 0]
    if not with_views:
        return 0, 0, 0  # avg, std_dev, count

    values = [v[metric] for v in with_views]
    avg = sum(values) / len(values)

    # Calculate standard deviation
    if len(values) > 1:
        variance = sum((x - avg) ** 2 for x in values) / (len(values) - 1)
        std_dev = math.sqrt(variance)
    else:
        std_dev = 0

    return avg, std_dev, len(values)


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

    # Track art×music combinations (the 81 factorial combos)
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


def generate_suggestions(by_mood, by_art_period, by_music_style, by_category, overall_avg):
    """Generate actionable suggestions based on correlations."""
    suggestions = []

    # Analyze moods - include ALL videos, show total count alongside with_views count
    all_stats = []
    for mood, videos in by_mood.items():
        avg, std_dev, count_with_views = calc_stats(videos)
        total_count = len(videos)  # Total including 0 views
        delta = avg - overall_avg if count_with_views > 0 else 0
        all_stats.append({
            "type": "mood", "name": mood, "avg": avg,
            "delta": delta, "count": count_with_views, "total": total_count, "std_dev": std_dev
        })

    # Analyze art periods - include ALL videos
    for period, videos in by_art_period.items():
        avg, std_dev, count_with_views = calc_stats(videos)
        total_count = len(videos)
        delta = avg - overall_avg if count_with_views > 0 else 0
        all_stats.append({
            "type": "art_period", "name": period, "avg": avg,
            "delta": delta, "count": count_with_views, "total": total_count, "std_dev": std_dev
        })

    # Analyze music styles - include ALL videos
    for style, videos in by_music_style.items():
        avg, std_dev, count_with_views = calc_stats(videos)
        total_count = len(videos)
        delta = avg - overall_avg if count_with_views > 0 else 0
        all_stats.append({
            "type": "music_style", "name": style, "avg": avg,
            "delta": delta, "count": count_with_views, "total": total_count, "std_dev": std_dev
        })

    # Sort by delta (best performers first)
    all_stats.sort(key=lambda x: x["delta"], reverse=True)

    # Generate suggestions (only for groups meeting minimum sample size)
    for stat in all_stats[:5]:  # Top 5
        if stat["delta"] > MIN_DELTA_THRESHOLD:
            # Determine confidence based on sample size
            if stat["count"] < MIN_SAMPLE_SIZE:
                confidence = "low"
                note = f"(n={stat['count']}, need {MIN_SAMPLE_SIZE}+)"
            elif stat["count"] < 10:
                confidence = "medium"
                note = f"(n={stat['count']})"
            else:
                confidence = "high"
                note = f"(n={stat['count']})"

            suggestions.append({
                "action": "increase",
                "type": stat["type"],
                "name": stat["name"],
                "reason": f"+{stat['delta']:.1f}% vs avg {note}",
                "confidence": confidence,
                "sample_size": stat["count"]
            })
    
    for stat in all_stats[-3:]:  # Bottom 3
        if stat["delta"] < -MIN_DELTA_THRESHOLD:
            # Determine confidence based on sample size
            if stat["count"] < MIN_SAMPLE_SIZE:
                confidence = "low"
                note = f"(n={stat['count']}, need {MIN_SAMPLE_SIZE}+)"
            elif stat["count"] < 10:
                confidence = "medium"
                note = f"(n={stat['count']})"
            else:
                confidence = "high"
                note = f"(n={stat['count']})"

            suggestions.append({
                "action": "reduce",
                "type": stat["type"],
                "name": stat["name"],
                "reason": f"{stat['delta']:.1f}% vs avg {note}",
                "confidence": confidence,
                "sample_size": stat["count"]
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

    # Calculate overall average (only from videos with views)
    if len(with_views) >= 1:
        overall_avg = sum(get_metric(v, "average_view_percentage") for v in with_views) / len(with_views)
    else:
        overall_avg = 0

    # Generate suggestions (performance analysis)
    suggestions, all_stats = generate_suggestions(
        by_mood, by_art_period, by_music_style, by_category, overall_avg
    )

    # Save to JSON (includes coverage data)
    output = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "overall_avg_retention": round(overall_avg, 2),
        "videos_analyzed": len(videos),
        "videos_with_views": len(with_views),
        "coverage": coverage,
        "suggestions": suggestions,
        "all_stats": all_stats
    }

    os.makedirs(os.path.dirname(SUGGESTIONS_PATH), exist_ok=True)
    with open(SUGGESTIONS_PATH, "w") as f:
        json.dump(output, f, indent=2)

    # Print human-readable output (for Step Summary)
    print("=" * 60)
    print("🤖 ML CORRELATION ANALYSIS")
    print("=" * 60)
    print(f"\n📊 Data: {len(videos)} videos, {len(with_views)} with views")
    print(f"📈 Overall avg retention: {overall_avg:.1f}%")

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
    print("💡 SUGGESTIONS")
    print("=" * 60)

    if not suggestions:
        print("\n⚠️ No strong patterns yet - need more data")
    else:
        for s in suggestions:
            icon = "⬆️" if s["action"] == "increase" else "⬇️"
            conf = f"[{s['confidence']}]"
            print(f"\n{icon} {s['action'].upper()}: {s['name']} ({s['type']})")
            print(f"   Reason: {s['reason']} {conf}")

    # === PERFORMANCE STATS ===
    print("\n" + "=" * 60)
    print("📋 ALL STATS (by retention %) - includes total produced")
    print("=" * 60)
    print(f"\n{'Type':<12} {'Name':<20} {'Avg%':>6} {'Delta':>7} {'Views':>5} {'Total':>5}")
    print("-" * 62)
    for s in all_stats[:15]:  # Top 15
        total = s.get('total', s['count'])
        print(f"{s['type']:<12} {s['name']:<20} {s['avg']:>5.1f}% {s['delta']:>+6.1f}% {s['count']:>5} {total:>5}")

    # Add warning about sample sizes
    low_sample = [s for s in all_stats if s['count'] < MIN_SAMPLE_SIZE]
    if low_sample:
        print(f"\n⚠️  {len(low_sample)} groups have n<{MIN_SAMPLE_SIZE} with views (low confidence)")

    print(f"\n✅ Suggestions saved to {SUGGESTIONS_PATH}")


if __name__ == "__main__":
    main()

