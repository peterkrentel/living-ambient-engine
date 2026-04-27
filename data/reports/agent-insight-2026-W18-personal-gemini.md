# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of personal channel analytics reports and suggestions for Week 18, 2026. My analysis will focus on identifying key performance trends, risks, and actionable insights to inform future content strategy for the personal YouTube ambient music channel, using only the data provided.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md` (Personal channel analytics report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md` (Run next — personal advisory)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Personal channel suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw personal channel analytics data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md` (Missing file)

## Summary

The personal channel tracked 114 videos over the period of March 30 to April 26, 2026, accumulating 728 total views and 3,730 minutes of watch time, gaining 4 subscribers. The overall average retention for videos with views is 20.22%, and the average watch time per video is approximately 82.89 minutes. "Deep focus" and "piano_deep_calm" moods are performing well in terms of total views and watch time, with specific videos like "Enter Flow State" and "Calm Anxiety Fast" being top performers. Conversely, "ceremony" mood shows significantly lower retention and watch time per video. The data coverage for `art_periods` and `music_styles` is entirely absent, indicating a lack of metadata for these categories in the `suggestions_personal.json` file.

## Risks / caveats

1.  **Limited Data for Retention Analysis:** The "Top 5 by Retention" table shows several videos with only 1 or 2 views, leading to potentially misleadingly high retention percentages (e.g., "Find Your Strength" at 96.8% with 1 view). These single-view data points are not statistically robust for drawing general conclusions about mood performance.
2.  **Missing Metadata:** The `suggestions_personal.json` file indicates zero videos with views for all `art_periods` and `music_styles`. This means any analysis or suggestions related to these categories are impossible with the current data.
3.  **Confounders in Packaging:** The `run-next` report explicitly warns that "CTR, impressions, and retention often move because of title, thumbnail, traffic source, and seasonality — not because a mood or art-period label 'caused' an outcome." Without CTR and impressions data (which is an optional next step), it's difficult to isolate the impact of mood/content from packaging elements.
4.  **Incomplete `generations.json` Join:** Only 31.6% of videos are "identity-aligned" with `generations.json`, meaning a significant portion of content might lack detailed generation parameters for deeper analysis.
5.  **Brand vs. Personal Channel:** The report highlights that brand metrics are separate and not merged into personal correlates. Cross-analysis is suggested as a manual next step, indicating that insights from the personal channel may not directly translate to the brand channel without further investigation.

## Insights

1.  **Deep Focus and Deep Calm Piano Drive Watch Time:** The "deep_focus" and "piano_deep_calm" moods are significant drivers of total views and watch time. "Enter Flow State" (deep_focus) garnered 298 minutes of watch time from 119 views, and "Calm Anxiety Fast" (piano_deep_calm) accumulated 806 and 793 minutes from 53 and 47 views respectively. This suggests a strong audience preference for content designed for concentration and anxiety relief, particularly with piano elements.
2.  **High Retention for Short, Specific Moods:** While views are low, videos like "Find Your Strength" (warrior, 96.8% retention) and "sleep_30s" (sleep, 83.6% retention) demonstrate extremely high retention percentages, albeit with only 1 view each. This might indicate that when these specific, short-form moods are discovered, they resonate strongly with the viewer for their intended purpose.
3.  **Speculative: Short-Form Content for Niche Needs:** The top retention videos are often 30-second clips with very specific moods (warrior, sleep, trance). While their view counts are minimal, their high retention suggests that users who find these short, targeted pieces may be engaging deeply with the content for its immediate utility. This contrasts with the longer-form videos driving overall watch time.
4.  **Ceremony Mood Underperforms:** The "ceremony" mood shows poor performance, with an average retention of 1.5% and a negative deviation of -17.9% vs. channel average retention. It also has a significantly lower average watch time per video (-42.6 minutes vs. channel average). This indicates that content categorized under "ceremony" is not resonating well with the audience in its current form.
5.  **Piano-Based Content Shows Mixed Signals:** The `piano_deep_calm` mood shows a -4.7% retention vs. channel average, yet a substantial +270.5 minutes vs. channel average in watch time per video. This suggests that while individual viewers might not watch a *high percentage* of these videos, those who do watch them for a *very long time*, contributing significantly to overall watch time. This could imply that these videos are effective as long-form background or focus tracks, even if not watched to completion by every viewer.

## Experiments or packaging ideas

*   **Double Down on "Deep Focus" and "Piano Deep Calm":**
    *   Create more 1-hour+ videos in the "deep_focus" and "piano_deep_calm" moods, given their strong performance in total views and watch time.
    *   Experiment with titles and thumbnails that clearly communicate the benefits of these moods (e.g., "Boost Focus," "Calm Mind," "Study Music").
*   **Investigate High-Retention, Low-View Moods:**
    *   **Speculative:** Explore creating longer versions (e.g., 1-hour) of "warrior," "sleep," and "trance" moods, while maintaining the core sonic elements that led to high retention in their 30-second forms.
    *   **Speculative:** Promote these high-retention, low-view videos through specific playlists or end screens to increase their discoverability.
*   **Re-evaluate "Ceremony" Content:**
    *   Analyze the specific content of "ceremony" videos to understand why retention and watch time are low.
    *   Consider pausing production of new "ceremony" content until further insights are gathered, or experiment with different interpretations of the "ceremony" mood, perhaps combining it with more popular elements like "piano_deep_calm."
*   **Enhance Metadata for Deeper Analysis:**
    *   Implement logging for `art_periods` and `music_styles` in `generations.json` for future videos to enable analysis of these dimensions.
*   **Expand Analytics for Packaging Insights:**
    *   Prioritize extending the personal fetcher to include CTR and impressions as suggested in `docs/PERSONAL_ANALYTICS.md`. This will provide crucial data to understand the impact of titles and thumbnails.
*   **Cross-Reference with Brand Channel (Manual):**
    *   Manually compare the performance of similar moods and content lengths on the brand channel (`data/reports/2026-W14.md`) to identify any transferable insights or discrepancies.
