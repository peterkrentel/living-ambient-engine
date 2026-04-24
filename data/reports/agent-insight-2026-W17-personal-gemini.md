# Agent advisory — Gemini (API) (personal, 2026-W17)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of personal channel analytics reports and related data for 2026-W17. This response will summarize the key performance metrics, identify potential risks, and offer insights and experimental ideas based solely on the context provided.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W17-personal.md` (Personal channel Analytics Report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W17-personal.md` (Run next — personal advisory)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md` (Run intent — BLOCKED)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Personal suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw personal analytics data)

## Summary

The personal channel, over the analytics window of March 27 to April 23, 2026, generated 650 total views and 1,987 minutes of watch time, gaining 6 subscribers. The overall average retention was 18.59%, with an average watch time of 43.196 minutes per video for the 46 videos with views. The planner for this week was blocked due to no actionable mood increases meeting the criteria (n≥5, group_views≥200). "Piano_deep_calm" was identified as an exploratory mood with high watch time per video but lower retention.

## Risks / caveats

*   **Low N for Top Retention:** The top retention videos ("Find Your Strength", "sleep_30s_20260124_031441", "trance_30s_20260124_055344", "Sounds for an Overactive Mind") each have only 1 view, making their high retention percentages unreliable indicators for future performance without more data. The "warrior_10s_20260124_160306" video has 9 views, which is still a small sample size.
*   **Planner Blocked:** The system's planner was blocked because no mood passed the actionable threshold (n≥5 videos, group views≥200). This means there's no machine-generated "lean in" recommendation for immediate scaling, requiring manual interpretation of exploratory data.
*   **Confounders:** The `run-next` report explicitly states that CTR, impressions, and retention are influenced by packaging (title, thumbnail, traffic source, seasonality), not solely by mood or art-period labels. Correlation does not imply causation.
*   **Limited Data:** The personal channel data lacks metrics like CTR and impressions, which are crucial for understanding audience engagement and discovery. The report suggests extending the personal fetcher to include these.
*   **Brand vs. Personal:** The report highlights that brand metrics are separate and not merged into personal correlate, requiring deliberate comparison between the two lanes.

## Insights

1.  **Deep Focus and Piano Deep Calm Drive Views and Watch Time:** The "deep_focus" mood accounts for the highest total views (232) and includes the top-performing video by views, "Enter Flow State" (124 views, 334 watch minutes). "Piano_deep_calm" also performs strongly in total views (225) and watch time, with "Calm Anxiety Fast" generating significant watch time (244 minutes for 38 views, and 145 minutes for 29 views). These moods appear to resonate well with the audience for longer viewing sessions.
2.  **Short-form Content Shows High Retention, but Low Views:** Videos with very high retention percentages (e.g., "Find Your Strength" at 96.8%, "sleep_30s_20260124_031441" at 83.6%) are predominantly short-form (30 seconds or 10 seconds) and have only 1 to 9 views. This suggests that while these short clips hold attention effectively for those who click, they are not currently driving significant overall viewership.
3.  **"Piano_deep_calm" is a Mixed Signal:** While "piano_deep_calm" shows promising watch time per video (+83.1 min vs channel avg) in the exploratory "lean in" section, it simultaneously appears in the "tread carefully" section for having lower retention (-11.2% vs channel avg). This indicates that while viewers might watch these videos for a long duration, they might not be watching a large *percentage* of the video, suggesting potential issues with overall video length or initial engagement.
4.  **Speculative: Warrior Mood Potential for Engagement:** The "warrior" mood, despite having only 10 total views across 11 videos, shows a very high average retention of 76.9%. One specific "warrior" video, "warrior_10s_20260124_160306", has 9 views and 57.0% retention. This suggests that while discovery is low, the content itself is highly engaging for those who find it.
5.  **Lack of Diversity in Top Performers:** The top 5 videos by views are dominated by "deep_focus" and "piano_deep_calm" moods. While these are strong performers, relying too heavily on a few moods might limit channel growth if audience preferences shift or if these niches become saturated. The `suggestions_personal.json` also shows many moods with 0 views, indicating a broad content library with uneven performance.

## Experiments or packaging ideas

*   **Deep Focus & Piano Deep Calm Long-Form Optimization:**
    *   Create more 1-hour or longer videos explicitly titled for "deep focus" and "calm anxiety" using piano-based ambient sounds, similar to "Enter Flow State" and "Calm Anxiety Fast."
    *   Experiment with different thumbnail designs for these proven moods to potentially improve CTR.
*   **Investigate "Piano_deep_calm" Retention:**
    *   Analyze the specific videos within the "piano_deep_calm" mood that have high watch time but low retention. Are they too long? Is the intro too slow?
    *   Test shorter versions of "piano_deep_calm" videos (e.g., 30-minute or 45-minute versions) to see if retention improves while maintaining watch time.
*   **Short-Form Content Strategy Review:**
    *   For high-retention short videos (e.g., "Find Your Strength" - warrior, "sleep_30s"), consider repurposing them as YouTube Shorts or as promotional snippets for longer videos.
    *   Experiment with different titles and descriptions for these short videos to improve discoverability, as their current view counts are very low despite high retention.
*   **Warrior Mood Exploration:**
    *   Given the high average retention for "warrior" mood, consider producing a longer-form "warrior" ambient track (e.g., 30 minutes to 1 hour) to see if the high engagement translates to longer watch times and more views.
    *   **Speculative:** Explore titles that explicitly target "strength," "focus," or "motivation" for the "warrior" mood.
*   **Cross-Promote High-Retention, Low-View Content:**
    *   Add end screens or cards to popular "deep_focus" or "piano_deep_calm" videos that link to the high-retention, low-view videos (e.g., "warrior" or "sleep" shorts) to drive internal traffic.
