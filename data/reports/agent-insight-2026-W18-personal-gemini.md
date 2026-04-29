# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of personal channel analytics reports and related data files for 2026-W18. This analysis will summarize the channel's performance, highlight key insights from the data, and propose experiments or packaging ideas based on the available metrics.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md` (Personal channel Analytics Report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md` (Run next — personal advisory)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Personal channel suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw personal channel analytics data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md` (Missing file)

## Summary

For the period of April 1st to April 28th, 2026, the personal channel accumulated 783 total views and 4,991 minutes of watch time, gaining 4 subscribers. The overall average retention for videos with views is 21.63%, and the average watch time per video is approximately 113.4 minutes. "Piano_deep_calm" and "deep_focus" moods are the top performers in terms of total views, with "piano_deep_calm" showing a significantly higher watch time per video despite slightly lower retention than the channel average. Conversely, "ceremony" mood videos show underperformance in both retention and watch time per video. The majority of videos tracked (114) have analytics, but only 44 have recorded views, and a significant portion (71.9%) are joined with `generations.json` ledger rows.

## Risks / caveats

The `run-intent-blocked-personal.md` file is missing, which could indicate a blocked intent or a gap in the reporting pipeline. The advisory explicitly states that correlation does not imply causation, especially regarding mood/art-period labels and outcomes, as packaging (title, thumbnail, traffic source, seasonality) are significant confounders. The "Top 5 by Retention" table shows several videos with 1 or 2 views, leading to potentially misleadingly high retention percentages (e.g., 96.8%) that are not statistically robust. The `suggestions_personal.json` data indicates that there is no data for `art_periods`, `music_styles`, or `art_music_combos`, limiting insights into these dimensions.

## Insights

1.  **Deep Focus and Piano Calm are Strong Performers:** The "deep_focus" and "piano_deep_calm" moods consistently drive the most views and significant watch time. "Enter Flow State · 1 Hour Zero Distracti" (deep_focus) and "Calm Anxiety Fast · 1 Hour Deep Piano Re" (piano_deep_calm) are the top two videos by views and contribute substantially to total watch time. This suggests a strong audience preference for these moods, particularly in longer formats.
2.  **Piano Deep Calm Drives High Watch Time:** While "piano_deep_calm" has a retention percentage slightly below the channel average (-2.4%), it significantly outperforms the average in watch minutes per video (+360.2 minutes). This indicates that viewers who start these videos tend to watch them for a very long duration, making them highly valuable for overall channel watch time.
3.  **Short, High-Retention Videos Lack Overall Impact:** Videos like "Find Your Strength · 30 Seconds Power Dr" (warrior) and "Sounds for an Overactive Mind · 30 Secon" (deep_focus) show extremely high retention (96.8%) but only 1 view each. While high retention is generally good, with such low view counts, these short videos are not contributing meaningfully to overall channel growth or watch time in the current reporting window.
4.  **Ceremony Mood Underperforms:** The "ceremony" mood shows a notable underperformance, with retention percentage -19.3% below the channel average and watch minutes per video -71.1 minutes below the average. This suggests that content in this mood is not resonating well with the audience, leading to viewers dropping off quickly.
5.  **Speculative: Opportunity for Longer Deep Focus Content:** Given that "Enter Flow State · 1 Hour Zero Distracti" (deep_focus) is the top video by views (121) and has a decent watch time (299 minutes), and the "deep_focus" mood overall has strong views, there might be an opportunity to explore even longer-form content within this mood, or to create more variations of "deep_focus" videos that explicitly target "flow state" or "zero distraction" themes.

## Experiments or packaging ideas

*   **Double Down on "Piano Deep Calm" and "Deep Focus":**
    *   Create more 1-hour or longer videos in the "piano_deep_calm" and "deep_focus" moods, explicitly using titles that highlight "flow state," "zero distraction," or "calm anxiety."
    *   Experiment with different visual styles or subtle ambient elements within these moods to see if they further enhance engagement.
*   **Re-evaluate "Ceremony" Content:**
    *   Analyze the specific "ceremony" videos that underperformed. Are there commonalities in their titles, thumbnails, or sound design that could explain the low retention?
    *   Consider pausing new "ceremony" content until a clearer understanding of its performance issues is gained, or experiment with significantly different packaging (titles/thumbnails) for existing "ceremony" videos to see if it impacts CTR and retention.
*   **Test Longer Versions of High-Retention Short Videos:**
    *   For short videos with very high retention but low views (e.g., "Find Your Strength · 30 Seconds Power Dr" or "Sounds for an Overactive Mind · 30 Secon"), consider creating longer, 30-60 minute versions. This would test if the core mood/concept resonates over a longer duration, potentially converting high retention into significant watch time.
*   **Leverage "Binaural Beats & Solfeggio Frequencies":**
    *   The `analytics_personal.json` shows several videos mentioning "Uses binaural beats & Solfeggio frequencies for brainwave entrainment." This feature is highlighted in descriptions but not explicitly in the top-performing video titles or moods. Experiment with incorporating this benefit into titles or thumbnails for "deep_focus" or "piano_deep_calm" videos to see if it attracts a specific audience segment.
*   **Cross-Reference with Brand Metrics (Manual Step):**
    *   As suggested in the "Next steps (personal)" report, manually compare personal channel retention and watch time against brand weekly reports (e.g., `data/reports/2026-W15.md`) to identify any overarching trends or discrepancies between the two channels. This could inform a broader content strategy.
