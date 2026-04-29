# Agent advisory — Gemini (API) (brand, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of committed repository files and analytics pipeline excerpts for 2026-W18. My goal is to synthesize this information into actionable insights and suggest experiments for the YouTube ambient music channel, focusing on metrics like views and retention.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18.md`: The primary analytics report for the period 2026-04-01 to 2026-04-28, detailing total views, watch time, subscribers, and top performers by retention and views, as well as performance by mood.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18.md`: The machine-assembled advisory report, including brand snapshot metrics, evidence paths, and a note that the planner was blocked.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked.md`: A specific report indicating why the planner was blocked for this week, citing a lack of qualifying mood suggestion rows.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions.json`: A JSON file containing overall channel metrics and coverage data for moods, art periods, music styles, and their combinations.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics.json`: A comprehensive JSON file with detailed metrics for individual videos, including titles, descriptions, and performance data.

## Summary

The channel generated 1,191 views and 836 minutes of watch time across 352 videos in the last 28 days, gaining 4 subscribers. The `art_creator` mood category dominates views, accounting for 1,093 views from 230 videos, though its average retention is 17.7%. Several "micro" moods show exceptionally high retention percentages, albeit with very low view counts (1-2 views). The planner for this week was blocked due to insufficient data to identify actionable mood increases, specifically lacking mood suggestions that passed the `n>=5, group_views>=200` threshold.

## Risks / caveats

*   **Low View Counts for High Retention:** The "Top 5 by Retention" videos have extremely low view counts (1-2 views). The 559.0% retention for "30 Seconds to Enter Flow State" is an outlier and likely a data anomaly given the short duration and low views, making it unreliable for drawing broad conclusions. Similarly, other high-retention videos with 1 view are not statistically significant.
*   **Confounders & Packaging:** The `run-next` report explicitly warns against treating bucket-level correlation as proof that generation parameters drove a result when packaging (title, thumbnail, traffic source, seasonality) differed. This is crucial as the data does not provide insights into these packaging elements.
*   **Planner Blocked:** The lack of actionable suggestions from the planner means there are no automatically identified "lean in" or "tread carefully" categories based on the defined thresholds. This indicates thin data for robust, automated recommendations.
*   **Limited Data for Many Moods:** Many moods listed in `Performance by Mood` and `suggestions.json` have very few videos or zero views, making it impossible to assess their performance accurately. For example, `ocean_waves`, `deep_focus`, `rain_sleep`, and several "micro" moods have 0 views.

## Insights

1.  **Dominance of `art_creator` Mood:** The `art_creator` mood is by far the most prolific and viewed category, with 230 videos generating 1,093 views. While its average retention is 17.7%, which is below the overall average of 24.85%, its sheer volume of content and views suggests it's a primary driver of overall channel activity. The top 5 videos by views are all `art_creator` videos, with "Ambient ancient · 5 Mins · Evolving taik" leading with 224 views and 156 minutes of watch time.
2.  **High Retention in Niche "Micro" Moods (with caveats):** Several "micro" moods show impressive retention percentages, such as `micro_focus_lock` (559.0%), `piano_relax` (97.1%), `micro_drop_inward` (91.8%), and `micro_noise_hush` (84.0%). However, these are based on 1-2 views, making them highly unreliable indicators of scalable success. The `piano_relax` mood, despite having only 2 videos and 1 view, shows strong retention, which might be worth exploring further if more data becomes available.
3.  **Speculative: Potential for "Ancient" and "Contemporary" Art Periods with Specific Music Styles:** Looking at the top 5 videos by views, "Ambient ancient · 5 Mins · Evolving taik" and "Ambient ancient · 5 Mins · Evolving kuku" perform well. Similarly, "Ambient contemporary · 5 Mins · Evolving" and "Ambient future · 5 Mins · Evolving none" also rank high. This suggests that art periods like `ancient`, `contemporary`, and `future`, especially when combined with music styles like `taiko`, `kuku`, or `none` (implying a more general ambient sound), resonate with viewers.
4.  **Speculative: Short-form Content for Specific States:** The high retention (even if on low views) for titles like "30 Seconds to Enter Flow State" and "10 Seconds to Drop Inward" suggests a potential interest in very short, targeted ambient tracks designed for quick mental shifts. While the data is too thin to confirm, this could indicate a niche for "micro-dose" ambient experiences.
5.  **Underperforming Categories:** Many moods, including `ocean_waves`, `deep_focus`, `rain_sleep`, `ceremony`, `warrior`, and `energize`, have 0 views despite having multiple videos. This indicates either a lack of discoverability, poor packaging, or low audience interest in these specific categories. `fireplace` also has very low retention (0.3%) despite 5 videos and 3 views.

## Experiments or packaging ideas

*   **Focus on `art_creator` variations:**
    *   Create more `art_creator` videos, specifically exploring combinations that have shown some success, such as `ancient+taiko`, `ancient+kuku`, `contemporary+none`, and `future+none`.
    *   Experiment with different titles and thumbnails for these `art_creator` combinations to improve CTR and impressions, as packaging is a known confounder.
*   **Investigate `piano_relax`:**
    *   Generate a small batch of 3-5 new `piano_relax` videos. Given its high retention (97.1% on 1 view), even with limited data, it warrants further testing to see if the retention holds with more views.
    *   Use titles that clearly communicate the mood, e.g., "Soft Piano for Relaxation," "Gentle Piano for Stress Relief."
*   **Test "Micro-Dose" Ambient:**
    *   Produce a small series of very short (e.g., 30-60 second) videos explicitly designed for quick mental shifts, similar to "30 Seconds to Enter Flow State."
    *   Monitor retention and views closely to see if this format gains traction, acknowledging the current data is highly speculative.
*   **Re-evaluate zero-view moods:**
    *   For moods with 0 views (e.g., `ocean_waves`, `deep_focus`, `rain_sleep`), review their existing titles and thumbnails. Consider re-packaging a few existing videos with new titles/thumbnails to see if discoverability improves.
    *   Alternatively, pause production on these categories until there's a clearer signal of audience interest or a specific hypothesis for their underperformance.
*   **A/B Test Titles for Top Performers:**
    *   For existing top-performing `art_creator` videos (e.g., "Ambient ancient · 5 Mins · Evolving taik"), consider creating slightly varied titles or thumbnails and re-uploading them as new videos (if channel policy allows) to A/B test packaging effectiveness.
*   **Explore `chill` and `micro_overthink_b`:**
    *   The `chill` mood has 11 videos with 9 views and 36.8% average retention, which is above the overall average. `micro_overthink_b` has 1 video, 3 views, and 60.5% retention. These might be worth a small, cautious increase in content generation to gather more data.
