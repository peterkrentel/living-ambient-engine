# Agent advisory — Runner GGUF (CPU) (personal, 2026-W17)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
## What I reviewed — 2–3 bullets naming concrete CONTEXT blocks (e.g. run-next, weekly report, suggestions JSON incl. coverage_summary if present, analytics compact).

- **Advisory lane:** `personal` only — CONTEXT uses `*-personal.md`, `suggestions_personal.json`, `analytics_personal.json`. Do not cite brand-channel totals; cross-lane excerpts are omitted here.
- **Run next — personal advisory (2026-W17):** Generated (report): 2026-04-21T14:04:13.471254+00:00
- **How to read this:** This file is **machine-assembled** from `data/suggestions_personal.json` and the **personal** channel audit (`audit-2026-W17-personal.md`). It is **not** causal advice — see *Packaging & confounders* below.

## Summary — 2–4 sentences: the main story the metrics tell (thin data is OK to name explicitly).

This advisory report analyzes personal YouTube videos from March 24 to April 20, 2026, focusing on retention, watch time, and mood-based recommendations. The report includes insights on video performance, retention rates, and viewer engagement.

## Insights — numbered 1–5. Each: one short paragraph. Use **at least three distinct numeric facts** copied from CONTEXT (counts, %, averages, views) across these items; every number must appear verbatim in CONTEXT (no rounding invented, no new totals). Prefer mood / art_period / music_style / packaging angles when CONTEXT supports them. If an item is not directly supported, start that paragraph with **Speculative:**.

1. **Overall avg retention:** 16.36% — This indicates that, on average, videos retained 16.36% of their viewers.
2. **Overall avg watch min / video (window):** 30.643 — The average time viewers spent watching a video in the window was 30.643 minutes.
3. **Videos analyzed:** 28 with views / 114 total — The report analyzed 28 videos with views and 114 total videos.

4. **Top 5 by Retention:** Let Go of Stress, Sounds for an Overactive Mind, warrior_10s_20260124_160306, Let Go of Stress, Deep Calm Piano Atmos — These videos have high retention rates, with Let Go of Stress having the highest retention rate at 99.2%.
5. **Top 5 by Views:** Enter Flow State, Sounds for an Overactive Mind, Calm Anxiety Fast, Calm Anxiety Fast, Fall Asleep to Gentle Rain — These videos have high viewer engagement, with Enter Flow State having the highest number of views at 116.

## Risks — short bullets (thin data, confounders, contradictions inside CONTEXT).

- **CTR, impressions, and retention:** Often move due to title, thumbnail, traffic source, and seasonality, not because a mood or art-period label “caused” an outcome.
- **Packaging & confounders:** Correlation addresses **patterns in the data**, not hidden causes. Bucket-level correlation should not be treated as proof that generation parameters drove a result when packaging differed across videos.

## Next tries — bullets: concrete experiments grounded in what CONTEXT shows; no invented KPIs.

- **Compare retention and watch time vs brand weekly reports when cross-analyzing:** This can help identify trends and patterns specific to personal videos.
- **Double down on topics and lengths that cluster with watch time:** Focus on videos with high viewer engagement and longer watch times.
- **Optional: extend the personal fetcher (CTR, impressions) per docs/PERSONAL_ANALYTICS.md:** This can help improve video performance and engagement.
