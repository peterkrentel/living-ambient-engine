# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of personal channel analytics reports and suggestions for Week 18, 2026. My analysis will focus on identifying key performance trends, risks, and actionable insights based solely on this data, concluding with experiment and packaging ideas.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md` (Personal channel analytics report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md` (Run next — personal advisory)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Personal channel suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw personal channel analytics data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md` (Missing file)

## Summary

The personal channel generated 728 total views and 3,730 minutes of watch time, gaining 4 subscribers over the `2026-03-30` to `2026-04-26` analytics window. The overall average retention is 20.22%, with an average watch time of 82.889 minutes per video. "Piano_deep_calm" and "deep_focus" moods are leading in total views, while "warrior" and "sleep" moods show exceptionally high retention percentages on videos with very low view counts. The "ceremony" mood is identified as an underperformer in both retention and watch time per video.

## Risks / caveats

*   **Low View Counts for High Retention Videos:** Several videos with very high retention (e.g., "Find Your Strength" at 96.8%, "sleep_30s" at 83.6%) have only 1 or 2 views. This makes their high retention statistically unreliable for broader conclusions.
*   **Confounders & Packaging:** The `run-next` report explicitly states that CTR, impressions, and retention are often influenced by title, thumbnail, traffic source, and seasonality, not solely by mood or art-period labels. Correlation does not imply causation, and packaging differences across videos are a significant confounder.
*   **Limited Data for Many Moods:** Many moods (e.g., piano_evening, rain_piano, chill, lofi_study, ocean_waves) have 0 views, making it impossible to assess their performance.
*   **Missing `run-intent-blocked-personal.md`:** The absence of this file means any blocked intent for the personal channel is not visible in this bundle.
*   **No CTR or Impressions Data:** The personal fetcher has not been extended to include CTR or impressions, which are crucial metrics for understanding discoverability and initial engagement.
*   **Thin Data for Art Periods/Music Styles:** The `suggestions_personal.json` shows zero total videos and zero videos with views for all listed `art_periods` and `music_styles`, as well as `art_music_combos`. This means no insights can be drawn from these categories.

## Insights

1.  **High Watch Time for "Piano_deep_calm" and "Deep_focus":** The moods "piano_deep_calm" and "deep_focus" are significant drivers of watch time. "Calm Anxiety Fast" (piano_deep_calm) generated 806 and 793 minutes of watch time from 53 and 47 views respectively, while "Enter Flow State" (deep_focus) garnered 298 minutes from 119 views. This suggests a strong audience need for these calming and focus-oriented piano sounds.
2.  **Retention vs. Views Discrepancy:** There's a clear split between videos with high retention and those with high views. Videos like "Find Your Strength" (warrior, 96.8% retention) and "sleep_30s" (sleep, 83.6% retention) have excellent retention but only 1 view each. Conversely, top-viewed videos like "Enter Flow State" (deep_focus) and "Calm Anxiety Fast" (piano_deep_calm) have lower average retention (15.7% and 16.9% for their respective moods) but contribute significantly to overall watch time. This indicates that while some short, niche content might hook the few viewers it gets, longer, more broadly appealing content drives overall engagement.
3.  **"Ceremony" Mood Underperformance:** The "ceremony" mood shows poor performance, with an average retention of 1.5% and a negative deviation in watch time per video (-42.6 min vs. channel avg). Despite having 11 videos, its total views are only 129, indicating it's not resonating well with the current audience.
4.  **Speculative: Potential for Short, High-Retention Content:** The existence of 30-second videos like "Find Your Strength" (warrior) and "sleep_30s" (sleep) with extremely high retention, even with minimal views, suggests that very short, targeted content *could* be highly engaging for its intended purpose if discoverability were improved. The "trance" mood also shows a relatively high average retention of 39.7% across 10 videos, despite low total views (6).
5.  **Speculative: Long-Form Content Dominates Watch Time:** The top-performing videos by watch time are all 1-hour or longer ("Enter Flow State | 1 Hour Zero Distracti", "Calm Anxiety Fast | 1 Hour Deep Piano Re"). This reinforces the idea that for ambient music, longer formats are crucial for accumulating significant watch time, even if their average retention percentage is lower than very short clips.

## Experiments or packaging ideas

*   **Prioritize "Piano_deep_calm" and "Deep_focus" Long-Form Content:**
    *   Create more 1-hour+ videos in the "piano_deep_calm" and "deep_focus" moods, leveraging titles that emphasize "flow state," "calm anxiety," and "zero distraction."
    *   **Speculative:** Experiment with titles that explicitly mention the duration (e.g., "1 Hour," "2 Hours") as this seems to be a common pattern in top-performing titles.
*   **Re-evaluate "Ceremony" Mood:**
    *   Investigate the packaging (titles, thumbnails) of "ceremony" videos to understand if discoverability or initial appeal is the issue, given its low retention and watch time.
    *   Consider pausing new "ceremony" content until further analysis or a clear strategy emerges.
*   **Test Discoverability for High-Retention, Low-View Content:**
    *   For moods like "warrior," "sleep," and "trance" that show high retention on short clips, create new, longer versions (e.g., 1-hour versions of "Find Your Strength" or "sleep" tracks) to see if the high engagement translates to longer formats and more views.
    *   **Speculative:** Promote these high-retention short clips on other platforms (e.g., TikTok, Instagram Reels) to drive traffic to the YouTube channel and test their broader appeal.
*   **Expand Analytics to Include CTR and Impressions:**
    *   As suggested in the `Next steps (personal)` and `run-next` reports, extend the personal fetcher to gather CTR and impressions data. This is critical for understanding why videos are or aren't getting views, especially for those with high retention but low view counts.
*   **Experiment with "Rain_sleep" and "Fireplace" Moods:**
    *   These moods have some views (24 and 1 respectively) and decent retention (2.0% and 47.8%). While low view counts make retention less reliable, they are established ambient categories.
    *   **Speculative:** Create new content in these moods, perhaps combining them with "piano_deep_calm" or "deep_focus" elements, to see if they can capture more audience attention.
