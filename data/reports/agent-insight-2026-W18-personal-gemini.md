# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of committed repository files and excerpts from the analytics pipeline for the personal YouTube ambient music channel. My analysis will focus on identifying key performance trends, risks, and actionable insights based solely on this context.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md`: Personal channel analytics report for Week 18, 2026.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md`: Personal advisory report for Week 18, 2026, including actionable and exploratory suggestions.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md`: This file was missing from the bundle.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json`: Raw JSON data for personal channel suggestions.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json`: Raw JSON data for personal channel video analytics.

## Summary

The personal channel, over the analytics window of March 31 to April 27, 2026, generated 753 total views and 4,164 minutes of watch time, gaining 4 subscribers. The channel has 114 videos tracked, with 46 having views. "Piano_deep_calm" and "deep_focus" moods are the top performers in terms of total views, with "piano_deep_calm" showing a significantly higher watch time per video despite a lower average retention percentage compared to the channel average. Conversely, "ceremony" mood videos are underperforming in both retention and watch time per video. There is very limited data on "art_periods" and "music_styles," indicating a lack of content or views in these categories.

## Risks / caveats

*   **Limited Data for Deeper Analysis:** The `data/suggestions_personal.json` shows zero views for many moods, and all `art_periods` and `music_styles` have zero total videos and zero views, making it impossible to derive insights for these categories.
*   **Confounders:** The `run-next` report explicitly states that "CTR, impressions, and retention often move because of title, thumbnail, traffic source, and seasonality — not because a mood or art-period label 'caused' an outcome." This means that observed correlations at the mood level should not be treated as direct causal proof without considering packaging differences.
*   **Missing Report:** The `run-intent-blocked-personal.md` file was missing, so any blocked intents or issues are unknown.
*   **Incomplete Join:** Only 31.6% of videos are "identity-aligned" in the `generations.json` join, which could limit the depth of analysis linking content generation parameters to performance.
*   **No CTR/Impressions:** The current personal fetcher does not include CTR or impressions, which are crucial metrics for understanding discoverability and initial audience engagement. This is noted as an optional next step.

## Insights

1.  **"Piano_deep_calm" drives significant watch time:** Despite having an average retention percentage (-4.3% vs channel avg) that is slightly below the channel average (21.63%), videos categorized under "piano_deep_calm" generate a substantially higher watch time per video (+324.5 min vs channel avg). This suggests that while viewers might not watch the entire video, those who do engage stay for a very long time, indicating strong appeal for long-form content in this mood.
2.  **"Deep_focus" is a strong performer:** The "deep_focus" mood has a high number of total views (243) and a respectable average retention of 25.8%, which is above the overall channel average. The top-viewed video, "Enter Flow State | 1 Hour Zero Distracti," is a "deep_focus" video, accumulating 299 minutes of watch time from 120 views. This indicates a consistent demand for focus-oriented ambient music.
3.  **Short-form content shows high retention, but low views:** The top 5 videos by retention are all very short (e.g., "30 Seconds Power Dr," "30 Secon"), with retention percentages ranging from 74.8% to 96.8%. However, each of these videos only has 1 view. This suggests that while short clips can hold attention effectively, they are not currently driving significant overall viewership or watch time.
4.  **"Ceremony" mood is underperforming:** Videos with the "ceremony" mood are identified as underperformers, with retention % at -19.3% vs channel avg and watch time per video at -50.2 min vs channel avg. This indicates that content in this mood is not resonating well with the audience, leading to both lower engagement and shorter viewing durations.
5.  **Speculative: Potential for long-form "sleep" content:** The "sleep" mood has one video with an impressive 83.6% retention, despite only having 1 view. This high retention for a single instance, if it were a longer video, could indicate a strong potential for long-form sleep-related content to capture and hold audience attention, similar to the "piano_deep_calm" trend.

## Experiments or packaging ideas

*   **Double down on "piano_deep_calm" and "deep_focus" long-form content:**
    *   Create more videos in the "piano_deep_calm" and "deep_focus" moods, specifically targeting longer durations (e.g., 1-2 hours) given their high watch time performance.
    *   Experiment with titles and thumbnails that clearly communicate the "deep calm" or "focus" benefit and the extended duration.
*   **Re-evaluate "ceremony" content:**
    *   Analyze the specific "ceremony" videos that are underperforming. Are there common elements in their titles, thumbnails, or audio characteristics that could be contributing to low engagement?
    *   Consider pausing production of new "ceremony" content or experimenting with significantly different packaging (titles, thumbnails) for existing videos to see if performance improves.
*   **Test longer "sleep" videos:**
    *   Given the high retention of the single "sleep" video, create a few longer-form "sleep" ambient tracks (e.g., 1 hour+) and monitor their performance closely, especially retention and watch time.
*   **Investigate high-retention, low-view short videos:**
    *   While the 30-second clips have high retention, their 1 view makes them statistically insignificant. Consider if these short clips could be repurposed as promotional material or teasers for longer, related content to drive traffic.
*   **Prioritize extending personal fetcher for CTR and impressions:**
    *   As noted in the next steps, adding CTR and impressions metrics is crucial for understanding how titles and thumbnails are performing and where traffic is originating. This data would significantly enhance future creative advisories.
