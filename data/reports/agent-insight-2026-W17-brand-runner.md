# Agent advisory — Runner GGUF (CPU) (brand, 2026-W17)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
## Summary
The analytics for the brand shows a total of 354 videos analyzed, with 123 videos having views. The overall average retention is 24.5%, and the average watch time per video is 7.756 minutes. The brand has gained 4 subscribers over the past week.

## Insights
1. **Retention Analysis**: The brand has a high average retention of 24.5%, indicating that the majority of videos are retained by viewers. The top 5 videos by retention are "30 Seconds to Enter Flow State" with a 559.0% retention and 2 views, and "Ambient medieval" with an 99.7% retention and 1 view.
2. **View Analysis**: The brand has a high average watch time of 7.756 minutes per video, with the top 5 videos by views being "Ambient ancient" with 289 views and 240 minutes, and "Ambient contemporary" with 105 views and 51 minutes.
3. **Mood Analysis**: The brand has a high average retention of 19.0% for videos created by the "art_creator" mood, indicating that this mood is well-received. The "trance" mood has an average retention of 4.9%, and the "sleep" mood has an average retention of 18.6%.

## Risks
1. **Insufficient Mood Suggestions**: There were no qualifying mood suggestion rows at all, which may indicate that the brand is not generating enough mood suggestions to meet the planner gate requirements.
2. **Insufficient Video Views**: The brand has gained only 4 subscribers, which may indicate that the brand is not reaching a sufficient number of viewers to generate meaningful mood suggestions.

## Next Tries
1. **Increase Mood Suggestions**: To increase the number of mood suggestions, the brand should focus on generating mood suggestions for the "art_creator" mood, which has a high average retention.
2. **Increase Video Views**: To increase the number of views, the brand should focus on generating mood suggestions for the "trance" and "sleep" moods, which have lower average retention but still have a high average watch time per video.
