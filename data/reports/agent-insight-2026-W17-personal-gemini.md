# Agent advisory — Gemini (API) (personal, 2026-W17)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of personal channel analytics reports and suggestions for Week 17, 2026. My analysis will focus on identifying patterns in video performance related to mood and watch time, while acknowledging the current limitations in actionable insights due to data thresholds.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W17-personal.md` (Personal channel analytics report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W17-personal.md` (Run next — personal advisory)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md` (Run intent — BLOCKED report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Personal channel suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw personal channel analytics data)

## Summary

The personal channel saw 680 total views and 2,404 minutes of watch time, gaining 6 subscribers over the `2026-03-28` to `2026-04-24` period. The overall average retention is 18.94%, and average watch time per video is 52.261 minutes. While `deep_focus` and `piano_deep_calm` moods show high total views and watch time, their average retention percentages are below the channel average. The automated planner is currently blocked from generating actionable intent due to insufficient video count or total views for any single mood to pass the `n≥5, group_views≥200` threshold.

## Risks / caveats

*   **Limited Actionable Insights:** The planner is blocked, meaning no mood increases currently meet the criteria for actionable recommendations (n≥5 videos, group views ≥200). All current mood-based suggestions are exploratory.
*   **Confounders:** The `run-next` report explicitly states that CTR, impressions, and retention are heavily influenced by packaging (title, thumbnail, traffic source, seasonality) and not solely by mood or art-period labels. Direct correlation between generation parameters and outcomes should be treated with caution.
*   **Data Thinness:** Many moods have very few videos with views (e.g., `sleep` with 1 video, `trance` with 3 videos, `warrior` with 2 videos), making it difficult to draw robust conclusions about their performance. Several moods have 0 views.
*   **Incomplete Metadata Join:** Only 31.6% of videos in analytics are "identity-aligned" with `generations.json`, which might limit the depth of parameter-driven analysis.

## Insights

1.  **Deep Focus and Piano Deep Calm Drive Watch Time:** The `deep_focus` mood, with 10 videos, generated 238 views and had videos like "Enter Flow State" contributing significantly to watch time (347 minutes from 125 views). Similarly, `piano_deep_calm` (14 videos) generated 236 views, with "Calm Anxiety Fast" accounting for 427 minutes of watch time from 44 views. These moods are strong contenders for total watch time, even if their average retention is below the channel average.
2.  **Retention vs. Watch Time Discrepancy:** While `deep_focus` and `piano_deep_calm` are top performers by total views and watch time, their average retention is 15.7% and 11.8% respectively, both below the overall channel average of 18.94%. Conversely, moods like `warrior` (78.1%), `sleep` (83.6%), and `trance` (32.1%) show high average retention but have very low total views (8, 1, and 4 views respectively), often from short-form content (e.g., "Find Your Strength" at 96.8% retention from 1 view). This suggests that short, highly engaging content exists but isn't driving overall channel growth in views or watch time.
3.  **Speculative: Short-form Content for Engagement, Long-form for Watch Time:** The top retention videos are often short (e.g., 30-second or 10-second clips), indicating strong initial engagement for specific moods like `warrior`, `sleep`, and `trance`. However, the top videos by views and watch time are longer (e.g., "1 Hour Zero Distraction" for `deep_focus`, "1 Hour Deep Piano Re" for `piano_deep_calm`). This suggests a potential strategy where short, high-retention content could serve as entry points or promotional material, while longer videos are the primary drivers of watch time.
4.  **Underperforming Moods:** Moods like `ceremony` (1.5% avg retention, 130 total views) and `rain_sleep` (2.0% avg retention, 24 total views) are significantly underperforming in terms of average retention. The `ceremony` mood is also flagged as an exploratory underperformer for watch time per video. These moods may require re-evaluation or different packaging strategies.
5.  **Speculative: Piano-based Moods Show Potential:** Several piano-related moods (`piano_deep_calm`, `piano_ambient`, `piano_relax`, `piano_evening`, `rain_piano`, `piano_gentle`) are present. While `piano_deep_calm` is a top performer, others like `piano_ambient` (49.8% retention from 2 views) show high retention but low volume. `piano_evening`, `rain_piano`, and `piano_gentle` currently have 0 views. This suggests that piano-centric content has a mixed performance, with "deep calm" resonating, but other variations needing more exposure or refinement.

## Experiments or packaging ideas

*   **Test longer versions of high-retention short videos:** For moods like `warrior`, `sleep`, and `trance` that show high retention on short clips, experiment with creating 1-hour or 2-hour versions to see if that engagement translates to longer watch times.
*   **Refine packaging for `deep_focus` and `piano_deep_calm`:** Since these moods drive high watch time but have lower average retention, investigate titles, thumbnails, and descriptions that explicitly set expectations for long-form listening or focus sessions to potentially improve retention.
*   **Cross-promote high-retention short-form content:** Use short, high-retention clips (e.g., 30-second `warrior` or `sleep` videos) as YouTube Shorts or social media snippets to drive traffic to longer, related videos on the channel.
*   **A/B test thumbnails/titles for underperforming moods:** For `ceremony` and `rain_sleep`, try new visual and textual packaging to see if it improves initial click-through and subsequent retention.
*   **Focus on `piano_deep_calm` for next batch:** Given its strong watch time performance, even with exploratory status, prioritize generating more `piano_deep_calm` content, ensuring it meets the `n≥5, group_views≥200` threshold to become actionable for the planner.
