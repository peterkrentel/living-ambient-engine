"""Tests for youtube/trend_advisor.py — YouTube trending topics and correlation."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

import pytest

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from youtube.trend_advisor import (  # noqa: E402
    AMBIENT_KEYWORDS,
    TrendAdvisor,
    _keyword_overlap,
    _load_analytics,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SAMPLE_ANALYTICS: Dict[str, Any] = {
    "videos": [
        {
            "video_id": "aaa",
            "title": "Deep Focus Study Music 1 Hour",
            "mood": "deep_focus",
            "metrics": {"views": 5000, "average_view_percentage": 70.0},
        },
        {
            "video_id": "bbb",
            "title": "Rain Sleep 8 Hours White Noise",
            "mood": "rain_sleep",
            "metrics": {"views": 2000, "average_view_percentage": 55.0},
        },
    ]
}

SAMPLE_TRENDS: List[Dict[str, Any]] = [
    {
        "video_id": "t1",
        "title": "Lofi Hip Hop Chill Study Beats",
        "description": "Relaxing chill lofi music to study and focus",
        "channel_title": "ChillTunes",
        "view_count": 1_000_000,
        "ambient_overlap": 0.12,
        "category_id": 10,
    },
    {
        "video_id": "t2",
        "title": "Cooking Tutorial Episode 5",
        "description": "Today we make pasta",
        "channel_title": "FoodChannel",
        "view_count": 800_000,
        "ambient_overlap": 0.0,
        "category_id": 26,
    },
    {
        "video_id": "t3",
        "title": "Nature Forest Morning Birds",
        "description": "Ambient sounds for sleep and relaxation",
        "channel_title": "NatureAudio",
        "view_count": 300_000,
        "ambient_overlap": 0.08,
        "category_id": 10,
    },
]


# ---------------------------------------------------------------------------
# Tests: helpers
# ---------------------------------------------------------------------------


def test_keyword_overlap_detects_ambient_keywords() -> None:
    title = "Lofi Study Beats for Focus"
    description = "Chill music for studying and relaxation"
    score = _keyword_overlap(title, description)
    assert score > 0


def test_keyword_overlap_non_ambient_is_low() -> None:
    score = _keyword_overlap("Sports News Today", "Latest football match results")
    assert score == 0.0


def test_keyword_overlap_full_match_is_bounded() -> None:
    # Max overlap should be <= 1.0
    full_title = " ".join(AMBIENT_KEYWORDS)
    score = _keyword_overlap(full_title, full_title)
    assert 0.0 <= score <= 1.0


def test_load_analytics_missing_returns_empty(tmp_path) -> None:
    result = _load_analytics(str(tmp_path / "nonexistent.json"))
    assert result == {"videos": []}


def test_load_analytics_reads_file(tmp_path) -> None:
    p = tmp_path / "analytics.json"
    p.write_text(json.dumps(SAMPLE_ANALYTICS))
    result = _load_analytics(str(p))
    assert len(result["videos"]) == 2


# ---------------------------------------------------------------------------
# Tests: correlation
# ---------------------------------------------------------------------------


def test_correlate_high_overlap_count() -> None:
    result = TrendAdvisor.correlate(SAMPLE_TRENDS, SAMPLE_ANALYTICS)
    # t1 (0.12) and t3 (0.08) should be high overlap (>= 0.04)
    assert result["high_overlap_count"] == 2


def test_correlate_total_trends_count() -> None:
    result = TrendAdvisor.correlate(SAMPLE_TRENDS, SAMPLE_ANALYTICS)
    assert result["total_trending_fetched"] == len(SAMPLE_TRENDS)


def test_correlate_top_trending_ambient_excludes_non_ambient() -> None:
    result = TrendAdvisor.correlate(SAMPLE_TRENDS, SAMPLE_ANALYTICS)
    titles = [t["title"] for t in result["top_trending_ambient"]]
    assert "Cooking Tutorial Episode 5" not in titles


def test_correlate_channel_top_performers() -> None:
    result = TrendAdvisor.correlate(SAMPLE_TRENDS, SAMPLE_ANALYTICS)
    performers = result["channel_top_performers"]
    assert len(performers) >= 1
    # Should be sorted by views descending
    assert performers[0]["views"] >= performers[-1]["views"]


def test_correlate_empty_trends() -> None:
    """Correlation should work with zero trends (just reports channel state)."""
    result = TrendAdvisor.correlate([], SAMPLE_ANALYTICS)
    assert result["total_trending_fetched"] == 0
    assert result["high_overlap_count"] == 0
    assert isinstance(result["channel_content_gaps"], list)


def test_correlate_empty_analytics() -> None:
    """Correlation should gracefully handle empty channel data."""
    result = TrendAdvisor.correlate(SAMPLE_TRENDS, {"videos": []})
    assert result["channel_top_performers"] == []


# ---------------------------------------------------------------------------
# Tests: TrendAdvisor.fetch_trending (mocked)
# ---------------------------------------------------------------------------


def test_fetch_trending_deduplicates_videos() -> None:
    """Same video in multiple categories should appear only once."""
    if not _has_google_api():
        pytest.skip("google-api-python-client not installed")

    duplicate_item = {
        "id": "dup1",
        "snippet": {
            "title": "Chill Study Lofi",
            "description": "Relax and focus with ambient music",
            "channelTitle": "ChillChannel",
            "publishedAt": "2026-08-01T00:00:00Z",
        },
        "statistics": {"viewCount": "100000", "likeCount": "5000", "commentCount": "200"},
    }

    mock_response = {"items": [duplicate_item]}

    mock_yt = MagicMock()
    mock_yt.videos().list().execute.return_value = mock_response

    with patch("youtube.trend_advisor.build", return_value=mock_yt):
        advisor = TrendAdvisor(api_key="fake-key")
        # Two categories → same video returned twice, should be deduped
        results = advisor.fetch_trending(region_code="US", category_ids=[10, 22])

    titles = [r["title"] for r in results]
    assert titles.count("Chill Study Lofi") == 1


def test_fetch_trending_sets_ambient_overlap() -> None:
    """fetch_trending should compute ambient_overlap for each video."""
    if not _has_google_api():
        pytest.skip("google-api-python-client not installed")

    item = {
        "id": "v1",
        "snippet": {
            "title": "Ambient chill lofi for study and focus",
            "description": "Relax and meditate",
            "channelTitle": "Ch",
            "publishedAt": "2026-08-01T00:00:00Z",
        },
        "statistics": {"viewCount": "50000"},
    }

    mock_yt = MagicMock()
    mock_yt.videos().list().execute.return_value = {"items": [item]}

    with patch("youtube.trend_advisor.build", return_value=mock_yt):
        advisor = TrendAdvisor(api_key="fake-key")
        results = advisor.fetch_trending(region_code="US", category_ids=[10])

    assert results[0]["ambient_overlap"] > 0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _has_google_api() -> bool:
    try:
        from googleapiclient.discovery import build  # noqa: F401
        return True
    except ImportError:
        return False
