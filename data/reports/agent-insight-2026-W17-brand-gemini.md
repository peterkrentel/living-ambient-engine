# Agent advisory — Gemini (API) (brand, 2026-W17)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of analytics reports, suggestions, and raw analytics data for the 2026-W17 period. My goal is to synthesize this information into actionable insights and potential experiments for the YouTube ambient music channel, focusing on metrics like views and retention.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W17.md`: The primary analytics report for the week, summarizing total views, watch time, subscribers, and top videos by retention and views, as well as performance by mood.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W17.md`: The "Run next" advisory, including brand snapshot metrics, evidence paths, and a note on the planner being blocked.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked.md`: A specific report indicating why the planner was blocked for this week.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions.json`: Detailed coverage data for moods, art periods, music styles, and their combinations, along with overall channel metrics.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics.json`: Raw, detailed metrics for individual videos, including titles, descriptions, and performance data.

## Summary

The channel had a total of 1,297 views and 953 minutes of watch time, gaining 4 subscribers during the `2026-03-29` to `2026-04-25` analytics window. The `art_creator` mood category dominates in terms of total views (1,235 views from 230 videos), though its average retention is 19.1%. Several "micro" mood videos show exceptionally high retention percentages, albeit with very low view counts (1-2 views). The "Run next" planner was blocked due to a lack of qualifying mood suggestions passing the actionable thresholds (n≥5, group_views≥200).

## Risks / caveats

*   **Low View Counts for High Retention:** The top retention videos have extremely low view counts (1-2 views), making their high retention percentages (e.g., 559.0%, 99.7%) statistically unreliable for broad conclusions. These are likely anomalies or internal testing views.
*   **Confounders & Packaging:** The `run-next` report explicitly warns against treating bucket-level correlation as proof that generation parameters drove a result when packaging (title, thumbnail, traffic source, seasonality) differed. This means observed performance could be due to factors outside of the mood/art-period/music-style labels.
*   **Limited Actionable Data:** The planner being blocked indicates a lack of statistically significant trends that meet the defined thresholds for "actionable" suggestions. This means most insights will be exploratory.
*   **Data Coverage:** Only 121 out of 354 total videos had views, and only 62 videos had a `generations.json` join (with 48 being identity-aligned). This suggests a significant portion of the content either hasn't been viewed or isn't fully tracked in the generation ledger, limiting comprehensive analysis.

## Insights

1.  **Dominance of `art_creator` mood:** The `art_creator` mood category accounts for the vast majority of views (1,235 out of 1,297 total views) and videos (230 out of 354 tracked). While its average retention is moderate at 19.1%, its sheer volume of content and views makes it the primary driver of channel performance. This suggests that content categorized under `art_creator` resonates most broadly with the current audience.
2.  **Strong performance of "ancient" and "contemporary" art periods with specific music styles:** The top-viewed videos, "Ambient ancient | 5 Mins | Evolving taik | art_creator" (287 views, 239 min watch time) and "Ambient contemporary | 5 Mins | Evolving | art_creator" (105 views, 51 min watch time), indicate that the "ancient" and "contemporary" art periods, particularly when combined with music styles like "taiko" and potentially "none" (as seen in "Ambient future | 5 Mins | Evolving none"), are attracting significant viewership within the `art_creator` mood.
3.  **High retention in "micro" moods, but with negligible views:** Videos like "30 Seconds to Enter Flow State" (`micro_focus_lock`) and "10 Seconds to Drop Inward" (`micro_drop_inward`) show extremely high retention percentages (559.0% and 91.8% respectively). However, these each have only 1-2 views, making it impossible to draw reliable conclusions about their broader appeal or effectiveness. **Speculative:** The high retention could suggest that for the very few who found them, these short, highly specific mood pieces delivered exactly what they promised, leading to re-watches or very engaged initial viewing.
4.  **Underperforming moods with existing content:** Several moods, such as `deep_focus`, `ocean_waves`, `fireplace`, `energize`, and various "micro" moods (e.g., `micro_energy_boost`, `micro_clarity_sharp`), have multiple videos published but zero views in the analytics window. This indicates either a lack of discoverability, poor packaging, or a lack of audience interest in these specific mood offerings.
5.  **"Evolving" soundscapes are a consistent theme:** Across the top-performing videos and many descriptions in `analytics.json`, the phrase "Evolving" or "Continuously Evolving" is frequently used to describe the soundscapes. This suggests that the concept of non-repeating, dynamic ambient music is a key feature being highlighted and potentially valued by viewers.

## Experiments or packaging ideas

*   **Focus on `art_creator` with proven art periods/music styles:**
    *   Create more videos combining `ancient` and `contemporary` art periods with `taiko` and `none` music styles, given their strong view counts.
    *   **Packaging:** Experiment with titles that explicitly mention "Ancient Taiko Ambient" or "Contemporary Evolving Soundscape" to leverage these successful combinations.
*   **Investigate "micro" mood potential:**
    *   Given the extremely high retention on `micro_focus_lock` and `micro_drop_inward` (despite low views), consider creating a small batch of 3-5 more videos for these specific "micro" moods.
    *   **Packaging:** Use very direct, benefit-oriented titles like "20 Seconds to Instant Focus" or "Quick Drop-In Meditation" to see if improved discoverability can translate the high retention into more views.
*   **Re-evaluate underperforming moods:**
    *   For moods with multiple videos but zero views (e.g., `deep_focus`, `ocean_waves`, `fireplace`), review their titles and thumbnails in `analytics.json` to identify potential packaging weaknesses.
    *   **Experiment:** Re-package a few existing `deep_focus` or `ocean_waves` videos with new titles/thumbnails that are more aligned with the successful `art_creator` video formats (e.g., "Ambient Ocean Waves | 5 Mins | Evolving Calm").
*   **Emphasize "Evolving" nature in titles/descriptions:**
    *   Continue to prominently feature "Evolving" or "Never Repeats" in titles and descriptions for all new content, as this seems to be a recognized and potentially valued characteristic.
*   **Explore "baroque+gamelan" and "medieval+bamboula" combos:**
    *   While not top-tier, the `suggestions.json` shows `baroque+gamelan` (3 total, 2 with views) and `medieval+bamboula` (4 total, 2 with views) have some traction. These could be small-scale experiments to diversify successful combinations within the `art_creator` umbrella.
