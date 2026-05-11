# Run next — personal advisory (2026-W20)

Generated (report): 2026-05-11T05:58:40.903975+00:00
**Correlate bundle `generated_at`:** 2026-05-11T05:58:40.625196Z

## How to read this

This file is **machine-assembled** from `data/suggestions_personal.json` and the **personal** channel audit (`audit-2026-W20-personal.md`).  It is **not** causal advice — see *Packaging & confounders* below.

### Packaging & confounders

**CTR, impressions, and retention** often move because of **title, thumbnail, traffic source, and seasonality** — not because a mood or art-period label “caused” an outcome. Do **not** treat bucket-level correlation as proof that generation **parameters** drove a result when **packaging** differed across videos. Correlation addresses **patterns in the data**, not hidden causes. (Spec: [`docs/spec/AGENT.md`](../../docs/spec/AGENT.md) § *Confounders & packaging*.)

## Personal snapshot (this run)

- **Overall avg retention:** 23.14%
- **Overall avg watch min / video (window):** 219.396
- **Videos analyzed:** 53 with views / 118 total

## Evidence (paths)

- **Suggestions:** `data/suggestions_personal.json`
- **Channel audit:** `data/reports/audit-2026-W20-personal.md`

## Actionable (correlate gates passed)

↑ **`mood` / `piano_deep_calm`** (watch min / video (window)) — +607.9 min vs channel avg (n=13, views=853) — `high` — evidence index **`data/suggestions_personal.json` → `suggestions[1]`**

## Exploratory — lean in (low n / views)

_No exploratory "increase" rows._

## Exploratory — tread carefully (underperformers)

↓ `mood` / `ceremony` (retention %) — -20.8% vs channel avg (n=3, views=111, exploratory) — `suggestions[0]`
↓ `mood` / `ceremony` (watch min / video (window)) — -176.4 min vs channel avg (n=3, views=111, exploratory) — `suggestions[2]`

## Audit — overview excerpt (personal)

- **Videos in analytics:** 118
- **generations.json join (any ledger row):** 86 / 118 (72.9%)
- **generations.json join (identity-aligned):** 40 / 118 (33.9%)
  - *Identity-aligned uses optional ledger `channel`, else infers from `workflow` (e.g. `Content Factory (Brand)`). Rows with neither still count only toward “any”.*
  - *Historic uploads may lack rows until logged by the upload pipeline.*

## Brand lane (cross-read only)

- `data/analytics.json` — **354** videos in snapshot; `fetched_at`: 2026-05-10T02:46:32.459421+00:00
- **Latest brand markdown report:** `data/reports/2026-W15.md`
- **Not merged** into personal correlate — `data/suggestions.json` remains the **brand** bundle; compare lanes deliberately ([`docs/PERSONAL_ANALYTICS.md`](../../docs/PERSONAL_ANALYTICS.md)).

## Production hooks (manual)

- **`data/run_intent_personal.json` present** — validate and run via [`run-intent-consumer.yml`](../../.github/workflows/run-intent-consumer.yml) (still **manual** / gated). Set workflow inputs **`intent_path`** = `data/run_intent_personal.json` and **`blocked_report_path`** = `data/reports/run-intent-blocked-personal.md` when dispatching the consumer.
- **Batch strategy reminder:** before scaling one lever, skim mood vs algorithm batch intent in [`piano-batch.yml`](../../.github/workflows/piano-batch.yml) (personal cross-read there).

---

*Produced by `scripts/run_next_report.py` (deterministic v0; no LLM, no `batch_generate`).*
