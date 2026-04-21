"""Tests for scripts/agent_dual_advisory.py."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

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


def test_dim_coverage_stats():
    assert adv._dim_coverage_stats(None) == {
        "labels": 0,
        "produced_at_least_one": 0,
        "produced_zero_views": 0,
    }
    d = {
        "a": {"total": 2, "with_views": 0},
        "b": {"total": 0, "with_views": 0},
        "c": {"total": 1, "with_views": 1},
    }
    assert adv._dim_coverage_stats(d) == {
        "labels": 3,
        "produced_at_least_one": 2,
        "produced_zero_views": 1,
    }


def test_strip_run_next_removes_brand_cross_read_for_personal():
    body = """# Run next — personal

## Personal snapshot (this run)

- **Videos analyzed:** 10 with views / 108 total

## Brand lane (cross-read only)

- 338 videos — brand-only cross-read.

## Production hooks (manual)

- hook line
"""
    out = adv._strip_run_next_cross_lane_section(body, "personal")
    assert "## Brand lane" not in out
    assert "338" not in out
    assert "Personal snapshot" in out
    assert "## Production hooks (manual)" in out
    assert "hook line" in out


def test_strip_run_next_removes_personal_cross_read_for_brand():
    body = """## Brand snapshot

x

## Personal lane (context only)

- 108 personal-only.

## Production hooks (manual)

y
"""
    out = adv._strip_run_next_cross_lane_section(body, "brand")
    assert "## Personal lane" not in out
    assert "108 personal" not in out
    assert "## Production hooks (manual)" in out
    assert out.strip().endswith("y")


def test_strip_run_next_noop_when_markers_absent():
    assert adv._strip_run_next_cross_lane_section("plain", "personal") == "plain"


def test_runner_bundle_includes_scope_and_strips_cross_lane_when_present():
    rn = _REPO / "data" / "reports" / "run-next-2026-W17-personal.md"
    if not rn.exists():
        pytest.skip("no run-next personal fixture")
    b = adv.build_runner_bundle("personal", "2026-W17")
    assert "### runner scope" in b
    assert "Advisory lane:" in b
    assert "personal" in b
    if "## Brand lane (cross-read only)" in rn.read_text(encoding="utf-8", errors="replace"):
        assert "## Brand lane (cross-read only)" not in b


def test_runner_bundle_stays_within_ctx_budget():
    """Lean runner bundle must stay under RUNNER_BUNDLE_MAX_CHARS (missing files = small)."""
    b = adv.build_runner_bundle("personal", "2099-W99")
    assert len(b) <= adv.RUNNER_BUNDLE_MAX_CHARS + 400


def test_compact_suggestions_includes_coverage_summary_when_present():
    sug = _REPO / "data" / "suggestions_personal.json"
    if not sug.exists():
        pytest.skip("no fixtures/data/suggestions_personal.json in checkout")
    text = adv._compact_suggestions(sug)
    assert "coverage_summary" in text
    assert '"moods"' in text


def test_compact_analytics_retention_slice_key_when_present():
    ana = _REPO / "data" / "analytics_personal.json"
    if not ana.exists():
        pytest.skip("no fixtures/data/analytics_personal.json in checkout")
    text = adv._compact_analytics(ana)
    assert "top_by_avg_view_pct_min_views_2" in text


def test_gemini_min_interval_sec_default(monkeypatch):
    monkeypatch.delenv("GEMINI_MIN_INTERVAL_SEC", raising=False)
    assert adv._gemini_min_interval_sec() == 6.0


def test_gemini_min_interval_sec_env(monkeypatch):
    monkeypatch.setenv("GEMINI_MIN_INTERVAL_SEC", "15")
    assert adv._gemini_min_interval_sec() == 15.0
    monkeypatch.setenv("GEMINI_MIN_INTERVAL_SEC", "0")
    assert adv._gemini_min_interval_sec() == 0.0


def test_gemini_max_retries_env(monkeypatch):
    monkeypatch.setenv("GEMINI_MAX_RETRIES", "2")
    assert adv._gemini_max_retries() == 2


def test_gemini_429_min_sleep_sec(monkeypatch):
    monkeypatch.delenv("GEMINI_429_MIN_SLEEP_SEC", raising=False)
    assert adv._gemini_429_min_sleep_sec() == 0.0
    monkeypatch.setenv("GEMINI_429_MIN_SLEEP_SEC", "20")
    assert adv._gemini_429_min_sleep_sec() == 20.0


def test_gemini_model_defaults_to_25_flash(monkeypatch):
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    assert adv._gemini_model() == "gemini-2.5-flash"


def test_max_runner_tokens_default(monkeypatch):
    monkeypatch.delenv("MAX_RUNNER_TOKENS", raising=False)
    assert adv.max_runner_tokens() == adv.MAX_RUNNER_TOKENS == 1536


def test_max_runner_tokens_env(monkeypatch):
    monkeypatch.setenv("MAX_RUNNER_TOKENS", "2048")
    assert adv.max_runner_tokens() == 2048


def test_gemini_max_output_tokens_default(monkeypatch):
    monkeypatch.delenv("GEMINI_MAX_OUTPUT_TOKENS", raising=False)
    assert adv._gemini_max_output_tokens() == 4096


def test_gemini_thinking_config_25_vs_20(monkeypatch):
    monkeypatch.delenv("GEMINI_THINKING_BUDGET", raising=False)
    monkeypatch.setenv("GEMINI_MODEL", "gemini-2.5-flash")
    assert adv._gemini_thinking_config() == {"thinkingBudget": 0}
    monkeypatch.setenv("GEMINI_MODEL", "gemini-2.0-flash")
    assert adv._gemini_thinking_config() is None
    monkeypatch.setenv("GEMINI_THINKING_BUDGET", "omit")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-2.5-flash")
    assert adv._gemini_thinking_config() is None


def test_log_gemini_response_smoke(capsys, monkeypatch):
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    raw = {
        "modelVersion": "gemini-2.5-flash",
        "usageMetadata": {
            "promptTokenCount": 100,
            "candidatesTokenCount": 50,
            "totalTokenCount": 200,
            "thoughtsTokenCount": 10,
        },
        "candidates": [{"finishReason": "STOP", "content": {"parts": [{"text": "x"}]}}],
    }
    adv._log_gemini_response(
        raw,
        "## Summary\n\nShort body.",
        lane="personal",
        week="2026-W99",
        prompt_chars=500,
        context_chars=400,
    )
    out = capsys.readouterr().out
    assert "[gemini-advisory]" in out
    assert "finishReason" in out
    assert "thoughtsTokenCount=10" in out


def test_gemini_api_key_brand_only_generic(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY_PERSONAL", raising=False)
    assert adv._gemini_api_key("brand") == ""
    monkeypatch.setenv("GEMINI_API_KEY", "brand-key")
    assert adv._gemini_api_key("brand") == "brand-key"


def test_gemini_api_key_personal_prefers_personal_secret(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setenv("GEMINI_API_KEY_PERSONAL", "personal-key")
    assert adv._gemini_api_key("personal") == "personal-key"
    monkeypatch.setenv("GEMINI_API_KEY", "override")
    assert adv._gemini_api_key("personal") == "override"
