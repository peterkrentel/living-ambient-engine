# Agent advisory — Gemini (API) (brand, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of analytics reports and production planning documents for 2026-W18. My analysis will focus on identifying patterns in video performance, highlighting potential risks, and suggesting experiments based on the available data.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18.md` (Analytics Report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18.md` (Run next — advisory)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked.md` (Run intent — BLOCKED)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions.json` (Suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics.json` (Raw analytics data)

## Summary

The channel generated 1,201 total views and 827 minutes of watch time, gaining 4 subscribers over the analytics window (March 31 - April 27, 2026). The "art_creator" mood category dominates in terms of total views (1,123 views from 230 videos), but its average retention is relatively low at 17.6%. Several "micro" mood videos show exceptionally high retention percentages, though with very low view counts (1-2 views each). The planner for this week is blocked due to no actionable mood increases passing the gate, indicating a lack of strong, data-backed signals for scaling specific mood categories.

## Risks / caveats

*   **Low View Counts for High Retention:** Many of the videos with extremely high retention (e.g., "30 Seconds to Enter Flow State" at 559%) have only 1-2 views. This makes it difficult to draw statistically significant conclusions about their performance or scalability. The 559% retention is likely an artifact of very short videos being watched multiple times or beyond their stated duration by a single viewer.
*   **Planner Blocked:** The `run-intent-blocked.md` report clearly states that no actionable mood increases passed the planner gate, meaning there are no strong, data-driven recommendations for scaling specific moods this week. This limits the ability to make confident production suggestions.
*   **Confounders & Packaging:** The `run-next-2026-W18.md` explicitly warns against treating bucket-level correlation as proof that generation parameters drove a result when packaging (title, thumbnail, traffic source, seasonality) differed. This means that while "art_creator" videos are popular, their success might be due to their presentation rather than the underlying mood itself.
*   **Data Thinness:** A significant number of moods and art/music combos in `suggestions.json` have "total" videos but "with_views" counts of zero, indicating many videos are not getting any traction. This makes it hard to assess their potential.
*   **Limited "Identity-Aligned" Data:** Only 48 out of 354 videos (13.6%) are identity-aligned with `generations.json`, suggesting a large portion of the tracked videos might lack detailed metadata for deeper analysis.

## Insights

1.  **"art_creator" Mood Dominates Views, but Retention is Average:** The "art_creator" mood category accounts for the vast majority of views (1,123 out of 1,201 total views) and watch time. However, its average retention of 17.6% is lower than the overall average retention of 24.52%. This suggests that while these videos attract initial clicks, viewers may not be staying for a significant portion of the content. The top 5 videos by views are all "art_creator" videos, specifically "Ambient ancient · 5 Mins · Evolving taik" (237 views, 161 min watch time) and "Ambient contemporary · 5 Mins · Evolving" (105 views, 51 min watch time).
2.  **Micro-Duration Videos Show Extreme Retention (with Low Views):** Several "micro" mood videos, such as "30 Seconds to Enter Flow State" (micro_focus_lock, 559.0% retention) and "10 Seconds to Drop Inward" (micro_drop_inward, 91.8% retention), exhibit exceptionally high retention percentages. While these have very low view counts (1-2 views), their ability to hold or even exceed their duration suggests a strong engagement for those who do click. This could indicate a niche for very short, highly targeted ambient experiences.
3.  **"Ancient" and "Contemporary" Art Periods are Strong Performers:** Among the "art_creator" videos, those tagged with "ancient" and "contemporary" art periods appear frequently in the top 5 by views. Specifically, "Ambient ancient · 5 Mins · Evolving taik" and "Ambient ancient · 5 Mins · Evolving kuku" perform well, as does "Ambient contemporary · 5 Mins · Evolving". This suggests a preference for these aesthetic styles within the "art_creator" category.
4.  **"Taiko" and "None" Music Styles are Popular:** Within the top-performing "art_creator" videos, "taiko" and "none" music styles are notable. "Ambient ancient · 5 Mins · Evolving taik" is the top video by views, and "Ambient future · 5 Mins · Evolving none" is also in the top 5. This indicates that percussive, traditional sounds like Taiko, or perhaps more minimalist soundscapes ("none"), resonate well with the audience.
5.  **Speculative: Potential for "Piano Relax" and "Micro Noise Hush" if Scaled:** The "piano_relax" mood has one video with 97.1% retention from 1 view, and "micro_noise_hush" has 84.0% retention from 1 view. While these are based on extremely limited data, their high retention, even from a single viewer, suggests a strong initial engagement. If these moods could attract more views, they might prove to be highly effective in terms of watch time.

## Experiments or packaging ideas

*   **Test "Micro" Moods with Enhanced Packaging:** Given the extremely high retention of "micro_focus_lock" and "micro_drop_inward" (despite low views), create 3-5 new videos in these or similar "micro" moods (e.g., micro_noise_hush, micro_overthink_b) with optimized titles and thumbnails to try and drive more impressions and clicks. Focus on very specific, immediate benefits in the titles (e.g., "30 Seconds to Instantly Calm Your Mind").
*   **Deep Dive into "Art_Creator" Top Performers:** Analyze the titles, thumbnails, and descriptions of the top 5 "art_creator" videos by views ("Ambient ancient · 5 Mins · Evolving taik", "Ambient contemporary · 5 Mins · Evolving", etc.). Identify common elements in their packaging that might contribute to their higher view counts, and apply these learnings to new "art_creator" content, particularly those with "ancient" and "contemporary" art periods and "taiko" or "none" music styles.
*   **Explore "Piano Relax" with More Content:** Despite only 1 view, the "piano_relax" video showed 97.1% retention. Create 2-3 additional "piano_relax" videos, perhaps varying duration slightly (e.g., 5 mins, 10 mins), to see if this high retention can be replicated and if the mood can attract more viewers.
*   **Re-evaluate Low-Performing Moods with Zero Views:** Review the moods with multiple videos but zero views (e.g., "deep_focus", "energize", "ceremony", "warrior", "ocean_waves"). Consider if their packaging is unappealing or if the mood itself is not resonating. Perhaps a small experiment with a completely different title/thumbnail approach for one of these moods could reveal if the issue is content or presentation.
*   **A/B Test Titles for "Evolving" Content:** Many top-performing videos use "Evolving" in their title. Experiment with different phrasing or additional descriptive words around "evolving" to see if it impacts CTR or views. For example, "Continuously Evolving Soundscape" vs. "Never-Ending Ambient Flow."
