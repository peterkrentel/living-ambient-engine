# Agent advisory — Runner GGUF (CPU) (brand, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
## What I reviewed
- deterministic facts (computed by script)
- run-next digest + tail
- one other CONTEXT section you used

- deterministic facts (computed by script): 1201 views, 827 watch minutes, 123 videos with views
## Summary
Channel totals: 1201 views, 827 watch minutes, 123 videos with views.
The analytics report for the brand covers the period from 2026-03-31 to 2026-04-27. It includes total views and watch time, as well as insights into video retention and views. The report also highlights top videos by retention and views, and provides a breakdown of performance by mood.

## Insights
1. The overall average retention is 24.52%, and the average watch time per video is 6.724 minutes.
2. The videos analyzed are 123 with views out of 354 total.

## Risks
- There are no actionable mood increases in the suggestions.json file, which could impact the brand's strategy.
- The retention and views metrics may not be accurate due to the analytics API range.

## Next tries
1. Re-run the plan intent with `--force-moods trance,sleep` to emit `data/run_intent.json` without using suggestions.
2. Ensure that the analytics API range is the same when comparing totals in Studio.
