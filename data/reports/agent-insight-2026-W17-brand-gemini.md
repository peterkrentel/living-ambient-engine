# Agent advisory — Gemini (API) (brand, 2026-W17)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of analytics reports, suggestions, and raw analytics data for the 2026-W17 period. My analysis will focus on identifying patterns in video performance, highlighting key insights, and suggesting potential experiments based on the available metrics.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W17.md` (Analytics Report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W17.md` (Run next — advisory)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked.md` (Run intent — BLOCKED)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions.json` (Suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics.json` (Raw analytics data)

## Summary

The channel had a total of 1,337 views and 989 minutes of watch time, gaining 4 subscribers over the analytics window (March 27 - April 23, 2026). The `art_creator` mood category dominates in terms of video count (230) and total views (1,276), with an average retention of 19.4%. Several "micro" mood videos show exceptionally high retention percentages, albeit with very low view counts. The "Run intent" for this week was blocked due to a lack of qualifying mood suggestions passing the planner gate, indicating insufficient data or performance to warrant scaling specific mood categories.

## Risks / caveats

The `run-next-2026-W17.md` explicitly warns against treating bucket-level correlation as proof that generation parameters drove a result when packaging (title, thumbnail, traffic source, seasonality) differed. This is a crucial confounder, especially when observing high retention on videos with only 1 or 2 views. The low view counts for many "micro" mood videos make it difficult to draw statistically significant conclusions about their performance. The planner being blocked indicates that there isn't enough robust data to confidently recommend scaling any specific mood category at this time.

## Insights

1.  **Micro-content shows extreme retention, but low reach:** Videos like "30 Seconds to Enter Flow State" (`micro_focus_lock`) and "10 Seconds to Drop Inward" (`micro_drop_inward`) exhibit remarkably high retention rates (559.0% and 91.8% respectively). However, these videos only have 1 or 2 views. This suggests that while they are highly engaging for the few who find them, their discoverability or initial appeal is very low.
2.  **"Art Creator" mood is the primary driver of views:** The `art_creator` mood category accounts for the vast majority of views (1,276 out of 1,337 total views) and videos (230 out of 354 total videos). This indicates that content categorized under `art_creator` is currently the channel's main source of audience engagement, despite its average retention being 19.4%, which is below the overall average of 24.67%.
3.  **"Ancient" art period and "Taiko" music style are top performers by views:** The video "Ambient ancient | 5 Mins | Evolving taik | art_creator" is the top-performing video by views (290 views, 241 min watch time). Another "Ambient ancient | 5 Mins | Evolving kuku | art_creator" also appears in the top 5 by views. This suggests that the "ancient" art period, particularly when combined with music styles like "taiko" or "kuku," resonates well with the current audience.
4.  **Speculative: Short-form, highly specific content might have niche appeal:** The high retention on "micro" videos, despite low views, could indicate a strong, albeit small, demand for very short, targeted ambient experiences. This might be a signal for exploring short-form content strategies or specific calls-to-action for these types of videos.
5.  **Data sparsity limits actionable insights for many moods:** Many mood categories, such as `ocean_waves`, `deep_focus`, `rain_sleep`, and numerous other "micro" moods, have 0 views or very few videos with views. This makes it impossible to draw conclusions about their performance or potential, as the planner correctly identified by blocking any actionable mood increases.

## Experiments or packaging ideas

*   **Experiment with packaging for "micro" content:**
    *   Create dedicated playlists for "micro" mood videos (e.g., "Instant Focus Boosts," "Quick Calm Breaks").
    *   **Speculative:** Test different titles and thumbnails for "micro" videos to improve CTR and discoverability, perhaps emphasizing their short duration and immediate benefit (e.g., "10-Second Flow State," "Quick Stress Relief").
    *   Consider promoting these "micro" videos as YouTube Shorts, if applicable, to leverage short-form content trends.
*   **Double down on successful `art_creator` combinations:**
    *   Produce more videos in the "ancient" art period, especially those incorporating "taiko" or "kuku" music styles, given their strong view performance.
    *   Analyze the specific visual and auditory characteristics of the top-performing `art_creator` videos to inform future generations.
*   **Investigate low-performing `music_style` / `none`:**
    *   The `music_style` / `none` category showed a -16.7% retention vs. channel average (n=3, views=161). Review these specific videos to understand if the "none" music style is genuinely underperforming or if other factors (e.g., packaging, specific art period combinations) are at play.
*   **Gather more data for underrepresented moods:**
    *   Systematically generate and publish a small batch of videos for moods with 0 or very few views (e.g., `deep_focus`, `sleep`, `chill`, `study`) to get initial performance data. This could be done with `--force-moods` as suggested in the `run-intent-blocked.md` report.
*   **Review and refine mood definitions:**
    *   As suggested in the "Next Steps" of the analytics report, review `moods.yaml` based on learnings. This might involve consolidating similar "micro" moods or clarifying their intended use to improve data clarity and generation strategy.
