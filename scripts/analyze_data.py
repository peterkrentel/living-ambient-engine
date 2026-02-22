#!/usr/bin/env python3
"""Quick analysis of analytics data."""
import json
from collections import defaultdict

# Load data
with open('data/analytics.json') as f:
    data = json.load(f)

videos = data['videos']


def get_metric(video, key, default=0):
    """Safely get a metric value, handling empty metrics dicts."""
    return video.get('metrics', {}).get(key, default)


print("=" * 60)
print("📊 ANALYTICS DATA SUMMARY")
print("=" * 60)

total = len(videos)
with_views = [v for v in videos if get_metric(v, 'views') > 0]

print(f"\n📹 Total videos: {total}")
print(f"   With views: {len(with_views)}")
print(f"   Zero views: {total - len(with_views)}")

total_views = sum(get_metric(v, 'views') for v in videos)
total_watch = sum(get_metric(v, 'watch_time_minutes') for v in videos)
print(f"\n👁️  Total views: {total_views}")
print(f"⏱️  Total watch time: {total_watch} minutes")

# Parse type from title
def parse_type(title):
    t = title.lower()
    if title.startswith("Ambient "):
        return "art-creator"
    for kw, mood in [('lofi','lofi_study'),('piano','piano_relax'),('ocean','ocean_waves'),
                      ('rain','rain_sleep'),('fire','fireplace'),('forest','forest_morning'),
                      ('focus','deep_focus'),('sleep','sleep'),('chill','chill'),
                      ('study','study'),('energiz','energize'),('trance','trance'),
                      ('strength','warrior'),('warrior','warrior'),('ceremon','ceremony')]:
        if kw in t:
            return mood
    return "other"

# Group by type
by_type = defaultdict(list)
for v in videos:
    by_type[parse_type(v['title'])].append(v)

print("\n" + "=" * 60)
print("📈 PERFORMANCE BY TYPE")
print("=" * 60)

stats = []
for vtype, vids in by_type.items():
    views = sum(get_metric(v, 'views') for v in vids)
    with_data = [v for v in vids if get_metric(v, 'views') > 0]
    if with_data:
        avg_ret = sum(get_metric(v, 'average_view_percentage') for v in with_data) / len(with_data)
        avg_dur = sum(get_metric(v, 'average_view_duration_seconds') for v in with_data) / len(with_data)
    else:
        avg_ret, avg_dur = 0, 0
    stats.append({'type': vtype, 'count': len(vids), 'views': views, 'ret': avg_ret, 'dur': avg_dur})

stats.sort(key=lambda x: x['ret'], reverse=True)

print(f"\n{'Type':<20} {'#Vids':>5} {'Views':>5} {'Ret%':>6} {'AvgSec':>6}")
print("-" * 50)
for s in stats:
    print(f"{s['type']:<20} {s['count']:>5} {s['views']:>5} {s['ret']:>5.1f}% {s['dur']:>5.0f}s")

# Top 5
print("\n" + "=" * 60)
print("🏆 TOP 5 VIDEOS (by retention %)")
print("=" * 60)

ranked = sorted(with_views, key=lambda v: get_metric(v, 'average_view_percentage'), reverse=True)[:5]
print(f"\n{'Title':<40} {'Ret%':>6} {'Views':>5}")
print("-" * 55)
for v in ranked:
    title = v['title'][:37] + "..." if len(v['title']) > 40 else v['title']
    title = title.replace("&#39;", "'").replace("&amp;", "&")
    ret = get_metric(v, 'average_view_percentage')
    views = get_metric(v, 'views')
    print(f"{title:<40} {ret:>5.1f}% {views:>5}")

print("\n" + "=" * 60)
print("💡 SUMMARY")
print("=" * 60)
print(f"""
• {total} videos tracked
• {len(with_views)} have at least 1 view
• {total_views} total views, {total_watch} mins watched
• Best retention so far: lofi_study (~32%)
• Need more data (and promotion) for real insights
""")

