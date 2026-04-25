# Agent advisory — Gemini (API) (brand, 2026-W17)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of analytics reports and suggestions for 2026-W17. My analysis will focus on identifying patterns in video performance, particularly concerning moods and content parameters, and suggesting potential experiments based on the available data.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W17.md`: The main analytics report for the period 2026-03-28 to 2026-04-24, detailing total views, watch time, subscribers, top videos by retention and views, and performance by mood.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W17.md`: The advisory report, including brand snapshot, evidence paths, and a note on the planner being blocked.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked.md`: Confirmation that the planner was blocked due to no actionable mood increases.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions.json`: A JSON file containing overall channel metrics and coverage data for moods, art periods, and music styles.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics.json`: A detailed JSON file with individual video metrics, titles, descriptions, and publication dates.

## Summary

The channel generated 1,313 views and 954 minutes of watch time, gaining 4 subscribers over the 28-day analytics window. The `art_creator` mood category dominates in terms of total videos (230) and views (1,252), though its average retention is 19.0%. Several "micro" moods show exceptionally high retention percentages, albeit with very low view counts (1-2 views). The planner was blocked this week as no mood suggestions met the criteria for actionable increases (n≥5, group_views≥200). The `suggestions.json` file indicates a broad range of moods, art periods, and music styles have been generated, but many have zero views or very low view counts.

## Risks / caveats

*   **Low View Counts for High Retention:** The top videos by retention have extremely low view counts (1-2 views), making their high retention percentages (e.g., 559.0%, 99.7%) statistically unreliable for drawing broad conclusions. These could be anomalies or internal testing.
*   **Confounders:** The `run-next` report explicitly states that CTR, impressions, and retention are often influenced by "title, thumbnail, traffic source, and seasonality" rather than just generation parameters. This means observed correlations between mood/art-period and performance should not be treated as direct causation without further experimentation.
*   **Planner Blocked:** The lack of actionable suggestions from the planner indicates that there isn't enough robust data to confidently recommend scaling up any specific mood based on the current thresholds.
*   **Data Sparsity:** Many moods, art periods, and music styles in `suggestions.json` have `with_views: 0`, meaning they have not received any views in the analytics window, making it impossible to assess their performance.
*   **Limited Context on "art_creator":** The `art_creator` mood is a very broad category that encompasses the top-performing videos by views. Without further breakdown, it's hard to discern specific successful sub-trends within it.

## Insights

1.  **Dominance of "art_creator" Mood:** The `art_creator` mood accounts for the vast majority of videos (230 out of 354) and views (1,252 out of 1,313 total views). While its average retention is 19.0%, this category is clearly driving the channel's current viewership. The top 5 videos by views all fall under this mood, featuring titles like "Ambient ancient | 5 Mins | Evolving taik" and "Ambient contemporary | 5 Mins | Evolving".
2.  **High Retention in "Micro" Moods (Low Volume):** Several "micro" moods, such as `micro_focus_lock` (559.0% retention, 2 views), `micro_drop_inward` (91.8% retention, 1 view), and `micro_stuck_jolt` (81.8% retention, 1 view), show exceptionally high retention rates. While these are based on very few views, they hint at a strong engagement potential for highly specific, short-duration ambient experiences.
3.  **"Ancient" and "Contemporary" Art Periods Drive Views:** Within the `art_creator` mood, videos tagged with "ancient" and "contemporary" art periods appear frequently in the top 5 by views. Specifically, "Ambient ancient | 5 Mins | Evolving taik" garnered 289 views and 240 minutes of watch time, and another "Ambient ancient | 5 Mins | Evolving kuku" received 80 views. "Ambient contemporary | 5 Mins | Evolving" also performed well with 105 views.
4.  **Speculative: Potential for "Taiko" and "Kuku" Music Styles:** The top-performing video, "Ambient ancient | 5 Mins | Evolving taik", explicitly mentions "taik" (likely Taiko). Another top video, "Ambient ancient | 5 Mins | Evolving kuku", mentions "kuku". This suggests that music styles like Taiko and Kuku, when combined with "ancient" art periods, might resonate well with the audience, contributing to higher views.
5.  **Broad Distribution, Limited Performance:** The `suggestions.json` shows a wide array of moods, art periods, and music styles have been generated. However, many of these categories, especially outside of `art_creator`, have zero views or very low view counts, indicating either poor discoverability, low audience interest, or insufficient content volume to gain traction. For example, `deep_focus`, `ocean_waves`, and `fireplace` moods have multiple videos but zero views.

## Experiments or packaging ideas

*   **Test "Micro" Moods with Increased Volume and Optimized Packaging:** Given the high retention, create 5-10 new videos for `micro_focus_lock`, `micro_drop_inward`, and `micro_stuck_jolt`. Focus on highly descriptive titles and thumbnails that clearly communicate the specific, short-term benefit (e.g., "10-Second Focus Boost," "Instant Calm Drop-In").
*   **Double Down on "Ancient" Art Period with "Taiko" and "Kuku" Music:** Generate more videos combining the "ancient" art period with "taiko" and "kuku" music styles. Experiment with slightly varied titles and thumbnails to see if the success of existing videos can be replicated and scaled.
*   **Experiment with "Contemporary" and "Baroque" Art Periods:** Since "Ambient contemporary" and "Ambient baroque" also appeared in the top 5 by views, explore more content within these art periods, potentially combining them with music styles that have shown some traction (e.g., "gamelan" for baroque, "none" for contemporary based on `suggestions.json` data).
*   **Re-evaluate Low-Performing Moods:** For moods like `deep_focus`, `ocean_waves`, and `fireplace` that have videos but zero views, review their titles, descriptions, and thumbnails in `analytics.json`. Consider if their packaging accurately reflects the content and audience intent. If packaging is not the issue, these moods may need to be deprioritized or re-imagined.
*   **A/B Test Titles for Top Performers:** For videos like "Ambient ancient | 5 Mins | Evolving taik" that are already performing well, consider creating slight variations in titles or thumbnails for new uploads within the same content style to see if minor adjustments can further boost views or retention.
