# Agent advisory — Gemini (API) (brand, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of committed repo files and excerpts from the analytics pipeline for 2026-W18. This analysis will summarize the channel's performance, highlight key insights from the available data, and suggest potential experiments, while acknowledging any data limitations.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18.md` (Analytics Report - 2026-W18)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18.md` (Run next — advisory (2026-W18))
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked.md` (Run intent — BLOCKED)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions.json` (Suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics.json` (Raw analytics data)

## Summary

The channel had a total of 1,201 views and 827 minutes of watch time, gaining 4 subscribers during the analytics window (2026-03-31 to 2026-04-27). The "art_creator" mood category dominates in terms of total views (1,123 views from 230 videos), though its average retention is 17.6%. Several "micro" mood videos show exceptionally high retention percentages, albeit with very low view counts (1-2 views). The planner was blocked this week due to a lack of qualifying mood suggestions that passed the actionable thresholds (n≥5, group_views≥200).

## Risks / caveats

*   **Low View Counts for High Retention Videos:** The extremely high retention percentages (e.g., 559.0% for "30 Seconds to Enter Flow State") are based on only 1 or 2 views. This makes them statistically unreliable for drawing broad conclusions about audience engagement.
*   **Confounders:** The `run-next-2026-W18.md` explicitly states that CTR, impressions, and retention are often influenced by "title, thumbnail, traffic source, and seasonality," not solely by mood or art-period labels. Correlation does not imply causation, and packaging differences across videos are a significant confounder.
*   **Planner Blocked:** The lack of actionable mood suggestions means there's no machine-driven guidance for scaling up specific moods, indicating insufficient data or performance to meet the defined thresholds.
*   **Limited Data Coverage:** Only 123 out of 354 total videos had views in the analytics window, and only a small percentage (13.6%) are identity-aligned with `generations.json`, suggesting a significant portion of the channel's content lacks detailed generation parameter context.

## Insights

1.  **Dominance of "art_creator" Mood:** The `art_creator` mood category accounts for the vast majority of views (1,123 out of 1,201 total views) and videos (230 out of 354). Within this category, videos featuring "Ambient ancient" and "Ambient contemporary" art periods, often paired with music styles like "taiko" or "none," are top performers by views. This suggests a strong existing audience preference for this general aesthetic.
2.  **Exceptional Micro-Content Retention:** Videos with "micro" moods like "micro_focus_lock" (559.0% retention), "micro_drop_inward" (91.8%), and "micro_noise_hush" (84.0%) show remarkably high retention rates. While these are based on very low view counts (1-2 views), they hint at a potential for highly engaging, short-form content if discoverability can be improved.
3.  **Specific Art Period & Music Style Combinations Drive Views:** "Ambient ancient · 5 Mins · Evolving taik" is the top-performing video by views (237 views, 161 min watch time), followed by "Ambient contemporary · 5 Mins · Evolving" (105 views, 51 min watch time) and "Ambient future · 5 Mins · Evolving none" (92 views, 44 min watch time). This indicates that specific combinations of art periods and music styles within the `art_creator` mood resonate well with the current audience.
4.  **Speculative: Potential for "Piano Relax" Niche:** The video "Let Go of Stress · 30 Seconds Soft Piano" under the `piano_relax` mood has a very high retention of 97.1% (from 1 view). While data is thin, this suggests that piano-based relaxation music, potentially in shorter formats, could be a highly engaging niche if more content is produced and promoted.
5.  **Underperforming Moods:** Many moods, such as `ocean_waves`, `deep_focus`, `rain_sleep`, `ceremony`, `warrior`, and various `micro_` moods (e.g., `micro_energy_boost`, `micro_clarity_sharp`), have 0 views despite having multiple videos. This could indicate issues with discoverability, titles, thumbnails, or a lack of audience interest for these specific themes.

## Experiments or packaging ideas

*   **Replicate Top-Performing `art_creator` Combinations:**
    *   Create more 5-minute videos combining "ancient" art periods with "taiko" music.
    *   Produce additional 5-minute videos with "contemporary" and "future" art periods, especially with "none" or "gamelan" music styles.
    *   **Speculative:** Test titles that explicitly mention the art period and music style, e.g., "Ancient Taiko Ambient: 5 Mins for Focus."
*   **Boost Discoverability for High-Retention Micro-Content:**
    *   Experiment with dedicated playlists for "micro" ambient tracks (e.g., "Quick Focus Boosts," "Instant Calm").
    *   **Speculative:** Create short-form content (YouTube Shorts) using snippets of the high-retention "micro" videos, linking to the full versions.
    *   Test different titles and thumbnails for "micro" videos to improve CTR, focusing on immediate benefit (e.g., "30 Seconds to Flow State: Instant Focus Music").
*   **Explore "Piano Relax" with More Content:**
    *   Produce a small batch of 5-minute and 10-minute videos under the `piano_relax` mood, similar to "Let Go of Stress," to see if the high retention observed on the 30-second version scales.
    *   **Speculative:** Use titles that emphasize "soft piano," "gentle melodies," and "stress relief."
*   **A/B Test Thumbnails for Underperforming Moods:**
    *   For moods with 0 views but existing videos (e.g., `deep_focus`, `ocean_waves`), design and test new, more engaging thumbnails to see if impressions and CTR can be improved.
*   **Review and Refine `unknown` Mood Videos:**
    *   Investigate the 32 videos categorized as `unknown` mood with only 1 total view and 0.4% average retention. Assign appropriate moods and update metadata to improve categorization and potential performance.
