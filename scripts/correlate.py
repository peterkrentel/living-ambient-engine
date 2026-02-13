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


def generate_suggestions(by_mood, by_art_period, by_music_style, by_category, overall_avg):
    """Generate actionable suggestions based on correlations."""
    suggestions = []

    # Analyze moods
    all_stats = []
    for mood, videos in by_mood.items():
        avg, std_dev, count = calc_stats(videos)
        if count > 0:
            delta = avg - overall_avg
            all_stats.append({
                "type": "mood", "name": mood, "avg": avg,
                "delta": delta, "count": count, "std_dev": std_dev
            })

    # Analyze art periods
    for period, videos in by_art_period.items():
        avg, std_dev, count = calc_stats(videos)
        if count > 0:
            delta = avg - overall_avg
            all_stats.append({
                "type": "art_period", "name": period, "avg": avg,
                "delta": delta, "count": count, "std_dev": std_dev
            })

    # Analyze music styles
    for style, videos in by_music_style.items():
        avg, std_dev, count = calc_stats(videos)
        if count > 0:
            delta = avg - overall_avg
            all_stats.append({
                "type": "music_style", "name": style, "avg": avg,
                "delta": delta, "count": count, "std_dev": std_dev
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


def main():
    data = load_analytics()
    if not data:
        return
    
    videos = data["videos"]
    with_views = [v for v in videos if v["metrics"]["views"] > 0]
    
    if len(with_views) < 5:
        print("⚠️ Not enough data yet (need 5+ videos with views)")
        print(f"   Currently have: {len(with_views)} videos with views")
        return
    
    # Calculate overall average
    overall_avg = sum(v["metrics"]["average_view_percentage"] for v in with_views) / len(with_views)
    
    # Get correlations
    by_mood, by_art_period, by_music_style, by_category = calculate_correlations(videos)
    
    # Generate suggestions
    suggestions, all_stats = generate_suggestions(
        by_mood, by_art_period, by_music_style, by_category, overall_avg
    )
    
    # Save to JSON
    output = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "overall_avg_retention": round(overall_avg, 2),
        "videos_analyzed": len(videos),
        "videos_with_views": len(with_views),
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
    
    print("\n" + "=" * 60)
    print("📋 ALL STATS (by retention %)")
    print("=" * 60)
    print(f"\n{'Type':<12} {'Name':<20} {'Avg%':>6} {'Delta':>7} {'StdDev':>7} {'n':>4}")
    print("-" * 62)
    for s in all_stats[:15]:  # Top 15
        std = s.get('std_dev', 0)
        print(f"{s['type']:<12} {s['name']:<20} {s['avg']:>5.1f}% {s['delta']:>+6.1f}% {std:>6.1f}% {s['count']:>4}")

    # Add warning about sample sizes
    low_sample = [s for s in all_stats if s['count'] < MIN_SAMPLE_SIZE]
    if low_sample:
        print(f"\n⚠️  {len(low_sample)} groups have n<{MIN_SAMPLE_SIZE} (low confidence)")

    print(f"\n✅ Suggestions saved to {SUGGESTIONS_PATH}")


if __name__ == "__main__":
    main()

