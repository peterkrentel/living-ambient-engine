# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of personal channel analytics reports and suggestions for Week 18, 2026. My analysis will focus on identifying key performance trends, risks, and actionable insights to inform content strategy for the personal YouTube ambient music channel, using only the data provided.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md` (Personal channel analytics report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md` (Run next — personal advisory)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Personal channel suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw personal channel analytics data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md` (Missing file)

## Summary

The personal channel tracked 114 videos over the analytics window (March 30 to April 26, 2026), accumulating 755 total views and 4,224 minutes of watch time, gaining 4 subscribers. The overall average retention was 22.33%, and the average watch time per video with views was approximately 91.8 minutes. "Deep focus" and "piano_deep_calm" moods are performing well in terms of views and watch time, with "piano_deep_calm" showing a significant positive deviation in watch time per video despite lower retention. Conversely, "ceremony" mood videos are underperforming in both retention and watch time. A significant portion of videos (68 out of 114) did not register any views during this period. The `run-intent-blocked-personal.md` file was missing, indicating no blocked intents for the personal channel.

## Risks / caveats

*   **Low View Counts:** Many videos, especially those with high retention, have only 1 view, making their retention percentages less reliable for generalization.
*   **Limited Data for Moods:** Several moods have very few videos or zero views, making it difficult to draw conclusions about their performance. For example, "piano_evening", "rain_piano", "piano_gentle", "chill", "lofi_study", and "ocean_waves" all have 0 views.
*   **Confounders:** The `run-next` report explicitly states that "CTR, impressions, and retention often move because of title, thumbnail, traffic source, and seasonality" and not necessarily due to mood or art-period labels. This means that observed correlations are not proof of causation by generation parameters alone.
*   **Missing Data:** The `run-intent-blocked-personal.md` file is missing, so any potential blocked content intents are unknown.
*   **Incomplete Metadata Join:** Only 31.6% of videos are "identity-aligned" with `generations.json`, which could limit the depth of analysis if more detailed generation parameters were needed.

## Insights

1.  **Deep Focus and Piano Deep Calm Drive Watch Time:** The "deep_focus" mood is a strong performer, with "Enter Flow State" (deep_focus) being the top video by views (299) and watch time (120 minutes). "piano_deep_calm" videos, while having a slightly lower average retention than the channel average, contribute significantly to watch time per video (323.2 minutes above average for 7 videos with 255 views). This suggests that while viewers might not watch the entire "piano_deep_calm" video, those who do engage for a very long duration.
2.  **Short, High-Retention Content:** Videos with very high retention (e.g., "Find Your Strength" and "Sounds for an Overactive Mind" at 96.8%) are all 30-second clips with only 1 view. While these show excellent engagement for their short duration, their low view count limits their impact on overall channel performance and generalizability.
3.  **Ceremony Mood Underperforms:** The "ceremony" mood shows significant underperformance, with retention 20.0% below the channel average and watch time per video 51.5 minutes below average (for 3 videos with 105 views). This indicates that content tagged with "ceremony" is not resonating well with the audience in terms of sustained engagement.
4.  **Speculative: Trance and Warrior Moods for Niche Engagement:** While "trance" and "warrior" moods have very low total views (7 and 5 respectively), their average retention percentages are quite high (40.5% and 78.0%). This suggests that for the few viewers who discover these, the content is highly engaging, potentially indicating a niche but dedicated audience.
5.  **Speculative: Opportunity for Longer-Form Deep Focus Content:** Given that "Enter Flow State" (1 Hour Zero Distraction) and "Sounds for an Overactive Mind" (1 Hour E) are top performers by views and watch time, and both are "deep_focus" mood, there's a strong indication that longer-form content in the "deep_focus" category is highly valued and drives significant engagement.

## Experiments or packaging ideas

*   **Double Down on "Deep Focus" Long-Form:**
    *   Create more 1-hour or longer videos explicitly tagged with "deep_focus" and titles emphasizing concentration, flow state, or zero distraction.
    *   Experiment with different visual styles or subtle ambient elements within the "deep_focus" mood to see if it further enhances engagement.
*   **Optimize "Piano Deep Calm" for Retention:**
    *   Investigate the titles and thumbnails of the "piano_deep_calm" videos that are driving high watch time but lower retention. Are they attracting viewers who quickly realize it's not what they expected, or are they simply very long videos where a 18.5% retention still means significant watch time?
    *   Consider A/B testing titles and descriptions for "piano_deep_calm" videos to better set expectations for the content and potentially improve initial retention.
*   **Re-evaluate "Ceremony" Content:**
    *   Analyze the specific "ceremony" videos that are underperforming. Are there common themes in their titles, descriptions, or audio characteristics that could explain the low retention and watch time?
    *   Consider pausing new "ceremony" content or experimenting with significantly different packaging (titles, thumbnails) for existing "ceremony" videos to see if performance improves.
*   **Explore "Trance" and "Warrior" Niche:**
    *   Given the high retention for "trance" and "warrior" despite low views, consider creating a small batch of new content in these moods.
    *   Focus on optimizing titles and descriptions for discoverability within these niche categories, perhaps targeting specific search terms or communities.
*   **Analyze 30-Second Clips:**
    *   While high retention for 30-second clips is notable, their impact is minimal due to 1 view. Investigate if these short clips could be repurposed as promotional material for longer videos or as Shorts to drive traffic to the main channel.
