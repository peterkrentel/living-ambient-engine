# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of committed repository files and analytics pipeline excerpts for the personal YouTube ambient music channel for Week 18, 2026. My analysis will focus on identifying key performance trends, risks, and actionable insights based *solely* on this data, and suggest experiments or packaging ideas.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md`: Personal channel analytics report for 2026-W18.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md`: Machine-assembled personal advisory report for 2026-W18.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md`: This file was reported as missing.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json`: JSON data containing suggestions and coverage metrics for the personal channel.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json`: Raw analytics data for individual videos on the personal channel.

## Summary

The personal channel had 753 total views and 4,164 minutes of watch time, gaining 4 subscribers over the analytics window (March 31 to April 27, 2026). The overall average retention was 21.63%, and average watch time per video was 90.522 minutes. "Deep Focus" and "Piano Deep Calm" moods are driving the majority of views and watch time, with "Enter Flow State" being the top-performing video by views. Short-form videos (30 seconds) show exceptionally high retention, but only have 1 view each. Conversely, "Ceremony" mood videos are underperforming significantly in both retention and watch time. The data lacks CTR and impressions, which are noted as optional for the personal fetcher.

## Risks / caveats

*   **Limited Data for Retention Leaders:** The top videos by retention ("Find Your Strength," "Sounds for an Overactive Mind," "sleep_30s_20260124_031441," "trance_30s_20260124_055344") each have only 1 view. While their retention percentages are high (e.g., 96.8%), this is based on an extremely small sample size and is not indicative of broad audience engagement or watch time potential.
*   **Missing CTR and Impressions:** The absence of Click-Through Rate (CTR) and impression data makes it difficult to assess the effectiveness of titles, thumbnails, and discoverability. The report explicitly states that CTR and impressions often move due to packaging and traffic source, which cannot be analyzed here.
*   **Confounders:** The advisory report highlights that correlation at the bucket level (e.g., mood) should not be treated as proof that generation parameters drove a result when packaging differed. This means observed performance differences could be due to factors like titles, thumbnails, or traffic sources, which are not fully analyzed in this bundle.
*   **Low Coverage for Some Moods:** Many moods have very few videos with views (e.g., "trance" with 4 videos, "warrior" with 2, "sleep" with 1), or no views at all (e.g., "chill," "ocean_waves"). This makes it difficult to draw robust conclusions about their performance.
*   **Missing `run-intent-blocked-personal.md`:** The absence of this file means we cannot see if any specific content generation intents were blocked, which could provide context for content strategy.
*   **No Art Period or Music Style Data:** The `suggestions_personal.json` shows zero videos with views for any `art_periods` or `music_styles`, indicating these metadata fields are not currently being tracked or are not relevant to the current content.

## Insights

1.  **Deep Focus and Piano Deep Calm Drive Engagement:** The "deep_focus" and "piano_deep_calm" moods are the strongest performers. "Piano_deep_calm" has the highest total views (304) and significantly high watch time per video (+324.5 min vs channel avg), despite having slightly lower retention than the channel average. "Deep_focus" also performs well with 243 views and 25.8% average retention. This suggests a strong audience preference for these types of ambient music.
2.  **Long-Form Content is Key for Watch Time:** The top videos by views, such as "Enter Flow State" (deep_focus, 299 views, 120 min watch time) and "Calm Anxiety Fast" (piano_deep_calm, 55 views, 867 min watch time), are all 1-hour or longer. This indicates that while short 30-second clips might have high retention percentages, they contribute negligible watch time and views. The audience on this channel appears to be seeking longer, sustained ambient experiences.
3.  **"Ceremony" Mood Underperforms:** The "ceremony" mood is a significant underperformer, showing -19.3% retention vs. channel average and -50.2 min watch time per video vs. channel average, despite having 11 videos tracked and 6 with views. This suggests that content categorized under "ceremony" is not resonating with the audience in its current form.
4.  **Speculative: Short-Form Content for Discovery vs. Watch Time:** The 30-second videos with high retention but only 1 view ("Find Your Strength," "Sounds for an Overactive Mind," "sleep_30s_20260124_031441," "trance_30s_20260124_055344") might indicate a potential for short-form content as hooks or teasers, but they are not currently generating significant viewership. Their high retention on single views is not a reliable indicator of success.
5.  **Speculative: Opportunity in Under-explored High-Retention Moods:** Moods like "warrior" (78.0% avg retention from 11 videos, 2 with views) and "sleep" (83.6% avg retention from 9 videos, 1 with view) show high average retention, albeit with very low view counts. This could indicate a niche interest or a strong connection with the few viewers they have attracted. Further exploration with more videos and better packaging in these moods might reveal untapped potential.

## Experiments or packaging ideas

*   **Double Down on "Deep Focus" and "Piano Deep Calm":**
    *   Create more long-form videos (1+ hour) in the "deep_focus" and "piano_deep_calm" moods.
    *   Experiment with variations within these moods, e.g., "Deep Focus with gentle rain" or "Piano Deep Calm with subtle nature sounds."
    *   Analyze the titles and thumbnails of top-performing videos like "Enter Flow State" and "Calm Anxiety Fast" to identify common elements that could be replicated.
*   **Re-evaluate "Ceremony" Content:**
    *   Investigate the specific videos under the "ceremony" mood to understand why they are underperforming. Are the titles, thumbnails, or actual audio experiences not aligning with audience expectations?
    *   Consider pausing new "ceremony" content until more data or insights are gathered, or experiment with drastically different packaging (titles, thumbnails) for existing "ceremony" videos to see if performance improves.
*   **Explore "Warrior" and "Sleep" with Caution:**
    *   Given the high retention but low views for "warrior" and "sleep," consider creating a small batch of new videos for these moods.
    *   Focus on compelling titles and thumbnails that clearly communicate the mood and potential benefits (e.g., "Warrior's Focus: Epic Ambient for Strength" or "Deep Sleep Ambient: Uninterrupted Rest").
    *   Monitor these new videos closely for initial views and watch time to determine if the high retention was an anomaly or a sign of niche appeal.
*   **Short-Form Content Strategy (Speculative):**
    *   If the goal is to leverage high retention from short clips, consider using 30-second videos as YouTube Shorts or as promotional snippets for longer videos.
    *   Do not rely on 30-second videos as primary content for watch time generation.
*   **Implement CTR and Impressions Tracking:**
    *   Prioritize extending the personal fetcher to include CTR and impressions as suggested in `docs/PERSONAL_ANALYTICS.md`. This data is crucial for understanding discoverability and the effectiveness of packaging elements like titles and thumbnails.
