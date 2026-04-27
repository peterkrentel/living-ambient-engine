# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of personal channel analytics reports and suggestions for Week 18, 2026. This analysis focuses on identifying patterns in video performance, particularly concerning mood categories, to inform future content strategy for the personal YouTube ambient music channel.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md`: Personal channel analytics report for 2026-W18.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md`: Personal advisory report for 2026-W18, including actionable and exploratory suggestions.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json`: Raw JSON data for personal channel suggestions.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json`: Raw JSON data for personal channel video metrics.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md`: This file was missing, indicating no blocked run intent for the personal channel.

## Summary

The personal channel had 728 total views and 3,730 minutes of watch time, gaining 4 subscribers over the `2026-03-30` to `2026-04-26` period. The overall average retention was 20.22%, and the average watch time per video was approximately 82.89 minutes. "Deep focus" and "piano_deep_calm" moods are driving the most views and watch time, with "Calm Anxiety Fast" videos performing exceptionally well in watch time. Short-form videos (30 seconds) show very high retention percentages but contribute minimally to overall views or watch time. The `ceremony` mood is underperforming in both retention and watch time. There is no data available for `art_periods` or `music_styles` in the `suggestions_personal.json` file.

## Risks / caveats

*   **Confounders & Packaging:** The `run-next` report explicitly states that CTR, impressions, and retention are often influenced by title, thumbnail, traffic source, and seasonality, not solely by mood or art-period labels. Correlations should not be treated as causal proof for generation parameters when packaging differs.
*   **Limited Data for Retention:** The top 5 videos by retention all have only 1 or 2 views, making their high retention percentages potentially misleading due to a very small sample size.
*   **Missing Data:** There is no data for `art_periods` or `music_styles` in the `suggestions_personal.json` file, limiting insights into these dimensions. The `run-intent-blocked-personal.md` file is also missing, so any blocked intents cannot be reviewed.
*   **Personal vs. Brand:** The report clearly distinguishes between personal and brand metrics, emphasizing that they should be compared deliberately and not merged. This analysis focuses solely on the personal channel.
*   **Low `n` for some moods:** Several moods have very few videos or views, making it difficult to draw robust conclusions about their performance. For example, `sleep` has 9 videos but only 1 view, despite high retention.

## Insights

1.  **Deep Focus and Piano Deep Calm Drive Views and Watch Time:** The moods `deep_focus` and `piano_deep_calm` are the clear leaders in terms of total views (239 and 287 respectively) and contribute significantly to watch time. Two "Calm Anxiety Fast" videos (mood: `piano_deep_calm`) alone account for over 1600 minutes of watch time. This suggests a strong audience demand for content targeting focus and deep calm, particularly with a piano sound.
2.  **High Retention in Short-Form Content (with low views):** While the overall average retention is 20.22%, several 30-second videos, particularly those with `warrior`, `sleep`, and `trance` moods, exhibit extremely high retention rates (e.g., `Find Your Strength` at 96.8%, `sleep_30s_20260124_031441` at 83.6%). However, these videos have only 1-2 views, indicating they are not currently attracting significant audience attention despite their strong engagement for those who do watch.
3.  **`Piano_Deep_Calm` Exhibits Mixed Signals but Overall Positive Impact:** The `piano_deep_calm` mood shows a -4.7% retention vs. channel average, but a significant +270.5 minutes watch time per video vs. channel average. This suggests that while viewers might not watch the *entire* video as often as the channel average, the videos they do watch are watched for much longer durations, leading to high overall watch time. This could indicate that longer-form content within this mood is highly effective.
4.  **`Ceremony` Mood Underperforms:** The `ceremony` mood is identified as an underperformer, with -17.9% retention and -42.6 minutes watch time per video compared to the channel average. With 11 videos and 129 total views, this mood is not resonating well with the current audience.
5.  **Speculative: Opportunity for Longer-Form High-Retention Moods:** The high retention seen in short `sleep`, `trance`, and `warrior` videos, despite low views, suggests that if these moods could be packaged into longer-form content that attracts more initial views, they might also yield high watch times. This would require careful experimentation with titles and thumbnails to boost initial engagement.

## Experiments or packaging ideas

*   **Double Down on "Deep Focus" and "Piano Deep Calm":**
    *   Create more long-form videos (e.g., 1-hour or 2-hour) in the `deep_focus` and `piano_deep_calm` moods, similar to the top-performing "Enter Flow State" and "Calm Anxiety Fast" videos.
    *   Experiment with titles and thumbnails that explicitly highlight "focus," "concentration," "calm," and "anxiety relief" for these moods.
*   **Investigate and Revamp "Ceremony" Content:**
    *   Analyze the titles, thumbnails, and descriptions of existing `ceremony` videos to identify potential reasons for underperformance.
    *   Consider pausing new `ceremony` content until a clearer strategy for improving its engagement is developed, or experiment with drastically different packaging.
*   **Explore Longer Versions of High-Retention, Low-View Moods:**
    *   Take a high-retention 30-second video (e.g., "Find Your Strength" - `warrior` or a `sleep` track) and create a longer version (e.g., 1 hour).
    *   Package this longer version with a compelling title and thumbnail designed to attract more initial views, testing if the high retention translates to longer watch times at scale.
*   **A/B Test Titles/Thumbnails for `Piano_Deep_Calm`:**
    *   Given the high watch time but slightly lower retention for `piano_deep_calm`, test different titles and thumbnails that might improve initial click-through rate and signal the long-form nature of the content more effectively, potentially improving overall retention percentage.
*   **Cross-Reference with Brand Data (Manual Step):**
    *   As suggested in the `personal.md` report, manually compare retention and watch time trends for similar moods or themes against the brand's weekly reports (`data/reports/2026-W15.md` and `data/suggestions.json`) to identify any broader market trends or successful strategies that could be adapted for the personal channel.
