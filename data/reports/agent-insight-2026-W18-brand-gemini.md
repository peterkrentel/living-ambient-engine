# Agent advisory — Gemini (API) (brand, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of analytics reports, including the weekly analytics, the "run next" advisory, the "run intent blocked" report, and the `suggestions.json` and `analytics.json` files. My aim is to synthesize these metrics into actionable insights and suggest experiments for the YouTube ambient music channel.

## What I reviewed

- `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18.md` (Weekly Analytics Report)
- `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18.md` (Run next — advisory)
- `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked.md` (Run intent — BLOCKED)
- `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions.json` (Suggestions data)
- `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics.json` (Raw analytics data)

## Summary

The channel had a total of 1,201 views and 827 minutes of watch time, gaining 4 subscribers over the analytics window (March 31 - April 27, 2026). The "art_creator" mood category dominates in terms of total views (1,123 views from 230 videos), but its average retention is 17.6%. Several "micro" moods and "piano_relax" show exceptionally high retention percentages, though with very low view counts (1-2 views). The "run intent" for this week is blocked due to no actionable mood increases passing the planner gate, indicating a lack of statistically significant trends for scaling.

## Risks / caveats

The "Packaging & confounders" section in `run-next-2026-W18.md` explicitly states that correlation between mood/art-period labels and outcomes should not be treated as proof of causation, as CTR, impressions, and retention are heavily influenced by title, thumbnail, traffic source, and seasonality. Many of the high-retention videos have extremely low view counts (1-2 views), making their retention percentages statistically unreliable for drawing broad conclusions. The planner being blocked also indicates that there aren't strong, statistically significant signals for scaling specific moods this week. A significant portion of videos (82.5%) lack a `generations.json` join, which could limit the depth of analysis for generation parameters.

## Insights

1.  **"art_creator" mood drives volume but has moderate retention.** The "art_creator" mood accounts for the vast majority of views (1,123 out of 1,201 total views) and videos (230 out of 354). While it's the primary driver of channel activity, its average retention of 17.6% is below the overall average retention of 24.52%. This suggests that while these videos attract viewers, there might be opportunities to improve their engagement. The top 5 videos by views are all within the "art_creator" mood, featuring "Ambient ancient," "Ambient contemporary," "Ambient future," and "Ambient baroque" themes, often with "Evolving" soundscapes like "taik," "none," "game," and "kuku."

2.  **Micro-duration videos show extremely high, but low-volume, retention.** Several "micro" moods, such as "micro_focus_lock" (559.0% retention), "micro_drop_inward" (91.8%), "micro_noise_hush" (84.0%), and "micro_stuck_jolt" (68.2%), exhibit exceptionally high retention percentages. Similarly, "piano_relax" shows 97.1% retention. However, these videos each have only 1 or 2 views, making these retention figures highly unreliable as indicators of broad success. The "559.0%" retention for "30 Seconds to Enter Flow State" is an outlier and likely a data anomaly given its 2 views.

3.  **"Ancient" and "Contemporary" art periods are strong view drivers.** Within the "art_creator" mood, videos featuring "Ambient ancient" and "Ambient contemporary" themes appear multiple times in the Top 5 by Views. Specifically, "Ambient ancient | 5 Mins | Evolving taik" garnered 237 views and 161 minutes of watch time, and another "Ambient ancient | 5 Mins | Evolving kuku" received 81 views and 41 minutes. "Ambient contemporary | 5 Mins | Evolving" had 105 views and 51 minutes. This suggests these specific art periods, combined with "Evolving" soundscapes, resonate well with the audience in terms of initial attraction.

4.  **Speculative: Short, targeted "micro" experiences could be a niche.** Despite the low view counts, the extremely high retention percentages for "micro" moods like "micro_focus_lock" and "micro_drop_inward" suggest that for the few viewers who discover them, these very short, highly specific ambient tracks might be incredibly effective for their intended purpose. If these videos can gain more visibility, their high engagement could translate into valuable audience segments.

5.  **Many moods and categories have zero or very few views.** A significant number of moods (e.g., "ocean_waves," "deep_focus," "rain_sleep," "ceremony," "warrior," "energize," and many "micro" moods) have 0 views or very few views (1-4 views). Similarly, many `art_music_combos` in `suggestions.json` have 0 views. This indicates either a lack of discovery for these videos or that these specific combinations are not currently appealing to the audience. This wide distribution of low-performing content dilutes overall channel performance and makes it harder to identify clear winners.

## Experiments or packaging ideas

*   **Focus on "art_creator" variations with strong view counts:**
    *   Create more videos combining "ancient" and "contemporary" art periods with "evolving" soundscapes, specifically exploring "taiko" and "kuku" music styles, given their performance in the Top 5 by Views.
    *   Experiment with titles and thumbnails for these high-view "art_creator" videos to see if CTR can be improved, potentially boosting overall retention for this dominant category.

*   **Test discoverability for high-retention "micro" moods:**
    *   Given the high retention but low views for "micro_focus_lock," "piano_relax," and "micro_drop_inward," create new videos in these moods with more descriptive and enticing titles/thumbnails.
    *   **Speculative:** Consider promoting these "micro" videos as short, targeted solutions (e.g., "30-Second Focus Boost," "1-Minute Stress Release") in community posts or as YouTube Shorts to drive initial traffic and see if retention holds at higher volumes.

*   **Investigate low-performing moods:**
    *   For moods with 0 views like "deep_focus," "ocean_waves," and "energize," review their existing titles and thumbnails. Are they accurately representing the content? Are they competitive?
    *   **Speculative:** Try re-packaging one or two of these zero-view moods with completely different titles and thumbnails to see if discoverability is the primary issue, rather than the mood itself.

*   **Analyze video duration impact:**
    *   The top performing videos are all "5 Mins." The high-retention "micro" videos are shorter ("30 Seconds," "10 Seconds"). Explore if there's an optimal duration for different mood categories.
    *   **Speculative:** Experiment with slightly longer versions (e.g., 10-15 minutes) of the successful "art_creator" themes to see if watch time can be extended without significantly dropping retention.

*   **Improve data coverage and reporting:**
    *   Address the low `generations.json` join rate (only 13.6% identity-aligned). Better logging of historic uploads is crucial for a more comprehensive analysis of generation parameters.
    *   Since the planner is blocked, consider using the `--force-moods` option for development/smoke testing to generate `run_intent.json` and gain more insights, even if not immediately actionable for scaling.
