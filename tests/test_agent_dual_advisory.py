"""Tests for scripts/agent_dual_advisory.py."""

from __future__ import annotations

import importlib.util
import json
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
    assert "### deterministic facts (computed by script)" in b
    assert "sum_views_all_videos" in b
    assert "### run-next digest (snapshot only)" in b
    assert "### run-next tail (actionable → end)" in b
    if "## Brand lane (cross-read only)" in rn.read_text(encoding="utf-8", errors="replace"):
        assert "## Brand lane (cross-read only)" not in b


def test_runner_bundle_stays_within_ctx_budget():
    """Lean runner bundle must stay under runner_bundle_max_chars() (missing files = small)."""
    b = adv.build_runner_bundle("personal", "2099-W99")
    assert len(b) <= adv.runner_bundle_max_chars() + 400


def test_runner_bundle_max_chars_env(monkeypatch):
    monkeypatch.setenv("RUNNER_BUNDLE_MAX_CHARS", "6000")
    assert adv.runner_bundle_max_chars() == 6000


def test_llama_n_ctx_env(monkeypatch):
    monkeypatch.setenv("AGENT_LLAMA_N_CTX", "6144")
    assert adv.llama_n_ctx() == 6144


def test_runner_temperature_env(monkeypatch):
    monkeypatch.setenv("AGENT_RUNNER_TEMPERATURE", "0.2")
    assert adv.runner_temperature() == 0.2


def test_runner_verbose_logs_env(monkeypatch):
    assert adv.runner_verbose_logs() is False
    monkeypatch.setenv("AGENT_RUNNER_VERBOSE", "1")
    assert adv.runner_verbose_logs() is True
    monkeypatch.setenv("AGENT_RUNNER_VERBOSE", "false")
    assert adv.runner_verbose_logs() is False


def test_sanitize_runner_prose_noop():
    t, n = adv._sanitize_runner_prose("hello\nworld")
    assert n == 0
    assert t == "hello\nworld"


def test_sanitize_runner_prose_drops_tautology():
    raw = (
        "1. **Retention:** The channel has 24.67%, which is slightly higher than the channel's average of 24.67%.\n"
        "2. **OK:** Real line with 12 and 34 views.\n"
    )
    out, removed = adv._sanitize_runner_prose(raw)
    assert removed == 1
    assert "slightly higher" not in out.lower()
    assert "12" in out and "34" in out


def test_sanitize_runner_prose_keeps_channel_totals_with_retention_tautology():
    """Regression: one line can cite 755/4224/46 and also repeat 22.33 vs 22.33 — must not drop whole line."""
    raw = (
        "## Summary\n"
        "Totals 755 views, 4224 watch minutes, 46 videos; retention 22.33% is slightly lower than 22.33%.\n"
        "## Insights\n"
        "1. ok\n"
    )
    out, removed = adv._sanitize_runner_prose(raw)
    assert removed == 0
    assert "755" in out and "4224" in out and "46" in out
    assert "slightly lower" in out.lower()


def test_sanitize_runner_prose_keeps_line_when_channel_total_plus_two_uniques():
    """<3 distinct parsed numbers but line mentions a deterministic total — do not strip (CI grounding)."""
    raw = "46 videos with views; retention 22.33% is slightly lower than 22.33%.\n"
    totals = (755, 4224, 46)
    out, removed = adv._sanitize_runner_prose(raw, totals)
    assert removed == 0
    assert "46" in out and "slightly lower" in out.lower()


def test_sanitize_runner_prose_drops_two_uniques_tautology_when_no_channel_totals():
    raw = "46 other meaning; retention 22.33% is slightly lower than 22.33%.\n"
    out, removed = adv._sanitize_runner_prose(raw, (999, 8888, 99))
    assert removed == 1
    assert "slightly lower" not in out.lower()


def test_runner_output_is_template_echo_detects_instruction_only():
    raw = (
        "## What I reviewed — **exactly 3** short bullets: name deterministic facts, run-next digest/tail, "
        "and one of (weekly / suggestions compact / analytics compact). No long pasted lists.\n"
        "## Summary — **2–3** sentences only: main story from metrics (thin data is OK to name).\n"
        "## Insights — numbered **1–5**. Each item: **at most 2 sentences**.\n"
        "## Risks — **2–4** short bullets (thin data, confounders); **do not** duplicate the same risk sentence.\n"
        "## Next tries — **2–5** bullets: concrete experiments tied to moods/styles named in CONTEXT.\n"
    )
    assert adv._runner_output_is_template_echo(raw) is True


def test_runner_output_is_template_echo_false_when_has_bullets():
    raw = (
        "## What I reviewed — **exactly 3** short bullets: name deterministic facts, run-next digest/tail, "
        "and one of (weekly / suggestions compact / analytics compact).\n"
        "- deterministic facts\n"
        "- run-next digest/tail\n"
        "- weekly report\n"
        "\n"
        "## Summary\n"
        "Two sentences.\n"
    )
    assert adv._runner_output_is_template_echo(raw) is False


