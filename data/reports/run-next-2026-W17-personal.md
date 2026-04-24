# Run next — personal advisory (2026-W17)

Generated (report): 2026-04-24T20:17:36.375082+00:00
**Correlate bundle `generated_at`:** 2026-04-24T20:17:36.152369Z

## How to read this

This file is **machine-assembled** from `data/suggestions_personal.json` and the **personal** channel audit (`audit-2026-W17-personal.md`).  It is **not** causal advice — see *Packaging & confounders* below.

### Packaging & confounders

**CTR, impressions, and retention** often move because of **title, thumbnail, traffic source, and seasonality** — not because a mood or art-period label “caused” an outcome. Do **not** treat bucket-level correlation as proof that generation **parameters** drove a result when **packaging** differed across videos. Correlation addresses **patterns in the data**, not hidden causes. (Spec: [`docs/spec/AGENT.md`](../../docs/spec/AGENT.md) § *Confounders & packaging*.)

## Personal snapshot (this run)

- **Overall avg retention:** 18.87%
- **Overall avg watch min / video (window):** 52.261
- **Videos analyzed:** 46 with views / 114 total

## Evidence (paths)

- **Suggestions:** `data/suggestions_personal.json`
- **Channel audit:** `data/reports/audit-2026-W17-personal.md`

## Actionable (correlate gates passed)

_None this week — all rows are exploratory or below actionable thresholds._

## Exploratory — lean in (low n / views)

↑ `mood` / `deep_focus` (watch min / video (window)) — +103.4 min vs channel avg (n=3, views=223, exploratory) — `suggestions[4]`
↑ `mood` / `piano_deep_calm` (watch min / video (window)) — +124.9 min vs channel avg (n=6, views=182, exploratory) — `suggestions[3]`

## Exploratory — tread carefully (underperformers)

↓ `mood` / `deep_focus` (retention %) — -14.5% vs channel avg (n=3, views=223, exploratory) — `suggestions[1]`
↓ `mood` / `piano_deep_calm` (retention %) — -9.7% vs channel avg (n=6, views=182, exploratory) — `suggestions[0]`
↓ `mood` / `ceremony` (retention %) — -16.6% vs channel avg (n=3, views=104, exploratory) — `suggestions[2]`
↓ `mood` / `ceremony` (watch min / video (window)) — -12.3 min vs channel avg (n=3, views=104, exploratory) — `suggestions[5]`

## Audit — overview excerpt (personal)

- **Videos in analytics:** 114
- **generations.json join (any ledger row):** 82 / 114 (71.9%)
- **generations.json join (identity-aligned):** 36 / 114 (31.6%)
  - *Identity-aligned uses optional ledger `channel`, else infers from `workflow` (e.g. `Content Factory (Brand)`). Rows with neither still count only toward “any”.*
  - *Historic uploads may lack rows until logged by the upload pipeline.*

## Brand lane (cross-read only)

- `data/analytics.json` — **350** videos in snapshot; `fetched_at`: 2026-04-21T14:04:29.370852+00:00
- **Latest brand markdown report:** `data/reports/2026-W15.md`
- **Not merged** into personal correlate — `data/suggestions.json` remains the **brand** bundle; compare lanes deliberately ([`docs/PERSONAL_ANALYTICS.md`](../../docs/PERSONAL_ANALYTICS.md)).

## Production hooks (manual)

- **Planner blocked** — see `data/reports/run-intent-blocked-personal.md` for this week's gate reason.
- **Batch strategy reminder:** before scaling one lever, skim mood vs algorithm batch intent in [`piano-batch.yml`](../../.github/workflows/piano-batch.yml) (personal cross-read there).

---

*Produced by `scripts/run_next_report.py` (deterministic v0; no LLM, no `batch_generate`).*
