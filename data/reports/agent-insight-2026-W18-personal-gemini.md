# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of personal channel analytics reports and suggestions for 2026-W18, along with the raw analytics JSON. My analysis will focus on identifying patterns in video performance related to mood, retention, and watch time, and suggesting experiments based on this data.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md` (Personal channel analytics report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md` (Run next — personal advisory)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Personal channel suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw personal channel analytics data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md` (Not found/missing)

## Summary

The personal channel tracked 114 videos over the period of 2026-03-31 to 2026-04-27, accumulating 753 total views and 4,164 minutes of watch time, gaining 4 subscribers. The overall average retention was 21.63%, and average watch time per video was 90.522 minutes. "Deep_focus" and "piano_deep_calm" moods show strong performance in terms of views and watch time, with some "deep_focus" videos also appearing in top retention. Conversely, "ceremony" mood videos are underperforming in both retention and watch time. The data coverage for `art_periods` and `music_styles` is entirely zero, indicating no videos are currently tagged with these parameters or they are not being tracked.

## Risks / caveats

*   The `run-intent-blocked-personal.md` file is missing, so any blocked intents for the personal channel are unknown.
*   The "Run next" report explicitly states that correlation addresses "patterns in the data," not "hidden causes," and that CTR, impressions, and retention are often influenced by "title, thumbnail, traffic source, and seasonality," not solely by generation parameters. This means that observed correlations with 'mood' might be confounded by packaging differences.
*   Many moods have very low view counts (e.g., "trance" with 7 views, "warrior" with 5 views), making their retention percentages (e.g., "warrior" at 78.0%, "trance" at 40.5%) potentially unreliable indicators of broad appeal.
*   The `suggestions_personal.json` shows no coverage for `art_periods` or `music_styles`, which means any insights related to these categories are not possible from the provided data.
*   Only 46 out of 114 videos had views, and only 31.6% of videos were "identity-aligned" with `generations.json`, suggesting incomplete metadata or tracking for a significant portion of the content.

## Insights

1.  **Deep Focus and Piano Deep Calm Drive Watch Time:** Videos categorized under "deep_focus" and "piano_deep_calm" moods are significant drivers of watch time. "Enter Flow State" (deep_focus) garnered 299 minutes of watch time from 120 views, and "Calm Anxiety Fast" (piano_deep_calm) had 867 and 854 minutes from 55 and 49 views respectively. The `piano_deep_calm` mood, in particular, shows a substantial +324.5 minutes vs. channel average for watch time per video, despite a slightly lower retention percentage (-4.3% vs channel avg). This suggests that while viewers might not watch the entire video, they engage for long durations when they do.
2.  **High Retention for Short, Specific Moods:** Shorter videos (e.g., "30 Seconds Power Dr" and "30 Secon") for moods like "warrior" and "deep_focus" achieved exceptionally high retention rates (96.8%) despite having only 1 view each. Similarly, "sleep" (83.6%) and "fireplace" (47.8%) moods also show high retention, though with very low view counts. This indicates that when these niche, shorter videos are discovered, they are highly effective at holding the viewer's attention for their intended duration.
3.  **Ceremony Mood Underperforms:** The "ceremony" mood is a clear underperformer, with significantly lower retention (-19.3% vs channel avg) and watch time per video (-50.2 min vs channel avg). With 11 videos and 131 total views, its average retention is only 1.5%. This suggests that content tagged with "ceremony" is not resonating well with the audience in its current form.
4.  **Speculative: Potential for Longer Deep Focus Content:** Given that "Enter Flow State" (deep_focus) is the top video by views and watch time, and other "deep_focus" videos also perform well, there might be an appetite for longer-form content within this mood. The high watch time suggests utility for users seeking extended periods of concentration.
5.  **Speculative: Explore Niche, High-Retention Moods with More Content:** While view counts are low, the high retention for moods like "warrior," "sleep," and "trance" (when viewed) indicates strong engagement for those who find them. Expanding the library or improving discoverability for these specific, high-retention niches could yield positive results, especially if the content fulfills a very specific user need.

## Experiments or packaging ideas

*   **Double Down on "Deep Focus" and "Piano Deep Calm" Long-Form:**
    *   Create more 1-hour+ videos for "deep_focus" and "piano_deep_calm" moods, focusing on titles and thumbnails that clearly communicate their utility for work, study, or deep relaxation.
    *   Experiment with different variations within these moods (e.g., "Deep Focus with gentle rain," "Piano Deep Calm with subtle binaural beats").
*   **Re-evaluate "Ceremony" Content:**
    *   Analyze the specific titles and thumbnails of "ceremony" videos to identify potential reasons for low performance beyond the mood itself.
    *   Consider pausing new "ceremony" content or significantly re-tooling its presentation and sound design based on what makes "deep_focus" and "piano_deep_calm" successful.
    *   **Speculative:** Test "ceremony" content with different lengths or as part of a themed playlist to see if context improves engagement.
*   **Promote High-Retention, Low-View Niche Content:**
    *   For moods like "warrior," "sleep," and "trance" that show high retention on individual videos, create dedicated playlists or promote them through community posts to increase discoverability.
    *   **Speculative:** Develop slightly longer versions (e.g., 5-10 minutes) of the highly retained 30-second clips to see if the engagement scales.
*   **Improve Metadata and Tracking:**
    *   Ensure all new and existing videos are properly tagged with `mood`, `art_periods`, and `music_styles` to enrich future analytics. The current lack of data for `art_periods` and `music_styles` is a missed opportunity for deeper insights.
    *   Investigate why only 31.6% of videos are "identity-aligned" with `generations.json` to improve data completeness.
*   **A/B Test Titles and Thumbnails for Top Performers:**
    *   Given the "Run next" report's emphasis on packaging, A/B test different titles and thumbnails for new "deep_focus" and "piano_deep_calm" videos to optimize CTR and impressions, which are currently not tracked but are crucial for overall performance.
