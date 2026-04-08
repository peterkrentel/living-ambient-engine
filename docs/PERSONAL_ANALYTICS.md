# Personal channel analytics

> **Purpose:** Record how to add **automated** YouTube analytics for the **personal** channel without mixing it with the **brand** pipeline. The personal line is a different product (long-form, different audience, [`content-factory.yml`](../.github/workflows/content-factory.yml)); treat data the same way.

**Companion:** [Cohesion Roadmap](COHESION_ROADMAP.md) (brand spine + `generations.json`). Personal analytics is **parallel**, not a merge into brand reports.

---

## Current state

| Piece | Brand | Personal |
|--------|--------|----------|
| Upload workflow | `content-factory-brand.yml`, batch workflows, `art-creator.yml` (brand) | [`content-factory.yml`](../.github/workflows/content-factory.yml) (`YOUTUBE_TOKEN_PICKLE`) |
| Scheduled analytics | [`analytics-agent.yml`](../.github/workflows/analytics-agent.yml) → `data/analytics.json` | **None** in repo |
| Manual / ad hoc | — | Studio screenshots, exports, external tools |

---

## Goals (v1)

1. Pull the **same class of metrics** as [`agent/fetch_analytics.py`](../agent/fetch_analytics.py) (uploads list + per-video analytics window).
2. Store them in **separate files** so brand `data/analytics.json` is **never overwritten**.
3. Keep **reports / correlation** personal-only until you explicitly design a cross-channel comparison.

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
- For personal: plan **`channel: "personal"`** rows in a shared file **or** `data/generations_personal.json`—same contract, separate namespace.

---

## Non-goals (v1)

- One unified “global” correlate across brand + personal.
- Replacing every manual Studio / screenshot workflow in one pass.

---

*Living stub — extend when the first personal analytics PR lands.*
