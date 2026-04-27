# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of personal channel analytics reports and suggestions for Week 18, 2026. My analysis will focus on identifying key performance trends, risks, and actionable insights based solely on this data, concluding with experiment and packaging ideas.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md` (Personal channel analytics report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md` (Run next — personal advisory)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Personal channel suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw personal channel analytics data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md` (Missing file, noted)

## Summary

The personal channel, over the analytics window of March 30th to April 26th, 2026, generated 728 total views, 3,730 minutes of watch time, and gained 4 subscribers across 114 tracked videos. The overall average retention is 20.22%, and the average watch time per video is approximately 82.89 minutes. "Deep Focus" and "Piano Deep Calm" moods are driving the most views and watch time, with specific videos like "Enter Flow State" and "Calm Anxiety Fast" performing exceptionally well in these metrics. Conversely, "Ceremony" mood videos show significantly lower retention and watch time per video compared to the channel average. Short-form content (30 seconds) often shows very high retention percentages but contributes minimal views. The data coverage for `art_periods` and `music_styles` is entirely absent, limiting insights in these areas.

## Risks / caveats

*   **Limited Data for Retention:** The top 5 videos by retention all have only 1 or 2 views, making their high retention percentages (e.g., 96.8% for "Find Your Strength") statistically unreliable for broader conclusions.
*   **Confounders:** The `run-next` report explicitly states that CTR, impressions, and retention are influenced by packaging (title, thumbnail), traffic source, and seasonality. The current data bundle does not include CTR or impressions, which limits the ability to diagnose why certain videos perform well or poorly beyond mood and length.
*   **Incomplete Metadata Join:** Only 31.6% of videos are "identity-aligned" with `generations.json`, and 71.9% have "any ledger row." This suggests a significant portion of videos may lack detailed generation parameters, potentially skewing mood-based analysis if the metadata is inconsistent or missing for high-performing content.
*   **Missing Brand Comparison:** The `run-next` report advises comparing personal metrics against brand weekly reports, but the brand data (`data/analytics.json`) and its latest report (`2026-W15.md`) are present for cross-read only and not merged into the personal correlate, preventing a direct comparison within this bundle.
*   **Lack of Art/Music Style Data:** There is no data for `art_periods`, `music_styles`, or `art_music_combos` in `data/suggestions_personal.json`, meaning no insights can be drawn regarding these creative parameters.
*   **Missing `run-intent-blocked-personal.md`:** The absence of this file means any blocked intent for personal channel runs is not visible.

## Insights

1.  **High-Performing Long-Form Deep Focus and Piano Deep Calm:** Videos categorized under "deep_focus" and "piano_deep_calm" moods are significant drivers of views and watch time. "Enter Flow State | 1 Hour Zero Distracti" (deep_focus) garnered 119 views and 298 minutes of watch time, while two "Calm Anxiety Fast | 1 Hour Deep Piano Re" videos (piano_deep_calm) collectively achieved 100 views and 1599 minutes of watch time. This indicates a strong audience demand for longer-form content in these specific moods.
2.  **Discrepancy in Piano Deep Calm Performance:** While "piano_deep_calm" videos show a significantly higher watch time per video (+270.5 min vs channel avg), their average retention is -4.7% lower than the channel average. This suggests that while viewers are willing to watch these videos for extended periods, a portion might not be engaging for the entire duration, possibly indicating opportunities for refinement in pacing or content structure within these longer pieces.
3.  **Underperformance of Ceremony Mood:** The "ceremony" mood is a clear underperformer, with its retention percentage -17.9% below the channel average and watch time per video -42.6 minutes below average. Despite having 11 videos, it only generated 129 total views, suggesting this mood is not resonating well with the current audience.
4.  **High Retention for Short-Form Content (with low views):** Several 30-second videos, such as "Find Your Strength" (warrior, 96.8% retention) and "sleep_30s_20260124_031441" (sleep, 83.6% retention), exhibit extremely high retention rates. However, each of these videos only has 1 or 2 views, making it difficult to generalize this retention performance to a larger audience or to longer-form content.
5.  **Speculative: Potential for "Warrior" and "Trance" Moods:** While currently having very low views (5-6 views each), "warrior" and "trance" moods show promising average retention rates of 78.0% and 39.7% respectively, significantly above the overall channel average of 20.22%. This could indicate a niche but highly engaged audience for these moods, warranting further exploration with more content.

## Experiments or packaging ideas

*   **Double Down on "Deep Focus" and "Piano Deep Calm" Long-Form:**
    *   Produce more 1-hour+ videos in "deep_focus" and "piano_deep_calm" moods, leveraging titles and thumbnails similar to "Enter Flow State" and "Calm Anxiety Fast."
    *   Experiment with slightly varied themes within these moods (e.g., "Deep Focus for Coding," "Piano for Stress Relief & Focus").
*   **Investigate "Piano Deep Calm" Retention:**
    *   Analyze the specific "piano_deep_calm" videos with high watch time but lower retention. Look for common drop-off points in their analytics (if available in a more detailed report) to understand why viewers aren't completing them despite long watch times.
    *   Experiment with subtle variations in sound design or visual elements in new "piano_deep_calm" videos to improve overall retention.
*   **Deprioritize or Re-evaluate "Ceremony":**
    *   Temporarily reduce production of "ceremony" mood videos.
    *   If continuing, experiment with drastically different packaging (titles, thumbnails) for new "ceremony" content to see if discoverability or initial appeal is the issue, given its low views and retention.
*   **Test Longer "Warrior" and "Trance" Content:**
    *   Create a few longer-form (e.g., 30-minute or 1-hour) videos in the "warrior" and "trance" moods.
    *   Monitor their retention and views closely to see if the high engagement observed in short-form translates to longer formats with a larger audience.
*   **Explore "Sleep" and "Fireplace" for Retention:**
    *   Given the high retention of the single "sleep" video (83.6%) and "fireplace" (47.8%), consider producing more content in these moods, focusing on longer durations to capitalize on potential watch time.
*   **A/B Test Titles/Thumbnails for Top Performers:**
    *   While not directly supported by current metrics (missing CTR/impressions), based on the `run-next` report's mention of packaging, consider A/B testing different titles and thumbnails for new videos in high-performing moods ("deep_focus", "piano_deep_calm") to optimize click-through rates.
