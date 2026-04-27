# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of personal channel analytics reports and suggestions for Week 18, 2026. My goal is to extract actionable insights regarding content performance, particularly focusing on mood categories, and suggest experiments for future content creation and packaging.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md`: Personal channel analytics report for 2026-W18, covering March 30 to April 26, 2026.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md`: Machine-assembled personal advisory report, including actionable and exploratory suggestions.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json`: Raw JSON data for personal channel suggestions, including overall averages and mood coverage.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json`: Raw JSON data containing detailed video metrics for the personal channel.
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md`: This file was missing, indicating no blocked run intents for the personal channel.

## Summary

The personal channel saw 728 total views and 3,730 minutes of watch time, gaining 4 subscribers over the reporting period (March 30 - April 26, 2026). The overall average retention was 20.22%, with an average watch time of 82.889 minutes per video for the 45 videos with views. "Piano_deep_calm" and "deep_focus" moods are strong performers in terms of total views and watch time, with "piano_deep_calm" showing significantly higher watch time per video despite lower retention compared to the channel average. Conversely, "ceremony" mood videos are underperforming in both retention and watch time. Short-form videos (30 seconds) show very high retention but negligible views.

## Risks / caveats

*   **Low N for high retention videos:** The top 5 videos by retention all have only 1 or 2 views, making their high retention percentages (`96.8%`, `83.6%`, `78.3%`, `74.8%`, `62.4%`) statistically unreliable for drawing broad conclusions about content strategy.
*   **Confounders:** The `run-next` report explicitly states that CTR, impressions, and retention are often influenced by packaging (title, thumbnail, traffic source, seasonality), not solely by mood or art-period labels. Direct causal links between mood and performance should be treated with caution.
*   **Limited data for some moods:** Many mood categories have very few videos with views (e.g., `sleep`, `fireplace`, `trance`, `warrior`, `study`, `unknown`, `piano_relax`, `piano_ambient`) or zero views (`piano_evening`, `rain_piano`, `piano_gentle`, `chill`, `lofi_study`, `ocean_waves`), making it difficult to assess their true performance.
*   **Missing brand comparison:** The report advises comparing personal retention and watch time against brand weekly reports, but the brand data (`data/analytics.json`, `data/reports/2026-W15.md`, `data/suggestions.json`) was not merged into the personal correlate, so this cross-analysis could not be performed.
*   **No CTR/impressions:** The personal fetcher has not been extended to include CTR or impressions, which are crucial metrics for understanding discoverability and initial audience engagement.

## Insights

1.  **"Piano_deep_calm" is a watch time powerhouse:** Despite having a retention percentage (-4.7% vs channel avg) slightly below the channel average, videos tagged with `piano_deep_calm` generated an impressive +270.5 minutes of watch time per video compared to the channel average. This suggests that while viewers might not watch the entire video, those who do engage stay for a very long time, indicating strong appeal for long-form content in this mood.
2.  **"Deep_focus" is a consistent performer:** The `deep_focus` mood consistently appears in the top videos by views, with "Enter Flow State" and "Sounds for an Overactive Mind" being strong examples. This mood category has 10 videos, accumulating 239 total views and an average retention of 15.7%. This indicates a reliable audience for content designed for concentration.
3.  **Short-form videos show high retention but low views:** The top videos by retention are all 30-second clips (e.g., "Find Your Strength", "sleep_30s_20260124_031441"). While their retention rates are exceptionally high (up to 96.8%), they only garnered 1 or 2 views each. This suggests that while the content itself is engaging for those who find it, discoverability for these very short formats is extremely low, or they are not being effectively promoted.
4.  **"Ceremony" mood underperforms:** Videos categorized under `ceremony` show significantly lower performance, with retention % at -17.9% vs channel average and watch time per video at -42.6 minutes vs channel average. With 11 videos and 129 total views, this mood appears to struggle with audience engagement.
5.  **Speculative: Long-form "piano_deep_calm" resonates deeply:** The two top-performing videos by watch time, "Calm Anxiety Fast | 1 Hour Deep Piano Re" (53 views, 806 min) and "Calm Anxiety Fast | 1 Hour Deep Piano Re" (47 views, 793 min), are both `piano_deep_calm` and 1 hour in length. This strongly suggests that longer durations within this mood category are highly effective at capturing and retaining viewer attention for extended periods, leading to substantial watch time.

## Experiments or packaging ideas

*   **Double down on long-form "piano_deep_calm":**
    *   Create more 1-hour or longer videos with the `piano_deep_calm` mood.
    *   Experiment with titles and thumbnails that emphasize "deep calm," "anxiety relief," or "relaxation" to attract the proven audience.
*   **Investigate "deep_focus" content:**
    *   Analyze the specific elements (e.g., sound design, visual style) of "Enter Flow State" and "Sounds for an Overactive Mind" to replicate their success.
    *   Consider creating variations or sequels to these high-performing `deep_focus` videos.
*   **Re-evaluate short-form content strategy:**
    *   Given high retention but low views for 30-second clips, explore using these as shorts or promotional snippets for longer videos rather than standalone content.
    *   **Speculative:** Test different packaging (titles, thumbnails) for existing high-retention 30-second videos to see if discoverability can be improved.
*   **Tread carefully with "ceremony" mood:**
    *   Before deprioritizing entirely, consider a small experiment with different titles/thumbnails for `ceremony` videos to rule out packaging as the primary issue.
    *   If performance remains low, reduce production of this mood or explore combining it with more successful elements.
*   **Expand analytics for better insights:**
    *   Prioritize extending the personal fetcher to include CTR and impressions as per `docs/PERSONAL_ANALYTICS.md`. This will provide crucial data on how titles and thumbnails impact initial engagement.
*   **Cross-reference with brand performance:**
    *   Manually compare the performance of similar moods on the personal channel with the brand channel's `data/reports/2026-W15.md` and `data/suggestions.json` to identify broader trends or unique strengths of the personal channel.
