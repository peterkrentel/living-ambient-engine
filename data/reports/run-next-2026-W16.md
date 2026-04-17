# Run next — advisory (2026-W16)

Generated (report): 2026-04-17T19:35:54.647441+00:00
**Correlate bundle `generated_at`:** 2026-04-17T19:35:54.410566Z

## How to read this

This file is **machine-assembled** from `data/suggestions.json` and the **brand** channel audit (`audit-2026-W16.md`).  It is **not** causal advice — see *Packaging & confounders* below.

### Packaging & confounders

**CTR, impressions, and retention** often move because of **title, thumbnail, traffic source, and seasonality** — not because a mood or art-period label “caused” an outcome. Do **not** treat bucket-level correlation as proof that generation **parameters** drove a result when **packaging** differed across videos. Correlation addresses **patterns in the data**, not hidden causes. (Spec: [`docs/spec/AGENT.md`](../../docs/spec/AGENT.md) § *Confounders & packaging*.)

## Brand snapshot (this run)

- **Overall avg retention:** 11.42%
- **Overall avg watch min / video (window):** 6.838
- **Videos analyzed:** 117 with views / 334 total

## Evidence (paths)

- **Suggestions:** `data/suggestions.json`
- **Channel audit:** `data/reports/audit-2026-W16.md`

## Actionable (correlate gates passed)

_None this week — all rows are exploratory or below actionable thresholds._

## Exploratory — lean in (low n / views)

↑ `art_period` / `contemporary` (retention %) — +3.7% vs channel avg (n=3, views=179, exploratory) — `suggestions[0]`
↑ `music_style` / `heartbeat` (retention %) — +2.7% vs channel avg (n=4, views=113, exploratory) — `suggestions[1]`

## Exploratory — tread carefully (underperformers)

↓ `music_style` / `none` (retention %) — -3.6% vs channel avg (n=3, views=164, exploratory) — `suggestions[3]`
↓ `art_period` / `future` (retention %) — -2.5% vs channel avg (n=3, views=118, exploratory) — `suggestions[2]`

## Audit — overview excerpt (brand)

- **Videos in analytics:** 334
- **generations.json join (any ledger row):** 42 / 334 (12.6%)
- **generations.json join (identity-aligned):** 28 / 334 (8.4%)
  - *Identity-aligned uses optional ledger `channel`, else infers from `workflow` (e.g. `Content Factory (Brand)`). Rows with neither still count only toward “any”.*
  - *Historic uploads may lack rows until logged by the upload pipeline.*

## Personal lane (context only)

- `data/analytics_personal.json` — **90** videos in snapshot; `fetched_at`: 2026-04-17T19:18:21.645531+00:00
- **Latest personal markdown report:** `data/reports/audit-2026-W16-personal.md`
- **Not merged** into brand `suggestions.json` / correlate — use for cross-read only ([`docs/PERSONAL_ANALYTICS.md`](../../docs/PERSONAL_ANALYTICS.md)).

## Production hooks (manual)

- **Planner blocked** — see `data/reports/run-intent-blocked.md` for this week's gate reason.
- **Batch strategy reminder:** before scaling one lever, skim mood vs algorithm batch intent in [`piano-batch.yml`](../../.github/workflows/piano-batch.yml) (personal cross-read there).

---

*Produced by `scripts/run_next_report.py` (deterministic v0; no LLM, no `batch_generate`).*
