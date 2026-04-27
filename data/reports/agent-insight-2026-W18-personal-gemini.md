# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of personal channel analytics reports and suggestions for Week 18, 2026. My analysis will focus on identifying key performance trends, risks, and actionable insights to inform future content strategy for the personal YouTube ambient music channel, using only the data presented.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md` (Personal channel analytics report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md` (Run next — personal advisory)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Personal channel suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw personal channel analytics data)

## Summary

The personal channel tracked 114 videos over the period of March 30 to April 26, 2026, accumulating 728 total views and 3,730 minutes of watch time, and gaining 4 subscribers. The overall average retention for videos with views is 20.22%, with an average watch time of 82.889 minutes per video. "Piano_deep_calm" and "deep_focus" moods are leading in total views and watch time, while "warrior" and "sleep" moods show exceptionally high retention percentages on a very low view count. Conversely, "ceremony" mood shows significantly lower retention and watch time per video. The data coverage for `art_periods` and `music_styles` is currently zero, indicating a lack of metadata or views for these categories.

## Risks / caveats

*   **Low View Counts for High Retention:** The top 5 videos by retention all have 1 or 2 views. While their retention percentages (e.g., 96.8% for "Find Your Strength") are impressive, these are based on extremely small sample sizes and are not statistically significant for broader conclusions.
*   **Confounders and Packaging:** The `run-next` report explicitly states that CTR, impressions, and retention are often influenced by title, thumbnail, traffic source, and seasonality, not solely by mood or art-period labels. The current data bundle does not include CTR or impressions, limiting the ability to analyze these critical packaging factors.
*   **Limited Metadata Coverage:** There is no data for `art_periods` or `music_styles` with views, meaning no insights can be drawn from these categories at this time.
*   **"Unknown" Mood Category:** The "unknown" mood category has 8 videos and 5 views, with an average retention of 25.2%. This suggests a need to better categorize content to gain clearer insights.
*   **Brand Lane Not Merged:** The brand channel analytics are not merged into the personal correlate, requiring deliberate comparison if cross-channel insights are desired, which is outside the scope of this personal channel review.

## Insights

1.  **Deep Focus and Piano Deep Calm Drive Watch Time:** The moods "deep_focus" and "piano_deep_calm" are the clear leaders in terms of total views (239 and 287 respectively) and contribute significantly to overall watch time. "Calm Anxiety Fast | 1 Hour Deep Piano Re" (piano_deep_calm) alone accounts for over 1500 minutes of watch time across two entries. This indicates a strong audience preference for these types of ambient music.
2.  **High Retention on Short, Specific Content (Low Volume):** Videos like "Find Your Strength" (warrior, 96.8% retention) and "sleep_30s_20260124_031441" (sleep, 83.6% retention) demonstrate extremely high retention, albeit with only 1 view each. This suggests that when these specific, short-form moods are discovered, they resonate strongly with the viewer.
3.  **Ceremony Mood Underperforms:** The "ceremony" mood, despite having 11 videos, shows a very low average retention of 1.5% and is flagged as an underperformer in both retention and watch time per video (down -17.9% and -42.6 min vs. channel average, respectively). This indicates a potential mismatch between content and audience expectation or poor packaging for this mood.
4.  **Speculative: Short-Form Content for Niche Engagement:** While the top videos by views are 1-hour long, the top videos by retention are 30-second clips. This could suggest that short, highly targeted clips are effective at capturing initial interest and demonstrating value, even if they don't contribute significantly to total watch time due to their length.
5.  **Speculative: Opportunity in Trance and Warrior Moods:** The "trance" and "warrior" moods, despite having very few views (6 and 5 respectively), show high average retention (39.7% and 78.0%). This might indicate an untapped potential for these moods if they can attract more initial views, possibly through improved discoverability or packaging.

## Experiments or packaging ideas

*   **Prioritize "piano_deep_calm" and "deep_focus" for new long-form content:** Given their strong performance in views and watch time, continue to produce 1-hour or longer videos in these moods.
*   **A/B test thumbnails and titles for "ceremony" videos:** Investigate why "ceremony" videos are underperforming in retention and watch time. Experiment with different packaging (titles, thumbnails) to see if discoverability or initial viewer expectation can be improved.
*   **Create longer versions of high-retention, low-view 30-second clips:** For moods like "warrior" and "sleep" that show exceptional retention on short clips, consider producing longer versions (e.g., 1-hour) to capitalize on demonstrated viewer engagement.
*   **Categorize "unknown" mood videos:** Review the 8 videos currently labeled as "unknown" mood and assign appropriate categories to gain clearer insights into their performance.
*   **Explore "trance" and "warrior" moods with more deliberate packaging:** Given their high retention despite low views, consider creating a small batch of new videos in these moods with optimized titles and thumbnails to test if increased impressions can translate into higher overall views and watch time.
*   **Implement CTR and impressions tracking:** As suggested in the "Next steps (personal)" in the analytics report, extending the personal fetcher to include CTR and impressions would provide crucial data for understanding packaging effectiveness and traffic sources.
