# Agent advisory — Gemini (API) (personal, 2026-W17)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of files, including the personal channel analytics report for 2026-W17, the `run-next` advisory, the `run-intent-blocked` report, and the `suggestions_personal.json` and `analytics_personal.json` data files. My analysis will focus on identifying key performance trends, risks, and potential content strategies based solely on this information.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W17-personal.md` (Personal channel analytics report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W17-personal.md` (Run next personal advisory)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md` (Run intent blocked report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Personal channel suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw personal channel analytics data)

## Summary

The personal channel generated 313 total views and 892 minutes of watch time, gaining 4 subscribers during the 2026-03-23 to 2026-04-19 analytics window. The overall average retention is 16.25%, with an average watch time of 31.857 minutes per video for the 28 videos that received views. The "deep_focus" mood category leads in total views, while "piano_ambient" shows exceptionally high retention for a single video. The planner for this week was blocked due to a lack of actionable mood suggestions meeting the required thresholds (n≥5, group_views≥200).

## Risks / caveats

*   **Limited actionable insights:** The planner was blocked, indicating no mood suggestions met the criteria for "actionable" status (n≥5, group_views≥200). This means there are no strong, data-backed recommendations for increasing specific mood content this week.
*   **Low view counts for top retention videos:** Several videos with very high retention percentages (e.g., "Let Go of Stress | 2 Hours Soft Piano Am" at 99.2%) have only 1 view, making their retention metrics statistically less reliable for broader content strategy.
*   **Confounders:** The `run-next` report explicitly states that CTR, impressions, and retention are influenced by packaging (title, thumbnail), traffic source, and seasonality. Direct correlation between mood labels and outcomes should not be treated as causal proof without considering these factors.
*   **Thin data for many moods:** Many mood categories have zero views or very few videos with views, making it difficult to draw conclusions about their performance. For example, "sleep," "chill," "fireplace," "ocean_waves," and "lofi_study" all have videos but no views in this period.
*   **Missing metrics:** The personal fetcher has not been extended to include CTR and impressions, which are crucial for a complete understanding of video performance and packaging effectiveness.

## Insights

1.  **High Retention for Long-Form Piano Ambient:** The video "Let Go of Stress | 2 Hours Soft Piano Am" achieved an outstanding 99.2% retention, albeit with only 1 view. This suggests that when a viewer *does* discover this specific type of content, they are highly engaged. The mood is `piano_ambient`.
2.  **Deep Focus Drives Views:** The "deep_focus" mood category generated the most views (172) across 9 videos, with "Enter Flow State | 1 Hour Zero Distracti" being the top performer by views (116) and watch time (289 minutes). This indicates a strong audience interest in content designed for concentration.
3.  **Piano Deep Calm Shows Mixed Performance:** Videos tagged as "piano_deep_calm" appear in both top retention and top views lists. While "Let Go of Stress | Deep Calm Piano Atmos" has 41.8% retention with 11 views, "Calm Anxiety Fast | 1 Hour Deep Piano Re" (two entries) garnered 27 and 24 views respectively. This suggests potential, but also variability in performance within this mood.
4.  **Speculative: Short-Form Content for Overactive Minds:** The video "Sounds for an Overactive Mind | 30 Secon" (deep_focus) has a high retention of 74.8% with 1 view. While low views, this hints that very short, targeted content for specific needs (like an "overactive mind") could be highly engaging if discovered.
5.  **Speculative: Warrior Mood's Niche Appeal:** The video "warrior_10s_20260124_160306" (warrior) shows a high retention of 57.0% with 9 views. This suggests a niche but engaged audience for "warrior" themed content, even for very short durations (10 seconds).

## Experiments or packaging ideas

*   **Test longer durations for "deep_focus" content:** Given "Enter Flow State | 1 Hour Zero Distracti" performed well, explore creating more 1-2 hour videos within the "deep_focus" mood, potentially with similar titles emphasizing "zero distraction" or "flow state."
*   **Re-package high-retention, low-view videos:** For videos like "Let Go of Stress | 2 Hours Soft Piano Am" (99.2% retention, 1 view), experiment with different titles and thumbnails to improve discoverability (CTR/impressions, once those metrics are tracked).
*   **Create more "piano_ambient" content:** The exceptional retention of the 2-hour piano ambient video, even with low views, suggests a strong potential for this mood. Produce more content in this style, varying durations and specific use cases (e.g., "study," "sleep," "meditation").
*   **Explore short, highly specific content:** Investigate the potential of more 30-second to 1-minute videos targeting highly specific mental states or needs, similar to "Sounds for an Overactive Mind."
*   **Investigate "warrior" mood further:** Despite low overall views, the high retention of the "warrior" video suggests a dedicated audience. Consider producing a few more "warrior" themed pieces, perhaps at slightly longer durations, to see if this engagement scales.
*   **Prioritize enabling CTR and Impressions tracking:** As noted in the next steps, extending the personal fetcher to include CTR and impressions is critical for understanding why videos are or aren't getting views, and for optimizing packaging.
