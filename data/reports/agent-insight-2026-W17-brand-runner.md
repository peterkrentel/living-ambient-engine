# Agent advisory — Runner GGUF (CPU) (brand, 2026-W17)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
### What I reviewed — 2–3 bullets naming concrete CONTEXT blocks (e.g. run-next, weekly report, suggestions JSON incl. coverage_summary if present, analytics compact).

- **Advisory lane:** `brand` only — CONTEXT uses `YYYY-WW.md` (brand), `suggestions.json`, `analytics.json`. Do not cite personal-channel totals; cross-lane excerpts are omitted here.
- **Run next — advisory (2026-W17):** Generated (report): 2026-04-21T14:04:29.873463+00:00
- **Evidence (paths):** Suggestions: `data/suggestions.json`; Channel audit: `data/reports/audit-2026-W17.md`

### Summary — 2–3 sentences: the main story the metrics tell (thin data is OK to name explicitly).

This run reviewed 350 videos across 350 identities, focusing on brand-specific content. The retention rate was 18.44%, with an average watch time of 6.780 minutes per video. The top 5 videos by retention were all ambient music with titles like "Evolving bam" and "Evolving taiko". The top 5 videos by views were "Evolving taiko" with 305 views and 251 minutes of watch time.

### Insights — numbered 1–5. Each: one short paragraph. Use **at least three distinct numeric facts** copied from CONTEXT (counts, %, averages, views) across these items; every number must appear verbatim in CONTEXT (no rounding invented, no new totals). Prefer mood / art_period / music_style / packaging angles when CONTEXT supports them. If an item is not directly supported, start that paragraph with **Speculative:**.

1. **Brand Snapshot (this run):** The overall average retention rate is 18.44%, and the average watch time per video is 6.780 minutes.
2. **Evidence (paths):** The suggestions JSON file was used to generate the report, and the channel audit provided insights into the videos analyzed.
3. **Actionable (correlate gates passed):** None this week — all rows are exploratory or below actionable thresholds.
4. **Exploratory — lean in (low n / views):** There were no "increase" rows in the exploratory section.
5. **Exploratory — tread carefully (underperformers):** The retention percentage for videos with music style "none" (art_creator) is -10.1% compared to the channel average, indicating a significant underperformance.

### Risks — short bullets (thin data, confounders, contradictions inside CONTEXT).

- **Confounders:** The retention rate could be influenced by factors such as title, thumbnail, traffic source, and seasonality, not just the mood or art period label.
- **Speculative:** The retention percentage for videos with music style "none" (art_creator) is -10.1% compared to the channel average, indicating a significant underperformance.
- **Confusion:** The retention percentage for videos with music style "none" (art_creator) is -10.1% compared to the channel average, indicating a significant underperformance.

### Next tries — bullets: concrete experiments grounded in what CONTEXT shows; no invented KPIs.

- **Tune the retention rate:** Experiment with different titles, thumbnails, or traffic sources to see if they improve retention.
- **Adjust the mood or art period:** Experiment with changing the mood or art period label to see if it improves retention or watch time.
- **Monitor and adjust:** Continuously monitor the retention rate and adjust the mood or art period label based on the results.
