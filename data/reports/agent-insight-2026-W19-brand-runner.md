# Agent advisory — Runner GGUF (CPU) (brand, 2026-W19)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
## What I reviewed
- **Channel totals JSON**: `analytics_totals`
- **Run-next digest snapshot**: `run-next digest`
- **Run-next tail actionable**: `run-next tail`
- **Weekly report excerpt**: `weekly report`
- **Suggestions compact**: `suggestions`
- **Analytics compact top videos + retention slice**: `analytics`

- deterministic facts (computed by script): 867 views, 731 watch minutes, 95 videos with views
## Summary
Channel totals: 867 views, 731 watch minutes, 95 videos with views.
- **Total videos tracked**: 354
- **Videos with analytics**: 354
- **Total views**: 867
- **Total watch time**: 731 minutes

## Insights
- **Top 5 by Retention**: 252.9% for "30 Seconds to Enter Flow State"
- **Top 5 by Views**: 134 views for "Ambient ancient | 5 Mins | Evolving taiko Soundscape"
- **Performance by M**: 27.22% retention for "Ambient ancient | 5 Mins | Evolving taiko Soundscape"

## Risks
- **No actionable mood increases** in `data/suggestions.json` passed the planner gate

## Next tries
- **Re-run with `--force-moods trance,sleep`** to emit `data/run_intent.json` without using suggestions
