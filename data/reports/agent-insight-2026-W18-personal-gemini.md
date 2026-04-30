# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of files, including the personal analytics report for 2026-W18, the `run-next` personal advisory, and the raw `suggestions_personal.json` and `analytics_personal.json` data. My analysis will focus on identifying key performance trends, risks, and actionable insights for the personal YouTube ambient music channel based *only* on this context.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md` (Personal channel analytics report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md` (Run next personal advisory)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md` (Missing file)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Raw suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw video analytics data)

## Summary

The personal channel tracked 114 videos during the analytics window (2026-04-02 to 2026-04-29), accumulating 819 total views and 5,901 minutes of watch time, with 4 subscribers gained. The overall average retention for videos with views is 23.45%, and the average watch time per video is approximately 131 minutes. `piano_deep_calm` and `deep_focus` moods are driving the most views and significant watch time, despite `piano_deep_calm` having slightly below-average retention. Conversely, `ceremony` shows low retention and watch time per video. Short 30-second videos, particularly `warrior` and `deep_focus` moods, demonstrate very high retention percentages, though with minimal views.

## Risks / caveats

1.  **Low View Counts for High Retention Videos:** The top 5 videos by retention all have only 1 view each. This makes their high retention percentages (e.g., 96.8%) statistically unreliable for drawing broad conclusions about content strategy.
2.  **Confounders in Data:** The `run-next` advisory explicitly states that CTR, impressions, and retention are often influenced by packaging elements (title, thumbnail, traffic source, seasonality) and not solely by generation parameters like mood. Without data on these packaging elements, causal links are difficult to establish.
3.  **Limited Data Coverage:** While 114 videos are tracked, only 45 have views, and only 31.6% are "identity-aligned" with `generations.json`. This limits the ability to correlate mood/style directly with performance for a significant portion of the content.
4.  **Missing `run-intent-blocked-personal.md`:** The absence of this file means any blocked intent for the personal channel is unknown, which could impact future production decisions.
5.  **Lack of CTR/Impressions:** The "Next steps" suggest extending the personal fetcher for CTR and impressions. Without these metrics, understanding the initial discoverability and appeal of videos is challenging.

## Insights

1.  **`piano_deep_calm` is a high-performing mood for watch time:** Despite its retention being slightly below the channel average (-2.3%), `piano_deep_calm` videos (n=9) generated a significant +411.9 minutes of watch time per video compared to the channel average. This indicates that while viewers might not watch the entire duration, the absolute time spent on these videos is very high, suggesting strong engagement for those who click.
2.  **`deep_focus` is a strong performer for views:** The top two videos by views, "Enter Flow State · 1 Hour Zero Distracti" (121 views) and "Sounds for an Overactive Mind · 1 Hour E" (81 views), are both categorized under the `deep_focus` mood. This mood also contributes significantly to total views (246 views across 10 videos) and has a respectable average retention of 18.7%.
3.  **Long-form content drives watch time:** The top videos by views are 1-hour durations, and the `piano_deep_calm` videos, which excel in watch time, are likely also longer-form. This suggests that viewers are seeking and engaging with extended ambient experiences on this channel.
4.  **`ceremony` mood is underperforming:** The `ceremony` mood shows significantly lower retention (-21.1% vs channel avg) and watch time per video (-88.8 min vs channel avg) based on an exploratory analysis of 3 videos with 110 views. This mood appears to struggle with viewer engagement.
5.  **Speculative: Short, high-retention content might serve as discovery hooks:** While the 30-second videos with extremely high retention (e.g., `warrior`, `deep_focus`, `sleep`, `trance`) only have 1 view each, their near-perfect retention suggests that for the single viewer, the content was highly engaging for its short duration. If these short clips could gain more visibility (e.g., via Shorts or as promotional snippets), they might act as effective introductions to the channel's longer-form offerings.

## Experiments or packaging ideas

*   **Double down on `piano_deep_calm` and `deep_focus`:**
    *   Create more 1-hour or longer videos in these moods, focusing on titles and thumbnails that clearly communicate their purpose (e.g., "Zero Distraction," "Calm Anxiety Fast").
    *   Analyze the specific elements (e.g., sound design, visual style) of the top-performing `piano_deep_calm` and `deep_focus` videos to replicate success.
*   **Investigate `ceremony` mood:**
    *   Review the titles and thumbnails of `ceremony` videos to see if they accurately represent the content or if there's a mismatch in viewer expectation.
    *   Consider A/B testing different packaging for existing `ceremony` videos to see if discoverability or initial engagement improves.
    *   If performance remains low, consider deprioritizing this mood for new content.
*   **Explore short-form content strategy:**
    *   Experiment with promoting the high-retention 30-second clips as YouTube Shorts to drive new traffic and potential subscribers to the channel's longer videos.
    *   Create new short-form content (e.g., 30-60 seconds) specifically designed for high retention and quick engagement, perhaps as teasers for longer pieces.
*   **Cross-reference with brand reports (manual step):**
    *   As suggested in the "Next steps," manually compare retention and watch time trends for similar moods/lengths on the brand channel (`data/reports/2026-W16.md`) to identify broader market trends or successful strategies that could be adapted for the personal channel.
*   **Prioritize fetching CTR and impressions:**
    *   Implement the optional extension to the personal fetcher to gather CTR and impressions data. This will provide crucial insights into how titles and thumbnails are performing and help diagnose issues with discoverability versus on-video engagement.
