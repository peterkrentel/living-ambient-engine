# Run intent — BLOCKED

Generated: 2026-04-25T00:42:41.911927+00:00

**No actionable mood increases** in `data/suggestions_personal.json` passed the planner gate.

- Require `type=mood`, `action=increase`, `actionable=true` (n≥5, group_views≥200).

**Exploratory / non-actionable mood rows (sample):**
- Mood 'piano_deep_calm': not actionable (n=6, views=182, need n≥5 and views≥200).
- Mood 'deep_focus': not actionable (n=3, views=223, need n≥5 and views≥200).

**Smoke / dev:** re-run with `--force-moods trance,sleep` (or any valid keys) to emit `data/run_intent_personal.json` without using suggestions.

---
*Produced by `scripts/plan_run_intent.py`.*
