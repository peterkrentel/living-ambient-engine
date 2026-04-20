# Run next — personal advisory (2026-W17)

Generated (report): 2026-04-20T12:56:42.520037+00:00
**Correlate bundle `generated_at`:** 2026-04-20T12:56:42.284596Z

## How to read this

This file is **machine-assembled** from `data/suggestions_personal.json` and the **personal** channel audit (`audit-2026-W17-personal.md`).  It is **not** causal advice — see *Packaging & confounders* below.

### Packaging & confounders

**CTR, impressions, and retention** often move because of **title, thumbnail, traffic source, and seasonality** — not because a mood or art-period label “caused” an outcome. Do **not** treat bucket-level correlation as proof that generation **parameters** drove a result when **packaging** differed across videos. Correlation addresses **patterns in the data**, not hidden causes. (Spec: [`docs/spec/AGENT.md`](../../docs/spec/AGENT.md) § *Confounders & packaging*.)

## Personal snapshot (this run)

- **Overall avg retention:** 20.16%
- **Overall avg watch min / video (window):** 21.000
- **Videos analyzed:** 22 with views / 108 total

## Evidence (paths)

- **Suggestions:** `data/suggestions_personal.json`
- **Channel audit:** `data/reports/audit-2026-W17-personal.md`

## Actionable (correlate gates passed)

_None this week — all rows are exploratory or below actionable thresholds._

## Exploratory — lean in (low n / views)

_No exploratory "increase" rows._

## Exploratory — tread carefully (underperformers)

_No exploratory "reduce" rows._

## Audit — overview excerpt (personal)

- **Videos in analytics:** 108
- **generations.json join (any ledger row):** 76 / 108 (70.4%)
- **generations.json join (identity-aligned):** 30 / 108 (27.8%)
  - *Identity-aligned uses optional ledger `channel`, else infers from `workflow` (e.g. `Content Factory (Brand)`). Rows with neither still count only toward “any”.*
  - *Historic uploads may lack rows until logged by the upload pipeline.*

## Brand lane (cross-read only)

- `data/analytics.json` — **338** videos in snapshot; `fetched_at`: 2026-04-19T02:31:56.644105+00:00
- **Latest brand markdown report:** `data/reports/2026-W15.md`
- **Not merged** into personal correlate — `data/suggestions.json` remains the **brand** bundle; compare lanes deliberately ([`docs/PERSONAL_ANALYTICS.md`](../../docs/PERSONAL_ANALYTICS.md)).

## Production hooks (manual)

- **Planner blocked** — see `data/reports/run-intent-blocked-personal.md` for this week's gate reason.
- **Batch strategy reminder:** before scaling one lever, skim mood vs algorithm batch intent in [`piano-batch.yml`](../../.github/workflows/piano-batch.yml) (personal cross-read there).

---

*Produced by `scripts/run_next_report.py` (deterministic v0; no LLM, no `batch_generate`).*
