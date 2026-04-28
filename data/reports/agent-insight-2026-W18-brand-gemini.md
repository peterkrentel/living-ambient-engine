# Agent advisory — Gemini (API) (brand, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of analytics reports and suggestions for 2026-W18. My goal is to extract actionable insights and suggest experiments based solely on this data, while acknowledging any limitations or blocked recommendations.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18.md`: The primary analytics report for the period 2026-03-31 to 2026-04-27, detailing total views, watch time, subscribers, and top videos by retention and views, as well as performance by mood.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18.md`: An advisory report summarizing overall channel performance and indicating that no actionable suggestions passed the planner gate this week. It also highlights confounders related to packaging.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked.md`: A report explicitly stating that no actionable mood increases passed the planner gate due to insufficient qualifying mood suggestion rows.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions.json`: A JSON file containing overall channel metrics and coverage data for various moods, art periods, music styles, and their combinations.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics.json`: A detailed JSON file with metrics for individual videos, including titles, descriptions, and published dates.

## Summary

The channel had a total of 1,201 views and 827 minutes of watch time, gaining 4 subscribers during the analytics window (March 31 - April 27, 2026). The overall average retention was 24.52%. The `art_creator` mood category dominates in terms of views, accounting for 1,123 out of 1,201 total views. However, the planner for generating new content is currently blocked as no mood suggestions met the criteria for an "actionable increase." There's a significant disparity between the total number of videos tracked (354) and those with analytics (353), and an even smaller subset (123) with views. Only a small percentage of videos (13.6%) are identity-aligned with `generations.json`.

## Risks / caveats

*   **Confounders:** The `run-next-2026-W18.md` explicitly warns that CTR, impressions, and retention are often influenced by "title, thumbnail, traffic source, and seasonality," not solely by mood or art-period labels. Therefore, correlations observed should not be treated as direct causation by generation parameters alone.
*   **Low N for retention:** Several videos with exceptionally high retention percentages (e.g., `micro_focus_lock` at 559.0%) have very low view counts (e.g., 2 views). These outliers are likely statistical anomalies due to small sample sizes and should not be over-interpreted.
*   **Planner Blocked:** The system is currently unable to provide actionable "increase" recommendations for moods due to insufficient data or criteria not being met (n≥5, group_views≥200). This limits the ability to confidently scale specific mood categories based on automated suggestions.
*   **Data Thinness:** Many moods, art periods, and music styles have very few videos with views, or even zero views, making it difficult to draw robust conclusions about their performance. For example, `deep_focus`, `ocean_waves`, `rain_sleep`, `ceremony`, `warrior`, `energize`, and several `micro_` moods have 0 views despite having multiple videos.

## Insights

1.  **`art_creator` Mood Dominance:** The `art_creator` mood category is overwhelmingly responsible for the channel's views, with 230 videos generating 1,123 views out of a total of 1,201. This suggests that content categorized under `art_creator` is resonating most with the current audience, despite its average retention of 17.6% being lower than some other moods with fewer views. The top 5 videos by views are all `art_creator` videos, featuring "Ambient ancient," "Ambient contemporary," "Ambient future," and "Ambient baroque" themes.
2.  **High Retention Micro-Moods (with caveats):** Several `micro_` moods show extremely high retention percentages, such as `micro_focus_lock` (559.0%), `micro_overthink_b` (60.5%), `micro_stuck_jolt` (68.2%), `micro_noise_hush` (84.0%), and `micro_drop_inward` (91.8%). However, these are based on very low view counts (1-3 views per video), making them statistically unreliable for broad conclusions. The `piano_relax` mood also shows high retention (97.1%) from a single video with 1 view.
3.  **"Ancient" and "Contemporary" Art Periods Perform Well by Views:** Within the `art_creator` mood, videos featuring "Ambient ancient" and "Ambient contemporary" art periods are among the top performers by views. Specifically, "Ambient ancient | 5 Mins | Evolving taik" garnered 237 views and "Ambient contemporary | 5 Mins | Evolving" received 105 views. This indicates a potential audience preference for these aesthetic themes.
4.  **Music Style "Taiko" and "None" are Top Performers:** The top-viewed video, "Ambient ancient | 5 Mins | Evolving taik," explicitly mentions "taik" (likely Taiko) as a music style. Another top video, "Ambient future | 5 Mins | Evolving none," suggests that some successful videos might not have a specific music style explicitly called out or are categorized as "none."
5.  **Speculative: Short-form Focus/Relaxation Potential:** While the high retention micro-moods are based on thin data, the titles "30 Seconds to Enter Flow State" and "10 Seconds to Drop Inward" suggest a focus on very short, targeted ambient experiences. If these concepts could be validated with more views, they might indicate a niche for extremely brief, high-impact ambient tracks for specific mental states.

## Experiments or packaging ideas

*   **Focus on `art_creator` variations:** Given its dominance in views, continue to produce content within the `art_creator` mood. Experiment with different combinations of art periods and music styles that have shown some traction, such as "ancient" and "contemporary" art periods, and "taiko" or "none" music styles.
*   **Investigate top-viewed `art_creator` videos:** Analyze the titles, thumbnails, and descriptions of the top 5 videos by views (e.g., "Ambient ancient | 5 Mins | Evolving taik") to identify common packaging elements that might contribute to their higher view counts.
*   **Test micro-moods with increased exposure:** Despite low view counts, the extremely high retention percentages for `micro_focus_lock`, `micro_drop_inward`, and `piano_relax` are intriguing. Consider creating a small batch of new videos for these moods, ensuring consistent and compelling packaging (titles, thumbnails) to see if increased impressions lead to sustained high retention and more views.
*   **Re-evaluate zero-view categories:** For moods and art/music combos with 0 views (e.g., `deep_focus`, `ocean_waves`, `baroque+gnawa`), review their existing packaging. Are the titles clear? Are the thumbnails appealing? Consider A/B testing new packaging for a few of these to see if discoverability improves before deprioritizing them.
*   **Experiment with "Evolving" and "Never Repeats" in titles/descriptions:** Many top-performing and existing videos use phrases like "Evolving" and "never repeats" in their titles or descriptions. This could be a strong selling point for ambient music. Test emphasizing these phrases more prominently in new video titles and descriptions across various moods.
