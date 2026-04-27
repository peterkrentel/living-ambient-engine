# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of personal channel analytics reports and suggestions for Week 18, 2026. My analysis will focus on identifying patterns in video performance related to mood, retention, and watch time, and suggesting actionable insights and experiments based solely on this data.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md` (Personal channel analytics report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md` (Run next — personal advisory)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Personal channel suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw personal channel analytics data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md` (Missing file, noted)

## Summary

The personal channel tracked 114 videos over the period of March 30 to April 26, 2026, accumulating 728 total views and 3,730 minutes of watch time, gaining 4 subscribers. The overall average retention for videos with views was 20.22%, and the average watch time per video was approximately 82.89 minutes. "Deep focus" and "piano_deep_calm" moods are driving the most views and watch time, with specific long-form videos performing exceptionally well. Conversely, "ceremony" mood videos are underperforming in both retention and watch time. Short-form videos, particularly 30-second clips, show very high retention percentages but contribute minimally to total views and watch time.

## Risks / caveats

The `run-next-2026-W18-personal.md` explicitly states that correlation addresses "patterns in the data, not hidden causes," and that CTR, impressions, and retention are often influenced by "title, thumbnail, traffic source, and seasonality," not solely by mood or art-period labels. The data for many moods is thin, with several moods having 0 views or only 1-2 videos with views, making it difficult to draw statistically significant conclusions. The `run-intent-blocked-personal.md` file is missing, which might indicate a lack of specific blocked intents for this period. The `suggestions_personal.json` shows no data for `art_periods`, `music_styles`, or `art_music_combos`, indicating these dimensions are not currently being analyzed for performance.

## Insights

1.  **Deep Focus and Piano Deep Calm Drive Engagement:** Videos categorized under "deep_focus" and "piano_deep_calm" moods are significant drivers of views and watch time. "Enter Flow State | 1 Hour Zero Distracti" (deep_focus) garnered 119 views and 298 minutes of watch time, while "Calm Anxiety Fast | 1 Hour Deep Piano Re" (piano_deep_calm) had 53 views and 806 minutes of watch time (and another instance with 47 views and 793 minutes). This suggests a strong audience preference for these themes, especially in longer formats.
2.  **Long-Form Content Dominates Watch Time:** The top videos by views and watch time are consistently 1-hour or longer formats. For example, "Calm Anxiety Fast | 1 Hour Deep Piano Re" videos contribute significantly to total watch time, indicating that viewers are willing to engage with extended content in these moods.
3.  **High Retention in Short-Form, Low Overall Impact:** Short 30-second videos, such as "Find Your Strength" (warrior, 96.8% retention) and "sleep_30s_20260124_031441" (sleep, 83.6% retention), show exceptionally high retention rates. However, these videos only have 1-2 views each, contributing negligibly to overall views and watch time. This suggests they might be effective as short-form content but are not currently attracting a broad audience.
4.  **Ceremony Mood Underperforms:** The "ceremony" mood shows significantly lower performance compared to the channel average, with a retention percentage of 1.5% and an average watch time per video of -42.6 minutes versus the channel average. This indicates that content in this mood is not resonating well with the audience.
5.  **Speculative: Potential for Sleep and Trance:** While "sleep" and "trance" moods have very few views (1 and 6 respectively), their average retention percentages are relatively high (83.6% for sleep, 39.7% for trance), especially for the short-form videos. This could indicate a niche but engaged audience for these moods, potentially warranting further exploration with longer-form content if packaging and discoverability can be improved.

## Experiments or packaging ideas

*   **Double Down on "Deep Focus" and "Piano Deep Calm" Long-Form:**
    *   Create more 1-hour+ videos in "deep_focus" and "piano_deep_calm" moods, leveraging successful titles and themes like "Enter Flow State" and "Calm Anxiety Fast."
    *   Experiment with slight variations in titles and thumbnails for these high-performing moods to see if CTR can be further optimized (requires CTR/impressions data).
*   **Re-evaluate "Ceremony" Content:**
    *   Analyze the specific "ceremony" videos that are underperforming. Are there common elements in their titles, thumbnails, or audio characteristics that could explain the low retention?
    *   Consider pausing production of "ceremony" content or experimenting with a completely different approach to packaging or sound design if the mood is to be kept.
*   **Explore Longer Form "Sleep" and "Trance":**
    *   Given the high retention of short "sleep" and "trance" videos, create a few longer-form (e.g., 1-hour) videos in these moods.
    *   Monitor their performance closely for watch time and retention to see if the engagement scales with duration.
*   **Leverage High-Retention Short-Form for Discovery:**
    *   Consider how the highly retained 30-second clips could be used strategically, perhaps as YouTube Shorts, or as promotional snippets for longer videos, to drive traffic to the main channel.
*   **Expand Analytics to Include CTR and Impressions:**
    *   As suggested in the `next steps (personal)` and `run-next` reports, extending the personal fetcher to include CTR and impressions would provide crucial data for understanding why certain videos gain views and others do not, moving beyond just retention and watch time.
