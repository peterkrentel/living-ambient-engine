# Agent advisory — Gemini (API) (brand, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of analytics reports and suggestions for 2026-W18. My analysis will focus on identifying patterns in video performance, highlighting risks, and proposing experiments based solely on the data presented in these files.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18.md` (Main Analytics Report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18.md` (Run Next Advisory)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked.md` (Run Intent Blocked Report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions.json` (Suggestions Data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics.json` (Raw Analytics Data)

## Summary

The channel had a total of 1,223 views and 855 minutes of watch time, gaining 4 subscribers over the analytics window (2026-03-31 to 2026-04-27). The "art_creator" mood dominates in terms of total videos (230) and views (1,125), but its average retention is relatively low at 17.9%. Several "micro" moods show exceptionally high retention percentages, albeit with very low view counts (1-2 views). The planner for this week was blocked due to a lack of actionable mood increases passing the defined gates (n≥5, group_views≥200).

## Risks / caveats

*   **Low View Counts for High Retention:** Many of the top retention videos have only 1 or 2 views. This makes their high retention percentages highly susceptible to statistical noise and not indicative of broad audience engagement. For example, "30 Seconds to Enter Flow State" has 559.0% retention with only 2 views, which is an anomaly likely due to repeat viewing by a single user or a technical artifact.
*   **Confounders & Packaging:** The `run-next-2026-W18.md` explicitly states that "CTR, impressions, and retention often move because of title, thumbnail, traffic source, and seasonality — not because a mood or art-period label 'caused' an outcome." This means that observed correlations between moods/styles and performance metrics should not be directly attributed to the generation parameters without considering external packaging factors.
*   **Planner Blocked:** The `run-intent-blocked.md` report indicates that no mood suggestions met the criteria for actionable increases (n≥5, group_views≥200). This suggests a lack of sufficiently strong, broad performance trends to confidently recommend scaling specific moods.
*   **Data Coverage:** Only 124 out of 354 videos had views in the analytics window, and only 48 videos were "identity-aligned" with `generations.json`. This means a significant portion of the channel's content is not actively contributing to the current performance metrics or is not fully tracked in the generation ledger.
*   **Short Video Focus:** The top retention videos are all very short (30 seconds, 5 minutes, 10 seconds). While they show high retention, their contribution to overall watch time might be limited compared to longer-form content.

## Insights

1.  **"art_creator" Mood Dominance:** The "art_creator" mood category is by far the most prolific and viewed, accounting for 230 videos and 1,125 views. This suggests a strong content pipeline for this category and some audience interest, despite its average retention being moderate at 17.9%. The top 5 videos by views are all within this mood, featuring various art periods and music styles.
2.  **Micro-Duration, High-Retention Niche:** Videos like "30 Seconds to Enter Flow State" (micro_focus_lock, 559.0% retention, 2 views) and "10 Seconds to Drop Inward" (micro_drop_inward, 91.8% retention, 1 view) demonstrate extremely high retention percentages for very short durations. **Speculative:** While views are low, this could indicate a strong, albeit small, demand for ultra-short, highly targeted ambient experiences. The "piano_relax" mood also shows high retention (97.1%) with one view for a 30-second video.
3.  **Ancient and Future Themes Resonate:** Among the "art_creator" videos, "Ambient ancient · 5 Mins · Evolving taik" (237 views) and "Ambient future · 5 Mins · Evolving none" (93 views) are top performers by views. This suggests that themes evoking historical or futuristic aesthetics, combined with specific music styles like Taiko or a "none" style, are currently capturing audience attention.
4.  **Underperforming Moods:** Several moods, such as "ocean_waves," "deep_focus," "rain_sleep," "ceremony," "warrior," "energize," and various "micro" moods (e.g., micro_energy_boost, micro_clarity_sharp), have 0 views despite having multiple videos. This indicates either a lack of discovery, poor packaging, or no audience interest for these specific themes in the current analytics window.
5.  **Music Style Impact within "art_creator":** Within the top-viewed "art_creator" videos, "taiko" and "none" (music styles) appear frequently, suggesting these might be more engaging than others. "Ambient ancient · 5 Mins · Evolving taik" is the clear leader in views, indicating a strong combination of mood, art period, and music style.

## Experiments or packaging ideas

*   **Test more "micro" content with clear utility:** Given the high retention of "micro" videos, create more short-form content (e.g., 30 seconds to 1 minute) with explicit, benefit-driven titles (e.g., "30 Seconds to Reset Your Mind," "1-Minute Focus Boost").
*   **Re-package high-view "art_creator" videos:** Analyze the titles and thumbnails of "Ambient ancient · 5 Mins · Evolving taik" and "Ambient future · 5 Mins · Evolving none" to identify successful packaging elements. Apply these learnings to other "art_creator" videos, especially those with similar art periods or music styles.
*   **Explore longer versions of high-retention "micro" videos:** For "micro_focus_lock" and "micro_drop_inward," consider creating 5-minute or 10-minute versions, maintaining the core sound and mood, to see if the high retention translates to longer watch times with a broader audience.
*   **Targeted promotion for underperforming moods:** For moods with 0 views but existing content (e.g., "ocean_waves," "deep_focus"), experiment with different titles, descriptions, and thumbnails to improve discoverability. This could involve A/B testing or specific social media pushes.
*   **Investigate "piano_relax" further:** The "Let Go of Stress · 30 Seconds Soft Piano" video has excellent retention (97.1%) with one view. Explore creating more "piano_relax" content, perhaps at slightly longer durations (e.g., 2-5 minutes), to see if this mood can attract more views while maintaining high engagement.
