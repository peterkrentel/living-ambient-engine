# Agent advisory — Gemini (API) (brand, 2026-W19)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of committed repository files and analytics pipeline excerpts for the 2026-W19 period. My analysis will focus on identifying patterns in video performance, highlighting areas of success and potential for improvement based solely on the given data.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W19.md` (Analytics Report - 2026-W19)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W19.md` (Run next — advisory (2026-W19))
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked.md` (Run intent — BLOCKED)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions.json` (Suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics.json` (Raw analytics data)

## Summary

The channel had a total of 867 views and 731 minutes of watch time, gaining 2 subscribers over the `2026-04-12` to `2026-05-09` analytics window. The "art_creator" mood category, despite having a lower average retention (18.2%), generated the vast majority of views (690 views from 230 videos). Micro-duration videos, particularly those with "micro_focus_lock" and "piano_relax" moods, show exceptionally high retention percentages, with one "micro_focus_lock" video reaching 252.9% retention. The automated planner was blocked this week due to no actionable mood increases passing the gate, indicating insufficient data or performance thresholds for automated scaling.

## Risks / caveats

The `run-next-2026-W19.md` explicitly states that "CTR, impressions, and retention often move because of title, thumbnail, traffic source, and seasonality — not because a mood or art-period label 'caused' an outcome." This means that while correlations are observed, direct causation by generation parameters (like mood or art period) cannot be assumed without further controlled experimentation on packaging. Many mood categories have very few videos or views, making their average retention highly susceptible to single-video performance and not statistically robust. For instance, "micro_focus_lock" has only 1 video with 5 views, yet its retention is extremely high. The `generations.json` join coverage is low (13.6% identity-aligned), suggesting a significant portion of tracked videos may lack detailed generation parameter metadata, limiting deeper analysis.

## Insights

1.  **Micro-duration videos demonstrate exceptional retention:** The top 5 videos by retention are all short-duration "micro_" or "30 Seconds" videos, with retention percentages ranging from 91.8% to an astounding 252.9%. This suggests that when viewers engage with these short, targeted pieces, they often re-watch them or loop them, indicating high utility for specific, immediate needs like "Enter Flow State" or "Mental Clarity."
2.  **"art_creator" mood drives overall views, but with lower retention:** The "art_creator" mood category accounts for the bulk of total views (690 out of 867) and has the most videos (230). However, its average retention is 18.2%, which is below the overall average of 27.22%. This indicates that while these videos attract viewers, they might not hold attention as effectively as other, more niche moods.
3.  **Speculative: "Ancient" and "Future" art periods with "Taiko" and "None" music styles are strong performers within "art_creator":** The top videos by views are all within the "art_creator" mood, specifically "Ambient ancient · 5 Mins · Evolving taik" (134 views) and "Ambient ancient · 5 Mins · Evolving kuku" (86 views), followed by "Ambient future · 5 Mins · Evolving none" (77 views). This suggests that the combination of "ancient" or "future" aesthetics with specific musical styles like "taiko" or a "none" (perhaps more minimalist) approach resonates well with viewers, driving initial clicks.
4.  **Underperforming moods with existing content:** Several moods, such as "deep_focus," "rain_sleep," "ceremony," "warrior," "energize," and various "micro_" moods, have videos but zero views in the analytics window. This could indicate issues with discoverability, packaging (titles/thumbnails), or lack of audience interest for these specific themes.
5.  **Planner blocked due to insufficient actionable data:** The planner was blocked because no mood suggestions met the criteria for an "actionable increase" (n≥5, group_views≥200). This highlights a need for more robust data collection or a re-evaluation of the thresholds, as many moods have low video counts and views, preventing them from ever becoming "actionable" under current rules, despite some showing promising retention.

## Experiments or packaging ideas

*   **Create more micro-duration content:** Given the extremely high retention of "micro_focus_lock" and "piano_relax" videos, experiment with producing more short-form content (e.g., 10-30 seconds to 1 minute) targeting specific, immediate needs or states.
*   **Analyze packaging of top "art_creator" videos:** Investigate the titles, thumbnails, and descriptions of the top-performing "Ambient ancient · 5 Mins · Evolving taik" and "Ambient future · 5 Mins · Evolving none" videos. Identify common elements that might contribute to their higher view counts and apply these learnings to other "art_creator" content.
*   **Test variations of "art_creator" content:** Experiment with different combinations of art periods and music styles within the "art_creator" mood, particularly focusing on "ancient" and "future" art periods with "taiko" and "none" music styles, to see if the success is repeatable.
*   **Re-evaluate and re-package zero-view moods:** For moods like "deep_focus," "rain_sleep," and "energize" that have videos but no views, consider updating their titles, thumbnails, and descriptions to improve discoverability and appeal.
*   **Introduce A/B testing for titles/thumbnails:** To address the confounder risk, implement a systematic approach to A/B test different titles and thumbnails for new videos, especially for promising moods or art/music combinations, to isolate the impact of packaging on CTR and views.
