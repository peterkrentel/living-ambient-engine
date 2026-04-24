# Agent advisory — Gemini (API) (personal, 2026-W17)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of personal channel analytics reports, run intent, and suggestions for Week 17, 2026. This analysis will summarize the channel's performance, identify potential risks, and extract insights to inform future content strategy, focusing on moods and watch time.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W17-personal.md` (Personal channel analytics report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W17-personal.md` (Run next — personal advisory)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md` (Run intent — BLOCKED)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Personal channel suggestions)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw personal channel analytics data)

## Summary

The personal YouTube channel tracked 114 videos over the period of March 27 to April 23, 2026, accumulating 684 total views and 2,404 minutes of watch time, gaining 6 subscribers. The overall average retention for videos with views is 18.87%, and the average watch time per video is approximately 52.26 minutes. While no mood categories met the "actionable" threshold for an increase this week (requiring at least 5 videos and 200 group views), "deep_focus" and "piano_deep_calm" moods showed exploratory positive trends in watch time per video, despite also showing exploratory negative trends in retention percentage compared to the channel average. "Ceremony" mood showed exploratory negative trends in both retention and watch time.

## Risks / caveats

*   **Limited Actionable Insights:** The planner was blocked this week because no mood increases met the defined actionable thresholds (n≥5 videos, group_views≥200). This means current suggestions are exploratory and should be treated with caution.
*   **Confounders & Packaging:** The `run-next` report explicitly states that CTR, impressions, and retention are often influenced by title, thumbnail, traffic source, and seasonality, not solely by mood or art-period labels. Correlations observed at the bucket level do not prove that generation parameters caused the outcome if packaging differed.
*   **Thin Data for Some Moods:** Many mood categories have very few videos with views (e.g., "sleep" has 1 video with views out of 9 total, "trance" has 3 out of 10), making it difficult to draw robust conclusions from their performance.
*   **Brand vs. Personal Data:** The report advises comparing retention and watch time against brand weekly reports when cross-analyzing, but the brand data (`data/suggestions.json`) is not merged into the personal correlate, requiring deliberate comparison.

## Insights

1.  **Deep Focus and Piano Deep Calm Drive Watch Time:** The moods "deep_focus" and "piano_deep_calm" are exploratory indicators of high watch time, exceeding the channel average by approximately 103.4 minutes and 124.9 minutes per video, respectively. This suggests that content designed for intense concentration or profound calm resonates well with viewers seeking longer engagement, despite potentially lower retention percentages.
2.  **Retention vs. Watch Time Discrepancy:** While "deep_focus" and "piano_deep_calm" show strong watch time, they also exhibit exploratory lower retention percentages (down 14.5% and 9.7% respectively) compared to the channel average. This could imply that while these videos capture initial interest, some viewers might not complete them, but those who do watch for significant durations. This might be typical for longer-form ambient content where viewers drop in and out.
3.  **Short-Form Content Shows High Retention:** The top 5 videos by retention are all very short (30 seconds or 10 seconds), with "Find Your Strength" (warrior mood) achieving 96.8% retention and "sleep_30s" achieving 83.6%. While these videos have only 1 view each (except for one warrior video with 9 views), they demonstrate that very short, targeted content can hold attention effectively.
4.  **Ceremony Mood Underperforms:** The "ceremony" mood shows exploratory underperformance in both retention (down 16.6% vs. channel avg) and watch time (down 12.3 minutes per video vs. channel avg). This suggests that content categorized under "ceremony" might not be as engaging or relevant to the current audience.
5.  **Speculative: Long-Form Deep Focus and Piano Calm are Key:** The top-performing videos by views, "Enter Flow State" (deep_focus, 347 views, 125 min watch time) and "Calm Anxiety Fast" (piano_deep_calm, 44 views, 427 min watch time; and another instance with 30 views, 173 min watch time), are both long-form (1 hour) and align with the "deep_focus" and "piano_deep_calm" moods. This reinforces the idea that these moods, when presented in longer formats, are effective at generating significant watch time, even if individual video retention percentages might not be the highest.

## Experiments or packaging ideas

*   **Focus on Long-Form Deep Focus & Piano Deep Calm:**
    *   Create more 1-2 hour videos in the "deep_focus" and "piano_deep_calm" moods, leveraging titles that clearly communicate their purpose (e.g., "Zero Distraction," "Deep Piano Release").
    *   Experiment with different titles and thumbnails for these moods to see if CTR and initial engagement can be improved, potentially boosting overall retention.
*   **Analyze Short-Form High Retention:**
    *   Investigate the specific characteristics (sound design, visual elements) of the short videos with extremely high retention (e.g., "Find Your Strength," "sleep_30s").
    *   Consider if elements from these highly retained short clips could be incorporated into longer videos or used as promotional material.
*   **Re-evaluate Ceremony Content:**
    *   For future "ceremony" content, consider adjusting the mood's characteristics or packaging to improve engagement, or deprioritize this mood if performance doesn't improve.
*   **A/B Test Titles for Watch Time vs. Retention:**
    *   Run experiments with titles that emphasize either "deep focus" (for watch time) or "quick relief" (for retention on shorter videos) to understand audience intent better.
*   **Cross-Reference with Brand Data:**
    *   Manually compare the performance of "deep_focus" and "piano_deep_calm" on the personal channel with their performance on the brand channel (using `data/reports/2026-W15.md` and `data/suggestions.json`) to identify any consistent trends or divergences.
