# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of analytics reports and suggestions for the personal YouTube ambient music channel for Week 18, 2026. My analysis will focus on identifying key performance indicators, risks, and actionable insights based solely on this data, along with proposing experiments and packaging ideas.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md`: Personal channel analytics report for 2026-W18.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md`: Personal advisory report, including actionable and exploratory suggestions.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json`: Raw JSON data for personal channel suggestions and coverage.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json`: Raw JSON data containing detailed video metrics.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md`: This file was missing.

## Summary

The personal channel tracked 114 videos over the period of March 30 to April 26, 2026, accumulating 755 total views and 4,224 minutes of watch time, gaining 4 subscribers. The overall average retention was 22.33%, and the average watch time per video with views was approximately 91.8 minutes. "Deep focus" and "piano_deep_calm" moods are driving significant views and watch time, with "piano_deep_calm" showing a strong positive correlation with watch time per video despite slightly lower retention than the channel average. Conversely, "ceremony" mood videos are underperforming in both retention and watch time. Short-form videos (30 seconds) show exceptionally high retention but contribute very little to overall views or watch time.

## Risks / caveats

*   **Low View Counts for Retention Leaders:** The top videos by retention ("Find Your Strength," "Sounds for an Overactive Mind," "sleep_30s_20260124_031441," "trance_30s_20260124_055344") each have only 1 view. This makes their high retention percentages (e.g., 96.8%) statistically unreliable for drawing broad conclusions about content performance.
*   **Confounders & Packaging:** The `run-next` report explicitly states that CTR, impressions, and retention are often influenced by title, thumbnail, traffic source, and seasonality, not solely by mood or art-period labels. The current data does not include CTR or impressions, limiting the ability to analyze these critical packaging factors.
*   **Limited Data for Many Moods:** Many moods (e.g., `piano_evening`, `rain_piano`, `piano_gentle`, `chill`, `lofi_study`, `ocean_waves`) have 0 views, making it impossible to assess their performance.
*   **Missing `run-intent-blocked-personal.md`:** The absence of this file means any blocked intents for the personal channel are unknown.
*   **Thin Data on Art Periods/Music Styles:** The `suggestions_personal.json` shows zero videos with views for all listed `art_periods` and `music_styles`, and `art_music_combos`, indicating no data to analyze these dimensions.

## Insights

1.  **Deep Focus and Piano Deep Calm Drive Engagement:** The "deep_focus" mood accounts for 243 views and "piano_deep_calm" for 306 views, making them the top two moods by total views. Furthermore, "piano_deep_calm" shows a significant positive correlation with watch time per video, exceeding the channel average by over 323 minutes for the 7 videos analyzed. This suggests these moods resonate well with the audience for longer viewing sessions.
2.  **Long-Form Content is Key for Watch Time:** The top videos by views, such as "Enter Flow State" (1 Hour) and "Calm Anxiety Fast" (1 Hour), are long-form content. These videos contribute significantly to total watch time (e.g., "Calm Anxiety Fast" with 867 and 854 minutes for two instances), reinforcing that the audience is seeking and engaging with extended ambient experiences.
3.  **High Retention on Short Videos is Misleading:** While some 30-second videos like "Find Your Strength" and "Sounds for an Overactive Mind" show nearly 97% retention, they only have 1 view each. This indicates that while the content might be engaging for the single viewer, these short formats are not currently attracting significant viewership or contributing to overall watch time.
4.  **"Ceremony" Mood Underperforms:** The "ceremony" mood shows a notable underperformance, with retention 20% below the channel average and watch time per video 51.5 minutes below average (for 3 videos with 105 views). This suggests that content categorized under "ceremony" is not resonating effectively with the audience in its current form.
5.  **Speculative: Potential for "Warrior" and "Trance" with More Views:** The "warrior" and "trance" moods show relatively high average retention (78.0% and 40.5% respectively) despite very low view counts (5 and 7 views). If these moods could attract more viewers, their strong retention might translate into significant watch time.

## Experiments or packaging ideas

*   **Double Down on "Deep Focus" and "Piano Deep Calm":**
    *   Create more long-form (1+ hour) videos in the "deep_focus" and "piano_deep_calm" moods.
    *   Experiment with titles and thumbnails that explicitly highlight "focus," "concentration," "calm," and "relaxation" in combination with piano elements.
    *   **Speculative:** Test variations of "Deep Calm Piano Atmosphere" or "Zero Distraction" themes.
*   **Investigate "Ceremony" Underperformance:**
    *   Review the titles, thumbnails, and actual content of "ceremony" videos to understand why they have low retention and watch time.
    *   **Speculative:** Experiment with different sub-moods or re-categorizations if the current "ceremony" label is not clear or appealing to the target audience.
*   **Explore "Warrior" and "Trance" with Caution:**
    *   Produce a small batch of new "warrior" and "trance" videos, focusing on compelling titles and thumbnails to attract more initial views.
    *   Monitor their performance closely to see if the high retention holds with a larger audience.
    *   **Speculative:** Consider if these moods could be combined with other successful elements, e.g., "Warrior Focus" or "Trance for Deep Work."
*   **Focus on Watch Time over Short Retention:**
    *   Prioritize the creation of longer videos (1+ hour) that have demonstrated high watch time, even if their percentage retention is lower than short, single-view videos. The goal is total watch time, not just percentage retention on minimal views.
*   **Expand Analytics for Deeper Insights:**
    *   Implement the optional extension of the personal fetcher to include CTR and impressions, as suggested in `Next steps (personal)`. This data is crucial for understanding packaging effectiveness.
*   **Cross-Reference Brand Reports (Manual):**
    *   Manually compare personal channel performance with brand weekly reports (e.g., `2026-W15.md`) to identify any overarching trends or successful strategies from the brand channel that could be adapted for the personal channel.
