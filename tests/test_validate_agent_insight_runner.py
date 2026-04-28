"""Tests for scripts/validate_agent_insight_runner.py."""

from __future__ import annotations

import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

import importlib.util


def _load():
    path = _REPO / "scripts" / "validate_agent_insight_runner.py"
    spec = importlib.util.spec_from_file_location("var", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


var = _load()


def test_validate_runner_ok_when_totals_in_summary() -> None:
    md = """# Agent advisory — Runner GGUF (CPU) (brand, 2026-W18)
---
## What I reviewed
- digest

## Summary
Channel totals: 100 views, 50 watch minutes, 3 videos with views.

## Insights
1. x
"""
    errs = var.validate_runner_advisory(runner_text=md, totals=(100, 50, 3))
    assert errs == []


def test_validate_runner_fails_when_totals_missing() -> None:
    md = """# x
---
## What I reviewed
- digest

## Summary
No numbers here.

## Insights
1. x
"""
    errs = var.validate_runner_advisory(runner_text=md, totals=(100, 50, 3))
    assert len(errs) == 1
    assert "not all present" in errs[0]


def test_validate_runner_skip_when_llm_skipped() -> None:
    md = """# x
_Runner LLM skipped:_ `llama-cpp-python` not installed.
"""
    errs = var.validate_runner_advisory(runner_text=md, totals=(1, 2, 3))
    assert len(errs) == 1
    assert errs[0].startswith("SKIP:")


def test_validate_runner_inference_error_returns_single_err() -> None:
    md = """# x
## Inference error

broken

## What I reviewed
x
## Insights
y
"""
    errs = var.validate_runner_advisory(runner_text=md, totals=(1, 2, 3))
    assert len(errs) == 1
    assert "Inference error" in errs[0]


def test_main_integration_tmp(tmp_path: Path) -> None:
    reports = tmp_path / "reports"
    reports.mkdir()
    week = "2099-W01"
    runner = reports / f"agent-insight-{week}-brand-runner.md"
    ana = tmp_path / "analytics.json"
    ana.write_text(
        json.dumps(
            {
                "videos": [
                    {"metrics": {"views": 10, "watch_time_minutes": 5}},
                    {"metrics": {"views": 0, "watch_time_minutes": 0}},
                ]
            }
        ),
        encoding="utf-8",
    )
    runner.write_text(
        "# Agent advisory\n---\n## What I reviewed\n- a\n## Summary\n10 views and 5 minutes and 1 videos with views.\n## Insights\n1. z\n",
        encoding="utf-8",
    )
    assert (
        var.main(
            [
                "--lane",
                "brand",
                "--week",
                week,
                "--reports-dir",
                str(reports),
                "--analytics",
                str(ana),
            ]
        )
        == 0
    )
