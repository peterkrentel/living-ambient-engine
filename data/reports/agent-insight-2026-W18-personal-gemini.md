# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of personal channel analytics reports and suggestions for Week 18, 2026. My analysis will focus on identifying key performance trends, risks, and actionable insights based solely on this data to inform future content strategy.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md` (Personal channel analytics report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md` (Personal advisory and correlation report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Detailed suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw video analytics data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md` (Missing file)

## Summary

The personal channel tracked 114 videos during the analytics window (April 1st to April 28th, 2026), accumulating 783 total views and 4,991 minutes of watch time, gaining 4 subscribers. The overall average retention was 21.63%, with an average watch time of 113.432 minutes per video for the 44 videos with views. The `piano_deep_calm` mood shows a strong positive correlation with watch time per video, despite slightly below-average retention. Conversely, `ceremony` mood videos underperformed significantly in both retention and watch time per video. Short, 30-second videos show very high retention but negligible views.

## Risks / caveats

*   **Low View Counts for Retention Leaders:** The top 5 videos by retention all have only 1 or 2 views, making their high retention percentages statistically unreliable for broader conclusions.
*   **Confounders and Packaging:** The `run-next` report explicitly warns that correlations at the mood level do not prove causality, as packaging elements (title, thumbnail, traffic source, seasonality) are not accounted for in this analysis. Without CTR and impressions data (which the "Next steps" suggest extending the fetcher for), it's difficult to assess the initial appeal of videos.
*   **Limited Data for Many Moods:** Many moods have very few videos with views (e.g., `trance`, `warrior`, `study`, `sleep`, `fireplace`, `piano_relax`, `piano_ambient`), or even zero views (`piano_evening`, `rain_piano`, `piano_gentle`, `chill`, `lofi_study`, `ocean_waves`), making it challenging to draw robust conclusions about their performance.
*   **Missing `run-intent-blocked-personal.md`:** The absence of this file means any blocked intent for this personal channel is not visible in this bundle.
*   **No Art Period or Music Style Data:** The `suggestions_personal.json` shows zero videos with views for any `art_periods` or `music_styles`, indicating these dimensions are not currently contributing to actionable insights.

## Insights

1.  **`piano_deep_calm` is a Watch Time Driver:** Videos categorized under `piano_deep_calm` mood, despite having slightly below-average retention (-2.4% vs. channel average), significantly outperform in watch time per video (+360.2 minutes vs. channel average). This suggests that while viewers might not watch the entire video, those who engage tend to watch for a very long duration, indicating strong engagement for this specific mood. Two `piano_deep_calm` videos are among the top 5 by views and watch time, collectively generating over 2000 minutes of watch time from 112 views.
2.  **Deep Focus Content Performs Well for Views:** The `deep_focus` mood is a strong performer in terms of total views, with two videos ("Enter Flow State" and "Sounds for an Overactive Mind") ranking among the top 5 by views. This indicates a consistent demand for content aimed at concentration and minimizing distractions.
3.  **Short Videos Show High Retention, Low Impact:** While 30-second videos like "Find Your Strength" (warrior) and "Sounds for an Overactive Mind" (deep_focus) exhibit extremely high retention rates (96.8%), their view counts are negligible (1 view each). This suggests they are effective at holding the attention of the *very few* viewers they reach but are not currently contributing meaningfully to overall channel growth or watch time.
4.  **`ceremony` Mood Underperforms:** The `ceremony` mood is identified as an underperformer, with retention 19.3% below the channel average and watch time per video 71.1 minutes below average. This indicates that content in this mood is struggling to retain viewers and generate significant watch time.
5.  **Speculative: Long-Form Content is Key for Watch Time:** The top videos by views and watch time are all 1-hour or longer. For example, "Calm Anxiety Fast · 1 Hour Deep Piano Re" (piano_deep_calm) generated 992 and 1034 minutes of watch time from 60 and 52 views respectively. This strongly suggests that longer-form content is crucial for accumulating significant watch time, which is a primary metric for ambient music channels.

## Experiments or packaging ideas

*   **Double Down on `piano_deep_calm`:**
    *   Create more long-form videos (1+ hour) in the `piano_deep_calm` mood, focusing on titles and thumbnails that clearly communicate "deep calm," "focus," and "anxiety relief."
    *   Experiment with different video lengths within this mood, perhaps 2-hour or 3-hour versions, to see if watch time scales further.
*   **Optimize `deep_focus` Content:**
    *   Produce additional long-form `deep_focus` videos, building on the success of "Enter Flow State" and "Sounds for an Overactive Mind."
    *   Consider variations like "Zero Distraction" or "Enhanced Focus" in titles.
*   **Re-evaluate `ceremony` Mood:**
    *   Investigate the packaging (titles, thumbnails) of existing `ceremony` videos to identify potential reasons for low retention and watch time.
    *   **Speculative:** If packaging is not the primary issue, consider pausing new content generation for this mood until more insights are gathered, or experiment with drastically different approaches (e.g., shorter versions, different visual styles).
*   **Leverage High-Retention Shorts Strategically:**
    *   Analyze the audience that watches the high-retention 30-second videos. Are these new viewers? Are they converting to longer content?
    *   **Speculative:** Consider using these high-retention shorts as promotional snippets for longer, related content, or as YouTube Shorts to drive discovery.
*   **Extend Analytics Fetcher:**
    *   Prioritize extending the personal fetcher to include CTR and impressions as suggested in the next steps. This data is critical for understanding why videos are or aren't getting initial clicks, which is a significant confounder for retention and watch time analysis.
