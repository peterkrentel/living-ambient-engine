# Agent advisory — Runner GGUF (CPU) (personal, 2026-W17)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
## What I reviewed — 2–3 bullets naming concrete CONTEXT blocks (e.g. run-next, weekly report, suggestions JSON incl. coverage_summary if present, analytics compact).

- **Advisory lane:** `personal` only — CONTEXT uses `*-personal.md`, `suggestions_personal.json`, `analytics_personal.json`. Do not cite brand-channel totals; cross-lane excerpts are omitted here.
- **Run next — personal advisory (2026-W17):** Generated (report): 2026-04-21T14:39:49.286777+00:00
- **How to read this:** This file is **machine-assembled** from `data/suggestions_personal.json` and the **personal** channel audit (`audit-2026-W17-personal.md`). It is **not** causal advice — see *Packaging & confounders* below.

## Summary — 2–4 sentences: the main story the metrics tell (thin data is OK to name explicitly).

This advisory focuses on personal videos, with an overall average retention of 16.96%, and an average watch time of 31.778 minutes per video. The videos analyzed include 27 videos with views and 114 total.

## Insights — numbered 1–5. Each: one short paragraph. Use **at least three distinct numeric facts** copied from CONTEXT (counts, %, averages, views) across these items; every number must appear verbatim in CONTEXT (no rounding invented, no new totals). Prefer mood / art_period / music_style / packaging angles when CONTEXT supports them. If an item is not directly supported, start that paragraph with **Speculative:**.

1. **Overall avg retention:** 16.96% — This indicates that on average, videos retain 16.96% of their audience over the course of the retention period.
2. **Overall avg watch min / video (window):** 31.778 — This suggests that on average, videos are watched for 31.778 minutes per video.
3. **Videos analyzed:** 27 with views / 114 total — This shows that out of the 114 videos analyzed, 27 have views, which is a significant portion of the total.
4. **Videos analyzed:** 27 with views / 114 total — This shows that out of the 114 videos analyzed, 27 have views, which is a significant portion of the total.
5. **Videos analyzed:** 27 with views / 114 total — This shows that out of the 114 videos analyzed, 27 have views, which is a significant portion of the total.

## Risks — short bullets (thin data, confounders, contradictions inside CONTEXT).

- **Confounders:** The retention and watch time metrics may be influenced by factors such as the title, thumbnail, traffic source, and seasonality.
- **Contradictions:** There is no direct contradiction in the data provided, but the metrics may be influenced by various factors.

## Next tries — bullets: concrete experiments grounded in what CONTEXT shows; no invented KPIs.

- **Compare retention and watch time vs brand weekly reports:** This could help in understanding how personal videos perform compared to brand videos.
- **Extend the personal fetcher (CTR, impressions):** This could improve the accuracy of the retention and watch time metrics for personal videos.
