#!/usr/bin/env python3
"""Fetch YouTube Analytics data.

Pulls performance metrics from YouTube Analytics API and stores
them in data/analytics.json for correlation with generation parameters.

Spec: docs/spec/AGENT.md
Contract: docs/spec/contracts/agent-youtube.md
"""

import base64
import json
import os
import pickle
from datetime import datetime, timedelta, timezone, date
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    HAS_GOOGLE_API = True
except ImportError:
    HAS_GOOGLE_API = False


DATA_DIR = Path("data")
ANALYTICS_FILE = DATA_DIR / "analytics.json"
GENERATIONS_FILE = DATA_DIR / "generations.json"


class AnalyticsFetcher:
    """Fetches YouTube Analytics data for tracked videos."""
    
    def __init__(self, token_env: str = "YOUTUBE_TOKEN_PICKLE"):
        """Initialize with YouTube API credentials.
        
        Args:
            token_env: Environment variable containing base64-encoded token pickle
        """
        if not HAS_GOOGLE_API:
            raise ImportError("google-api-python-client not installed")
        
        self.credentials = self._load_credentials(token_env)
        self.youtube = build("youtube", "v3", credentials=self.credentials)
        self.analytics = build("youtubeAnalytics", "v2", credentials=self.credentials)
    
    def _load_credentials(self, token_env: str) -> Credentials:
        """Load OAuth credentials from environment or file."""
        # Try environment variable first
        token_b64 = os.environ.get(token_env)
        if token_b64:
            token_data = base64.b64decode(token_b64)
            return pickle.loads(token_data)
        
        # Try brand channel token
        token_b64 = os.environ.get("YOUTUBE_TOKEN_PICKLE_BRAND")
        if token_b64:
            token_data = base64.b64decode(token_b64)
            return pickle.loads(token_data)
        
        # Try local file
        token_file = Path("youtube_token.pickle")
        if token_file.exists():
            with open(token_file, "rb") as f:
                return pickle.load(f)
        
        raise ValueError("No YouTube credentials found")
    
    def get_channel_id(self) -> str:
        """Get the authenticated user's channel ID."""
        response = self.youtube.channels().list(part="id", mine=True).execute()
        return response["items"][0]["id"]
    
    def fetch_video_metrics(
        self,
        video_ids: List[str],
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Dict[str, Any]:
        """Fetch analytics for specific videos.
        
        Args:
            video_ids: List of YouTube video IDs
            start_date: Start of date range (default: 28 days ago)
            end_date: End of date range (default: yesterday)
        
        Returns:
            Dict with fetched_at timestamp and video metrics
        """
        if not video_ids:
            raise ValueError("video_ids must not be empty")
        
        if start_date is None:
            start_date = date.today() - timedelta(days=28)
        if end_date is None:
            end_date = date.today() - timedelta(days=1)
        
        if start_date > end_date:
            raise ValueError("start_date must be <= end_date")
        
        channel_id = self.get_channel_id()
        results = []
        
        for video_id in video_ids:
            try:
                response = self.analytics.reports().query(
                    ids=f"channel=={channel_id}",
                    startDate=start_date.isoformat(),
                    endDate=end_date.isoformat(),
                    metrics="views,estimatedMinutesWatched,averageViewDuration,"
                            "averageViewPercentage,subscribersGained,subscribersLost,"
                            "likes,dislikes,comments,shares",
                    filters=f"video=={video_id}",
                ).execute()
                
                metrics = self._parse_metrics(response)
                results.append({"video_id": video_id, "metrics": metrics})
                
            except HttpError as e:
                print(f"⚠️ Error fetching analytics for {video_id}: {e}")
                continue
        
        return {
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "date_range": {"start": start_date.isoformat(), "end": end_date.isoformat()},
            "videos": results,
        }
    
    def _parse_metrics(self, response: Dict) -> Dict[str, Any]:
        """Parse API response into our schema."""
        if not response.get("rows"):
            return {}
        
        row = response["rows"][0]
        headers = [h["name"] for h in response["columnHeaders"]]
        
        return {
            "views": row[headers.index("views")] if "views" in headers else 0,
            "watch_time_minutes": row[headers.index("estimatedMinutesWatched")] if "estimatedMinutesWatched" in headers else 0,
            "average_view_duration_seconds": row[headers.index("averageViewDuration")] if "averageViewDuration" in headers else 0,
            "average_view_percentage": row[headers.index("averageViewPercentage")] if "averageViewPercentage" in headers else 0,
            "subscribers_gained": row[headers.index("subscribersGained")] if "subscribersGained" in headers else 0,
            "subscribers_lost": row[headers.index("subscribersLost")] if "subscribersLost" in headers else 0,
            "likes": row[headers.index("likes")] if "likes" in headers else 0,
            "dislikes": row[headers.index("dislikes")] if "dislikes" in headers else 0,
            "comments": row[headers.index("comments")] if "comments" in headers else 0,
            "shares": row[headers.index("shares")] if "shares" in headers else 0,
        }


def load_analytics() -> Dict[str, Any]:
    """Load existing analytics data."""
    if ANALYTICS_FILE.exists():
        with open(ANALYTICS_FILE, "r") as f:
            return json.load(f)
    return {"fetched_at": None, "videos": []}


def save_analytics(data: Dict[str, Any]) -> None:
    """Save analytics data to file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(ANALYTICS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_tracked_video_ids() -> List[str]:
    """Get video IDs from generations.json."""
    if not GENERATIONS_FILE.exists():
        return []

    with open(GENERATIONS_FILE, "r") as f:
        data = json.load(f)

    return [v["video_id"] for v in data.get("videos", []) if v.get("video_id")]


def main():
    """CLI entry point - fetch analytics for all tracked videos."""
    import argparse

    parser = argparse.ArgumentParser(description="Fetch YouTube Analytics")
    parser.add_argument("--days", type=int, default=28, help="Days of data to fetch")
    args = parser.parse_args()

    video_ids = get_tracked_video_ids()

    if not video_ids:
        print("📊 No videos to fetch analytics for (generations.json is empty)")
        return

    print(f"📊 Fetching analytics for {len(video_ids)} videos...")

    try:
        fetcher = AnalyticsFetcher()
        start_date = date.today() - timedelta(days=args.days)
        end_date = date.today() - timedelta(days=1)

        result = fetcher.fetch_video_metrics(video_ids, start_date, end_date)

        # Merge with existing data
        existing = load_analytics()
        existing_ids = {v["video_id"]: i for i, v in enumerate(existing.get("videos", []))}

        for video in result["videos"]:
            vid = video["video_id"]
            if vid in existing_ids:
                existing["videos"][existing_ids[vid]] = video
            else:
                existing["videos"].append(video)

        existing["fetched_at"] = result["fetched_at"]
        existing["date_range"] = result["date_range"]

        save_analytics(existing)
        print(f"✅ Analytics saved to {ANALYTICS_FILE}")
        print(f"   Videos with data: {len(result['videos'])}")

    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("   Install with: pip install google-api-python-client google-auth")
    except Exception as e:
        print(f"❌ Error fetching analytics: {e}")
        raise


if __name__ == "__main__":
    main()