def test_instruction_scaffold_echo_first_line_only():
    raw = (
        "## What I reviewed — **exactly 3** short bullets: name deterministic facts, run-next digest/tail, "
        "and one of (weekly / suggestions compact / analytics compact). No long pasted lists.\n"
        "## Summary — **2–3** sentences only: main story from metrics (thin data is OK to name).\n"
    )
    assert adv._runner_output_is_instruction_scaffold_echo(raw) is True


def test_runner_normalize_h3_to_h2_known_sections():
    raw = (
        "### What I reviewed\n"
        "- a\n"
        "### Summary\n"
        "S.\n"
        "### Insights\n"
        "1. x\n"
        "### Risks\n"
        "- r\n"
        "### Next tries\n"
        "- n\n"
    )
    out, ch = adv._runner_normalize_known_h3_heads_to_h2(raw)
    assert ch is True
    assert "## What I reviewed" in out and "### What I reviewed" not in out
    assert adv._runner_output_schema_valid(out) is True


def test_runner_normalize_h3_does_not_touch_summary_of():
    raw = "### Summary of the week\n\nx\n"
    out, ch = adv._runner_normalize_known_h3_heads_to_h2(raw)
    assert ch is False
    assert out.splitlines() == raw.splitlines()


def test_runner_normalize_h3_does_not_touch_personal_snapshot():
    raw = "### Personal snapshot (this run)\n\n- x\n"
    out, ch = adv._runner_normalize_known_h3_heads_to_h2(raw)
    assert ch is False


def test_runner_output_schema_valid_minimal():
    prose = (
        "## What I reviewed\n"
        "- a\n"
        "## Summary\n"
        "Two sentences here.\n"
        "## Insights\n"
        "1. One\n"
        "## Risks\n"
        "- r\n"
        "## Next tries\n"
        "- n\n"
    )
    assert adv._runner_output_schema_valid(prose) is True


def test_runner_output_schema_invalid_only_h3_insights():
    assert adv._runner_output_schema_valid("### Insights\n\n- x\n") is False


def test_runner_output_schema_invalid_wrong_order():
    prose = (
        "## Summary\n"
        "s\n"
        "## What I reviewed\n"
        "- a\n"
        "## Insights\n"
        "1.\n"
        "## Risks\n"
        "-\n"
        "## Next tries\n"
        "-\n"
    )
    assert adv._runner_output_schema_valid(prose) is False


def test_runner_output_schema_inference_error_body_ok():
    assert adv._runner_output_schema_valid("## Inference error\n\noops.\n") is True


def test_runner_schema_failure_label_ok():
    prose = (
        "## What I reviewed\n"
        "- a\n"
        "## Summary\n"
        "Two sentences here.\n"
        "## Insights\n"
        "1. One\n"
        "## Risks\n"
        "- r\n"
        "## Next tries\n"
        "- n\n"
    )
    assert adv._runner_schema_failure_label(prose) == "ok"


def test_runner_schema_failure_label_missing_next_tries():
    prose = (
        "## What I reviewed\n"
        "- a\n"
        "## Summary\n"
        "s\n"
        "## Insights\n"
        "1.\n"
        "## Risks\n"
        "- r\n"
    )
    assert adv._runner_schema_failure_label(prose) == "missing:## Next tries"


def test_runner_schema_failure_label_wrong_order_reports_first_gap():
    prose = (
        "## Summary\n"
        "s\n"
        "## What I reviewed\n"
        "- a\n"
        "## Insights\n"
        "1.\n"
        "## Risks\n"
        "-\n"
        "## Next tries\n"
        "-\n"
    )
    assert adv._runner_schema_failure_label(prose) == "missing:## Summary"


def test_runner_grounding_slice_ok_requires_nonempty_slice_and_totals():
    totals = (755, 4224, 46)
    assert adv._runner_grounding_slice_ok("## Insights\n\n1. x\n", totals) is False
    minimal = (
        "## What I reviewed\n"
        "- 755 4224 46\n"
        "## Summary\n"
        "Channel 755 views 4224 min 46 vids.\n"
        "## Insights\n"
        "1. a\n"
        "## Risks\n"
        "- r\n"
        "## Next tries\n"
        "- n\n"
    )
    assert adv._runner_grounding_slice_ok(minimal, totals) is True


def test_runner_prose_quotes_channel_totals_ok():
    totals = (755, 4224, 46)
    slice_ok = (
        "## What I reviewed\n"
        "- facts: 755 views, 4224 watch minutes, 46 with views.\n"
        "## Summary\n"
        "Channel totals 755 / 4224 / 46.\n"
    )
    assert adv._runner_prose_quotes_channel_totals(slice_ok, totals) is True


def test_runner_prose_quotes_channel_totals_accepts_comma_thousands():
    totals = (755, 4224, 46)
    slice_ok = (
        "## What I reviewed\n"
        "- facts: 755 views, 4,224 watch minutes, 46 with views.\n"
        "## Summary\n"
        "Totals 755 / 4,224 / 46.\n"
    )
    assert adv._runner_prose_quotes_channel_totals(slice_ok, totals) is True


