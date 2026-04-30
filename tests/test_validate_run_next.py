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


def _base_run_next_md() -> str:
    return (
        "# Run next — advisory (2030-W05)\n\n"
        "**Correlate bundle `generated_at`:** 2030-01-01T00:00:00Z\n\n"
        "## Brand snapshot (this run)\n\n"
        "- **Overall avg retention:** 10.0%\n"
        "- **Overall avg watch min / video (window):** 2.000\n"
        "- **Videos analyzed:** 5 with views / 9 total\n"
    )


def _base_suggestions() -> dict:
    return {
        "generated_at": "2030-01-01T00:00:00+00:00",
        "overall_avg_retention": 10.0,
        "overall_avg_watch_minutes_per_video": 2.0,
        "videos_with_views": 5,
        "videos_analyzed": 9,
        "suggestions": [
            {"type": "music_style", "name": "none", "action": "increase", "actionable": True},
            {"type": "topic", "name": "x", "action": "reduce", "actionable": False},
        ],
    }


def test_validate_run_next_tranche2_actionable_and_exploratory_citations_ok():
    md = (
        _base_run_next_md()
        + "\n## Actionable (correlate gates passed)\n\n"
        + "↑ **`music_style` / `none`** (metric) — r — `high` — evidence index **`s.json` → `suggestions[0]`**\n"
        + "\n## Exploratory — lean in (low n / views)\n\n"
        + "↓ `topic` / `x` (metric) — r — `suggestions[1]`\n"
        + "\n## Audit — overview excerpt (brand)\n\n"
        + "First line of channel context.\n"
    )
    audit = "## Overview\n\nFirst line of channel context.\n\n## Next section\n"
    sug = _base_suggestions()
    assert vr.validate_run_next(run_next_text=md, suggestions_data=sug, audit_text=audit) == []


def test_validate_run_next_tranche2_suggestion_index_out_of_range():
    md = (
        _base_run_next_md()
        + "\n## Actionable (correlate gates passed)\n\n"
        + "↑ **`music_style` / `none`** (m) — r — `h` — **`p` → `suggestions[9]`**\n"
    )
    errs = vr.validate_run_next(run_next_text=md, suggestions_data=_base_suggestions())
    assert any("out of range" in e for e in errs)


def test_validate_run_next_tranche2_type_name_mismatch():
    md = (
        _base_run_next_md()
        + "\n## Actionable (correlate gates passed)\n\n"
        + "↑ **`wrong` / `none`** (m) — r — `h` — **`p` → `suggestions[0]`**\n"
    )
    errs = vr.validate_run_next(run_next_text=md, suggestions_data=_base_suggestions())
    assert any("type/name mismatch" in e for e in errs)


def test_validate_run_next_tranche2_action_icon_mismatch():
    md = (
        _base_run_next_md()
        + "\n## Actionable (correlate gates passed)\n\n"
        + "↓ **`music_style` / `none`** (m) — r — `h` — **`p` → `suggestions[0]`**\n"
    )
    errs = vr.validate_run_next(run_next_text=md, suggestions_data=_base_suggestions())
    assert any("expects leading ↑" in e for e in errs)


def test_validate_run_next_tranche2_audit_excerpt_without_audit_file_errors():
    md = (
        _base_run_next_md()
        + "\n## Audit — overview excerpt (brand)\n\n"
        + "Some excerpt body.\n"
    )
    errs = vr.validate_run_next(run_next_text=md, suggestions_data=_base_suggestions(), audit_text=None)
    assert any("no audit file was provided" in e for e in errs)


def test_validate_run_next_tranche2_audit_excerpt_mismatch():
    md = (
        _base_run_next_md()
        + "\n## Audit — overview excerpt (brand)\n\n"
        + "Run-next claims this text.\n"
    )
    audit = "## Overview\n\nAudit file says something else.\n"
    errs = vr.validate_run_next(run_next_text=md, suggestions_data=_base_suggestions(), audit_text=audit)
    assert any("audit overview excerpt mismatch" in e for e in errs)

