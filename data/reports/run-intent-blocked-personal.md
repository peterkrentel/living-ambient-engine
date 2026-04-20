# Run intent — BLOCKED

Generated: 2026-04-20T14:26:53.936545+00:00

**No actionable mood increases** in `data/suggestions_personal.json` passed the planner gate.

- Require `type=mood`, `action=increase`, `actionable=true` (n≥5, group_views≥200).

There were no qualifying mood suggestion rows at all.

**Smoke / dev:** re-run with `--force-moods trance,sleep` (or any valid keys) to emit `data/run_intent_personal.json` without using suggestions.

---
*Produced by `scripts/plan_run_intent.py`.*