def test_runner_prose_quotes_channel_totals_rejects_wrong_views():
    totals = (755, 4224, 46)
    slice_bad = (
        "## What I reviewed\n"
        "- facts: 754 views, 4224 watch minutes, 46 with views.\n"
        "## Summary\n"
        "x\n"
    )
    assert adv._runner_prose_quotes_channel_totals(slice_bad, totals) is False


def test_runner_insights_nonduplicate_rejects_copy_paste():
    prose = (
        "## What I reviewed\n"
        "- a\n"
        "## Summary\n"
        "S.\n"
        "## Insights\n"
        "1. Find Your Strength high retention.\n"
        "2. Other.\n"
        "3. Third.\n"
        "4. Find Your Strength high retention.\n"
        "5. Fifth.\n"
        "## Risks\n"
        "- r\n"
        "## Next tries\n"
        "- n\n"
    )
    assert adv._runner_insights_nonduplicate(prose) is False


def test_context_dump_detects_run_next_paste():
    raw = "### Personal snapshot (this run)\n\n- **Overall avg retention:** 20%\n"
    assert adv._runner_output_is_context_dump(raw) is True
    raw2 = "Good advisory.\n\n*Produced by `scripts/run_next_report.py`*\n"
    assert adv._runner_output_is_context_dump(raw2) is True
    assert adv._runner_output_is_context_dump("## Actionable (correlate gates passed)\n\n↓ mood") is True
    assert adv._runner_output_is_context_dump("## Summary\n\nFine prose.") is False


def test_runner_run_next_for_qwen_extracts_snapshot(tmp_path: Path):
    p = tmp_path / "run-next.md"
    p.write_text(
        """# Run next\n\n## Brand snapshot (this run)\n\n- **Overall:** 10%\n\n## Evidence (paths)\n\nx\n\n## Actionable\n\n_None._\n\n## Personal lane (context only)\n\n- cross\n\n## Production hooks (manual)\n\n- hook\n""",
        encoding="utf-8",
    )
    text = adv._runner_run_next_for_qwen(p, "brand")
    assert "Brand snapshot" in text
    assert "10%" in text
    assert "Personal lane" not in text
    assert "hook" in text


def test_runner_facts_block_sums(tmp_path: Path):
    ana = tmp_path / "analytics_personal.json"
    ana.write_text(
        json.dumps(
            {
                "date_range": {"start": "2026-03-27", "end": "2026-04-23"},
                "videos": [
                    {"title": "A", "metrics": {"views": 10, "watch_time_minutes": 5}},
                    {"title": "B", "metrics": {"views": 0, "watch_time_minutes": 0}},
                    {"title": "C", "metrics": {"views": 3, "watch_time_minutes": 12}},
                ],
            }
        ),
        encoding="utf-8",
    )
    sug = tmp_path / "suggestions_personal.json"
    sug.write_text(
        json.dumps({"videos_analyzed": 99, "videos_with_views": 2, "overall_avg_retention": 12.5}),
        encoding="utf-8",
    )
    text = adv._runner_facts_block(ana, sug)
    assert "deterministic facts" in text
    assert "sum_views_all_videos" in text
    data = json.loads(text.split("```json\n", 1)[1].split("\n```", 1)[0])
    assert data["analytics_totals"]["sum_views_all_videos"] == 13
    assert data["analytics_totals"]["sum_watch_time_minutes_all_videos"] == 17
    assert data["analytics_totals"]["count_videos_with_views_gt_0"] == 2
    assert data["suggestions_headline"]["videos_analyzed"] == 99


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


def test_max_runner_tokens_env_ceiling(monkeypatch):
    monkeypatch.setenv("MAX_RUNNER_TOKENS", "99999")
    assert adv.max_runner_tokens() == adv._RUNNER_MAX_OUTPUT_TOKENS_CEILING


class _FakeLlamaTokenize:
    def __init__(self, n_prompt: int) -> None:
        self._n_prompt = n_prompt

    def tokenize(self, data: bytes, add_bos: bool = True, special: bool = False) -> list[int]:
        return [0] * self._n_prompt


def test_runner_effective_max_tokens_uses_room(monkeypatch):
    monkeypatch.setenv("MAX_RUNNER_TOKENS", "4096")
    requested = adv.max_runner_tokens()
    fake = _FakeLlamaTokenize(3400)
    eff = adv._runner_effective_max_tokens(
        fake, prompt="irrelevant", n_ctx_eff=8192, requested=requested
    )
    assert eff == min(requested, 8192 - 3400 - adv._RUNNER_N_CTX_GENERATION_MARGIN)


def test_runner_effective_max_tokens_no_tokenize_returns_requested(monkeypatch):
    monkeypatch.setenv("MAX_RUNNER_TOKENS", "2048")
    requested = adv.max_runner_tokens()
    assert adv._runner_effective_max_tokens(object(), prompt="x", n_ctx_eff=8192, requested=requested) == requested


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
