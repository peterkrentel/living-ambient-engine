# Agent advisory — Runner GGUF (CPU) (personal, 2026-W17)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
## What I reviewed — 2–3 bullets naming concrete CONTEXT blocks (e.g. run-next, weekly report, suggestions JSON incl. coverage_summary if present, analytics compact).

- **Run Next Report:** `data/suggestions_personal.json` and `data/reports/audit-2026-W17-personal.md`.
- **Analytics Report:** `data/analytics_personal.json` and `data/analytics.json`.
- **Personal Snapshot:** 28 videos with views out of 114 total videos analyzed.

## Summary — 2–4 sentences: the main story the metrics tell (thin data is OK to name explicitly).

This report focuses on personal YouTube videos, analyzing 114 videos across 28 with views. The retention rate is 16.36%, and the average watch time per video is 30.643 minutes. The mood of the videos is varied, with deep focus, ambient, and ambient relaxation being common.

## Insights — numbered 1–5. Each: one short paragraph. Use **at least three distinct numeric facts** copied from CONTEXT (counts, %, averages, views) across these items; every number must appear verbatim in CONTEXT (no rounding invented, no new totals). Prefer mood / art_period / music_style / packaging angles when CONTEXT supports them. If an item is not directly supported, start that paragraph with **Speculative:**.

1. **Retention Rate:** The average retention rate is 16.36%, indicating that videos tend to retain viewers for about 16.36% of the time they are watched.
2. **Watch Time:** The average watch time per video is 30.643 minutes, suggesting that videos are typically watched for around 30.643 minutes.
3. **Mood Diversity:** The mood of the videos is varied, with common moods including deep focus, ambient, and ambient relaxation.
4. **Identity Alignment:** The identity-aligned generation uses the `channel` ledger if available, inferring from `workflow` if not, and rows with neither ledger still count toward "any".
5. **Actionable Insights:** There are no actionable insights this week, as all rows are exploratory or below actionable thresholds.

## Risks — short bullets (thin data, confounders, contradictions inside CONTEXT).

- **Confounding Factors:** The retention rate is influenced by packaging, title, thumbnail, and traffic source, not by the mood or art-period label.
- **Risks:** The retention rate is not causal but rather reflects patterns in the data, not hidden causes.
- **Confusion:** The mood and art-period labels are not the primary drivers of the retention rate; they are more indicative of the packaging and content.

## Next tries — bullets: concrete experiments grounded in what CONTEXT shows; no invented KPIs.

- **Compare Analytics:** Compare retention and watch time with brand weekly reports to cross-analyze.
- **Focus on Length:** Double down on topics and lengths that cluster with watch time.
- **Extend Fetcher:** Optional: extend the personal fetcher to include CTR, impressions, and other metrics for deeper analysis.
