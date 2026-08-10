"""Tests for agent/gemini_advisor.py — Gemini recommendation engine."""

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

from agent.gemini_advisor import (  # noqa: E402
    _build_prompt,
    _load_analytics,
    _load_trends,
    _top_performers,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SAMPLE_ANALYTICS: Dict[str, Any] = {
    "fetched_at": "2026-08-01T00:00:00Z",
    "date_range": {"start": "2026-07-01", "end": "2026-07-31"},
    "videos": [
        {
            "video_id": "aaa",
            "title": "Deep Focus | 1 Hour | Study Music",
            "mood": "deep_focus",
            "metrics": {
                "views": 5000,
                "watch_time_minutes": 30000,
                "average_view_percentage": 72.0,
                "subscribers_gained": 30,
            },
        },
        {
            "video_id": "bbb",
            "title": "Rain Sleep | 8 Hours | White Noise",
            "mood": "rain_sleep",
            "metrics": {
                "views": 2000,
                "watch_time_minutes": 10000,
                "average_view_percentage": 55.0,
                "subscribers_gained": 10,
            },
        },
        {
            "video_id": "ccc",
            "title": "Fireplace | 3 Hours | Cozy Ambience",
            "mood": "fireplace",
            "metrics": {},  # No analytics yet
        },
    ],
}

SAMPLE_TRENDS: List[Dict[str, Any]] = [
    {
        "video_id": "t1",
        "title": "Lofi Hip Hop Study Beats",
        "description": "Chill lofi music for studying and focus",
        "view_count": 1_000_000,
        "ambient_overlap": 0.08,
        "channel_title": "ChillTunes",
    },
    {
        "video_id": "t2",
        "title": "Nature Sounds Forest Morning",
        "description": "Relaxing birds and rain for sleep",
        "view_count": 500_000,
        "ambient_overlap": 0.06,
        "channel_title": "NatureAudio",
    },
]


# ---------------------------------------------------------------------------
# Tests: helpers
# ---------------------------------------------------------------------------


def test_top_performers_sorted_by_views() -> None:
    top = _top_performers(SAMPLE_ANALYTICS["videos"])
    assert top[0]["video_id"] == "aaa"
    assert top[1]["video_id"] == "bbb"
    # Videos with no metrics are excluded
    assert all(v["video_id"] != "ccc" for v in top)


def test_top_performers_limit() -> None:
    many = [
        {"video_id": f"v{i}", "metrics": {"views": i * 100}} for i in range(20)
    ]
    assert len(_top_performers(many, n=5)) == 5


# ---------------------------------------------------------------------------
# Tests: prompt building
# ---------------------------------------------------------------------------


def test_build_prompt_contains_key_sections() -> None:
    prompt = _build_prompt(SAMPLE_ANALYTICS, [])
    assert "Channel Performance Summary" in prompt
    assert "Top Performing Videos" in prompt
    assert "Performance by Mood" in prompt
    assert "recommendations" in prompt.lower()


def test_build_prompt_includes_date_range() -> None:
    prompt = _build_prompt(SAMPLE_ANALYTICS, [])
    assert "2026-07-01" in prompt
    assert "2026-07-31" in prompt


def test_build_prompt_includes_trend_section_when_provided() -> None:
    prompt = _build_prompt(SAMPLE_ANALYTICS, SAMPLE_TRENDS)
    assert "YouTube Trending Topics" in prompt
    assert "Lofi Hip Hop" in prompt


def test_build_prompt_no_trend_section_when_empty() -> None:
    prompt = _build_prompt(SAMPLE_ANALYTICS, [])
    assert "YouTube Trending Topics" not in prompt


def test_build_prompt_includes_video_titles() -> None:
    prompt = _build_prompt(SAMPLE_ANALYTICS, [])
    assert "Deep Focus" in prompt
    assert "Rain Sleep" in prompt


# ---------------------------------------------------------------------------
# Tests: load helpers
# ---------------------------------------------------------------------------


def test_load_analytics_missing_file_returns_empty(tmp_path) -> None:
    with patch("agent.gemini_advisor._analytics_json_path", return_value=tmp_path / "missing.json"):
        result = _load_analytics()
    assert result == {"videos": []}


def test_load_analytics_reads_json(tmp_path) -> None:
    data = {"videos": [{"video_id": "x"}]}
    p = tmp_path / "analytics.json"
    p.write_text(json.dumps(data))
    with patch("agent.gemini_advisor._analytics_json_path", return_value=p):
        result = _load_analytics()
    assert result["videos"][0]["video_id"] == "x"


def test_load_trends_missing_file_returns_empty() -> None:
    result = _load_trends("/nonexistent/path.json")
    assert result == []


def test_load_trends_reads_list(tmp_path) -> None:
    p = tmp_path / "trends.json"
    p.write_text(json.dumps({"trends": SAMPLE_TRENDS}))
    result = _load_trends(str(p))
    assert len(result) == 2
    assert result[0]["video_id"] == "t1"


# ---------------------------------------------------------------------------
# Tests: GeminiAdvisor (mocked)
# ---------------------------------------------------------------------------


def test_gemini_advisor_raises_without_api_key() -> None:
    """GeminiAdvisor requires GEMINI_API_KEY."""
    import os

    with patch.dict(os.environ, {}, clear=True):
        # Ensure GEMINI_API_KEY is not set
        os.environ.pop("GEMINI_API_KEY", None)

        # HAS_GENAI may be False in test env; either ImportError or ValueError is acceptable
        from agent import gemini_advisor as ga

        if not ga.HAS_GENAI:
            pytest.skip("google-generativeai not installed")

        with pytest.raises(ValueError, match="API key"):
            ga.GeminiAdvisor(api_key=None)


def test_gemini_advisor_get_recommendation_parses_json() -> None:
    """GeminiAdvisor.get_recommendation() should parse Gemini's JSON response."""
    import agent.gemini_advisor as ga

    if not ga.HAS_GENAI:
        pytest.skip("google-generativeai not installed")

    fake_json = json.dumps({
        "strategy": "Focus on lo-fi study beats.",
        "recommendations": [
            {
                "title": "LoFi Study Beats | 1 Hour",
                "mood": "lofi_study",
                "visual_style": "lissajous",
                "duration_minutes": 60,
                "rationale": "Trending topic with high overlap",
            }
        ],
    })

    mock_response = MagicMock()
    mock_response.text = fake_json

    mock_model = MagicMock()
    mock_model.generate_content.return_value = mock_response

    with patch("google.generativeai.configure"), \
         patch("google.generativeai.GenerativeModel", return_value=mock_model):
        advisor = ga.GeminiAdvisor(api_key="fake-key")
        result = advisor.get_recommendation(SAMPLE_ANALYTICS, SAMPLE_TRENDS)

    assert result["strategy"] == "Focus on lo-fi study beats."
    assert len(result["recommendations"]) == 1
    assert result["recommendations"][0]["visual_style"] == "lissajous"
    assert "generated_at" in result
    assert "model" in result


def test_gemini_advisor_handles_markdown_fenced_response() -> None:
    """Gemini sometimes wraps JSON in markdown code fences."""
    import agent.gemini_advisor as ga

    if not ga.HAS_GENAI:
        pytest.skip("google-generativeai not installed")

    payload = {"strategy": "test", "recommendations": []}
    fenced = f"```json\n{json.dumps(payload)}\n```"

    mock_response = MagicMock()
    mock_response.text = fenced

    mock_model = MagicMock()
    mock_model.generate_content.return_value = mock_response

    with patch("google.generativeai.configure"), \
         patch("google.generativeai.GenerativeModel", return_value=mock_model):
        advisor = ga.GeminiAdvisor(api_key="fake-key")
        result = advisor.get_recommendation(SAMPLE_ANALYTICS)

    assert result["strategy"] == "test"
