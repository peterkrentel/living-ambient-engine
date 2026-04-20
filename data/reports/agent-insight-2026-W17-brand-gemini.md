# Agent advisory — Gemini (API) (brand, 2026-W17)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of analytics reports, suggestions, and raw analytics data for 2026-W17. My goal is to synthesize this information into actionable insights and suggest experiments to optimize content performance.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W17.md`: The primary analytics report for the period 2026-03-23 to 2026-04-19, detailing total views, watch time, subscriber gains, and top videos by retention and views. It also includes performance broken down by mood.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W17.md`: An advisory report summarizing overall channel performance, outlining the methodology for suggestions, and noting that no actionable "increase" rows passed the planner gate this week. It also includes an audit overview.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked.md`: A report explicitly stating that the planner was blocked due to a lack of qualifying mood suggestions.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions.json`: A detailed JSON file containing aggregated data on moods, art periods, music styles, and art-music combos, including total videos and videos with views for each category.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics.json`: The raw, comprehensive analytics data for individual videos, including titles, descriptions, publication dates, and detailed metrics.

## Summary

The channel had a total of 1,305 views and 818 minutes of watch time, gaining 3 subscribers over the analytics window (2026-03-23 to 2026-04-19). The overall average retention is 17.82%. The "art_creator" mood dominates in terms of video count (230) and total views (1,280), but its average retention is relatively low at 16.9%. Other moods like "chill" (51.6%) and "micro_wake_spark" (47.1%) show significantly higher average retention, albeit with very few videos and views. The planner for this week was blocked, indicating no mood suggestions met the criteria for scaling up. The top-performing videos by views are primarily "Ambient ancient" and "Ambient contemporary" or "baroque" with "Evolving taiko" or "Evolving game" music styles. Interestingly, the top videos by retention all have 99.7% retention but only 1 view each, suggesting these are likely internal or test views and not indicative of broad audience engagement.

## Risks / caveats

*   **Low View Counts for High Retention:** The top 5 videos by retention all have 99.7% retention but only 1 view each. This is a significant confounder, as these are likely not representative of general audience behavior and should not be used to infer content success.
*   **Planner Blocked:** The planner was blocked because no actionable mood increases met the thresholds (n≥5, group_views≥200). This means there's insufficient data to confidently recommend scaling up any particular mood based on automated suggestions.
*   **Packaging Confounders:** The `run-next` report explicitly warns that CTR, impressions, and retention are heavily influenced by packaging (title, thumbnail, traffic source, seasonality), not just generation parameters. This makes it difficult to attribute success or failure solely to mood or art-period labels.
*   **Data Sparsity for Many Moods:** Many moods listed in the "Performance by Mood" table and `suggestions.json` have very few videos or zero views, making it impossible to draw meaningful conclusions about their performance. For example, "trance" has 10 videos but only 7 views, "sleep" has 14 videos but 6 views.
*   **Limited Identity-Aligned Data:** Only 40 out of 346 videos (11.6%) are identity-aligned with `generations.json`, which might limit the ability to correlate specific generation parameters with performance across the entire channel.

## Insights

1.  **Dominance of "art_creator" but with low retention:** The "art_creator" mood accounts for the vast majority of videos (230) and views (1,280) on the channel. However, its average retention is 16.9%, which is below the overall channel average of 17.82%. This suggests that while this category generates volume, there might be opportunities to improve engagement within it.
2.  **"Ambient ancient" and "taiko" are strong performers by views:** The video "Ambient ancient | 5 Mins | Evolving taik" is the top performer by views (317) and watch time (260 minutes). Another "Ambient ancient" video with "Evolving kuku" also performs well. This indicates that content related to "ancient" art periods, particularly when paired with music styles like "taiko" or "kuku," resonates with the audience.
3.  **High retention in niche moods with low views:** Moods like "chill" (51.6% retention with 5 views from 11 videos) and "micro_wake_spark" (47.1% retention with 2 views from 1 video) show promising retention rates. While the view counts are too low to be actionable, these high retention percentages suggest that when these videos do get discovered, they hold audience attention effectively. This could point to underserved niches.
4.  **Speculative: "Evolving" descriptor in titles is common across top videos:** Many of the top-performing videos by both retention (though with caveats) and views include the word "Evolving" in their titles (e.g., "Ambient medieval | 5 Mins | Evolving bam", "Ambient ancient | 5 Mins | Evolving taik"). This consistent phrasing might be a successful element in setting audience expectations for the dynamic nature of the ambient soundscapes.
5.  **"music_style / none" shows underperformance in retention:** The `run-next` report highlights "music_style / none" as an underperformer in retention, being -9.5% vs. the channel average (n=3, views=164). This suggests that videos without a specified music style might struggle to keep viewers engaged compared to those with a distinct musical identity.

## Experiments or packaging ideas

*   **Focus on "Ancient" Art Period with "Taiko" or "Kuku" Music:**
    *   Create more videos combining the "ancient" art period with "taiko" or "kuku" music styles, given their strong performance in views.
    *   **Packaging:** Experiment with thumbnails and titles that visually emphasize ancient aesthetics and clearly state the music style (e.g., "Ancient Taiko Ambient for Focus").
*   **Investigate High-Retention, Low-View Moods:**
    *   Generate a small batch of new videos for "chill" and "micro_wake_spark" moods.
    *   **Packaging:** Test different titles and thumbnails for these new videos to see if improved discoverability can translate their high retention into higher view counts. For "chill," consider titles like "Relaxing Chill Ambient: Unwind & De-stress."
*   **Improve "art_creator" Engagement:**
    *   Analyze the specific "art_creator" videos with higher-than-average retention within that mood. Identify commonalities in their titles, descriptions, or visual styles.
    *   **Experiment:** Create new "art_creator" videos incorporating these identified successful elements to try and lift the overall retention for this high-volume category.
*   **Address "music_style / none" Underperformance:**
    *   For future content, ensure all videos have a clearly defined `music_style` parameter.
    *   **Experiment:** Consider updating titles/descriptions of existing "music_style / none" videos (if feasible and if they have views) to retroactively assign or imply a music style, and monitor if retention improves.
*   **Standardize "Evolving" Descriptor:**
    *   Continue using "Evolving" in titles for new content, as it appears to be a consistent element across many top performers.
    *   **Experiment:** A/B test titles with and without "Evolving" for similar content to confirm its impact on CTR and retention.
