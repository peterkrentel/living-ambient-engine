# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of personal channel analytics reports and suggestions for Week 18, 2026. My analysis will focus on identifying key performance trends, risks, and actionable insights based solely on the data presented in these files.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md` (Personal channel analytics report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md` (Personal advisory report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Personal channel suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw personal channel analytics data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md` (Missing file)

## Summary

The personal channel tracked 114 videos over the analytics window of March 30 to April 26, 2026, accumulating 755 total views and 4,224 minutes of watch time, gaining 4 subscribers. The overall average retention for videos with views is 22.33%, and the average watch time per video is approximately 91.8 minutes. "Deep Focus" and "Piano Deep Calm" moods are driving the most views and watch time, with "Piano Deep Calm" showing a significant positive deviation in watch time per video despite lower retention compared to the channel average. Conversely, "Ceremony" mood videos are underperforming in both retention and watch time. A significant portion of videos (71.9%) are linked to a ledger row, but only 31.6% are identity-aligned.

## Risks / caveats

*   **Limited Data for Retention:** The "Top 5 by Retention" table shows several videos with very high retention (e.g., 96.8%) but only 1 view. This makes these retention figures unreliable for drawing conclusions about content quality or audience engagement.
*   **Confounders:** The `run-next` report explicitly states that CTR, impressions, and retention are often influenced by packaging (title, thumbnail, traffic source, seasonality) and not solely by generation parameters like mood. Without CTR and impressions data, it's difficult to fully understand why certain videos perform better or worse.
*   **Data Coverage:** Only 46 out of 114 videos had views in the analyzed window, meaning over half of the content is not contributing to the current performance metrics.
*   **Missing Report:** The `run-intent-blocked-personal.md` file is missing, which could indicate a blocked intent or simply that no intents were blocked. This absence means we cannot assess any potential issues with automated content generation or publishing.
*   **Thin Data for Moods:** Many moods have very low video counts and/or views (e.g., "trance" with 10 videos but only 7 views, "warrior" with 11 videos and 5 views). This makes it difficult to draw statistically significant conclusions about their performance.
*   **No Art Period/Music Style Data:** The `suggestions_personal.json` file shows zero totals and views for all listed `art_periods` and `music_styles`, indicating these parameters are not currently being tracked or applied to the personal channel's content.

## Insights

1.  **Deep Focus and Piano Deep Calm Drive Engagement:** The "deep_focus" mood has the highest total views (243) and "piano_deep_calm" has the highest total views (306) and significantly higher watch time per video (+323.2 min vs channel avg). This suggests these moods resonate strongly with the audience, indicating a preference for content that aids concentration or provides deep relaxation through piano.
2.  **Short-form Content Shows High Initial Retention:** The top retention videos are all 30-second clips, with "Find Your Strength" (warrior) and "Sounds for an Overactive Mind" (deep_focus) both achieving 96.8% retention. While these have only 1 view, it suggests that very short, targeted content can capture immediate attention effectively.
3.  **Long-form Content Drives Watch Time:** The top videos by views, such as "Enter Flow State" (1 Hour Zero Distracti, deep_focus) and "Calm Anxiety Fast" (1 Hour Deep Piano Re, piano_deep_calm), are longer-form content. These videos are responsible for substantial watch time, with "Calm Anxiety Fast" contributing over 850 minutes each from two separate uploads. This confirms the value of longer videos for overall channel engagement.
4.  **Speculative: Opportunity for "Warrior" and "Trance" in Short Form:** While "warrior" and "trance" moods have very low total views (5 and 7 respectively), their average retention percentages are high (78.0% and 40.5%). This is particularly notable for "warrior," which has a 30-second video at 96.8% retention. This hints that while these moods might not be attracting broad viewership, the few viewers they do attract are highly engaged, especially with shorter formats.
5.  **"Ceremony" Mood Underperforms:** The "ceremony" mood shows poor performance, with low average retention (1.5%) and a negative deviation in watch time per video (-51.5 min vs channel avg). This indicates that content tagged with "ceremony" is not engaging viewers effectively, leading to quick drop-offs.

## Experiments or packaging ideas

*   **Double Down on "Deep Focus" and "Piano Deep Calm":**
    *   Create more long-form videos (1 hour+) in these moods, focusing on titles and thumbnails that clearly communicate their benefits for concentration and relaxation.
    *   Experiment with different variations within these moods (e.g., "Deep Focus with gentle rain," "Piano Deep Calm for evening study").
*   **Investigate High-Retention, Low-View Short-Form Content:**
    *   Re-package the 30-second "warrior" and "deep_focus" clips that showed high retention into longer compilations or use them as promotional material for longer videos.
    *   **Speculative:** Test if similar short, impactful clips for "trance" could also achieve high retention, and then explore longer versions.
*   **Analyze "Ceremony" Content for Improvement:**
    *   Review the actual "ceremony" videos to understand what might be causing low retention. Is it the audio style, visual, or perceived utility?
    *   Experiment with different titles/thumbnails for existing "ceremony" videos to see if improved packaging can boost initial engagement.
    *   **Speculative:** Consider if "ceremony" might perform better as shorter, more intense experiences rather than long-form ambient.
*   **Improve Data Coverage:**
    *   Focus on generating content for moods that currently have low video counts or no views, to gather more data and identify potential hidden gems.
    *   Ensure all new uploads are correctly logged and identity-aligned in the `generations.json` ledger to improve data correlation.
*   **Expand Analytics Metrics (as per Next Steps):**
    *   Prioritize extending the personal fetcher to include CTR and impressions. This data is crucial for understanding the initial appeal of titles and thumbnails, which are identified as key confounders.
