# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of personal channel analytics reports and suggestions for Week 18, 2026. My goal is to synthesize these findings into actionable insights and suggest experiments to optimize content performance, focusing on watch time and retention.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md` (Personal channel analytics report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md` (Run next — personal advisory)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Personal channel suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw personal channel analytics data)

## Summary

The personal channel had 755 total views and 4,224 minutes of watch time, gaining 4 subscribers during the `2026-03-30` to `2026-04-26` analytics window. The overall average retention is 22.33%, and the average watch time per video is 91.826 minutes. "Deep focus" and "piano_deep_calm" moods are driving the most views and watch time, with specific long-form videos performing exceptionally well in watch time. Conversely, "ceremony" mood videos show significantly lower retention and watch time. Short-form videos (30 seconds) demonstrate high retention percentages but contribute very little to overall watch time due to their brevity.

## Risks / caveats

*   **Confounders & Packaging:** The `run-next` report explicitly states that CTR, impressions, and retention are often influenced by title, thumbnail, traffic source, and seasonality, not solely by mood or art-period labels. Correlation does not imply causation, and packaging differences across videos must be considered.
*   **Low `n` for retention:** While some 30-second videos show very high retention (e.g., 96.8%), they only have 1 view, making these percentages statistically unreliable for broader conclusions.
*   **Limited data points:** The `suggestions_personal.json` shows many moods, art periods, and music styles with zero videos or zero views, limiting the scope of actionable insights for these categories. Specifically, there is no data for `art_periods`, `music_styles`, or `art_music_combos`.
*   **Missing `run-intent-blocked-personal.md`:** The absence of this file means there's no information on any blocked intent runs, which could be relevant for understanding past production decisions or issues.
*   **Brand vs. Personal:** The report explicitly warns against merging brand and personal suggestions, emphasizing deliberate comparison. This analysis focuses solely on the personal channel.
*   **Lack of CTR/Impressions:** The personal report notes that extending the fetcher for CTR and impressions is optional. Without this data, it's harder to understand top-of-funnel performance and optimize titles/thumbnails effectively.

## Insights

1.  **Long-form "deep_focus" and "piano_deep_calm" content drives significant watch time.** Videos like "Enter Flow State | 1 Hour Zero Distracti" (deep_focus) and "Calm Anxiety Fast | 1 Hour Deep Piano Re" (piano_deep_calm) are the top performers by views and watch time. "piano_deep_calm" videos, despite having a retention percentage 5.0% below the channel average, contribute +323.2 minutes vs. channel average in watch time per video, indicating their long-form nature successfully captures extended engagement.
2.  **Short-form content shows high retention but negligible watch time contribution.** Videos explicitly labeled "30 Seconds" or "30s" (e.g., "Find Your Strength," "Sounds for an Overactive Mind," "sleep_30s_20260124_031441") appear in the Top 5 by Retention with percentages as high as 96.8% and 83.6%. However, each of these videos only has 1 view, resulting in minimal overall watch time. This suggests that while viewers who click these short videos watch almost all of them, they are not a primary driver of total watch time.
3.  **"Ceremony" mood is an underperformer.** The `run-next` report highlights "ceremony" mood videos as underperforming, with retention 20.0% below the channel average and watch time per video -51.5 minutes vs. channel average (n=3, views=105). The `Performance by Mood` table also shows "ceremony" with a low average retention of 1.5%. This indicates a significant drop-off for this mood.
4.  **Speculative: Niche moods with high retention but low views could be explored cautiously.** While "warrior" and "trance" moods have very few views (5 and 7 respectively), their average retention percentages are high (78.0% and 40.5%). Similarly, "sleep" has 1 view but 83.6% retention. This suggests that for the few viewers these videos attract, the content is highly engaging.
5.  **Lack of diversity in metadata usage.** The `suggestions_personal.json` shows zero videos with views for `art_periods`, `music_styles`, and `art_music_combos`. This indicates that the current content generation or metadata tagging primarily relies on `mood`, missing opportunities to categorize and analyze performance across other potentially valuable dimensions.

## Experiments or packaging ideas

*   **Double down on 1-hour "deep_focus" and "piano_deep_calm" content:**
    *   Create more videos with titles similar to "Enter Flow State | 1 Hour Zero Distracti" and "Calm Anxiety Fast | 1 Hour Deep Piano Re."
    *   Experiment with slightly longer durations (e.g., 1.5 or 2 hours) for these high-performing moods, given their strong watch time.
    *   **Speculative:** Test variations in titles and thumbnails for these moods that emphasize "focus," "calm," "no distractions," and "anxiety relief."
*   **Re-evaluate "ceremony" content:**
    *   Analyze the specific "ceremony" videos that performed poorly. Are there common elements in their titles, thumbnails, or audio characteristics?
    *   **Speculative:** Consider pausing new "ceremony" content until further investigation, or experiment with significantly different packaging (titles, thumbnails) to see if external factors are the primary cause of low engagement.
*   **Test longer versions of high-retention, low-view moods:**
    *   For moods like "warrior," "trance," and "sleep" that show high retention on short clips but low views, produce a few longer-form (e.g., 30-60 minute) videos. This could capture the existing niche interest for a longer duration.
    *   **Speculative:** Ensure packaging for these longer videos clearly communicates the mood and potential use case (e.g., "Warrior Meditation," "Trance Focus Session," "Deep Sleep Aid").
*   **Explore new metadata dimensions:**
    *   Begin tagging videos with `art_periods` and `music_styles` (even if "none" is the initial value for some) to gather data for future analysis. This will allow for insights beyond just `mood`.
    *   **Speculative:** Introduce new content that intentionally combines different `moods` with `art_periods` or `music_styles` to see if unique combinations resonate with audiences.
*   **Implement CTR and impressions tracking:**
    *   Prioritize extending the personal fetcher to include CTR and impressions as suggested in `docs/PERSONAL_ANALYTICS.md`. This data is crucial for understanding how well titles and thumbnails attract clicks, which is a key precursor to watch time and retention.
