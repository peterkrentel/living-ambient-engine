# Agent advisory — Gemini (API) (brand, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of analytics reports, suggestions, and raw analytics data for the 2026-W18 period. My analysis will focus on identifying patterns in video performance, highlighting risks, and proposing experiments based on the available metrics, while acknowledging any data limitations.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18.md`: Main analytics report for the period 2026-03-31 to 2026-04-27, detailing total views, watch time, subscribers, and top videos by retention and views. It also includes performance broken down by mood.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18.md`: Advisory report for the week, including brand snapshot metrics, a note on packaging confounders, and confirmation that no actionable suggestions passed the planner gate.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked.md`: Explicit confirmation that the planner was blocked due to a lack of qualifying mood suggestions.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions.json`: Raw JSON data detailing coverage of moods, art periods, music styles, and their combinations, including counts of videos with and without views.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics.json`: Raw JSON data for individual video metrics, including titles, descriptions, publication dates, and performance metrics (views, watch time, retention, etc.).

## Summary

The channel experienced a total of 1,201 views and 827 minutes of watch time, gaining 4 subscribers over the 28-day analytics window. The `art_creator` mood category, encompassing 230 videos, dominates total views with 1,123 views, though its average retention is 17.6%. Several "micro" moods show exceptionally high retention percentages, albeit with very low view counts (1-2 views). The planner was blocked this week as no mood suggestions met the actionable thresholds (n≥5 videos, group_views≥200). The overall average retention for the channel is 24.52%.

## Risks / caveats

*   **Low View Counts for High Retention:** The "Top 5 by Retention" list is heavily skewed by videos with only 1 or 2 views, leading to inflated retention percentages (e.g., 559.0% for "30 Seconds to Enter Flow State"). These numbers are not statistically significant and should not be used to drive production decisions without further data.
*   **Planner Blocked:** The lack of actionable suggestions from the planner indicates insufficient data or performance within defined thresholds to confidently recommend scaling specific moods. This means any "insights" derived from this report are largely exploratory.
*   **Confounders:** The `run-next` report explicitly warns against treating bucket-level correlation as proof that generation parameters drove a result, as packaging (title, thumbnail, traffic source, seasonality) can significantly influence CTR, impressions, and retention.
*   **Data Coverage:** Only 123 out of 354 videos had views in the analytics window, and only 48 videos were identity-aligned with `generations.json`, suggesting a significant portion of the content lacks detailed metadata linkage or has not yet gained traction. Many moods and art/music combos in `suggestions.json` have 0 views, making it impossible to assess their performance.

## Insights

1.  **Dominance of `art_creator` Mood:** The `art_creator` mood category accounts for the vast majority of views (1,123 out of 1,201 total views). This suggests that content categorized under `art_creator` is currently the primary driver of channel traffic, despite its average retention being moderate at 17.6%. The top 5 videos by views are all `art_creator` videos, indicating a strong correlation between this mood and overall viewership.
2.  **Strong Performance of "Ancient" and "Contemporary" Art Periods:** Within the `art_creator` mood, videos tagged with "Ambient ancient" and "Ambient contemporary" are leading in views. "Ambient ancient | 5 Mins | Evolving taik" has 237 views and 161 minutes of watch time, while "Ambient contemporary | 5 Mins | Evolving" has 105 views and 51 minutes. This suggests these specific art period themes resonate well with the audience.
3.  **High Retention for "Micro" Focus/Relaxation Content (Low Volume):** Videos like "30 Seconds to Enter Flow State" (`micro_focus_lock`) and "Let Go of Stress | 30 Seconds Soft Piano" (`piano_relax`) show extremely high retention (559.0% and 97.1% respectively). While these have only 1-2 views, their short duration combined with high retention indicates a potential niche for very brief, targeted ambient experiences.
4.  **Speculative: Potential for "Evolving" Soundscapes:** Many of the top-performing videos by views include "Evolving" in their titles (e.g., "Ambient ancient | 5 Mins | Evolving taik", "Ambient contemporary | 5 Mins | Evolving"). This phrasing might be a successful packaging element, suggesting a dynamic and non-repetitive listening experience, which could appeal to users seeking fresh ambient content.
5.  **Underperforming Moods with Zero Views:** A significant number of moods, such as `ocean_waves`, `deep_focus`, `rain_sleep`, `ceremony`, `warrior`, and various "micro" moods, have 0 views despite having videos published. This could be due to poor discoverability, lack of audience interest, or ineffective packaging for these specific themes.

## Experiments or packaging ideas

*   **Experiment with "Micro" Mood Packaging:**
    *   Create more videos in the `micro_focus_lock` and `piano_relax` moods, but with more descriptive and benefit-oriented titles (e.g., "Instant Calm: 30-Second Soft Piano for Stress Relief").
    *   Test different thumbnail styles for these short-form videos to clearly communicate their quick, targeted benefit.
*   **Double Down on `art_creator` with Top Art Periods:**
    *   Produce more content combining "ancient" and "contemporary" art periods with various music styles, particularly those that have shown some views (e.g., "taiko", "none", "game").
    *   Analyze the specific visual aesthetics or sound profiles of the top-performing "ancient" and "contemporary" videos to inform future generations.
*   **Test "Evolving" Keyword in Titles:**
    *   For new content, consistently use "Evolving" or similar language in titles to highlight the non-repetitive nature of the soundscapes, as this seems to be a common thread among top performers.
*   **Re-evaluate Underperforming Moods:**
    *   For moods with 0 views (e.g., `ocean_waves`, `deep_focus`, `rain_sleep`), review their existing titles and thumbnails. Experiment with completely different packaging strategies (e.g., more direct problem/solution titles like "Fall Asleep Fast: Gentle Ocean Waves for Deep Sleep").
    *   **Speculative:** Consider if some moods are too niche or if the current audio generation for them is not compelling enough.
*   **Focus on Longer-Form `art_creator` Content:**
    *   Given the high views and watch time for 5-minute `art_creator` videos, explore producing longer versions (e.g., 10-15 minutes) of the most successful "ancient" and "contemporary" themes to capture more watch time from engaged viewers.
