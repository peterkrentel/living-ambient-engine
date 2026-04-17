# Personal channel analytics

> **Purpose:** Use **YouTube performance data** on the **personal** channel to decide **what to do next**—not to drive a “fill the matrix” production machine. The personal library is **largely already shipped**; the win is **ongoing measurement** (retention, discovery, **CTR** where available, comparative performance) so strategy (titles, thumbnails, length, topics, what to double down on) is grounded in metrics instead of screenshots + ad hoc GPT.

**Companion:** [Cohesion Roadmap](COHESION_ROADMAP.md) (brand spine + `generations.json`). Brand = **coverage + join** for automated output; personal = **optimize and steer** an existing catalog.

**Two-lane strategy (personal vs brand, and where ML runs):** [`START_HERE.md` — *Two channels, two probes*](START_HERE.md#two-channels-two-probes) — same content so assistants read the map file first.

---

## Strategic focus (why this doc exists)

- **Not primary:** “Did we produce every combo?” (personal back catalog is treated as **done** for now.)
- **Primary:** From metrics, answer **what deserves more investment**, e.g. high **CTR** but weak retention vs the opposite, which lengths/topics cluster with watch time, where **impressions** stall, and which videos to **remix, repackage, or leave**.

**Metrics note:** [`agent/fetch_analytics.py`](../agent/fetch_analytics.py) today pulls a **core set** (views, watch time, retention %, engagement counts). **CTR**, **impressions**, and browse/search breakdowns may require **additional YouTube Analytics API** dimensions/metrics or **YouTube Studio** exports where the API is thin—plan to **extend the personal fetcher** over time; keep Studio as fallback for gaps.

**Inference note:** once **CTR** is in-repo, the same **packaging confounders** as the brand lane apply (title, thumbnail, traffic source). Cross-read [`AGENT.md`](spec/AGENT.md) § Phase 2 — *Confounders & packaging*; do not blend personal and brand rows in one correlate run until dimensions are explicit.

---

## Current state

| Piece | Brand | Personal |
|--------|--------|----------|
| Upload workflow | `content-factory-brand.yml`, batch workflows, `art-creator.yml` (brand) | [`content-factory.yml`](../.github/workflows/content-factory.yml) (`YOUTUBE_TOKEN_PICKLE`) — catalog mostly produced |
| Scheduled analytics | [`analytics-agent.yml`](../.github/workflows/analytics-agent.yml) → `data/analytics.json` | [`analytics-personal.yml`](../.github/workflows/analytics-personal.yml) → `data/analytics_personal.json` + `data/reports/*-personal.md` |
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

**Implementation:** Use **`python -m agent.fetch_analytics --channel personal`**, which ignores `YOUTUBE_TOKEN_PICKLE_BRAND` and defaults output to `data/analytics_personal.json`. The personal workflow never sets the brand secret.

If CI fails with **`insufficient authentication scopes`** on `channels.list`, the secret pickle was created without read/analytics scopes — see **[`docs/youtube-auth.md`](youtube-auth.md)** (Troubleshooting table + **Re-create the token with the right scopes**). Upload-only tokens are not enough for analytics.

---

## Workflow choice (locked in v1)

**Separate workflow** [`analytics-personal.yml`](../.github/workflows/analytics-personal.yml) — personal-only env, no `YOUTUBE_TOKEN_PICKLE_BRAND`, offset cron vs brand. Alternative (extra job in `analytics-agent.yml`) was not needed once isolation was the priority.

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

**v1 shipped:** separate workflow + JSON + suffixed reports.

### Roadmap (order matters)

1. **Operate:** run **`analytics-personal.yml`** on `main` (`workflow_dispatch` first is fine); confirm `data/analytics_personal.json`, `data/reports/*-personal.md`, **`data/suggestions_personal.json`**, and **`data/reports/run-next-*-personal.md`** commit cleanly and **never** touch `data/analytics.json` / `data/suggestions.json`.
2. **Parity — correlate + run-next:** **Shipped** in CI: **`scripts/correlate.py`** with `SUGGESTIONS_JSON_PATH` → **`suggestions_personal.json`**, then **`scripts/run_next_report.py --lane personal`**. **Still optional / later:** CTR/impressions in fetch when API allows; richer personal-only tooling — still **separate files**, no blended correlate rows. **Audit:** **`scripts/audit_channel.py`** → `data/reports/audit-*-personal.md` (ledger join uses optional `channel` on `generations.json` + `workflow` inference; see `docs/spec/workflows.md` § analytics-personal).
3. **Generalize (when boring or N≥3 channels):** a **channel profile** template — e.g. reusable GitHub workflow with inputs (`token_secret`, `analytics_json_path`, `report_suffix`, `run_correlate`), or a small registry in Python — so “add a channel” is config + one new secret, not duplicated YAML. Until then, two explicit workflows are intentional ([`HANDOFF.md`](HANDOFF.md) § next actions).
