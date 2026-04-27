# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of personal channel analytics reports and suggestions for Week 18, 2026. This analysis will summarize the channel's performance, highlight key insights from the data, and propose experiments or packaging ideas based on the findings.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md` (Personal channel analytics report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md` (Personal advisory and correlation report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Detailed suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw analytics data for individual videos)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md` (This file was missing)

## Summary

The personal channel tracked 114 videos during the analytics window (2026-03-30 to 2026-04-26), accumulating 755 total views and 4,224 minutes of watch time, gaining 4 subscribers. The overall average retention for videos with views is 22.33%, and the average watch time per video is approximately 91.8 minutes.

"Deep focus" and "piano_deep_calm" moods are performing well in terms of views and watch time, with "Calm Anxiety Fast | 1 Hour Deep Piano Re" being a standout performer for watch time. Short "30 Seconds" videos, particularly "Find Your Strength" (warrior) and "Sounds for an Overactive Mind" (deep_focus), show exceptionally high retention percentages, though with very low view counts. Conversely, the "ceremony" mood shows significantly lower retention and watch time per video compared to the channel average.

A significant portion of videos (71.9%) have some record in `generations.json`, but only 31.6% are identity-aligned, suggesting potential gaps in metadata or logging for older uploads.

## Risks / caveats

*   **Low View Counts:** Many of the top retention videos have only 1 view, making their high retention percentages unreliable indicators of broader audience engagement. This is explicitly stated in the report for "Find Your Strength" and "Sounds for an Overactive Mind".
*   **Confounders:** The `run-next` report explicitly warns that CTR, impressions, and retention are influenced by packaging (title, thumbnail, traffic source, seasonality) and not solely by mood or art-period labels. Therefore, correlations should not be treated as causal proof for generation parameters without considering packaging.
*   **Missing Data:** The `run-intent-blocked-personal.md` file was missing, which could indicate a blocked intent or a gap in the reporting process.
*   **Limited Metrics:** The personal report lacks CTR and impressions data, which are crucial for understanding audience discovery and initial engagement. The "Next steps" section suggests extending the personal fetcher to include these.
*   **Exploratory Data:** Some suggestions are based on "low n / views" or "exploratory" data, which means they might not be statistically robust.

## Insights

1.  **Deep Focus and Piano Deep Calm Drive Watch Time:** The moods "deep_focus" and "piano_deep_calm" are strong performers for total views and watch time. "Enter Flow State" (deep_focus) has the highest views at 299, and "Calm Anxiety Fast" (piano_deep_calm) has the highest watch time at 867 minutes (for one instance) and 854 minutes (for another instance). The `run-next` report confirms "piano_deep_calm" has +323.2 min vs channel avg watch time per video, despite a -5.0% retention vs channel avg. This suggests that while not every viewer stays for the entire duration, those who do watch for a very long time.
2.  **Short-Form Content Shows High Retention Potential (with caveats):** Videos like "Find Your Strength" (warrior) and "Sounds for an Overactive Mind" (deep_focus) in 30-second formats show exceptionally high retention (96.8% and 96.8% respectively). However, these each have only 1 view, making it difficult to draw definitive conclusions about their broad appeal.
3.  **"Ceremony" Mood Underperforms:** The "ceremony" mood has a significantly lower average retention (1.5%) and watch time per video (-51.5 min vs channel avg) compared to the channel average, despite having 11 videos and 131 total views. This indicates a potential area for deprioritization or re-evaluation.
4.  **Speculative: Long-form Piano Content for Anxiety Relief is a Niche:** The top performing videos by watch time, "Calm Anxiety Fast | 1 Hour Deep Piano Re", strongly suggest a demand for long-form, calming piano music specifically targeted at anxiety relief. The titles clearly communicate the benefit and duration.
5.  **Speculative: Short, Punchy Moods for Quick Impact:** While view counts are low, the high retention of 30-second videos like "Find Your Strength" (warrior) and "Sounds for an Overactive Mind" (deep_focus) could indicate a potential for very short, targeted ambient tracks designed for immediate, intense mood shifts or quick breaks.

## Experiments or packaging ideas

*   **Double Down on "Piano Deep Calm" and "Deep Focus" Long-Form:**
    *   Create more 1-hour or longer videos in the "piano_deep_calm" and "deep_focus" moods, explicitly targeting benefits like "Calm Anxiety Fast" or "Enter Flow State."
    *   **Packaging:** Use clear, benefit-driven titles and thumbnails that emphasize relaxation, focus, and anxiety relief.
*   **Investigate High-Retention Short Videos:**
    *   Produce a small batch of new 30-second videos in the "warrior" and "deep_focus" moods, but with more varied titles and thumbnails to see if higher view counts can be achieved while maintaining high retention.
    *   **Packaging:** Experiment with titles like "30-Second Power Boost" or "Instant Focus Reset."
*   **Re-evaluate or Deprioritize "Ceremony" Mood:**
    *   Analyze the specific "ceremony" videos to understand why retention is so low. Are the titles, thumbnails, or actual audio content failing to meet expectations?
    *   Consider deprioritizing new content in this mood unless specific improvements can be identified and tested.
*   **Speculative: Explore "Sleep" and "Trance" for Retention:**
    *   The "sleep" mood has an 83.6% retention (from 1 video), and "trance" has 40.5% (from 10 videos). While views are low, these moods show promising retention.
    *   **Packaging:** Experiment with longer-form content for "sleep" and "trance" with titles that clearly indicate their purpose (e.g., "Deep Sleep Ambient," "Trance Inducing Focus Music").
*   **Address Missing Metrics (CTR, Impressions):**
    *   Prioritize extending the personal fetcher to include CTR and impressions as suggested in the "Next steps." This will provide crucial data for understanding how viewers discover content and initial engagement, which is vital for optimizing packaging.
