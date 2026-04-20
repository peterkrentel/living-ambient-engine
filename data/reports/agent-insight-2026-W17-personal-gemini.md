# Agent advisory — Gemini (API) (personal, 2026-W17)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of personal channel analytics reports and suggestions for Week 17, 2026. My goal is to extract actionable insights and suggest experiments based *only* on the data presented, acknowledging any limitations or blocked recommendations.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W17-personal.md`: Personal channel analytics report for 2026-W17.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W17-personal.md`: Personal advisory report for 2026-W17, including packaging and confounder notes.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md`: Report indicating that no actionable mood increases passed the planner gate.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json`: Raw JSON data for personal channel suggestions, including overall metrics and mood coverage.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json`: Raw JSON data containing detailed video metrics for the personal channel.

## Summary

The personal channel saw modest activity in the `2026-03-23` to `2026-04-19` window, with 312 total views, 892 minutes of watch time, and 4 new subscribers across 107 videos with analytics. The overall average retention was 16.85%, and average watch time per video was approximately 33 minutes. The automated planner for "actionable mood increases" was blocked this week due to insufficient data (n<5 or group_views<200 for any mood suggestion). "Deep focus" and "piano_deep_calm" moods appear to be driving the most views, while "piano_ambient" and "warrior" show strong retention on individual videos, albeit with very low view counts.

## Risks / caveats

*   **Low N for Top Performers:** Many top retention videos have only 1 view, making their high retention percentages unreliable for generalization. Similarly, some moods with high average retention (e.g., `warrior` at 57.0%, `piano_ambient` at 49.8%) are based on a very small number of videos (11 and 2 videos respectively) and low total views (9 and 2 views respectively).
*   **Planner Blocked:** The automated system could not identify any "actionable" mood increases, meaning there isn't enough statistically significant data to confidently recommend doubling down on specific moods based on the defined thresholds (n≥5, group_views≥200).
*   **Confounders:** The `run-next` report explicitly warns that CTR, impressions, and retention are heavily influenced by packaging (title, thumbnail, traffic source, seasonality) and not solely by mood or art-period labels. Without CTR and impressions data (which is an optional extension for the personal fetcher), it's difficult to assess the full funnel performance.
*   **Limited Data Scope:** The analysis is limited to the personal channel only. Cross-analysis with brand reports is suggested in the next steps but not performed here.
*   **Missing Metadata:** The `suggestions_personal.json` shows zero coverage for `art_periods` and `music_styles`, indicating these metadata fields are not being tracked or are not present in the analyzed videos, limiting insights into these dimensions.

## Insights

1.  **Deep Focus Dominates Views:** The `deep_focus` mood category is a clear leader in terms of total views (172 views from 9 videos) and watch time, with "Enter Flow State | 1 Hour Zero Distracti" alone garnering 116 views and 289 minutes of watch time. This suggests a strong audience interest in content designed for concentration.
2.  **High Retention for Specific Piano Ambient:** The video "Let Go of Stress | 2 Hours Soft Piano Am" (mood: `piano_ambient`) achieved an exceptional 99.2% retention from its single view, indicating that for the viewer who found it, it was highly engaging. Another `piano_deep_calm` video, "Let Go of Stress | Deep Calm Piano Atmos", also showed decent retention at 41.8% with 11 views.
3.  **Speculative: Longer Content for Engagement:** The top retention video is 2 hours long, and the top view-generating video is 1 hour long. This, combined with the overall average watch time of 33 minutes per video, suggests that longer-form ambient content (1-2 hours) might be more successful in capturing and retaining audience attention on this channel.
4.  **Warrior Mood Shows Potential Retention:** Despite only 9 views across 11 videos, the `warrior` mood has a high average retention of 57.0%. This is based on a single video `warrior_10s_20260124_160306` which has 9 views and 57.0% retention. This could indicate a niche but engaged audience for this specific mood, though the low view count makes it highly speculative.
5.  **Underperforming Moods:** Several moods, including `piano_evening`, `rain_piano`, `piano_gentle`, `chill`, `sleep`, `lofi_study`, and `ocean_waves`, show 0 views across multiple videos. This indicates either a lack of audience interest, poor discoverability, or issues with packaging for these categories.

## Experiments or packaging ideas

*   **Deep Focus Expansion:**
    *   Create more videos in the `deep_focus` mood, potentially exploring variations in soundscapes or visual styles.
    *   Experiment with different lengths for `deep_focus` content, given the success of the 1-hour video.
*   **Long-form Piano Ambient:**
    *   Produce more 2-hour `piano_ambient` videos, specifically replicating the "Soft Piano Ambient" style that achieved 99.2% retention.
    *   Test titles and thumbnails that emphasize "soft piano" and "stress relief" or "relaxation."
*   **Warrior Mood Niche Test:**
    *   Given the high retention on one `warrior` video, consider creating 1-2 more `warrior` mood videos with similar characteristics (e.g., short, impactful).
    *   Focus on strong, descriptive titles and thumbnails that clearly convey the "warrior" theme to attract the right audience.
*   **Content Length Analysis:**
    *   Systematically analyze the relationship between video duration and retention/watch time across all moods, especially for videos with more than a few views.
*   **Revitalize Underperforming Moods:**
    *   For moods with 0 views, such as `sleep` or `chill`, experiment with different titles and thumbnails to improve discoverability.
    *   **Speculative:** Consider if these moods are adequately represented by the generated audio/visuals or if the current packaging doesn't resonate with potential viewers.
*   **A/B Test Titles/Thumbnails:**
    *   Since packaging is a known confounder, plan to A/B test different titles and thumbnails for new videos within successful mood categories to optimize CTR and impressions (once these metrics are fetched).
*   **Binaural Beats & Solfeggio Callout:**
    *   Many video descriptions mention "Uses binaural beats & Solfeggio frequencies." Experiment with highlighting this more prominently in titles or thumbnails for relevant videos, as it could be a strong selling point for a specific audience segment.
