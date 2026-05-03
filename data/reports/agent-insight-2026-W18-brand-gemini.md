# Agent advisory — Gemini (API) (brand, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of committed repository files and analytics pipeline excerpts for the 2026-W18 period. My analysis will focus on identifying patterns in video performance, particularly regarding mood and style, and suggesting potential experiments based on the available data.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18.md` (Analytics Report - 2026-W18)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18.md` (Run next — advisory (2026-W18))
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked.md` (Run intent — BLOCKED)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions.json` (Suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics.json` (Raw analytics data)

## Summary

The channel had a total of 1,189 views and 844 minutes of watch time, gaining 3 subscribers over the `2026-04-05` to `2026-05-02` analytics window. The `art_creator` mood category, despite having a relatively low average retention of 14.7%, accounts for the vast majority of views (1,054 out of 1,189 total views) and dominates the top 5 videos by views. Conversely, "micro" mood videos show exceptionally high retention rates, with "30 Seconds to Enter Flow State" achieving 383.9% retention, though these videos have very low view counts (1-5 views each). The planner for this week was blocked due to no actionable mood increases meeting the defined thresholds (n≥5, group_views≥200).

## Risks / caveats

The `run-next-2026-W18.md` explicitly states that "CTR, impressions, and retention often move because of title, thumbnail, traffic source, and seasonality — not because a mood or art-period label 'caused' an outcome." This is a critical confounder, meaning observed correlations between mood/style and performance are not necessarily causal. The "micro" mood videos, while showing impressive retention, have extremely low view counts (1-5 views), making their retention percentages statistically less reliable for broader conclusions. Many moods and art/music combos have zero views, indicating a lack of data for analysis. The "art_creator" mood is a very broad category, encompassing various art periods and music styles, which makes it difficult to pinpoint specific successful elements within it without further breakdown.

## Insights

1.  **Dominance of `art_creator` mood in views:** The `art_creator` mood, comprising 230 videos, generated 1,054 views, which is over 88% of the total views for the period. The top 5 videos by views are all within this category, featuring "Ambient ancient," "Ambient contemporary," "Ambient future," and "Ambient baroque" art periods combined with various evolving soundscapes like "taik," "kuku," and "game." This suggests that the general aesthetic and concept of "evolving art-period ambient" resonates with viewers for initial engagement.
2.  **Exceptional retention in "micro" mood videos:** Several "micro" mood videos, such as "30 Seconds to Enter Flow State" (micro_focus_lock, 383.9% retention), "Let Go of Stress · 30 Seconds Soft Piano" (piano_relax, 94.9%), and "10 Seconds to Drop Inward" (micro_drop_inward, 91.8%), exhibit remarkably high retention rates. This indicates that for the few viewers who discover them, these short, targeted pieces are highly engaging, potentially being replayed multiple times or watched for longer than their stated duration.
3.  **Speculative: Potential for short-form, highly targeted content:** The high retention of "micro" mood videos, despite low views, suggests a strong user need for very specific, short-duration ambient experiences. These videos might be serving a niche of users looking for quick mental shifts or resets. The mood names like `micro_focus_lock`, `micro_sharpen_edge`, and `micro_noise_hush` clearly indicate their intended purpose.
4.  **Low average retention for high-view content:** While `art_creator` videos drive views, their average retention is only 14.7%. This contrasts sharply with the "micro" moods. This could imply that while the titles and thumbnails for `art_creator` videos are effective at attracting clicks, the content itself might not be holding attention for a significant portion of the video's length, or viewers are seeking longer-form content that isn't being provided.
5.  **Planner blockage indicates lack of clear, scalable winners:** The `run-intent-blocked.md` report clearly states "No actionable mood increases... There were no qualifying mood suggestion rows at all." This means no single mood category (with n≥5 videos and group_views≥200) demonstrated strong enough, consistent performance to warrant an automatic increase in production. This highlights the need for more targeted experimentation or a re-evaluation of the thresholds.

## Experiments or packaging ideas

*   **Experiment with packaging "micro" moods:** Given their high retention, explore different titles and thumbnails for "micro" mood videos to improve their discoverability and view counts. Perhaps bundle them into playlists or create "micro-compilations" to leverage their strong engagement.
*   **Analyze `art_creator` sub-categories:** Break down the `art_creator` mood by specific art periods and music styles (e.g., "ancient+taiko," "contemporary+none") to identify which combinations within this high-view category perform best in terms of retention, not just views. The `suggestions.json` shows coverage for these combos, but `2026-W18.md` only aggregates to `art_creator`.
*   **Test longer versions of successful "micro" moods:** If a "30 Seconds to Enter Flow State" video has 383.9% retention, it implies viewers are replaying it. Consider creating 5-minute or 10-minute versions of these highly engaging "micro" concepts to capture more watch time from interested users.
*   **Investigate zero-view moods:** Many moods like `deep_focus`, `energize`, `ceremony`, `warrior`, and `lofi_study` have videos but zero views. Review their titles, thumbnails, and descriptions in `analytics.json` to identify potential reasons for lack of discovery. Are they poorly optimized for search, or is there no audience for these specific moods?
*   **A/B test titles/thumbnails for `art_creator` videos:** Since `art_creator` videos get views but have lower retention, experiment with titles and thumbnails that more accurately set expectations for the content, potentially attracting a more engaged audience, or titles that highlight the "evolving" nature to encourage longer viewing.
