"""Unit tests for scripts/plan_run_intent.py anti-repeat helpers."""

from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]


def _load():
    path = _REPO / "scripts" / "plan_run_intent.py"
    spec = importlib.util.spec_from_file_location("plan_run_intent", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


pri = _load()


def test_duration_label_to_seconds():
    assert pri.duration_label_to_seconds("10min") == 600
    assert pri.duration_label_to_seconds("1h") == 3600
    assert pri.duration_label_to_seconds("30s") == 30


def test_parse_iso_datetime_z():
    dt = pri.parse_iso_datetime("2026-05-01T12:00:00Z")
    assert dt is not None
    assert dt.tzinfo is not None
    assert dt.year == 2026


def test_recent_blocked_respects_channel_and_window(tmp_path: Path):
    now = datetime(2026, 5, 10, 12, 0, 0, tzinfo=timezone.utc)
    gen = {
        "schema_version": 1,
        "videos": [
            {
                "mood": "sleep",
                "duration_seconds": 600,
                "channel": "brand",
                "uploaded_at": "2026-05-09T12:00:00+00:00",
            },
            {
                "mood": "sleep",
                "duration_seconds": 600,
                "channel": "personal",
                "uploaded_at": "2026-05-09T12:00:00+00:00",
            },
            {
                "mood": "trance",
                "duration_seconds": 600,
                "channel": "brand",
                "uploaded_at": "2026-03-01T12:00:00+00:00",
            },
            {
                "mood": "forest_morning",
                "duration_seconds": 600,
                "channel": "brand",
                "uploaded_at": "2026-05-09T12:00:00+00:00",
            },
        ],
    }
    p = tmp_path / "generations.json"
    p.write_text(json.dumps(gen), encoding="utf-8")

    b = pri.recent_blocked_mood_duration_keys(
        p, channel="brand", weeks=4, now_utc=now
    )
    assert ("sleep", 600) in b
    assert ("trance", 600) not in b
    assert ("forest_morning", 600) in b

    pers = pri.recent_blocked_mood_duration_keys(
        p, channel="personal", weeks=4, now_utc=now
    )
    assert pers == {("sleep", 600)}


def test_recent_blocked_skips_rows_without_channel(tmp_path: Path):
    now = datetime(2026, 5, 10, tzinfo=timezone.utc)
    gen = {
        "videos": [
            {
                "mood": "sleep",
                "duration_seconds": 600,
                "uploaded_at": "2026-05-09T12:00:00+00:00",
            }
        ]
    }
    p = tmp_path / "g.json"
    p.write_text(json.dumps(gen), encoding="utf-8")
    assert pri.recent_blocked_mood_duration_keys(p, channel="brand", weeks=4, now_utc=now) == set()


def test_filter_moods_anti_repeat():
    blocked = {("sleep", 600)}
    kept, skips = pri.filter_moods_anti_repeat(
        ["sleep", "trance"], duration_seconds=600, blocked=blocked
    )
    assert kept == ["trance"]
    assert len(skips) == 1


def test_recent_blocked_weeks_zero(tmp_path: Path):
    p = tmp_path / "empty.json"
    p.write_text('{"videos":[]}', encoding="utf-8")
    assert (
        pri.recent_blocked_mood_duration_keys(
            p, channel="brand", weeks=0, now_utc=datetime.now(timezone.utc)
        )
        == set()
    )
