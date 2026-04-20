# Run next — advisory (2026-W17)

Generated (report): 2026-04-20T23:24:20.503965+00:00
**Correlate bundle `generated_at`:** 2026-04-20T23:24:20.200546Z

## How to read this

This file is **machine-assembled** from `data/suggestions.json` and the **brand** channel audit (`audit-2026-W17.md`).  It is **not** causal advice — see *Packaging & confounders* below.

### Packaging & confounders

**CTR, impressions, and retention** often move because of **title, thumbnail, traffic source, and seasonality** — not because a mood or art-period label “caused” an outcome. Do **not** treat bucket-level correlation as proof that generation **parameters** drove a result when **packaging** differed across videos. Correlation addresses **patterns in the data**, not hidden causes. (Spec: [`docs/spec/AGENT.md`](../../docs/spec/AGENT.md) § *Confounders & packaging*.)

## Brand snapshot (this run)

- **Overall avg retention:** 17.82%
- **Overall avg watch min / video (window):** 6.760
- **Videos analyzed:** 121 with views / 346 total

## Evidence (paths)

- **Suggestions:** `data/suggestions.json`
- **Channel audit:** `data/reports/audit-2026-W17.md`

## Actionable (correlate gates passed)

_None this week — all rows are exploratory or below actionable thresholds._

## Exploratory — lean in (low n / views)

_No exploratory "increase" rows._

## Exploratory — tread carefully (underperformers)

↓ `music_style` / `none` (retention %) — -9.5% vs channel avg (n=3, views=164, exploratory) — `suggestions[0]`

## Audit — overview excerpt (brand)

- **Videos in analytics:** 346
- **generations.json join (any ledger row):** 54 / 346 (15.6%)
- **generations.json join (identity-aligned):** 40 / 346 (11.6%)
  - *Identity-aligned uses optional ledger `channel`, else infers from `workflow` (e.g. `Content Factory (Brand)`). Rows with neither still count only toward “any”.*
  - *Historic uploads may lack rows until logged by the upload pipeline.*

## Personal lane (context only)

- `data/analytics_personal.json` — **108** videos in snapshot; `fetched_at`: 2026-04-20T21:26:35.401678+00:00
- **Latest personal markdown report:** `data/reports/audit-2026-W16-personal.md`
- **Not merged** into brand `suggestions.json` / correlate — use for cross-read only ([`docs/PERSONAL_ANALYTICS.md`](../../docs/PERSONAL_ANALYTICS.md)).

## Production hooks (manual)

- **Planner blocked** — see `data/reports/run-intent-blocked.md` for this week's gate reason.
- **Batch strategy reminder:** before scaling one lever, skim mood vs algorithm batch intent in [`piano-batch.yml`](../../.github/workflows/piano-batch.yml) (personal cross-read there).

---

*Produced by `scripts/run_next_report.py` (deterministic v0; no LLM, no `batch_generate`).*
