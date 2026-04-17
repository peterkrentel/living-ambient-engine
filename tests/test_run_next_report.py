"""Tests for scripts/run_next_report.py (deterministic run-next advisory)."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]


def _load_run_next():
    path = _REPO / "scripts" / "run_next_report.py"
    spec = importlib.util.spec_from_file_location("run_next_report", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


rn = _load_run_next()


def test_iso_week_suffix_format():
    from datetime import datetime, timezone

    s = rn.iso_week_suffix(datetime(2026, 4, 15, tzinfo=timezone.utc))
    assert s == "2026-W16"


def test_build_markdown_lists_actionable_and_indices():
    sug = {
        "generated_at": "2026-01-01T00:00:00Z",
        "overall_avg_retention": 10.0,
        "overall_avg_watch_minutes_per_video": 1.5,
        "videos_analyzed": 100,
        "videos_with_views": 50,
        "suggestions": [
            {
                "action": "increase",
                "type": "mood",
                "name": "sleep",
                "reason": "test exploratory",
                "confidence": "low",
                "actionable": False,
                "sample_size": 3,
                "group_views": 50,
                "metric": "average_view_percentage",
            },
            {
                "action": "increase",
                "type": "mood",
                "name": "trance",
                "reason": "test actionable",
                "confidence": "medium",
                "actionable": True,
                "sample_size": 10,
                "group_views": 500,
                "metric": "average_view_percentage",
            },
        ],
    }
    audit = """# Channel coverage audit (2026-W99)\n\n## Overview\n\n- **Videos in analytics:** 100\n\n## Mood\n\nx\n"""
    md = rn.build_markdown(
        "2026-W99",
        sug,
        Path("/tmp/audit-2026-W99.md"),
        audit,
        lane="brand",
        suggestions_citation_path="data/suggestions.json",
        cross_analytics_summary="`data/analytics_personal.json` — **3** videos",
        cross_latest_report_rel="data/reports/2026-W01-personal.md",
    )
    assert "Packaging & confounders" in md
    assert "`data/suggestions.json` → `suggestions[1]`" in md
    assert "`suggestions[0]`" in md
    assert "Videos in analytics:** 100" in md


def test_main_writes_file(tmp_path: Path):
    reports = tmp_path / "reports"
    reports.mkdir()
    (reports / "audit-2030-W05.md").write_text(
        "# Channel coverage audit (2030-W05)\n\n## Overview\n\n- line\n",
        encoding="utf-8",
    )
    sug_path = tmp_path / "suggestions.json"
    sug_path.write_text(
        json.dumps(
            {
                "generated_at": "2030-01-01T00:00:00Z",
                "overall_avg_retention": 5.0,
                "videos_analyzed": 1,
                "videos_with_views": 1,
                "suggestions": [],
            }
        ),
        encoding="utf-8",
    )
    argv = [
        "--week",
        "2030-W05",
        "--suggestions",
        str(sug_path),
        "--reports-dir",
        str(reports),
        "--personal-analytics",
        str(tmp_path / "missing.json"),
    ]
    assert rn.main(argv) == 0
    out = reports / "run-next-2030-W05.md"
    assert out.is_file()
    assert "Run next — advisory (2030-W05)" in out.read_text(encoding="utf-8")


def test_main_missing_suggestions(tmp_path: Path):
    assert rn.main(["--week", "2030-W05", "--suggestions", str(tmp_path / "nope.json"), "--reports-dir", str(tmp_path)]) == 1


def test_main_personal_writes_file(tmp_path: Path):
    reports = tmp_path / "reports"
    reports.mkdir()
    (reports / "audit-2030-W07-personal.md").write_text(
        "# Channel coverage audit (2030-W07)\n\n## Overview\n\n- **Videos:** 2\n",
        encoding="utf-8",
    )
    sug_path = tmp_path / "suggestions_personal.json"
    sug_path.write_text(
        json.dumps(
            {
                "generated_at": "2030-02-01T00:00:00Z",
                "overall_avg_retention": 4.0,
                "videos_analyzed": 2,
                "videos_with_views": 2,
                "suggestions": [],
            }
        ),
        encoding="utf-8",
    )
    argv = [
        "--lane",
        "personal",
        "--week",
        "2030-W07",
        "--suggestions",
        str(sug_path),
        "--reports-dir",
        str(reports),
        "--brand-analytics",
        str(tmp_path / "missing-brand.json"),
    ]
    assert rn.main(argv) == 0
    out = reports / "run-next-2030-W07-personal.md"
    assert out.is_file()
    text = out.read_text(encoding="utf-8")
    assert "Run next — personal advisory (2030-W07)" in text
    assert "suggestions_personal.json" in text
