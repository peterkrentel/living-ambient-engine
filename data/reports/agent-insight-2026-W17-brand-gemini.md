# Agent advisory — Gemini (API) (brand, 2026-W17)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of analytics reports and suggestions for 2026-W17. My analysis will focus on identifying patterns in video performance, particularly regarding moods and content parameters, and suggesting potential experiments based on the available data.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W17.md` (Analytics Report - 2026-W17)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W17.md` (Run next — advisory (2026-W17))
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked.md` (Run intent — BLOCKED)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions.json`
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics.json` (excerpt)

## Summary

The channel had a total of 1,337 views and gained 4 subscribers over the analytics window (March 27 - April 23, 2026). The `art_creator` mood category dominates in terms of total videos (230) and views (1,276), but its average retention is 19.4%, below the overall average of 24.67%. Several "micro" moods show exceptionally high retention percentages, though with very low view counts. The "Run intent" for this week is blocked as no actionable mood increases passed the planner gate, indicating insufficient data or thresholds not met for automated scaling.

## Risks / caveats

The `run-next-2026-W17.md` explicitly states that "CTR, impressions, and retention often move because of title, thumbnail, traffic source, and seasonality — not because a mood or art-period label 'caused' an outcome." Therefore, any correlations observed should not be treated as direct proof that generation parameters alone drove the results, as packaging differences across videos are a significant confounder. Many moods and art/music combos have very low view counts, making statistical inference difficult. The `suggestions.json` file is truncated, limiting the full scope of available data on combinations.

## Insights

1.  **High Retention in "Micro" Moods:** Videos like "30 Seconds to Enter Flow State" (`micro_focus_lock`) and "10 Seconds to Drop Inward" (`micro_drop_inward`) show extremely high retention rates (559.0% and 91.8% respectively), despite having only 1-2 views. This suggests that for the few viewers who found these, the content was highly engaging. The "micro" prefix implies shorter, more targeted experiences.
2.  **Dominance of `art_creator` Mood:** The `art_creator` mood accounts for the vast majority of videos (230) and views (1,276) on the channel. While its average retention of 19.4% is below the channel average, its sheer volume of content and views makes it the primary driver of channel activity. The titles in the "Top 5 by Views" list ("Ambient ancient | 5 Mins | Evolving taik", "Ambient contemporary | 5 Mins | Evolving", etc.) all fall under this broad category.
3.  **Strong Performance of "Ancient" Art Period with "Taiko" Music Style:** The video "Ambient ancient | 5 Mins | Evolving taik | art_creator" is the top performer by views (290) and watch time (241 minutes). Another "Ambient ancient | 5 Mins | Evolving kuku | art_creator" is also in the top 5 by views. This suggests a potential strong audience resonance with the "ancient" art period, particularly when combined with "taiko" or "kuku" music styles.
4.  **Speculative: Potential for Short-Form Content:** The exceptionally high retention of "micro" mood videos, even with low views, might indicate an untapped potential for very short, highly focused ambient tracks designed for quick engagement. While the overall channel focuses on longer 5-minute pieces, these micro-segments could serve as highly effective "hooks" or specific utility tools.
5.  **Underperformance of `music_style` / `none`:** The `run-next` report highlights `music_style` / `none` as an underperformer in retention, at -16.7% vs channel average, with 161 views across 3 videos. This suggests that videos explicitly labeled with "none" for music style might be less engaging than those with a defined musical element.

## Experiments or packaging ideas

*   **Experiment with "Micro" Moods:**
    *   Create more videos specifically targeting `micro_focus_lock` and `micro_drop_inward` moods, keeping them very short (e.g., 30 seconds to 1 minute).
    *   Test different titles and thumbnails for these micro-videos to see if impressions and views can be increased, leveraging their high intrinsic retention.
    *   **Speculative:** Consider promoting these micro-videos as "quick resets" or "instant calm" to a new audience segment.
*   **Optimize `art_creator` Content:**
    *   Analyze the specific "art period" and "music style" combinations within the top-performing `art_creator` videos (e.g., "ancient+taiko", "ancient+kuku").
    *   Produce more videos with these successful combinations, while experimenting with slight variations in titles and descriptions to improve discoverability.
*   **Address `music_style` / `none` Underperformance:**
    *   Review the titles and thumbnails of the 3 videos categorized as `music_style` / `none` to identify if packaging is a contributing factor to lower retention.
    *   Consider adding subtle musical elements or re-categorizing future "none" videos if a distinct sound profile exists, to avoid the "none" label.
    *   **Speculative:** Test if explicitly stating "no music" in titles for truly ambient tracks without a distinct music style improves audience expectation and retention.
*   **Explore "Ancient" and "Taiko" Synergy:**
    *   Create a dedicated mini-series or playlist focusing on the "ancient" art period, specifically incorporating "taiko" and "kuku" music styles, given their strong performance.
    *   Use titles that clearly highlight these elements, e.g., "Ancient Taiko Drum Ambient for Focus" or "Meditative Kuku Rhythms from Ancient Times."
*   **Data Collection for Underperforming Moods:**
    *   The planner is blocked due to insufficient data for actionable mood increases. For moods with low views (e.g., `trance`, `sleep`, `chill`, `study`, `forest_morning`), consider a small batch of new uploads for each to gather more data and potentially reach the `n>=5, group_views>=200` threshold for future actionable insights. This could be done using the `--force-moods` option for development.
