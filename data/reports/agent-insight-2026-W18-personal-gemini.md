# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of files, including the personal channel analytics report, the `run-next` personal advisory, and the `suggestions_personal.json` and `analytics_personal.json` files. My analysis will focus on identifying key performance trends and suggesting creative strategies based solely on this data.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md` (Personal channel analytics report for 2026-W18)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md` (Run next personal advisory for 2026-W18)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Personal channel suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw personal channel analytics data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md` (Missing file, noted)

## Summary

The personal channel generated 753 total views and 4,164 minutes of watch time, gaining 4 subscribers during the analytics window (2026-03-31 to 2026-04-27). The overall average retention is 21.63%, and the average watch time per video is 90.522 minutes. "deep_focus" and "piano_deep_calm" moods are performing well in terms of views and watch time, with "piano_deep_calm" showing significantly higher watch time per video despite slightly lower retention than the channel average. Conversely, "ceremony" mood videos are underperforming in both retention and watch time per video. Short-form videos (30 seconds) are showing exceptionally high retention rates, though with very low view counts.

## Risks / caveats

*   **Limited Data for Retention:** The top 5 videos by retention all have only 1 view, making their high retention percentages (e.g., 96.8%) statistically unreliable for drawing broad conclusions.
*   **Confounders:** The `run-next` report explicitly states that "CTR, impressions, and retention often move because of title, thumbnail, traffic source, and seasonality — not because a mood or art-period label 'caused' an outcome." This means correlations observed at the mood level should not be directly attributed to the generation parameters without considering packaging differences.
*   **Missing Data:** The `run-intent-blocked-personal.md` file is missing, which might indicate a lack of blocked intent reports.
*   **Thin Data for Many Moods:** Many moods listed in the "Performance by Mood" table have very low view counts (e.g., 0-5 views), making it difficult to assess their true performance or potential.
*   **No CTR/Impressions Data:** The report notes that extending the personal fetcher for CTR and impressions is optional, and this data is not present in the current bundle, limiting insights into discoverability.
*   **Low Join Rate:** Only 31.6% of videos are "identity-aligned" with `generations.json`, which could limit the depth of analysis linking video performance to specific generation parameters.

## Insights

1.  **Deep Focus and Deep Calm Piano Drive Watch Time:** The "deep_focus" mood is a strong performer, with "Enter Flow State" alone garnering 299 minutes of watch time from 120 views. "piano_deep_calm" also stands out, with 14 videos generating 304 views and an average watch time per video of +324.5 minutes above the channel average, despite its average retention being slightly below the channel average. This suggests that while viewers might not watch the *entire* video, they are watching a substantial portion, leading to high overall watch time.
2.  **Short-Form Content Shows High Retention, Low Views:** Videos like "Find Your Strength" (warrior) and "Sounds for an Overactive Mind" (deep_focus) with "30 Seconds" in their titles show extremely high retention (96.8%). However, these videos only have 1 view each. This indicates that while the short format might be highly engaging for those who click, it's not currently driving significant traffic.
3.  **"Calm Anxiety Fast" is a High-Performing Title/Mood Combination:** Two videos titled "Calm Anxiety Fast | 1 Hour Deep Piano Re" (mood: piano_deep_calm) are among the top 5 by views, collectively bringing in 104 views and a significant 1721 minutes of watch time. This suggests that the combination of "Calm Anxiety Fast" in the title and the "piano_deep_calm" mood resonates strongly with the audience.
4.  **`ceremony` Mood Underperforms:** The `ceremony` mood is identified as an underperformer, with significantly lower retention (-19.3% vs channel avg) and watch time per video (-50.2 min vs channel avg). This indicates that content tagged with this mood is not engaging viewers effectively.
5.  **Speculative: Potential for Mood-Specific Short-Form Content:** Given the extremely high retention on 30-second videos, particularly for moods like "warrior" and "deep_focus," there might be an opportunity to explore short-form content more strategically. While current views are low, if discoverability could be improved (e.g., through Shorts or targeted promotion), these highly engaging snippets could serve as effective hooks or teasers.

## Experiments or packaging ideas

*   **Double Down on "Deep Focus" and "Piano Deep Calm":**
    *   Create more long-form content (1 hour+) in the "deep_focus" and "piano_deep_calm" moods, explicitly using titles that highlight benefits like "Enter Flow State" or "Calm Anxiety Fast."
    *   Experiment with variations of "Calm Anxiety Fast" titles, perhaps focusing on different durations or slight thematic shifts within the "piano_deep_calm" mood.
*   **Re-evaluate "Ceremony" Content:**
    *   Analyze the specific videos tagged "ceremony" to understand why they are underperforming. Is it the audio style, visual aesthetic, or title/thumbnail?
    *   Consider pausing new "ceremony" content generation until more data or insights are gathered, or experiment with significantly different packaging (titles, thumbnails) for existing "ceremony" videos.
*   **Explore Short-Form Hooks:**
    *   **Speculative:** Repurpose highly retentive 30-second segments from longer "deep_focus" or "warrior" videos into YouTube Shorts. This could potentially drive traffic to the longer versions if the short-form content acts as an effective teaser.
    *   **Speculative:** Create new 30-second "power boost" or "quick calm" videos for moods like "deep_focus" or "sleep," focusing on strong, benefit-driven titles and eye-catching thumbnails to improve initial click-through.
*   **Optimize Titles for Top Performers:**
    *   Ensure all new "deep_focus" and "piano_deep_calm" videos incorporate keywords and phrases from top-performing titles like "Enter Flow State" and "Calm Anxiety Fast."
    *   **Speculative:** Test adding explicit duration in titles (e.g., "1 Hour") for these successful moods, as "1 Hour" appears in the top-performing view titles.
*   **Investigate Low-View, High-Retention Moods:**
    *   For moods like "sleep" (83.6% retention, 1 view) and "fireplace" (47.8% retention, 1 view), consider creating a small batch of new content with improved packaging (titles, thumbnails) to see if increased impressions can translate the high retention into more views.
