# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of files, including the personal channel analytics report, the run-next personal advisory, and the raw suggestions and analytics JSON files. My analysis will focus on identifying key performance trends, risks, and actionable insights for the personal YouTube ambient music channel based *only* on this data.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md` (Personal channel analytics report for 2026-W18)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md` (Run next — personal advisory for 2026-W18)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Raw suggestions data for the personal channel)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw analytics data for the personal channel)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md` (Missing file)

## Summary

The personal channel tracked 114 videos over the analytics window (2026-03-30 to 2026-04-26), generating 755 total views and 4,224 minutes of watch time, and gaining 4 subscribers. The overall average retention for videos with views is 22.33%, and the average watch time per video is approximately 91.8 minutes. "Deep focus" and "piano_deep_calm" moods are driving the most views and watch time, with "Calm Anxiety Fast" and "Enter Flow State" being top-performing videos. Conversely, "ceremony" mood videos show significantly lower retention and watch time compared to the channel average. Many moods have very low view counts, making it difficult to draw strong conclusions.

## Risks / caveats

1.  **Low View Counts for Retention Analysis:** Many videos in the "Top 5 by Retention" table have only 1 view, making the high retention percentages (e.g., 96.8%) statistically unreliable for generalizable insights.
2.  **Confounders and Packaging:** The `run-next` report explicitly states that CTR, impressions, and retention are often influenced by title, thumbnail, traffic source, and seasonality, not solely by mood or art-period labels. The current data bundle does not include CTR or impressions, limiting the ability to analyze these critical packaging factors.
3.  **Limited Data Coverage:** The `suggestions_personal.json` shows that "art_periods" and "music_styles" have zero total videos and zero videos with views, meaning no insights can be drawn from these categories.
4.  **Missing `run-intent-blocked-personal.md`:** The absence of this file means any blocked intents for the personal channel are unknown, which could impact future production planning.
5.  **Brand vs. Personal Lane:** The report clearly distinguishes between personal and brand metrics, cautioning against merging them. This analysis is strictly for the personal channel.

## Insights

1.  **Deep Focus and Piano-Based Content Drives Engagement:** The "deep_focus" mood accounts for 243 views across 10 videos with an average retention of 25.8%. Similarly, "piano_deep_calm" videos, while having a lower average retention percentage (18.5%), contribute significantly to total watch time, with 306 views across 14 videos and a substantial +323.2 minutes vs. channel average for watch time per video. This suggests that piano-based deep calm and focus content resonates well with the audience for longer viewing sessions.
2.  **Longer Videos Perform Well for Watch Time:** The top-performing videos by views, "Enter Flow State" (1 Hour Zero Distracti) and "Calm Anxiety Fast" (1 Hour Deep Piano Re), are both 1-hour durations and contribute significantly to total watch time (299 and 867/854 minutes respectively). This indicates that longer-form content, especially in the "deep_focus" and "piano_deep_calm" categories, is effective for accumulating watch time.
3.  **Speculative: Short-Form Content for Initial Hook:** While the top retention videos ("Find Your Strength" and "Sounds for an Overactive Mind") are 30-second clips, their view counts are extremely low (1 view each). This makes it difficult to draw definitive conclusions about the effectiveness of short-form content for retention. However, if these 30-second clips were used as teasers or short-form content, their high retention *could* suggest potential for hooking viewers, though more data is needed.
4.  **"Ceremony" Mood Underperforms:** The "ceremony" mood shows poor performance, with an average retention of 1.5% across 11 videos and a significant negative deviation of -20.0% vs. channel average for retention and -51.5 minutes vs. channel average for watch time per video. This indicates that content tagged with "ceremony" is not engaging viewers effectively.
5.  **Many Moods Lack Sufficient Data for Analysis:** Several moods like "energize," "rain_sleep," "trance," "warrior," "study," "unknown," "piano_relax," "piano_ambient," "sleep," and "fireplace" have very low view counts (5-24 views) or even zero views, making it challenging to assess their true performance or potential. The "piano_evening," "rain_piano," "piano_gentle," "chill," "lofi_study," and "ocean_waves" moods have 0 views, offering no data for analysis.

## Experiments or packaging ideas

*   **Double Down on "Deep Focus" and "Piano Deep Calm":**
    *   Create more 1-hour or longer videos in the "deep_focus" and "piano_deep_calm" categories, similar to "Enter Flow State" and "Calm Anxiety Fast."
    *   Experiment with titles and thumbnails that explicitly highlight "zero distraction," "calm anxiety," and "flow state" benefits.
*   **Investigate "Ceremony" Underperformance:**
    *   Review the titles, thumbnails, and actual audio content of "ceremony" videos to understand why they have such low retention.
    *   **Speculative:** Consider re-packaging existing "ceremony" content under different mood labels if the actual sound aligns better with other performing categories, or deprioritize new content in this mood.
*   **Explore Short-Form Retention with More Views:**
    *   If possible, promote the 30-second "Find Your Strength" and "Sounds for an Overactive Mind" clips to gather more views and validate their high retention. This could inform a strategy for short-form content or teasers.
*   **Prioritize Fetching CTR and Impressions:**
    *   As suggested in the "Next steps (personal)" and "Packaging & confounders" sections, extend the personal fetcher to include CTR and impressions. This data is crucial for understanding why videos are clicked and how packaging impacts initial engagement.
*   **Batch Strategy Review:**
    *   Cross-read the `piano-batch.yml` workflow to understand the current batch strategy for piano-related content and align new content generation with successful patterns in "piano_deep_calm."
