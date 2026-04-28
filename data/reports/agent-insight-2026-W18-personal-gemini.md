# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of personal channel analytics reports and related data files for 2026-W18. My analysis will focus on identifying key performance indicators, risks, and actionable insights based *only* on the data presented in this context.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md` (Personal channel analytics report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md` (Run next — personal advisory)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Personal channel suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw personal channel analytics data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md` (Missing file)

## Summary

The personal channel tracked 114 videos over the period of March 31 to April 27, 2026, accumulating 753 total views and 4,164 minutes of watch time, with 4 subscribers gained. The overall average retention for videos with views is 21.63%, and the average watch time per video is approximately 90.5 minutes. "Deep focus" and "piano_deep_calm" moods are driving the most views and watch time, with specific long-form videos performing well in these categories. Conversely, "ceremony" mood videos show significantly lower retention and watch time per video. The data also highlights that while some short-form videos have very high retention percentages, their view counts are minimal (1 view each).

## Risks / caveats

*   **Low View Counts for High Retention:** The top 5 videos by retention all have only 1 view, making their high retention percentages (e.g., 96.8%) statistically unreliable for drawing general conclusions about content strategy.
*   **Confounders:** The `run-next` report explicitly warns that CTR, impressions, and retention are often influenced by packaging elements like title and thumbnail, and traffic source/seasonality, not solely by mood or art-period labels. This means correlations in the data do not necessarily imply causation from generation parameters.
*   **Limited Data for Some Moods:** Many moods have very few videos with views (e.g., "trance" with 7 views from 10 videos, "warrior" with 5 views from 11 videos, "sleep" with 1 view from 9 videos), making it difficult to assess their true performance or potential.
*   **Missing `run-intent-blocked-personal.md`:** The absence of this file means any blocked intent for the personal channel cannot be reviewed, which might contain important context for future production.
*   **No CTR or Impressions Data:** The personal fetcher has not been extended to include CTR or impressions, which are crucial metrics for understanding discoverability and initial audience engagement. This limits the ability to diagnose why certain videos might not be getting views despite potentially good content.

## Insights

1.  **Deep Focus and Piano Deep Calm Drive Engagement:** Videos categorized under "deep_focus" and "piano_deep_calm" moods are significant drivers of views and watch time. "Enter Flow State · 1 Hour Zero Distracti" (deep_focus) leads with 120 views and 299 minutes, while "Calm Anxiety Fast · 1 Hour Deep Piano Re" (piano_deep_calm) has 55 views and an impressive 867 minutes of watch time. This suggests a strong audience preference for these specific moods and their associated long-form content.
2.  **Long-Form Content Dominates Watch Time:** The top videos by views are all 1-hour or longer, and these also contribute significantly to total watch time. For example, two "Calm Anxiety Fast · 1 Hour Deep Piano Re" videos combined account for over 1700 minutes of watch time, demonstrating that when viewers engage with these longer pieces, they tend to watch for extended periods.
3.  **Speculative: Short-Form Retention is Misleading:** While some 30-second videos show extremely high retention (e.g., "Find Your Strength" at 96.8%), these only have 1 view each. This indicates that while the content might be engaging for the single viewer, it's not reaching a broader audience, making these high retention percentages unreliable as a general performance indicator for content strategy.
4.  **Ceremony Mood Underperforms:** The "ceremony" mood shows significantly lower retention (-19.3% vs. channel average) and watch time per video (-50.2 min vs. channel average) compared to the overall channel. Despite having 11 videos, its total views are only 131, and average retention is a low 1.5%. This suggests that "ceremony" content is not resonating well with the current audience.
5.  **Speculative: Opportunity in High-Retention, Low-View Moods:** Moods like "warrior" (78.0% avg retention from 5 views) and "sleep" (83.6% avg retention from 1 view) show very high retention, albeit from extremely low view counts. If these moods could gain more visibility, they might convert into significant watch time given their strong engagement with the few viewers they have attracted.

## Experiments or packaging ideas

*   **Double Down on "Deep Focus" and "Piano Deep Calm":**
    *   Create more 1-hour+ videos in the "deep_focus" and "piano_deep_calm" categories, leveraging successful titles or themes like "Enter Flow State" and "Calm Anxiety Fast."
    *   Experiment with slight variations in titles and thumbnails for these moods to optimize CTR (once CTR data is available).
*   **Re-evaluate "Ceremony" Content:**
    *   Analyze the specific "ceremony" videos that received views to understand if there are any commonalities in their low performance.
    *   Consider pausing new "ceremony" content or experimenting with different lengths, titles, or descriptions to see if engagement can be improved.
*   **Boost Visibility for High-Retention, Low-View Moods:**
    *   For "warrior" and "sleep" moods, try promoting existing high-retention, low-view videos through playlists or end screens on popular videos.
    *   Experiment with more compelling titles and thumbnails for these moods to attract initial clicks, aiming to convert high retention into higher view counts.
*   **Implement CTR and Impressions Tracking:**
    *   Prioritize extending the personal fetcher to include CTR and impressions as per `docs/PERSONAL_ANALYTICS.md`. This data is critical for understanding discoverability and optimizing packaging.
*   **Cross-Channel Comparison (Manual):**
    *   Manually compare personal channel retention and watch time metrics against brand weekly reports (`data/reports/2026-W18.md` and `data/suggestions.json`) to identify any overarching trends or successful strategies from the brand channel that could be adapted for the personal channel.
