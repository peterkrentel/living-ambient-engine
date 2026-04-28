"""Tests for agent/report.py (weekly analytics markdown)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from agent import report as ar  # noqa: E402


def test_md_table_cell_replaces_pipe_and_newlines() -> None:
    assert ar._md_table_cell("a | b | c") == "a · b · c"
    assert ar._md_table_cell("line1\nline2") == "line1 line2"
    assert ar._md_table_cell("  x  |  y  ") == "x · y"


def test_md_table_cell_truncates() -> None:
    long = "x" * 50
    assert len(ar._md_table_cell(long, max_chars=40)) == 40


def test_generate_report_top_tables_no_pipe_in_cells() -> None:
    data = [
        {
            "video_id": "vid1",
            "title": "Ambient ancient | 5 Mins | Evolving taik",
            "mood": "art_creator",
            "metadata": {"title": "Ambient ancient | 5 Mins | Evolving taik"},
            "metrics": {
                "average_view_percentage": 55.5,
                "views": 237,
                "watch_time_minutes": 161,
            },
        },
        {
            "video_id": "vid2",
            "title": "Second | Title",
            "mood": "trance",
            "metadata": {},
            "metrics": {
                "average_view_percentage": 10.0,
                "views": 10,
                "watch_time_minutes": 1,
            },
        },
    ]
    md = ar.generate_report(data, week="2026-W18")
    assert "Ambient ancient · 5 Mins · Evolving taik" in md or "Ambient ancient" in md
    assert "·" in md
    # Row for top views: exactly one pipe between title and mood (title must not contain raw |)
    for line in md.splitlines():
        if line.startswith("| ") and "237" in line and "161" in line:
            assert line.count("|") == 5  # | cell | cell | cell | cell | cell |
            break
    else:
        pytest.fail("expected top-by-views row with views 237 not found")
