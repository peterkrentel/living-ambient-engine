# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of files, including the personal channel analytics report for 2026-W18, the `run-next` advisory, and the raw `suggestions_personal.json` and `analytics_personal.json` files. My analysis will focus on identifying key performance trends, risks, and actionable insights for the personal YouTube channel based solely on this data.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md`
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md`
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json`
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json`

## Summary

The personal channel tracked 114 videos during the analytics window (April 3rd to April 30th, 2026), accumulating 816 total views and 5,889 minutes of watch time, gaining 4 subscribers. "Piano_deep_calm" and "deep_focus" moods are the top performers by total views, with "piano_deep_calm" also showing a significantly higher watch time per video despite slightly below-average retention. Short, 30-second videos, particularly in "warrior" and "deep_focus" moods, exhibit very high retention rates but minimal views. The `ceremony` mood is flagged for underperformance in both retention and watch time.

## Risks / caveats

*   **Low View Counts for High Retention:** The top 5 videos by retention all have only 1 view each. This makes their high retention percentages (e.g., 96.8%) statistically unreliable for drawing broad conclusions about content strategy.
*   **Limited Data for Many Moods:** Many moods have very low total views (e.g., `trance` with 6 views, `warrior` with 5 views, `sleep` with 1 view, and several with 0 views), making it difficult to assess their true performance or potential.
*   **Confounders:** The `run-next` report explicitly states that "CTR, impressions, and retention often move because of title, thumbnail, traffic source, and seasonality — not because a mood or art-period label 'caused' an outcome." This means correlations observed at the mood level should not be treated as direct causal links without further investigation into packaging and external factors.
*   **Missing Metrics:** The personal fetcher has not been extended to include CTR or impressions, which are crucial for understanding audience engagement and discoverability.
*   **Incomplete Metadata Join:** Only 31.6% (36 out of 114) of videos are identity-aligned with `generations.json`, and 71.9% are joined with any ledger row. This suggests a significant portion of content might lack detailed metadata for deeper analysis.
*   **No Art Period or Music Style Data:** The `suggestions_personal.json` file shows zero total videos and zero videos with views for all listed `art_periods` and `music_styles`, indicating no data for these dimensions in the current analysis.

## Insights

1.  **"Piano_deep_calm" and "deep_focus" are strong performers by views and watch time.** The "piano_deep_calm" mood has 14 videos, generating 361 views and a high watch time per video (+409.2 min vs. channel avg), despite an average retention of 20.5%, which is slightly below the overall channel average of 23.77%. Similarly, "deep_focus" has 10 videos with 246 views. This suggests these moods resonate well with the audience for longer viewing sessions.
2.  **Long-form content in "deep_focus" and "piano_deep_calm" drives significant watch time.** The top-viewed videos, "Enter Flow State · 1 Hour Zero Distracti" (deep_focus) and "Calm Anxiety Fast · 1 Hour Deep Piano Re" (piano_deep_calm), are both 1-hour durations and contribute substantially to total watch time (299 min and 1,114 min respectively for the top two "piano_deep_calm" videos). This indicates a preference for longer content in these specific moods.
3.  **Short-form content shows high retention but negligible views.** Videos like "Find Your Strength · 30 Seconds Power Dr" (warrior) and "Sounds for an Overactive Mind · 30 Secon" (deep_focus) have very high retention rates (96.8% and 96.8%) but only 1 view each. While this suggests the content is engaging for those who find it, their lack of discoverability or reach makes their high retention statistically insignificant for overall strategy.
4.  **Speculative: The "ceremony" mood is an underperformer.** The `run-next` report flags `mood` / `ceremony` for significantly lower retention (-21.5% vs channel avg) and watch time per video (-91.5 min vs channel avg) for videos with views. This suggests this mood is not resonating well with the audience currently.
5.  **Speculative: There's an opportunity to explore content beyond piano-centric moods.** While "piano_deep_calm" and "deep_focus" perform well, the channel has a wide range of moods with very few views. The high retention of "warrior" and "trance" (81.4% and 54.0% respectively, albeit on minimal views) suggests potential if these moods can gain more visibility.

## Experiments or packaging ideas

*   **Double down on "piano_deep_calm" and "deep_focus" long-form content.** Create more 1-hour videos in these moods, focusing on similar titles and themes that have already proven successful in terms of views and watch time.
*   **Investigate packaging for top-performing moods.** Analyze the titles and thumbnails of "Enter Flow State · 1 Hour Zero Distracti" and "Calm Anxiety Fast · 1 Hour Deep Piano Re" to identify common elements that might contribute to their high view counts, and apply these learnings to new content in "piano_deep_calm" and "deep_focus."
*   **Deprioritize "ceremony" mood content for now.** Given its low retention and watch time, reduce production or promotion efforts for this mood until further data or a clear strategy for improvement emerges.
*   **Experiment with discoverability for high-retention, low-view short videos.** Consider bundling these 30-second clips into longer compilations or promoting them through different channels (e.g., YouTube Shorts if applicable, though not explicitly mentioned in context) to see if their high retention can translate to more views.
*   **Extend the personal fetcher to include CTR and impressions.** This is a crucial next step to understand how titles and thumbnails are performing and to identify discoverability issues for underperforming content.
*   **Cross-analyze with brand reports (when available).** The report suggests comparing personal retention and watch time with brand weekly reports. This could reveal broader trends or successful strategies from the brand channel that could be adapted for the personal channel.
