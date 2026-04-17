"""Tests for scripts/consume_run_intent.py (production run intent validation)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "scripts"))
import consume_run_intent as cr  # noqa: E402


def _minimal_moods_yaml(tmp_path: Path) -> Path:
    p = tmp_path / "moods.yaml"
    p.write_text(
        "trance:\n  tags: [a]\n  description_template: x\n"
        "sleep:\n  tags: [b]\n  description_template: y\n",
        encoding="utf-8",
    )
    return p


def test_validate_ok(tmp_path: Path):
    moods_yaml = _minimal_moods_yaml(tmp_path)
    data = {
        "schema_version": 1,
        "channel": "brand",
        "moods": ["trance", "sleep"],
        "duration": "10min",
        "dual": True,
        "upload": False,
        "max_videos": None,
    }
    out = cr.validate_and_normalize(data, moods_yaml=moods_yaml)
    assert out["moods"] == ["trance", "sleep"]
    assert out["upload"] is False


def test_max_videos_truncates(tmp_path: Path):
    moods_yaml = _minimal_moods_yaml(tmp_path)
    data = {
        "schema_version": 1,
        "channel": "personal",
        "moods": ["trance", "sleep"],
        "duration": "30s",
        "dual": False,
        "upload": False,
        "max_videos": 1,
    }
    out = cr.validate_and_normalize(data, moods_yaml=moods_yaml)
    assert out["moods"] == ["trance"]


def test_unknown_mood(tmp_path: Path):
    moods_yaml = _minimal_moods_yaml(tmp_path)
    data = {
        "schema_version": 1,
        "channel": "brand",
        "moods": ["not_a_mood"],
        "duration": "1h",
        "dual": False,
        "upload": False,
        "max_videos": None,
    }
    with pytest.raises(ValueError, match="Unknown mood"):
        cr.validate_and_normalize(data, moods_yaml=moods_yaml)


def test_bad_duration(tmp_path: Path):
    moods_yaml = _minimal_moods_yaml(tmp_path)
    data = {
        "schema_version": 1,
        "channel": "brand",
        "moods": ["trance"],
        "duration": "999h",
        "dual": False,
        "upload": False,
        "max_videos": None,
    }
    with pytest.raises(ValueError, match="duration"):
        cr.validate_and_normalize(data, moods_yaml=moods_yaml)


def test_upload_must_be_bool(tmp_path: Path):
    moods_yaml = _minimal_moods_yaml(tmp_path)
    data = {
        "schema_version": 1,
        "channel": "brand",
        "moods": ["trance"],
        "duration": "1h",
        "dual": False,
        "upload": "no",
        "max_videos": None,
    }
    with pytest.raises(ValueError, match="upload must be a JSON boolean"):
        cr.validate_and_normalize(data, moods_yaml=moods_yaml)


def test_cli_missing_file(tmp_path: Path):
    missing = tmp_path / "nope.json"
    r = subprocess.run(
        [sys.executable, str(_REPO / "scripts" / "consume_run_intent.py"), "--intent", str(missing)],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 1


def test_allow_planner_blocked_exits_zero(tmp_path: Path):
    intent = tmp_path / "run_intent.json"
    blocked = tmp_path / "run-intent-blocked.md"
    blocked.write_text("# Run intent — BLOCKED\n", encoding="utf-8")
    r = subprocess.run(
        [
            sys.executable,
            str(_REPO / "scripts" / "consume_run_intent.py"),
            "--intent",
            str(intent),
            "--blocked-report",
            str(blocked),
            "--allow-planner-blocked",
        ],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0


def test_missing_intent_with_blocked_still_fails_without_flag(tmp_path: Path):
    intent = tmp_path / "run_intent.json"
    blocked = tmp_path / "run-intent-blocked.md"
    blocked.write_text("# blocked\n", encoding="utf-8")
    r = subprocess.run(
        [
            sys.executable,
            str(_REPO / "scripts" / "consume_run_intent.py"),
            "--intent",
            str(intent),
            "--blocked-report",
            str(blocked),
        ],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 1
