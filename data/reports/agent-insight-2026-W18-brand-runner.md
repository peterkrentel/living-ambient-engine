# Agent advisory — Runner GGUF (CPU) (brand, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
## What I reviewed
- **Channel totals JSON**: 354 videos, 1223 views, 855 minutes watched, 124 videos with views.
- **Run-next digest**: 24.84% overall avg retention, 6.895 avg watch time per video.
- **Run-next tail**: No actionable mood increases, all rows are exploratory or below actionable thresholds.

## Summary
- **Analytics window**: 2026-03-31 to 2026-04-27.
- **Total videos tracked**: 354.
- **Videos with analytics**: 353.

## Totals
- **Total views**: 1,223.
- **Total watch time**: 855 minutes.
- **Subscribers gained**: 4.

## Top 5 by Retention
| Video | Mood | Retention % | Views |
|-------|------|-------------|-------|
| 30 Seconds to Enter Flow State | micro_focus_lock | 559.0% | 2 |
| Ambient medieval · 5 Mins · Evolving bam | art_creator | 99.7% | 1 |
| Ambient impressionist · 5 Mins · Evolvin | art_creator | 99.7% | 1 |
| Let Go of Stress · 30 Seconds Soft Piano | piano_relax | 97.1% | 1 |
| 10 Seconds to Drop Inward | micro_drop_inward | 91.8% | 1 |

## Top 5 by Views
| Video | Mood | Views | Watch Time (min) |
|-------|------|-------|------------------|
| Ambient ancient · 5 Mins · Evolving taik | art_creator | 237 | 161 |
| Ambient contemporary · 5 Mins · Evolving | art_creator | 105 | 51 |
| Ambient future · 5 Mins · Evolving none | art_creator | 93 | 49 |
| Ambient baroque · 5 Mins · Evolving game | art_creator | 88 | 52 |
| Ambient ancient · 5 Mins · Evolving kuku | art_creator | 81 | 41 |

## Performance by Mood
| Mood | Videos | Total Views | Avg Retention |
|------|--------|-------------|---------------|
| art_creator | 230 | 1,125 | 17.9% |
| trance | 10 | 27 | 10.5% |
| sleep | 14 | 23 | 10.8% |
| chill | 11 | 9 | 36.8% |
| micro_relief_exhale | 1 | 6 | 14.2% |
| study | 10 | 4 | 28.6% |
| forest_morning | 6 | 4 | 17.0% |
| fireplace | 5 | 3 | 0.3% |
| micro_overthink_b | 1 | 3 | 60.5% |
|

## Insights
1. **Top 5 by Retention**: Videos with high retention rates include "Ambient ancient · 5 Mins · Evolving taik" and "Ambient medieval · 5 Mins · Evolving gamelan Soundscape".
2. **Top 5 by Views**: Videos with high view counts include "Ambient ancient · 5 Mins · Evolving taik" and "Ambient contemporary · 5 Mins · Evolving burundi Soundscape".
3. **Performance by Mood**: The art creator mood has the highest retention rate at 17.9%, followed by trance at 10.5%.
4. **Chill Mood**: Videos with "Chill" mood have the highest average retention rate at 36.8%.
5. **Forest Morning Mood**: Videos with "Forest Morning" mood have the lowest average retention rate at 17.0%.

## Risks
1. **No actionable mood increases**: There were no qualifying mood suggestion rows at all.
2. **No actionable mood increases**: No exploratory "increase" rows.

## Next tries
1. **Run intent**: Re-run with `--force-moods trance,sleep` to emit `data/run_intent.json` without using suggestions.
2. **Batch strategy**: Before scaling one lever, skim mood vs algorithm batch intent in `piano-batch.yml` (personal cross-read there).
