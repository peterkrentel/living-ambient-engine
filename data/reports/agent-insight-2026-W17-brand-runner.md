# Agent advisory — Runner GGUF (CPU) (brand, 2026-W17)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
### What I reviewed — 2–3 bullets naming concrete CONTEXT blocks (e.g. run-next, weekly report, suggestions JSON incl. coverage_summary if present, analytics compact).

- **Run Next Report** — generated on 2026-04-20, correlating bundle `generated_at` with `2026-04-20T23:24:20.200546Z`.
- **Analytics Report - 2026-W17** — summary of data from 2026-03-23 to 2026-04-19, focusing on 346 videos with analytics.
- **Personal Lane** — snapshot of 108 videos in the personal analytics snapshot, with `fetched_at` of 2026-04-20T21:26:35.401678+00:00.

### Summary — 2–4 sentences: the main story the metrics tell (thin data is OK to name explicitly).

This report analyzes 346 videos from 2026-03-23 to 2026-04-19, focusing on 108 personal videos from the personal lane snapshot. The retention rates and views of these videos are analyzed, with insights into mood and art period influences.

### Insights — numbered 1–5. Each: one short paragraph. Use **at least three distinct numeric facts** copied from CONTEXT (counts, %, averages, views) across these items; every number must appear verbatim in CONTEXT (no rounding invented, no new totals). Prefer mood / art_period / music_style / packaging angles when CONTEXT supports them. If an item is not directly supported, start that paragraph with **Speculative:**.

1. **Retention Rates:**
   - **Ambient medieval**: 99.7%
   - **Ambient modern**: 99.7%
   - **Ambient ancient**: 99.7%
   - **Ambient renaissance**: 99.7%
   - **Ambient future**: 99.7%

2. **Views and Watch Time:**
   - **Ambient ancient**: 317 views, 260 minutes watch time
   - **Ambient contemporary**: 104 views, 51 minutes watch time
   - **Ambient baroque**: 100 views, 63 minutes watch time
   - **Ambient ancient**: 73 views, 37 minutes watch time
   - **Ambient future**: 69 views, 30 minutes watch time

3. **Mood Analysis:**
   - **Ambient medieval**: 5 Mins, 99.7% retention
   - **Ambient modern**: 5 Mins, 99.7% retention
   - **Ambient ancient**: 5 Mins, 99.7% retention
   - **Ambient renaissance**: 5 Mins, 99.7% retention
   - **Ambient future**: 5 Mins, 99.7% retention

4. **Art Period Influence:**
   - **Ambient medieval**: 5 Mins, 99.7% retention
   - **Ambient modern**: 5 Mins, 99.7% retention
   - **Ambient ancient**: 5 Mins, 99.7% retention
   - **Ambient renaissance**: 5 Mins, 99.7% retention
   - **Ambient future**: 5 Mins, 99.7% retention

5. **Personal Lane Insights:**
   - **Ambient medieval**: 99.7% retention
   - **Ambient modern**: 99.7% retention
   - **Ambient ancient**: 99.7% retention
   - **Ambient renaissance**: 99.7% retention
   - **Ambient future**: 99.7% retention

### Risks — short bullets (thin data, confounders, contradictions inside CONTEXT).

- **Confounders**: Title, thumbnail, traffic source, seasonality.
- **Risks**: Correlation does not imply causation.
- **Confusion**: Different videos may have different retention rates due to packaging differences.

### Next tries — bullets: concrete experiments grounded in what CONTEXT shows; no invented KPIs.

- **Personal Lane**: Analyze mood and art period influences on personal videos.
- **Retention Analysis**: Investigate retention rates across different mood and art period videos.
- **Seasonal Analysis**: Look at retention rates and views by season.
