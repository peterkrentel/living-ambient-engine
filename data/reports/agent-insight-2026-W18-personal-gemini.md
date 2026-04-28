# Agent advisory — Gemini (API) (personal, 2026-W18)

> **Advisory only (v0).** Not `run_intent`, not `batch_generate`, not causal proof. Sparse metrics and packaging confounders apply — see `docs/spec/AGENT.md`.

---
I have reviewed the provided bundle of personal channel analytics reports and suggestions for Week 18, 2026. My analysis will focus on identifying key performance trends, risks, and actionable insights to guide content strategy for the personal YouTube ambient music channel, strictly based on the provided data.

## What I reviewed

*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/2026-W18-personal.md` (Personal channel analytics report)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-next-2026-W18-personal.md` (Run next — personal advisory)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/suggestions_personal.json` (Personal channel suggestions data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/analytics_personal.json` (Raw personal channel analytics data)
*   `/home/runner/work/living-ambient-engine/living-ambient-engine/data/reports/run-intent-blocked-personal.md` (Missing file)

## Summary

The personal channel tracked 114 videos over the analytics window (2026-03-31 to 2026-04-27), accumulating 753 total views and 4,164 minutes of watch time, with 4 new subscribers. While some short-form content shows high retention, long-form "deep_focus" and "piano_deep_calm" videos are driving the majority of views and watch time. The "piano_deep_calm" mood, in particular, shows a strong positive correlation with watch time per video, despite slightly below-average retention. Conversely, "ceremony" mood videos are underperforming in both retention and watch time. The data coverage for mood categories is good, but there is no data for `art_periods`, `music_styles`, or `art_music_combos`.

## Risks / caveats

*   **Low View Counts for Retention Data:** The top 5 videos by retention all have only 1 view, making their high retention percentages (e.g., 96.8%) statistically unreliable for drawing broad conclusions about content performance.
*   **Limited Metric Scope:** The personal fetcher has not been extended to include CTR or impressions, which are crucial for understanding audience engagement and discoverability. The `run-next` report explicitly states that CTR, impressions, and retention are often influenced by packaging (title, thumbnail, traffic source) and seasonality, which are not fully captured or analyzed here.
*   **Data Thinness for Certain Moods:** Many moods have very low total views (e.g., "trance" with 7 views, "warrior" with 5 views, "sleep" with 1 view), making it difficult to assess their true performance or potential. Several moods have 0 views, indicating either lack of content or poor discoverability.
*   **Missing `run-intent-blocked-personal.md`:** The absence of this file means there's no information on any blocked intent runs, which could indicate issues with automated content generation or deployment.
*   **Confounders:** The `run-next` report explicitly warns against treating bucket-level correlation as proof that generation parameters drove a result when packaging differed. This is a significant caveat for interpreting mood-based performance.

## Insights

1.  **Deep Focus and Piano Deep Calm Drive Watch Time:** The "deep_focus" and "piano_deep_calm" moods are the primary drivers of watch time and views. "Enter Flow State · 1 Hour Zero Distracti" (deep_focus) leads with 120 views and 299 minutes, while "Calm Anxiety Fast · 1 Hour Deep Piano Re" (piano_deep_calm) accounts for significant watch time (867 and 854 minutes across two videos) despite fewer views than the top "deep_focus" video. The `run-next` report confirms that `piano_deep_calm` has +324.5 min vs channel avg watch time per video.
2.  **Short-Form Retention is High but Low-Impact:** While 30-second videos like "Find Your Strength" (warrior) and "Sounds for an Overactive Mind" (deep_focus) show very high retention (96.8%), they only have 1 view each. This indicates that while the content itself might be engaging for those who find it, these short videos are not contributing meaningfully to overall channel views or watch time in the current analytics window.
3.  **"Ceremony" Mood Underperforms:** The "ceremony" mood is identified as an underperformer, with -19.3% retention vs. channel average and -50.2 min vs. channel average watch time per video, based on 3 videos and 105 views. This suggests that content in this mood category is not resonating well with the audience.
4.  **Speculative: Potential for "Warrior" and "Trance" in Longer Form:** While "warrior" and "trance" moods have very few views (5 and 7 respectively), their average retention percentages are relatively high (78.0% and 40.5%). This is based on very thin data, but it *speculatively* suggests that if these moods were presented in longer formats or given better discoverability, they might perform well in terms of engagement.
5.  **Speculative: Piano-Based Content is a Strong Performer:** Across the board, piano-related moods ("piano_deep_calm", "piano_relax", "piano_ambient", "piano_evening", "piano_gentle", "rain_piano") appear frequently in the data, with "piano_deep_calm" being a standout for watch time. This *speculatively* suggests a strong audience preference or engagement with piano-centric ambient music.

## Experiments or packaging ideas

*   **Double Down on "Deep Focus" and "Piano Deep Calm" Long-Form:**
    *   Create more 1-hour+ videos in the "deep_focus" and "piano_deep_calm" moods, focusing on titles and thumbnails that clearly communicate their purpose (e.g., "Zero Distraction," "Calm Anxiety").
    *   **Speculative:** Experiment with slightly longer durations (e.g., 2-3 hours) for these successful moods to capture even more watch time, if the content quality can be maintained.
*   **Re-evaluate "Ceremony" Content:**
    *   Analyze the specific "ceremony" videos that underperformed. Are there common elements in their titles, thumbnails, or audio characteristics that could explain the low retention and watch time?
    *   **Speculative:** Consider pausing new "ceremony" content or significantly altering its packaging/sound design before further investment.
*   **Test Longer Form for High-Retention, Low-View Moods:**
    *   Take a 30-second "warrior" or "trance" piece that showed high retention (even with 1 view) and expand it into a 1-hour version. Monitor its performance closely.
    *   **Speculative:** For "sleep" (83.6% retention, 1 view), consider creating a longer "sleep" track, perhaps combining it with a proven element like "rain_sleep" (though rain_sleep itself has low retention).
*   **Focus on Titles and Thumbnails for Discoverability:**
    *   Given the lack of CTR/impressions data, prioritize clear, benefit-driven titles and compelling thumbnails for all new content, especially for moods that show potential but have low views.
*   **Expand Analytics to Include CTR and Impressions:**
    *   As suggested in the "Next steps (personal)" and "Packaging & confounders" sections, extending the personal fetcher to include CTR and impressions is critical for a more complete understanding of video performance and discoverability. This should be a high-priority technical task.
