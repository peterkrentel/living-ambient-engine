# Agent advisory — Gemini (API) (brand, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of analytics reports and suggestions for 2026-W18. My analysis will focus on identifying patterns in video performance, particularly concerning mood and content parameters, and suggesting potential experiments, while acknowledging the limitations of the current data.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18.md`: The main analytics report for the period 2026-04-03 to 2026-04-30, detailing total views, watch time, subscribers, and top videos by retention and views, as well as performance by mood.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18.md`: The advisory report, including brand snapshot, evidence paths, and a crucial note on packaging and confounders. It also indicates that no actionable suggestions passed the planner gate.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked.md`: Confirms that the planner was blocked due to a lack of qualifying mood suggestion rows.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions.json`: Provides detailed coverage data for moods, art periods, music styles, and their combinations, indicating how many videos exist for each and how many have views.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics.json`: Raw analytics data for individual videos, including titles, descriptions, and metrics.

## Summary

The channel had a total of 1,214 views and 886 minutes of watch time, gaining 3 subscribers over the analytics window (April 3rd to April 30th, 2026). A total of 354 videos are tracked, with 114 having views. The overall average retention is 25.77%. The `art_creator` mood category dominates in terms of total views (1,103 views from 230 videos), though its average retention is 17.9%. Several "micro" moods show exceptionally high retention percentages, albeit with very low view counts (1-2 views). The planner for this week was blocked as no mood suggestions met the criteria for actionable increases (n≥5 videos, group_views≥200).

## Risks / caveats

*   **Low View Counts for High Retention:** Many of the top-performing videos by retention have only 1 or 2 views. This makes it difficult to draw statistically significant conclusions about their actual performance or the underlying mood/style parameters. The 559.0% retention for "30 Seconds to Enter Flow State" is likely an anomaly due to extremely low views and should be treated with extreme caution.
*   **Confounders and Packaging:** The `run-next` report explicitly warns that CTR, impressions, and retention are often influenced by "title, thumbnail, traffic source, and seasonality," not solely by the mood or art-period labels. Without data on these packaging elements, attributing success directly to content parameters is speculative.
*   **Planner Blocked:** The fact that no actionable suggestions passed the planner gate indicates a lack of robust, data-backed trends for increasing specific mood categories. This means any "lean in" suggestions are based on exploratory data.
*   **Limited Data Coverage:** While 354 videos are tracked, only 114 have views. Many moods, art periods, and music styles have very few videos with views, or even zero, making it hard to assess their potential. For example, `deep_focus`, `rain_sleep`, `ceremony`, `warrior`, `energize`, and several "micro" moods have 0 views from their respective videos.

## Insights

1.  **Dominance of `art_creator` Mood:** The `art_creator` mood category is by far the most prolific and viewed, accounting for 1,103 out of 1,214 total views with 230 videos. While its average retention (17.9%) is below the overall average (25.77%), its sheer volume of content and views suggests it's a core component of the channel's current output and audience engagement. The top 5 videos by views are all `art_creator` videos, featuring "ancient," "contemporary," "future," and "baroque" art periods combined with music styles like "taiko," "kuku," "none," and "gamelan."
2.  **High Retention in "Micro" Content:** Several short-duration, highly specific "micro" mood videos exhibit exceptionally high retention percentages, such as `micro_focus_lock` (559.0%), `piano_relax` (97.1%), `micro_noise_hush` (84.7%), and `micro_drop_inward` (91.8%). However, these videos have very low view counts (1-2 views each), making it difficult to determine if this retention is a genuine trend or a statistical artifact. The "30 Seconds to Enter Flow State" (micro_focus_lock) video, despite its anomalous retention, suggests a potential niche for very short, targeted ambient tracks.
3.  **Performance of "Ancient" Art Period:** The "Ambient ancient" art period appears to be a strong performer within the `art_creator` category, with two videos ("Ambient ancient · 5 Mins · Evolving taik" and "Ambient ancient · 5 Mins · Evolving kuku") ranking among the top 5 by views, contributing significantly to the overall watch time. This suggests a potential audience preference for content with this aesthetic.
4.  **Speculative: Potential for "Piano Relax" and "Micro Drop Inward":** The "Let Go of Stress · 30 Seconds Soft Piano" (piano_relax) and "10 Seconds to Drop Inward" (micro_drop_inward) videos show high retention (97.1% and 91.8% respectively) even with only 1 view each. **Speculative:** If these retention rates hold with higher view counts, these moods, particularly `piano_relax` with its clear benefit-oriented title, could indicate an untapped demand for short, calming, and focused content.
5.  **Underperforming Moods with Existing Content:** Moods like `deep_focus`, `rain_sleep`, `ceremony`, `warrior`, and `energize` have multiple videos (e.g., `deep_focus` has 3, `rain_sleep` has 1) but zero views. This suggests either a lack of discoverability, unappealing packaging (titles/thumbnails), or a mismatch with audience interest. These categories might need a re-evaluation of their content or promotional strategy before further investment.

## Experiments or packaging ideas

*   **Test "Micro" Moods with Enhanced Packaging:** Given the high retention (even with low views) of "micro" videos, create a small batch of new `micro_focus_lock`, `piano_relax`, or `micro_drop_inward` videos. Focus on compelling titles and thumbnails that clearly communicate the short duration and specific benefit (e.g., "30-Second Flow State Boost," "Instant Calm: 1-Min Piano Relief").
*   **Explore More "Ancient" Art Period Combinations:** Since "Ambient ancient" videos perform well in views, experiment with more combinations of "ancient" art periods with different music styles (e.g., "ancient+heartbeat" or "ancient+none" which have 2 videos with views each in `suggestions.json`) to see if the success is tied to the art period itself.
*   **Re-evaluate Titles/Thumbnails for Underperforming Moods:** For moods like `deep_focus` or `sleep` that have videos but zero views, analyze the existing titles and thumbnails. Consider A/B testing new packaging that is more descriptive, benefit-driven, or visually engaging to improve discoverability, rather than immediately reducing content generation for these moods.
*   **Create Longer Versions of High-Retention "Micro" Content:** If a "micro" video (e.g., "30 Seconds to Enter Flow State") shows promising retention with more views, consider creating slightly longer versions (e.g., 5-minute or 10-minute) of similar content to capture more watch time from an engaged audience.
*   **Analyze "Art_Creator" Sub-Categories:** The `art_creator` mood is broad. Dive deeper into the specific `art_period` and `music_style` combinations within `art_creator` that are driving the most views (e.g., "ancient+taiko," "contemporary+none," "ancient+kuku") to identify the most successful sub-niches for future content generation.
