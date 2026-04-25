# Agent advisory — Gemini (API) (personal, 2026-W17)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of personal channel analytics reports and suggestions for Week 17, 2026. This analysis will summarize the current performance, highlight key insights from the data, and propose experiments based on the available metrics, while acknowledging any limitations or blocked actions.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W17-personal.md` (Personal channel analytics report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W17-personal.md` (Run next — personal advisory)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md` (Run intent — BLOCKED report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Raw suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw analytics data for individual videos)

## Summary

The personal channel tracked 114 videos over the period of March 27 to April 23, 2026, accumulating 684 total views and 2,404 minutes of watch time, with 6 new subscribers. The overall average retention for videos with views is 18.87%, and the average watch time per video is approximately 52.26 minutes.

The planner for this week's run intent was blocked due to no actionable mood increases passing the required thresholds (n≥5 videos, group_views≥200). However, "deep_focus" and "piano_deep_calm" moods were identified as exploratory "lean in" opportunities due to high watch time per video, despite not meeting the full criteria for actionable status. Conversely, these same moods, along with "ceremony," showed lower retention percentages compared to the channel average, indicating a potential disconnect between initial engagement and sustained viewing.

Short-form "warrior" and "sleep" mood videos show exceptionally high retention percentages (e.g., 96.8% for "Find Your Strength" and 83.6% for "sleep_30s_20260124_031441"), but with very low view counts (1-9 views), suggesting these are niche or experimental. Longer-form "deep_focus" and "piano_deep_calm" videos are driving the most views and watch time.

## Risks / caveats

*   **Low View Counts for High Retention Videos:** The top videos by retention have extremely low view counts (1-9 views). This makes their high retention percentages statistically unreliable for generalization.
*   **Planner Blocked:** The system's planner was blocked, meaning no "actionable" suggestions for increasing mood-based content were generated due to insufficient data (specifically, not enough videos or views within certain mood categories to meet the threshold). This limits the confidence in scaling any particular mood.
*   **Confounders:** The `run-next` report explicitly warns against treating bucket-level correlation as proof that generation parameters drove a result when packaging (title, thumbnail, traffic source, seasonality) differed across videos. Without CTR and impressions data (an optional extension not yet implemented for the personal channel), it's harder to understand initial audience engagement.
*   **Thin Data:** Many moods have very few videos or zero views, making it impossible to draw conclusions about their performance.
*   **No Art/Music Style Data:** The `suggestions_personal.json` shows zero total and zero views for all `art_periods`, `music_styles`, and `art_music_combos`, meaning there is no data to analyze these dimensions.

## Insights

1.  **High Watch Time for "deep_focus" and "piano_deep_calm":** Videos categorized under "deep_focus" and "piano_deep_calm" are significantly contributing to total watch time. For example, "Enter Flow State" (deep_focus) has 347 watch minutes from 125 views, and "Calm Anxiety Fast" (piano_deep_calm) has 427 watch minutes from 44 views. These moods appear to resonate with viewers seeking longer-form content for sustained engagement.
2.  **Retention vs. Watch Time Discrepancy:** While "deep_focus" and "piano_deep_calm" lead in watch time, their average retention percentages (15.7% and 11.7% respectively) are below the overall channel average of 18.87%. This suggests that while these videos attract viewers for extended periods, a significant portion of the audience may not watch them to completion.
3.  **Exceptional Short-Form Retention:** Short-duration videos, particularly those with "warrior" and "sleep" moods (e.g., "Find Your Strength" at 96.8% retention for 1 view, "sleep_30s_20260124_031441" at 83.6% for 1 view), demonstrate extremely high retention. This indicates that for very specific, short-term needs, the content is highly effective at holding the few viewers it attracts.
4.  **Speculative: Potential for "Warrior" Mood:** Despite low view counts, the "warrior" mood shows the highest average retention (76.9%) among all moods with views. This suggests that if packaging and discoverability could be improved, this mood might have a highly engaged, albeit niche, audience. The video "Find Your Strength | 30 Seconds Power Dr" explicitly targets a specific need.
5.  **Underperforming "Ceremony" Mood:** The "ceremony" mood shows both low average retention (1.5%) and low watch time per video compared to the channel average. This mood, despite having 11 videos, is not performing well in terms of sustained engagement.

## Experiments or packaging ideas

*   **Focus on "deep_focus" and "piano_deep_calm" for Long-Form Content:**
    *   Create more 1-hour+ videos in these moods, as they are proven watch-time drivers.
    *   **Experiment:** Test different intros/outros or visualizers for these long-form videos to see if retention can be improved, given their current lower-than-average retention rates.
*   **Explore Short-Form "Warrior" Content:**
    *   Produce a small batch (e.g., 3-5) of new 30-second "warrior" mood videos, focusing on strong, actionable titles like "Find Your Strength" to see if the high retention can be replicated with slightly more views.
    *   **Experiment:** Test different thumbnail styles for "warrior" content, perhaps using more dynamic or energetic imagery, to improve initial click-through.
*   **Re-evaluate "Ceremony" Mood:**
    *   **Experiment:** For existing "ceremony" videos, try updating titles and descriptions to clarify their purpose or target audience, as current performance is very low.
    *   Consider a temporary deprioritization of new "ceremony" content until more insights can be gathered or a specific use case is identified.
*   **Analyze Retention Drop-offs:**
    *   While not directly supported by the current data, the discrepancy between high watch time and lower retention for "deep_focus" and "piano_deep_calm" suggests analyzing where viewers drop off in these longer videos (e.g., at specific transitions or repetitive sections) if more granular data becomes available.
*   **Cross-Reference with Brand Metrics (Manual):**
    *   Manually compare the performance of "deep_focus" and "piano_deep_calm" on the personal channel with any available brand reports (`data/reports/2026-W15.md`) to see if similar trends exist across channels, which could validate these moods as strong performers.
