# Personal channel analytics

> **Purpose:** Use **YouTube performance data** on the **personal** channel to decide **what to do next**—not to drive a “fill the matrix” production machine. The personal library is **largely already shipped**; the win is **ongoing measurement** (retention, discovery, **CTR** where available, comparative performance) so strategy (titles, thumbnails, length, topics, what to double down on) is grounded in metrics instead of screenshots + ad hoc GPT.

**Companion:** [Cohesion Roadmap](COHESION_ROADMAP.md) (brand spine + `generations.json`). Brand = **coverage + join** for automated output; personal = **optimize and steer** an existing catalog.

**Two-lane strategy (personal vs brand, and where ML runs):** [`START_HERE.md` — *Two channels, two probes*](START_HERE.md#two-channels-two-probes) — same content so assistants read the map file first.

---

## Strategic focus (why this doc exists)

- **Not primary:** “Did we produce every combo?” (personal back catalog is treated as **done** for now.)
- **Primary:** From metrics, answer **what deserves more investment**, e.g. high **CTR** but weak retention vs the opposite, which lengths/topics cluster with watch time, where **impressions** stall, and which videos to **remix, repackage, or leave**.

**Metrics note:** [`agent/fetch_analytics.py`](../agent/fetch_analytics.py) today pulls a **core set** (views, watch time, retention %, engagement counts). **CTR**, **impressions**, and browse/search breakdowns may require **additional YouTube Analytics API** dimensions/metrics or **YouTube Studio** exports where the API is thin—plan to **extend the personal fetcher** over time; keep Studio as fallback for gaps.

---

## Current state

| Piece | Brand | Personal |
|--------|--------|----------|
| Upload workflow | `content-factory-brand.yml`, batch workflows, `art-creator.yml` (brand) | [`content-factory.yml`](../.github/workflows/content-factory.yml) (`YOUTUBE_TOKEN_PICKLE`) — catalog mostly produced |
| Scheduled analytics | [`analytics-agent.yml`](../.github/workflows/analytics-agent.yml) → `data/analytics.json` | **None** in repo |
| Manual / ad hoc | — | Studio screenshots, exports, external tools (current “what’s next” loop) |

**Catalog vs analytics:** [`content_catalog.json`](../content_catalog.json) is **one** file and may list uploads from **both** channels. **`data/analytics.json`** is **brand-channel only**. Audit “join %” is therefore **brand-overlap**, not “every catalog row.” See [`START_HERE.md`](START_HERE.md#two-channels-two-probes).

---

## Goals (v1)

1. Pull a **regular snapshot** of personal-channel performance into git (start from the same **family** of metrics as the brand fetcher; **add** CTR/impressions when the pipeline supports them).
2. Store them in **separate files** so brand `data/analytics.json` is **never overwritten**.
3. Keep **reports / correlation** personal-only and orient them toward **“what next”** (rankings, outliers, week-over-week), not brand-style experiment coverage.

---

## Proposed artifacts

| Artifact | Suggestion |
|----------|------------|
| Raw snapshot | `data/analytics_personal.json` — mirror the shape of `analytics.json` where practical; optionally add `"source": "personal"` and/or `channel_id` for clarity. |
| Weekly report | `data/reports/personal/` **or** filenames like `2026-W15-personal.md` — avoid colliding with brand `data/reports/2026-W15.md`. |
| Suggestions | `data/suggestions_personal.json` for a first version (simpler than one JSON with mixed channels). |

Adjust names when implementing if you prefer a single `data/personal/` subtree.

---

## Authentication

- **Secret:** `YOUTUBE_TOKEN_PICKLE` (already used by Content Factory Personal).
- **Scopes:** Align with brand: at minimum **`youtube.readonly`** and **`yt-analytics.readonly`** on the token that owns the personal channel (same as [`agent-youtube` contract](spec/contracts/agent-youtube.md) where applicable).

**Implementation note:** Today `AnalyticsFetcher` loads **`YOUTUBE_TOKEN_PICKLE_BRAND` first** when that env var is set ([`fetch_analytics.py`](../agent/fetch_analytics.py)). A personal fetch step must use **only** the personal token—e.g. run in a job step that sets `YOUTUBE_TOKEN_PICKLE` and **does not** set `YOUTUBE_TOKEN_PICKLE_BRAND`, or add an explicit CLI flag / env like `ANALYTICS_TOKEN_ENV` once you extend the script.

---

## Workflow options

1. **Extra job** in [`analytics-agent.yml`](../.github/workflows/analytics-agent.yml) after the brand fetch: personal-only env, write `analytics_personal.json`, then personal report/suggestions steps (or stub reports until scripts are parameterized).
2. **Separate workflow** `analytics-personal.yml` — clearer ownership and scheduling (e.g. same weekly cron or different day).

Pick one; avoid two workflows writing the same path.

---

## Code changes (when you implement)

- **Fetcher:** Output path and credential selection parameterized (personal vs brand) without duplicating the whole module.
- **Reports / `analyze_data` / `correlate`:** Either separate entrypoints (`report_personal`, `INPUT=...`) or a `--channel personal` switch—**do not** blend rows into one correlate run until dimensions are explicit.

---

## Relation to `generations.json`

- Cohesion Phase 2 targets **brand** join first (`video_id` ↔ params).
- For personal: optional later—useful if you want **seed/params ↔ performance** for long-form; not required to get value from **CTR/retention-driven “what next.”** If added: **`channel: "personal"`** or `data/generations_personal.json`.

---

## Non-goals (v1)

- One unified “global” correlate across brand + personal.
- Replacing every manual Studio / screenshot workflow in one pass.
- Treating personal as another **full combinatorial production grid** (back catalog is the baseline; metrics inform **next** moves).

---

*Living stub — extend when the first personal analytics PR lands.*
