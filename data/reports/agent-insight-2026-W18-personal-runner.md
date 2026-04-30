# Agent advisory — Runner GGUF (CPU) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
## What I reviewed
- **Channel totals JSON:** `analytics_totals`
- **Weekly report excerpt:** `weekly report`
- **Run-next digest (snapshot only):** `run-next tail`
- **Run-next tail (actionable → end):** `Actionable (correlate gates passed)`
- **Exploratory — lean in (low n / views):** No exploratory "increase" rows.
- **Exploratory — tread carefully (underperformers):** `ceremony` (21.1% vs channel avg, 3 views, exploratory) and `ceremony` (88.8 min vs channel avg, 3 views, exploratory).
- **Audit — overview excerpt (personal):** `generations.json join (any ledger row):` 82 / 114 (71.9%), `generations.json join (identity-aligned):` 36 / 114 (31.6%).
- **Production hooks (manual):** `data/run_intent_personal.json` present, validate and run via `run-intent-consumer.yml`.
- **Batch strategy reminder:** Before scaling one lever, skim mood vs algorithm batch intent in `piano-batch.yml`.

- deterministic facts (computed by script): 819 views, 5901 watch minutes, 45 videos with views
## Summary
Channel totals: 819 views, 5901 watch minutes, 45 videos with views.
- **Total videos tracked:** 114
- **Videos with analytics:** 114
- **Total views:** 819
- **Total watch time:** 5,901 minutes
- **Subscribers gained:** 4

## Totals
- **Total views:** 819
- **Total watch time:** 5,901 minutes
- **Subscribers gained:** 4

## Top 5 by Retention
| Video | Mood | Retention % | Views |
|-------|------|-------------|-------|
| Find Your Strength · 30 Seconds Power Dr | warrior | 96.8% | 1 |
| Sounds for an Overactive Mind · 30 Seconds Power Dr | deep_focus | 96.8% | 1 |
| sleep_30s_20260124_031441 | sleep | 83.6% | 1 |
| trance_30s_20260124_055344 | trance | 78.3% | 1 |
| Find Your Strength · 30 Seconds Power Dr | warrior | 74.5% | 1 |

## Top 5 by Views
| Video | Mood | Views | Watch Time (min) |
|-------|------|-------|------------------|
| Enter Flow State · 1 Hour Zero Distraction Focus | deep_focus | 121 | 299 |
| Sounds for an Overactive Mind · 1 Hour Evolving Focus Music | deep_focus | 81 | 82 |
| Calm Anxiety Fast · 1 Hour Deep Piano Relief | piano_deep_calm | 65 | 1,114 |
| Ground Yourself Instantly | 1 Hour Deep Ritual Atmosphere | no loops | 61 | 34 |
| Calm Anxiety Fast · 1 Hour Deep Piano Relief | no loops | 55 | 1052 |
| Calm Anxiety Fast · 1 Hour Deep Piano Relief | no loops | 35 | 1034 |

## Insights
- **Top videos by retention:** `Find Your Strength · 30 Seconds Power Dr` and `Sounds for an Overactive Mind · 30 Seconds Power Dr` have high retention (96.8%).
- **Top videos by views:** `Enter Flow State · 1 Hour Zero Distraction Focus` and `Sounds for an Overactive Mind · 1 Hour Evolving Focus Music` have high views (121 and 81, respectively).
- **Mood / `piano_deep_calm`:** Retention decreased by -2.3% compared to the channel average (n=9, views=345), with a medium confidence level.
- **Mood / `ceremony`:** Retention decreased by -21.1% compared to the channel average (n=3, views=110, exploratory), with a low confidence level.

## Risks
- **Underperformers:** `ceremony` (21.1% vs channel avg, 3 views, exploratory) and `ceremony` (88.8 min vs channel avg, 3 views, exploratory).

## Next tries
- **Reduce `ceremony`:** `ceremony` (21.1% vs channel avg, 3 views, exploratory).
- **Increase `piano_deep_calm`:** `piano_deep_calm` (411.9 min vs channel avg, 345 views).
- **Reduce `ceremony`:** `ceremony` (88.8 min vs channel avg, 3 views, exploratory).
- **Reduce `ceremony`:** `ceremony` (88.8 min vs channel avg, 3 views, exploratory).
