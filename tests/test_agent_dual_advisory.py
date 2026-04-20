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


def test_runner_bundle_stays_within_ctx_budget():
    """Lean runner bundle must stay under RUNNER_BUNDLE_MAX_CHARS (missing files = small)."""
    b = adv.build_runner_bundle("personal", "2099-W99")
    assert len(b) <= adv.RUNNER_BUNDLE_MAX_CHARS + 200


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
