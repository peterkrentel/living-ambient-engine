# Agent advisory — Gemini (API) (personal, 2026-W20)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of personal channel analytics reports and related data files for the period 2026-W20. My analysis will focus on identifying key performance trends, risks, and actionable insights to inform content strategy for the personal YouTube ambient music channel, strictly using the provided context.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W20-personal.md` (Personal channel analytics report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W20-personal.md` (Run next — personal advisory)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Personal channel suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw personal channel analytics data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md` (Missing file, noted)

## Summary

The personal channel, over the analytics window of April 13th to May 10th, 2026, generated 1,371 total views and 11,628 minutes of watch time, gaining 8 subscribers. The `piano_deep_calm` mood category significantly outperforms others in terms of total views and watch time, with one video alone contributing over 3,300 minutes of watch time. Conversely, `ceremony` mood videos are underperforming in both retention and watch time. Short "warrior" mood videos show exceptionally high retention rates, though on very low view counts. The overall average retention for the channel is 23.14%.

## Risks / caveats

*   **Low View Counts for High Retention Videos:** The top retention videos (e.g., "warrior" mood) have extremely low view counts (1-5 views). This makes their high retention percentages statistically unreliable for broader strategy.
*   **Confounders:** The `run-next` report explicitly states that CTR, impressions, and retention are often influenced by packaging (title, thumbnail, traffic source, seasonality) and not solely by mood or art-period labels. The current data bundle does not include CTR or impressions, limiting the ability to analyze these critical packaging factors.
*   **Limited Data for Moods:** Many mood categories have very few videos with views (e.g., `sleep` with 3 videos, `fireplace` with 1, and several with 0 views), making it difficult to draw robust conclusions about their performance.
*   **Missing `run-intent-blocked-personal.md`:** The absence of this file means any blocked intent for the personal channel is not visible in this bundle.
*   **No Art Period or Music Style Data:** The `suggestions_personal.json` file shows zero total videos and zero videos with views for all listed `art_periods` and `music_styles`, indicating these dimensions are not currently contributing to performance analysis or content generation for this channel.

## Insights

1.  **`piano_deep_calm` is a strong performer:** Videos categorized under `piano_deep_calm` generated 856 total views from 18 videos and contributed significantly to watch time. Two "Calm Anxiety Fast · 1 Hour Deep Piano Re" videos alone accounted for over 5,700 minutes of watch time, indicating a strong audience demand for this specific mood and duration.
2.  **Long-form content drives watch time:** The top performing videos by watch time are "Calm Anxiety Fast · 1 Hour Deep Piano Re" (3,392 min and 2,327 min) and "Enter Flow State · 1 Hour Zero Distracti" (302 min). This suggests that longer-duration content, particularly around the 1-hour mark, is effective for accumulating watch time on the personal channel.
3.  **High retention in short "warrior" content, but low views:** While "warrior" mood videos show very high retention rates (e.g., 95.9% and 86.4%), these are based on extremely low view counts (1-2 views). This indicates that while the content itself might be engaging for those who find it, its discoverability or appeal to a wider audience is currently minimal.
4.  **`ceremony` mood is underperforming:** The `ceremony` mood category shows significantly lower average retention (1.5%) and watch time per video compared to the channel average. This suggests that content in this mood is not resonating well with the audience or is not effectively packaged.
5.  **Speculative: Opportunity for "deep focus" content:** `deep_focus` videos have 267 total views from 10 videos with an average retention of 16.5%. While not as high as `piano_deep_calm`, it's the second-highest performing mood by views. Given the success of "Enter Flow State · 1 Hour Zero Distracti" (128 views, 302 min), there might be an opportunity to explore more long-form content within the `deep_focus` mood.

## Experiments or packaging ideas

*   **Double down on `piano_deep_calm`:**
    *   Create more 1-hour (or longer) videos with the `piano_deep_calm` mood, focusing on "Calm Anxiety Fast" or similar stress-relief themes.
    *   Experiment with variations in titles and thumbnails for `piano_deep_calm` content to optimize CTR, as packaging is a known confounder.
*   **Investigate `ceremony` underperformance:**
    *   Review titles and thumbnails of existing `ceremony` videos to identify potential packaging issues.
    *   **Speculative:** Test short (e.g., 5-10 minute) `ceremony` videos with distinct titles/thumbnails to see if a different length or presentation improves initial engagement and retention, similar to the high retention seen in short "warrior" videos.
*   **Explore `deep_focus` long-form:**
    *   Produce new 1-hour `deep_focus` videos, perhaps with titles emphasizing "flow state" or "zero distraction" to build on the success of existing top performers.
*   **Re-evaluate short-form strategy:**
    *   Given the high retention but low views on short "warrior" videos, consider if these short formats are best suited for YouTube or if they could be repurposed for other platforms (e.g., Shorts, TikTok) where short, high-impact content thrives.
    *   If staying on YouTube, experiment with more compelling titles/thumbnails for short "warrior" content to boost impressions and views.
*   **Expand analytics scope (as per next steps):**
    *   Prioritize extending the personal fetcher to include CTR and impressions to gain a more complete understanding of video performance and packaging effectiveness.
