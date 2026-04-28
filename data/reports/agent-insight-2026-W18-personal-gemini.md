# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of files, including the personal channel analytics report, the run-next personal advisory, and the raw JSON data for suggestions and analytics. My analysis will focus on identifying key performance indicators, risks, and actionable insights for the personal YouTube ambient music channel based solely on this context.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md` (Personal channel analytics report for 2026-W18)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md` (Run next personal advisory for 2026-W18)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Raw suggestions data for the personal channel)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw analytics data for the personal channel)

## Summary

The personal channel, with 114 videos tracked, accumulated 753 total views and 4,164 minutes of watch time, gaining 4 subscribers during the `2026-03-31` to `2026-04-27` analytics window. The overall average retention for videos with views is 21.63%, and the average watch time per video is approximately 90.5 minutes. "Deep focus" and "piano_deep_calm" moods are significant drivers of views and watch time, with "piano_deep_calm" showing a strong positive correlation with watch time per video despite a lower retention percentage compared to the channel average. Conversely, "ceremony" mood videos are underperforming in both retention and watch time. Short-form "30 Seconds" videos show exceptionally high retention but contribute minimally to overall views or watch time.

## Risks / caveats

1.  **Low View Counts for Retention Leaders:** The top 5 videos by retention all have only 1 view, making their high retention percentages (`96.8%`, `83.6%`, `78.3%`, `74.8%`) statistically unreliable for drawing broad conclusions about content strategy.
2.  **Confounders and Packaging:** The `run-next` report explicitly states that "CTR, impressions, and retention often move because of title, thumbnail, traffic source, and seasonality" and warns against treating bucket-level correlation as proof that generation parameters drove a result when packaging differed. This means attributing performance solely to "mood" without considering other factors is risky.
3.  **Limited Data for Many Moods:** Many moods, such as `piano_evening`, `rain_piano`, `piano_gentle`, `chill`, `lofi_study`, and `ocean_waves`, have 0 views, making it impossible to assess their performance. Other moods like `trance`, `warrior`, `study`, `unknown`, `piano_relax`, `piano_ambient`, `sleep`, and `fireplace` have very low view counts (1-7 views), limiting the confidence in their reported average retention.
4.  **Missing Metrics:** The `run-next` report notes that extending the personal fetcher for CTR and impressions is optional, and these metrics are not present in the current reports. This limits the ability to analyze the top-of-funnel performance and diagnose issues related to discoverability.
5.  **Brand vs. Personal Lane:** The report explicitly states that brand metrics are not merged into the personal correlate, requiring deliberate comparison. This means insights from the brand channel are not automatically applied here and should be cross-referenced manually.
6.  **Lack of Art Period/Music Style Data:** The `data/suggestions_personal.json` shows zero videos with views for all listed `art_periods` and `music_styles`, and `art_music_combos`. This indicates a complete lack of data for these categories, preventing any analysis or recommendations based on them.

## Insights

1.  **Deep Focus and Piano Deep Calm Drive Watch Time:** The moods `deep_focus` and `piano_deep_calm` are the primary contributors to watch time. "Enter Flow State | 1 Hour Zero Distracti" (deep_focus) generated 299 minutes of watch time from 120 views, and "Calm Anxiety Fast | 1 Hour Deep Piano Re" (piano_deep_calm) generated 867 minutes from 55 views and 854 minutes from 49 views across two videos. This suggests a strong user demand for long-form content in these specific moods.
2.  **High Retention in Short-Form Content (with caveats):** Videos like "Find Your Strength" (warrior) and "Sounds for an Overactive Mind" (deep_focus) with "30 Seconds" in their titles show exceptionally high retention (96.8%). However, these videos only have 1 view each, making it difficult to determine if this retention is scalable or representative of broader appeal.
3.  **Underperformance of Ceremony Mood:** The `ceremony` mood shows significantly lower performance, with an average retention of 1.5% and a negative deviation of -19.3% vs. channel average retention, and -50.2 minutes vs. channel average watch time per video. This indicates that content tagged with `ceremony` is not resonating well with the audience.
4.  **Speculative: Longer Videos for Engagement:** While not directly stated, the top videos by views and watch time are consistently 1-hour durations (e.g., "Enter Flow State | 1 Hour...", "Sounds for an Overactive Mind | 1 Hour...", "Ground Yourself Instantly | 1 Hour Deep...", "Calm Anxiety Fast | 1 Hour Deep Piano Re"). This suggests that longer-form content (around 1 hour) is more effective at capturing and retaining audience attention for significant watch time, especially for moods like `deep_focus` and `piano_deep_calm`.
5.  **Speculative: "Calm Anxiety Fast" and "Let Go of Stress" Themes Resonate:** Several top-performing videos by views and watch time include phrases like "Calm Anxiety Fast" and "Let Go of Stress" in their titles. This suggests that content directly addressing stress relief and anxiety reduction is highly appealing to the channel's audience.

## Experiments or packaging ideas

*   **Double down on "deep_focus" and "piano_deep_calm" long-form content:** Create more 1-hour or longer videos with titles and thumbnails optimized for these moods, focusing on themes like "flow state," "zero distraction," and "calm anxiety."
*   **Investigate "ceremony" mood performance:** Analyze the titles, thumbnails, and descriptions of `ceremony` videos to understand why they underperform. Consider A/B testing different packaging for existing `ceremony` content or pausing new `ceremony` content generation until more data is available.
*   **Explore "warrior" and "sleep" moods with caution:** While "warrior" and "sleep" show high retention on single-view videos, experiment with a few more videos in these moods to see if the high retention holds with more views. Focus on short-form content (e.g., 30 seconds to 5 minutes) to test initial engagement.
*   **Prioritize fetching CTR and impressions:** Implement the optional personal fetcher for CTR and impressions to gain a better understanding of how titles and thumbnails are performing and to diagnose discoverability issues.
*   **A/B test titles and thumbnails for top-performing moods:** For new videos in `deep_focus` and `piano_deep_calm`, test variations of titles and thumbnails that emphasize benefits like "focus," "relaxation," "stress relief," and "calm."
*   **Cross-reference with brand reports:** Manually compare the performance of similar moods and content types on the brand channel (`data/reports/2026-W14.md`) to identify potential transferable insights or confirm trends.
*   **Experiment with "Let Go of Stress" variations:** Given the presence of "Let Go of Stress" in several video titles in `analytics_personal.json`, create more content with this theme, exploring different ambient styles (e.g., rain, gentle piano, pure ambience) and durations to see which combinations resonate most.
