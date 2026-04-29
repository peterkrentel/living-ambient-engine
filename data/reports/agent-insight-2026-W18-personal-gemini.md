# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of files, including the personal channel analytics report, the run-next advisory, and the raw suggestions and analytics JSON files. My analysis will focus on identifying trends and actionable insights for the personal YouTube ambient music channel based solely on this data.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md` (Personal channel analytics report for 2026-W18)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md` (Run next — personal advisory for 2026-W18)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Raw suggestions data for the personal channel)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw analytics data for the personal channel)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md` (Not found, indicating no blocked run intent for the personal channel)

## Summary

The personal channel generated 753 total views and 4,793 minutes of watch time, gaining 4 subscribers during the analytics window (April 1st to April 28th, 2026). The overall average retention for videos with views is 21.87%, and the average watch time per video is 111.465 minutes. "Piano_deep_calm" and "deep_focus" moods are performing well in terms of total views and watch time, with "piano_deep_calm" showing a significant positive correlation with watch time per video. Conversely, the "ceremony" mood is underperforming in both retention and watch time. Short 30-second videos, while having high retention percentages, contribute very little to overall views or watch time.

## Risks / caveats

*   **Low View Counts for Retention Leaders:** The top 5 videos by retention all have only 1 or 2 views, making their high retention percentages statistically unreliable for drawing broad conclusions.
*   **Confounders:** The `run-next` report explicitly states that CTR, impressions, and retention are influenced by packaging (title, thumbnail), traffic source, and seasonality, not solely by mood or art-period labels. Therefore, correlations should not be treated as causal proof without further investigation into packaging differences.
*   **Limited Metrics:** The personal fetcher has not been extended to include CTR or impressions, which are crucial for understanding audience engagement and discoverability. This limits the depth of analysis.
*   **Thin Data for Many Moods:** Many moods have very few videos or views, making it difficult to assess their true performance or identify reliable trends. For instance, "piano_evening", "rain_piano", "piano_gentle", "chill", "lofi_study", and "ocean_waves" all have 0 views.
*   **Missing `run-intent-blocked-personal.md`:** While not a risk to the current analysis, the absence of this file means there are no documented blocked run intents, which could be useful for understanding past decisions or constraints.
*   **No Art Period or Music Style Data:** The `suggestions_personal.json` shows zero videos with views for any `art_periods` or `music_styles`, indicating these categories are not currently being tracked or are not relevant to the content being analyzed.

## Insights

1.  **"Piano_deep_calm" and "deep_focus" are strong performers for watch time and views.** The "piano_deep_calm" mood has 14 videos, 296 total views, and an average retention of 19.9%. It also shows a significant positive correlation with watch time per video, exceeding the channel average by over 400 minutes. Similarly, "deep_focus" has 10 videos, 245 total views, and 18.7% average retention. The top two videos by views are both "deep_focus" themed, generating 121 and 81 views respectively. This suggests these moods resonate well with the audience for longer viewing sessions.
2.  **Longer videos, particularly 1-hour durations, drive significant watch time.** The top 5 videos by views are all 1-hour durations, with titles like "Enter Flow State · 1 Hour Zero Distracti" and "Calm Anxiety Fast · 1 Hour Deep Piano Re". These videos contribute substantially to the total watch time, with one "Calm Anxiety Fast" video alone generating 1,034 minutes of watch time. This indicates a preference for extended ambient experiences.
3.  **Short 30-second videos have high retention but negligible impact on overall metrics.** While videos like "Find Your Strength · 30 Seconds Power Dr" and "Sounds for an Overactive Mind · 30 Secon" boast 96.8% retention, they only have 1 view each. This high retention is likely due to their brevity rather than strong audience engagement with the content itself, and they contribute minimally to total views or watch time.
4.  **The "ceremony" mood is underperforming and requires attention.** With 11 videos and 136 total views, "ceremony" has a very low average retention of 1.5%. The `run-next` report also flags "ceremony" for significantly lower retention (-19.6% vs channel avg) and watch time per video (-69.1 min vs channel avg). This indicates that content within this mood category is not holding audience interest.
5.  **Speculative:** Given the success of "piano_deep_calm" and "deep_focus," there might be an opportunity to explore variations or combinations of these moods. For example, a "deep_focus" track with subtle piano elements could potentially leverage the strengths of both categories, appealing to an audience seeking both concentration and calming sounds.

## Experiments or packaging ideas

*   **Double down on "piano_deep_calm" and "deep_focus" 1-hour videos:** Create more content in these successful moods and durations, focusing on similar titles and thumbnail styles to the top performers.
*   **Investigate "ceremony" underperformance:**
    *   Review titles and thumbnails of "ceremony" videos to see if they accurately represent the content or are less appealing.
    *   Consider experimenting with different lengths for "ceremony" content, as its current low retention suggests viewers are not staying for long.
    *   **Speculative:** If "ceremony" implies a more intense or specific sound, consider if the current execution aligns with audience expectations for ambient music.
*   **Analyze top-performing video titles for keywords and structure:** The titles "Enter Flow State · 1 Hour Zero Distracti" and "Calm Anxiety Fast · 1 Hour Deep Piano Re" are clear and benefit-oriented. Replicate this structure for new content.
*   **Deprioritize 30-second videos for general content strategy:** While they show high retention, their minimal view and watch time contribution suggests they are not effective for channel growth. They could be repurposed for short-form content platforms if desired, but not as primary YouTube uploads.
*   **Extend personal fetcher for CTR and impressions:** As noted in the next steps, gaining access to CTR and impressions data would provide invaluable insights into how titles and thumbnails are performing, allowing for more informed packaging decisions.
