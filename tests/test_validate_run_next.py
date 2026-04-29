"""Tests for scripts/validate_run_next.py (run-next snapshot parity)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


_REPO = Path(__file__).resolve().parents[1]


def _load():
    path = _REPO / "scripts" / "validate_run_next.py"
    spec = importlib.util.spec_from_file_location("validate_run_next", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    # dataclasses expects the module to be present in sys.modules during exec
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


vr = _load()


def test_parse_run_next_snapshot_extracts_values():
    md = (
        "# Run next — advisory (2030-W05)\n\n"
        "**Correlate bundle `generated_at`:** 2030-01-15T12:00:00.000000Z\n"
        "\n"
        "## Brand snapshot (this run)\n\n"
        "- **Overall avg retention:** 12.34%\n"
        "- **Overall avg watch min / video (window):** 1.500\n"
        "- **Videos analyzed:** 50 with views / 100 total\n"
    )
    snap = vr.parse_run_next_snapshot(md)
    assert snap.correlate_generated_at == "2030-01-15T12:00:00.000000Z"
    assert snap.overall_avg_retention == 12.34
    assert snap.overall_avg_watch_minutes_per_video == 1.5
    assert snap.videos_with_views == 50
    assert snap.videos_analyzed == 100


def test_parse_run_next_snapshot_personal_heading():
    md = (
        "# Run next — personal advisory (2030-W05)\n\n"
        "**Correlate bundle `generated_at`:** 2030-01-15T12:00:00+00:00\n"
        "\n"
        "## Personal snapshot (this run)\n\n"
        "- **Overall avg retention:** 9%\n"
        "- **Overall avg watch min / video (window):** 3.000\n"
        "- **Videos analyzed:** 1 with views / 2 total\n"
    )
    snap = vr.parse_run_next_snapshot(md)
    assert snap.overall_avg_retention == 9.0
    assert snap.correlate_generated_at == "2030-01-15T12:00:00+00:00"


def test_validate_run_next_ok_when_matches():
    md = (
        "# Run next — advisory (2030-W05)\n\n"
        "**Correlate bundle `generated_at`:** 2030-01-01T00:00:00Z\n"
        "\n"
        "## Brand snapshot (this run)\n\n"
        "- **Overall avg retention:** 10.0%\n"
        "- **Overall avg watch min / video (window):** 2.000\n"
        "- **Videos analyzed:** 5 with views / 9 total\n"
    )
    sug = {
        "generated_at": "2030-01-01T00:00:00+00:00",
        "overall_avg_retention": 10.0,
        "overall_avg_watch_minutes_per_video": 2.0,
        "videos_with_views": 5,
        "videos_analyzed": 9,
        "suggestions": [],
    }
    assert vr.validate_run_next(run_next_text=md, suggestions_data=sug) == []


def test_validate_run_next_reports_mismatches():
    md = (
        "# Run next — advisory (2030-W05)\n\n"
        "**Correlate bundle `generated_at`:** 2030-01-01T00:00:00Z\n"
        "\n"
        "## Brand snapshot (this run)\n\n"
        "- **Overall avg retention:** 10.0%\n"
        "- **Videos analyzed:** 5 with views / 9 total\n"
    )
    sug = {
        "generated_at": "2030-01-01T00:00:00Z",
        "overall_avg_retention": 11.0,
        "videos_with_views": 6,
        "videos_analyzed": 9,
        "suggestions": [],
    }
    errs = vr.validate_run_next(run_next_text=md, suggestions_data=sug)
    assert any("overall_avg_retention mismatch" in e for e in errs)
    assert any("videos_with_views mismatch" in e for e in errs)


def test_validate_run_next_reports_generated_at_mismatch():
    md = (
        "# Run next — advisory (2030-W05)\n\n"
        "**Correlate bundle `generated_at`:** 2030-01-01T00:00:00Z\n"
        "\n"
        "## Brand snapshot (this run)\n\n"
        "- **Overall avg retention:** 10.0%\n"
        "- **Overall avg watch min / video (window):** 2.000\n"
        "- **Videos analyzed:** 5 with views / 9 total\n"
    )
    sug = {
        "generated_at": "2030-02-02T00:00:00Z",
        "overall_avg_retention": 10.0,
        "overall_avg_watch_minutes_per_video": 2.0,
        "videos_with_views": 5,
        "videos_analyzed": 9,
        "suggestions": [],
    }
    errs = vr.validate_run_next(run_next_text=md, suggestions_data=sug)
    assert any("generated_at mismatch" in e for e in errs)

