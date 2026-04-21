# Agent advisory — Gemini (API) (brand, 2026-W17)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of analytics reports and suggestions for 2026-W17. My analysis will focus on identifying patterns in video performance, highlighting potential areas for improvement, and suggesting experiments based on the available data.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W17.md`: The primary analytics report for the week, detailing total views, watch time, subscribers, and top-performing videos by retention and views, as well as performance by mood.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W17.md`: The advisory report, including brand snapshot, exploratory suggestions, and a note on the planner being blocked.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked.md`: Confirmation that the planner was blocked due to a lack of actionable mood increases.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions.json`: Detailed coverage data for moods, art periods, music styles, and their combinations.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics.json`: Raw analytics data for individual videos, including titles, descriptions, and metrics.

## Summary

The channel had a total of 1,260 views and 800 minutes of watch time, gaining 3 subscribers over the `2026-03-24` to `2026-04-20` period. The overall average retention is 18.44%. A significant portion of the channel's content (230 out of 350 videos) is categorized under the "art_creator" mood, which also accounts for the vast majority of views (1,235 out of 1,260). The planner for this week was blocked, indicating no mood suggestions met the criteria for actionable increases (n≥5, group_views≥200). There's an exploratory note about `music_style` / `none` having -10.1% retention vs channel average, but this is based on a small sample (n=3, views=156).

## Risks / caveats

*   **Thin Data:** Many moods and combinations have very low or zero views, making it difficult to draw statistically significant conclusions. For example, 28 out of 31 listed moods have 7 or fewer views, with many having 0 views.
*   **Confounders:** The `run-next` report explicitly warns that CTR, impressions, and retention are often influenced by packaging (title, thumbnail, traffic source, seasonality) and not solely by generation parameters. This means observed correlations should not be treated as direct causation.
*   **Limited "Actionable" Insights:** The planner was blocked, meaning no mood suggestions met the thresholds for immediate action. This limits the scope of data-driven recommendations for scaling specific content types.
*   **"art_creator" Mood Dominance:** The "art_creator" mood heavily skews the overall metrics due to its large number of videos and views. This makes it challenging to assess the true performance of other, smaller mood categories without more granular data.
*   **5-Minute Video Focus:** All top-performing videos by retention and views are 5 minutes long. While this indicates a potential sweet spot for engagement, it also means there's limited data on other durations.

## Insights

1.  **"art_creator" Mood is a Core Performer:** The "art_creator" mood dominates the channel's performance, accounting for 230 videos and 1,235 views, which is nearly all total views. Its average retention is 17.6%, close to the overall channel average of 18.44%. This suggests it's a foundational content type for the channel.
2.  **High Retention for 5-Minute "Ambient" Videos:** The top 5 videos by retention all achieve an impressive 99.7% retention. These videos consistently follow a "Ambient [art period] | 5 Mins | Evolving [music style]" title pattern. This indicates that when users click on these specific 5-minute ambient pieces, they tend to watch them almost entirely.
3.  **"Ancient" Art Period and "Taiko" Music Style Show Strong Viewership:** The "Ambient ancient | 5 Mins | Evolving taik" video is the top performer by views (305 views, 251 watch minutes). Another "Ambient ancient" video with "kuku" music style is also in the top 5 by views. The "taiko" music style also appears in the top 5 by views for "Ambient contemporary." This suggests a potential preference for the "ancient" art period and "taiko" music style among viewers.
4.  **Speculative: "Evolving" and "Never Repeats" Messaging Resonates:** While not directly quantifiable, the descriptions of videos like "Unwind After a Long Day" and "Can't Sleep?" emphasize "Evolving" and "never repeats." Given the high retention of the top videos, it's **speculative** that this unique selling proposition of non-looping, evolving soundscapes might be a key factor in user engagement and satisfaction, leading to full watch-throughs for shorter content.
5.  **Underperforming Moods and Music Styles:** Many moods like "trance," "sleep," "chill," and "study" have very few views despite having 10-14 videos each. The `music_style` / `none` is flagged as an exploratory underperformer with -10.1% retention compared to the channel average. This indicates that these categories either aren't attracting an audience or aren't retaining them effectively, though the data is too sparse for definitive conclusions.

## Experiments or packaging ideas

*   **Expand on Top-Performing Art Periods/Music Styles:**
    *   Create more 5-minute "Ambient ancient" videos, experimenting with various "evolving" music styles, particularly those that have shown some traction like "taiko" and "kuku."
    *   Explore other art periods that appear in top view counts, such as "contemporary" and "baroque," combined with successful music styles.
*   **Replicate High-Retention Packaging:**
    *   Analyze the titles, thumbnails (if available in a separate report), and descriptions of the top 5 retention videos (e.g., "Ambient medieval | 5 Mins | Evolving bam"). Apply similar clear, concise naming conventions and emphasize the "5 Mins" and "Evolving" aspects.
*   **Test "Evolving" Messaging in Titles:**
    *   For new videos, explicitly include "Evolving" or "Never Repeats" in the title or prominent thumbnail text to see if this unique selling proposition drives higher CTR and retention.
*   **Targeted Promotion for Underperforming Moods:**
    *   For moods like "sleep," "chill," and "study" that have low views but a decent number of videos, consider running small-scale experiments with different titles, thumbnails, or descriptions to see if discoverability or initial engagement can be improved.
*   **Investigate "music_style / none" Performance:**
    *   Given the exploratory flag for `music_style` / `none` underperforming in retention, review the specific videos in this category. Are they truly "none" or is there an implicit style? Consider adding a more descriptive music style or re-evaluating if "none" is a compelling offering.
*   **Longer Form Content for High-Retention Themes:**
    *   **Speculative:** If 5-minute videos are achieving near 100% retention, consider creating longer versions (e.g., 15-30 minutes) of the most successful "Ambient [art period] | Evolving [music style]" themes to capture more watch time from engaged viewers.
