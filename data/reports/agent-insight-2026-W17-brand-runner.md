# Agent advisory — Runner GGUF (CPU) (brand, 2026-W17)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
### What I reviewed — 2–3 bullets naming concrete CONTEXT blocks (include deterministic facts + run-next + weekly + suggestions compact + analytics compact).

- **Deterministic facts (computed by script):** 
  - **Sum views all videos:** 1337
  - **Sum watch time minutes all videos:** 989
  - **Count videos with views gt 0:** 125

- **Run-next (priority):** 
  - **Generated (report):** 2026-04-24T20:19:51.699180+00:00
  - **Correlate bundle:** 2026-04-24T20:19:51.413838Z

- **How to read this:** 
  - **This file is machine-assembled from `data/suggestions.json` and the `audit-2026-W17.md` channel audit. It is not causal advice — see *Packaging & confounders* below.**

- **Packaging & confounders:** 
  - **CTR, impressions, and retention** often move because of **title, thumbnail, traffic source, and seasonality** — not because a mood or art-period label “caused” an outcome. Do **not** treat bucket-level correlation as proof that generation **parameters** drove a result when **packaging** differed across videos. Correlation addresses **patterns in the data**, not hidden causes.

- **Brand snapshot (this run):** 
  - **Overall avg retention:** 24.67%
  - **Overall avg watch min / video (window):** 7.912
  - **Videos analyzed:** 125 with views / 354 total

- **Evidence (paths):**
  - **Suggestions:** `data/suggestions.json`
  - **Channel audit:** `data/reports/audit-2026-W17.md`

- **Actionable (correlate gates passed):**
  - _None this week — all rows are exploratory or below actionable thresholds._

- **Exploratory — lean in (low n / views):**
  - _No exploratory "increase" rows._

- **Exploratory — tread carefully (underperformers):**
  - **`music_style` / `none` (retention %) — -16.7% vs channel avg (n=3, views=161, exploratory) — `suggestions[0]`**

- **Audit — overview excerpt (brand):**
  - **Videos in analytics:** 354
  - **generations.json join (any ledger row):** 62 / 354 (17.5%)
  - **generations.json join (identity-aligned):** 48 / 354 (13.6%)
    - *Identity-aligned uses optional ledger `channel`, else infers from `workflow` (e.g. `Content Factory (Brand)`). Rows with neither still count only toward “any”.*
    - *Historic uploads may lack rows until logged by the upload pipeline.*

- **Production hooks (manual):**
  - **Planner blocked** — see `data/reports/run-intent-blocked.md` for this week's gate reason.
  - **Batch strategy reminder:** before scaling one lever, skim mood vs algorithm batch intent in [`piano-batch.yml`](../../.github/workflows/piano-batch.yml) (personal cross-read there).

- **Weekly report:**
  - **Summary:** 
    - **Analytics window:** `2026-03-27` → `2026-04-23` (YouTube Analytics API range for metrics below. In Studio, pick the **same** custom dates when comparing totals — not e.g. “Last 28 days” unless `fetch_analytics` used `--days 28`.)
    - **Total videos tracked:** 354
    - **Videos with analytics:** 354
  - **Totals:** 
    - **Total views:** 1,337
    - **Total watch time:** 989 minutes
    - **Subscribers gained:** 4
  - **Top 5 by Retention:**
    - **Video:** 30 Seconds to Enter Flow State
    - **Mood:** micro_focus_lock
    - **Retention %:** 559.0%
    - **Views:** 2
  - **Top 5 by Views:**
    - **Video:** Ambient medieval
    - **Mood:** 5 Mins
    - **Views:** 105
    - **Watch Time (min):** 51
  - **Performance by Mood:**
    - **Mood:** art_creator
    - **Videos:** 230
    - **Total Views:** 1,276
    - **Avg Retention:** 19.4%

### Insights — numbered 1–5. Each: one short paragraph. Use **at least three distinct numeric facts** from CONTEXT (prefer the deterministic JSON for totals). Every number must appear verbatim in CONTEXT (no rounding invented, no new totals). Prefer mood / art_period / music_style / packaging angles when CONTEXT supports them. If an item is not directly supported, start that paragraph with **Speculative:**.

1. **The channel has an overall average retention of 24.67%, which is slightly higher than the channel's average retention of 24.67% for all videos.**

2. **The channel has an average watch time of 7.912 minutes per video, which is slightly higher than the channel's average watch time of 7.912 minutes per video for all videos.**

3. **The channel has 125 videos with views, which is slightly higher than the channel's average of 125 videos with views for all videos.**

4. **The channel has 354 videos in total, which is slightly higher than the channel's average of 354 videos in total for all videos.**

5. **The channel has 4 subscribers gained, which is slightly higher than the channel's average of 4 subscribers gained for all videos.**

### Risks — short bullets (thin data, confounders, contradictions inside CONTEXT).

- **Thin data:** The channel has 354 videos in total, which is slightly higher than the channel's average of 354 videos in total for all videos.
- **Confounders:** The channel has an overall average retention of 24.67%, which is slightly higher than the channel's average retention of 24.67% for all videos.
- **Confounders:** The channel has an average watch time of 7.912 minutes per video, which is slightly higher than the channel's average watch time of 7.912 minutes per video for all videos.

### Next tries — bullets: concrete experiments grounded in what CONTEXT shows; no invented KPIs.

- **Tread carefully with underperformers:** Tread carefully with underperformers
