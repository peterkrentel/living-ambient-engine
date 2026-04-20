# Agent advisory — Runner GGUF (CPU) (brand, 2026-W17)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
### What I reviewed — 2–3 bullets naming concrete CONTEXT blocks (e.g. run-next, weekly report, suggestions JSON incl. coverage_summary if present, analytics compact).

- **Run Next Report** — generated on 2026-04-20, correlating bundle `generated_at` with `2026-04-20T23:40:09.076329Z`.
- **Analytics Report - 2026-W17** — summary of 346 videos analyzed, including top retention and view metrics.
- **Brand Snapshot (this run)** — overall average retention of 17.82%, average watch time per video of 6.760 minutes.

### Summary — 2–4 sentences: the main story the metrics tell (thin data is OK to name explicitly).

This report analyzes 346 videos, with an overall average retention of 17.82% and an average watch time per video of 6.760 minutes. The report identifies videos with low retention and underperforming music styles.

### Insights — numbered 1–5. Each: one short paragraph. Use **at least three distinct numeric facts** copied from CONTEXT (counts, %, averages, views) across these items; every number must appear verbatim in CONTEXT (no rounding invented, no new totals). Prefer mood / art_period / music_style / packaging angles when CONTEXT supports them. If an item is not directly supported, start that paragraph with **Speculative:**.

1. **Low retention videos:** 108 videos analyzed, with an average retention of 17.82%. This suggests that low retention videos are common, indicating a need for optimization.
2. **Underperforming music styles:** The music style `none` has a retention percentage of 99.7%, significantly higher than the overall average of 17.82%. This suggests that videos with no specific music style may perform better than others.
3. **Top retention videos:** The top retention videos are all ambient medieval, with an average retention of 99.7%. This indicates that ambient medieval music is particularly effective at retaining viewers.
4. **Top view videos:** The top view videos are all ambient ancient, with an average view of 317 and an average watch time of 260 minutes. This suggests that ambient ancient music is particularly effective at attracting viewers.
5. **Underperforming music styles:** The music style `none` has a retention percentage of 99.7%, significantly higher than the overall average of 17.82%. This suggests that videos with no specific music style may perform better than others.

### Risks — short bullets (thin data, confounders, contradictions inside CONTEXT).

- **Thin data:** The report does not provide specific details on how retention and view metrics were calculated.
- **Confounders:** The retention and view metrics may be influenced by factors such as traffic source and seasonality.
- **Contradictions:** The retention of ambient ancient music is significantly higher than the overall average, which may be due to the specific nature of ambient ancient music rather than a general trend.

### Next tries — bullets: concrete experiments grounded in what CONTEXT shows; no invented KPIs.

- **Optimize low retention videos:** Focus on optimizing videos with low retention to improve overall retention.
- **Identify underperforming music styles:** Investigate the underperforming music styles to understand why they perform poorly and make improvements.
- **Focus on ambient medieval music:** Continue to focus on ambient medieval music as it has a high retention rate and may be a good candidate for optimization.
- **Test ambient ancient music:** Experiment with ambient ancient music to see if it can be optimized further.
