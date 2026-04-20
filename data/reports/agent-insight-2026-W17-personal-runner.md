# Agent advisory — Runner GGUF (CPU) (personal, 2026-W17)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
### What I reviewed — 2–3 sentences naming the kinds of inputs (e.g. run-next, suggestions excerpt, weekly report).

- **run-next:** Personal advisory generated on April 20, 2026, based on suggestions and channel audit.
- **suggestions:** Data from `data/suggestions_personal.json`.
- **weekly report:** Analytics report for April 20, 2026, covering videos from March 23 to April 19.

### Insights — numbered 1–5. Each: one short paragraph. Prefer mood/style/packaging angles when CONTEXT supports them. If an item is not directly supported, start that paragraph with **Speculative:**.

1. **CTR, impressions, and retention:** These metrics often change due to title, thumbnail, traffic source, and seasonality, not because a mood or art-period label "caused" an outcome. Do not treat bucket-level correlation as proof that generation parameters drove a result when packaging differed across videos. Correlation addresses patterns in the data, not hidden causes.
2. **Personal snapshot:** The overall average retention is 20.16%, and the average watch time per video is 21 minutes. Videos analyzed are 22 with views out of 108 total.
3. **Evidence:** The evidence paths include suggestions and channel audit. The channel audit shows that 76 out of 108 generations are identity-aligned, with 30 aligning with the brand.
4. **Audit overview:** The videos analyzed are 108, and the latest brand markdown report is `data/reports/2026-W15.md`. The not merged into personal correlate is `data/suggestions.json`.
5. **Brand lane:** The videos in the analytics file are 338, and the latest brand markdown report is `data/reports/2026-W15.md`.

### Risks — short bullets (thin data, confounders, contradictions in CONTEXT).

- **CTR, impressions, and retention:** These metrics often change due to title, thumbnail, traffic source, and seasonality, not because a mood or art-period label "caused" an outcome. Do not treat bucket-level correlation as proof that generation parameters drove a result when packaging differed across videos. Correlation addresses patterns in the data, not hidden causes.
- **Personal snapshot:** The overall average retention is 20.16%, and the average watch time per video
