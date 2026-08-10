#!/usr/bin/env python3
"""YouTube Trending Topics Fetcher and Correlator.

Fetches currently trending YouTube videos in ambient/relaxation-adjacent
categories and correlates them with the channel's existing analytics to
surface actionable insights.

Usage (CLI)::

    python -m youtube.trend_advisor
    python -m youtube.trend_advisor --region US --category 10 --out data/youtube_trends.json
    python -m youtube.trend_advisor --correlate data/analytics.json

Environment variables:

- ``YOUTUBE_API_KEY``: YouTube Data API v3 key (required for trends fetch;
  server-side key, not OAuth token).  If absent the CLI will still produce
  a correlation report from ``--correlate`` file if provided.
- ``YOUTUBE_TOKEN_PICKLE`` / ``YOUTUBE_TOKEN_PICKLE_BRAND``: used for the
  uploader; NOT used here (trend fetching needs a server API key).

Spec: docs/spec/AGENT.md
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from googleapiclient.discovery import build  # type: ignore
    from googleapiclient.errors import HttpError  # type: ignore

    HAS_GOOGLE_API = True
except ImportError:
    HAS_GOOGLE_API = False

    class HttpError(Exception):  # type: ignore[no-redef]
        pass


DATA_DIR = Path("data")
DEFAULT_OUT = str(DATA_DIR / "youtube_trends.json")
DEFAULT_ANALYTICS = str(DATA_DIR / "analytics.json")

# YouTube category IDs most relevant to ambient / lo-fi / focus content
# 10 = Music, 22 = People & Blogs, 26 = Howto & Style, 27 = Education
AMBIENT_CATEGORIES = [10, 22, 27]

# Keywords that indicate overlap with ambient/focus/sleep content
AMBIENT_KEYWORDS = {
    "ambient", "lofi", "lo-fi", "chill", "relax", "focus", "study",
    "sleep", "meditation", "calm", "nature", "rain", "fireplace",
    "deep work", "concentration", "binaural", "white noise", "spa",
    "piano", "jazz", "cafe", "cozy",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _api_key() -> Optional[str]:
    return os.environ.get("YOUTUBE_API_KEY")


def _keyword_overlap(title: str, description: str) -> float:
    """Return fraction of ambient keywords found in title+description (0-1)."""
    text = (title + " " + description).lower()
    found = sum(1 for kw in AMBIENT_KEYWORDS if kw in text)
    return found / len(AMBIENT_KEYWORDS)


def _load_analytics(analytics_path: str) -> Dict[str, Any]:
    p = Path(analytics_path)
    if p.exists():
        with open(p) as f:
            return json.load(f)
    return {"videos": []}


# ---------------------------------------------------------------------------
# Trend Fetcher
# ---------------------------------------------------------------------------


class TrendAdvisor:
    """Fetch YouTube trending videos and correlate with channel analytics."""

    def __init__(self, api_key: Optional[str] = None):
        if not HAS_GOOGLE_API:
            raise ImportError(
                "google-api-python-client not installed. "
                "Install with: pip install google-api-python-client"
            )
        self.api_key = api_key or _api_key()
        if not self.api_key:
            raise ValueError(
                "YouTube API key required for trend fetching. "
                "Set YOUTUBE_API_KEY environment variable or pass api_key."
            )
        self.youtube = build("youtube", "v3", developerKey=self.api_key)

    def fetch_trending(
        self,
        region_code: str = "US",
        category_ids: Optional[List[int]] = None,
        max_results: int = 50,
    ) -> List[Dict[str, Any]]:
        """Fetch trending videos from YouTube.

        Args:
            region_code: ISO 3166-1 alpha-2 country code (e.g. "US", "GB").
            category_ids: List of YouTube category IDs to query. Defaults to
                :data:`AMBIENT_CATEGORIES`.
            max_results: Max results per category (API max 50).

        Returns:
            Deduplicated list of trending video dicts.
        """
        if category_ids is None:
            category_ids = AMBIENT_CATEGORIES

        seen: set[str] = set()
        results: List[Dict[str, Any]] = []

        for cat_id in category_ids:
            try:
                response = self.youtube.videos().list(
                    part="snippet,statistics",
                    chart="mostPopular",
                    regionCode=region_code,
                    videoCategoryId=str(cat_id),
                    maxResults=max_results,
                ).execute()
            except HttpError as e:
                print(f"⚠️  Could not fetch category {cat_id}: {e}")
                continue

            for item in response.get("items", []):
                vid = item.get("id")
                if not vid or vid in seen:
                    continue
                seen.add(vid)

                snippet = item.get("snippet", {})
                stats = item.get("statistics", {})
                title = snippet.get("title", "")
                description = snippet.get("description", "")

                results.append({
                    "video_id": vid,
                    "title": title,
                    "description": description[:300],
                    "channel_title": snippet.get("channelTitle", ""),
                    "category_id": cat_id,
                    "published_at": snippet.get("publishedAt", ""),
                    "view_count": int(stats.get("viewCount", 0) or 0),
                    "like_count": int(stats.get("likeCount", 0) or 0),
                    "comment_count": int(stats.get("commentCount", 0) or 0),
                    "ambient_overlap": round(_keyword_overlap(title, description), 3),
                })

        # Sort by ambient overlap then by views
        results.sort(key=lambda x: (x["ambient_overlap"], x["view_count"]), reverse=True)
        return results

    @staticmethod
    def correlate(
        trends: List[Dict[str, Any]],
        analytics: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Correlate YouTube trends with channel analytics.

        Identifies which trending topics overlap with the channel's best
        performers and suggests content gaps.

        Args:
            trends: Output of :meth:`fetch_trending`.
            analytics: Channel analytics (same schema as ``data/analytics.json``).

        Returns:
            Correlation report dict.
        """
        videos = analytics.get("videos", [])

        # Build a set of mood/topic keywords from the channel
        channel_topics: set[str] = set()
        for v in videos:
            title = (v.get("title") or "").lower()
            for kw in AMBIENT_KEYWORDS:
                if kw in title:
                    channel_topics.add(kw)

        # Classify trends by overlap level
        high_overlap = [t for t in trends if t["ambient_overlap"] >= 0.04]
        medium_overlap = [t for t in trends if 0.01 <= t["ambient_overlap"] < 0.04]
        # Topics trending on YouTube but not yet in channel
        channel_gaps: List[str] = []
        for t in high_overlap:
            words = set((t["title"] + " " + t["description"]).lower().split())
            for kw in AMBIENT_KEYWORDS:
                if kw in words and kw not in channel_topics:
                    channel_gaps.append(kw)

        # Top performers correlation
        top_channel = sorted(
            [v for v in videos if v.get("metrics", {}).get("views")],
            key=lambda v: v["metrics"]["views"],
            reverse=True,
        )[:5]

        top_channel_summary = [
            {
                "title": v.get("title", v["video_id"]),
                "views": v["metrics"].get("views", 0),
                "retention": v["metrics"].get("average_view_percentage", 0),
            }
            for v in top_channel
        ]

        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_trending_fetched": len(trends),
            "high_overlap_count": len(high_overlap),
            "medium_overlap_count": len(medium_overlap),
            "channel_content_gaps": sorted(set(channel_gaps)),
            "top_trending_ambient": [
                {
                    "title": t["title"],
                    "view_count": t["view_count"],
                    "ambient_overlap": t["ambient_overlap"],
                    "channel_title": t["channel_title"],
                }
                for t in high_overlap[:10]
            ],
            "channel_top_performers": top_channel_summary,
        }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Fetch YouTube trending topics and correlate with channel analytics"
    )
    parser.add_argument(
        "--region",
        default="US",
        help="ISO 3166-1 alpha-2 region code (default: US)",
    )
    parser.add_argument(
        "--category",
        type=int,
        action="append",
        dest="categories",
        help=(
            "YouTube category ID to include (can be repeated). "
            f"Defaults: {AMBIENT_CATEGORIES}"
        ),
    )
    parser.add_argument(
        "--correlate",
        metavar="ANALYTICS_JSON",
        default=DEFAULT_ANALYTICS,
        help=f"Analytics JSON to correlate against (default: {DEFAULT_ANALYTICS})",
    )
    parser.add_argument(
        "--out",
        default=DEFAULT_OUT,
        help=f"Output JSON for trends (default: {DEFAULT_OUT})",
    )
    parser.add_argument(
        "--correlation-out",
        default=str(DATA_DIR / "trend_correlation.json"),
        help="Output JSON for correlation report (default: data/trend_correlation.json)",
    )
    args = parser.parse_args()

    categories = args.categories or AMBIENT_CATEGORIES

    # --- Fetch trends ---
    api_key = _api_key()
    trends: List[Dict[str, Any]] = []

    if not api_key:
        print(
            "⚠️  YOUTUBE_API_KEY not set — skipping trend fetch. "
            "Will still run correlation if analytics data is available."
        )
    else:
        print(f"🔍 Fetching YouTube trending videos (region={args.region}, categories={categories})...")
        try:
            advisor = TrendAdvisor(api_key=api_key)
            trends = advisor.fetch_trending(
                region_code=args.region,
                category_ids=categories,
            )
            print(f"   Found {len(trends)} trending videos.")

            out_path = Path(args.out)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            payload = {
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "region": args.region,
                "categories": categories,
                "trends": trends,
            }
            with open(out_path, "w") as f:
                json.dump(payload, f, indent=2)
            print(f"✅ Trends saved to {out_path}")

        except ImportError as e:
            print(f"❌ {e}")
            sys.exit(1)
        except ValueError as e:
            print(f"❌ {e}")
            sys.exit(1)
        except HttpError as e:
            print(f"❌ YouTube API error: {e}")
            raise

    # --- Correlate ---
    analytics = _load_analytics(args.correlate)
    n = len(analytics.get("videos", []))
    if n == 0:
        print(f"⚠️  No analytics data at {args.correlate}. Run fetch_analytics first.")
    else:
        print(f"\n🔗 Correlating {len(trends)} trends with {n} channel videos...")
        # We can correlate even with zero trends (shows gap analysis from channel data)
        correlation = TrendAdvisor.correlate(trends, analytics)

        corr_path = Path(args.correlation_out)
        corr_path.parent.mkdir(parents=True, exist_ok=True)
        with open(corr_path, "w") as f:
            json.dump(correlation, f, indent=2)

        print(f"✅ Correlation saved to {corr_path}")
        print()
        print("📊 Correlation Summary:")
        print(f"   Trending videos with ambient overlap: {correlation['high_overlap_count']}")
        print(f"   Content gaps (trending but missing from channel): "
              f"{', '.join(correlation['channel_content_gaps']) or 'none'}")
        if correlation["top_trending_ambient"]:
            print("\n🔥 Top trending ambient videos right now:")
            for t in correlation["top_trending_ambient"][:5]:
                print(f"   - \"{t['title']}\" ({t['view_count']:,} views)")


if __name__ == "__main__":
    main()
