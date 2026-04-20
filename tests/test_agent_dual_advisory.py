"""Tests for scripts/agent_dual_advisory.py."""

from __future__ import annotations

import importlib.util
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]


def _load(name: str, rel: str):
    path = _REPO / rel
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


rn = _load("run_next_report", "scripts/run_next_report.py")
adv = _load("agent_dual_advisory", "scripts/agent_dual_advisory.py")


def test_iso_week_suffix_matches_run_next():
    from datetime import datetime, timezone

    dt = datetime(2026, 4, 15, tzinfo=timezone.utc)
    assert adv.iso_week_suffix(dt) == rn.iso_week_suffix(dt) == "2026-W16"
