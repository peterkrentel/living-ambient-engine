# Agent advisory — Runner GGUF (CPU) (brand, 2026-W17)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
### Summary

The analytics report for the week shows a total of 354 videos analyzed, with 121 videos having analytics data. The overall average retention is 25.05%, and the average watch time per video is 7.876 minutes. The total views for all videos combined is 1,297, and the total watch time is 953 minutes.

### Insights

1. **Top Retention Videos:** The top videos with the highest retention are "30 Seconds to Enter Flow State" with a retention of 559.0% and 2 views, and "Ambient medieval" with an evolving mood and 99.7% retention, having 105 views.

2. **Top View Videos:** The top videos with the highest number of views are "Ambient ancient" with 287 views and 239 minutes of watch time, and "Ambient contemporary" with 105 views and 51 minutes of watch time.

3. **Performance by Mood:** The mood "art_creator" has the highest retention with 19.1%, followed by "trance" with 4.9%, "sleep" with 18.6%, "chill" with 55.6%, "micro_relief_exhale" with 14.2%, "forest_morning" with 17.0%, "study" with 36.1%, and "micro_wake_spark" with 47.1%.

4. **Actionable Actions:** There were no actionable mood increases in the suggestions.json file, requiring re-running with specific mood suggestions to increase retention.

### Risks

1. **Insufficient Data:** The lack of actionable mood increases in the suggestions.json file may indicate that the current mood suggestions are not effective in increasing retention.

2. **Batch Strategy:** The batch strategy reminder suggests that before scaling one lever, it's important to skim the mood vs. algorithm batch intent in `piano-batch.yml` to ensure that the batch strategy aligns with the intended mood.

### Next Tries

1. **Re-run with Specific Mood Suggestions:** Re-run the run intent with specific mood suggestions to increase retention.

2. **Batch Strategy Review:** Review the batch strategy in `piano-batch.yml` to ensure it aligns with the intended mood and batch intent.

3. **Monitor Retention:** Monitor the retention of videos with specific moods to identify any patterns or issues that may require further investigation.
