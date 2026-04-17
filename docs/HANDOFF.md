# Handoff (active work snapshot)

> **[Doc map →](START_HERE.md)** · keep this file **short**; **overwrite** when state moves (no diary here).

## Updated

2026-04-17

## Branch / PR

- **Policy:** All **code and docs** ship via **feature branch → pull request → merge to `main`** (humans + agents). **Exception:** Actions may commit **`data/`** (analytics) or **`content_catalog.json`** (upload bots) on `main`.
- **Active branch / PR:** _Update when you start work (branch name + PR link)._

## Anchor

- **Analytics (two lanes):** **Brand** — [`analytics-agent.yml`](../.github/workflows/analytics-agent.yml) → `data/analytics.json`, `data/reports/YYYY-WW.md`, `suggestions.json`, `audit-*.md` (commit step uses `git pull --rebase` before push). **Personal** — [`analytics-personal.yml`](../.github/workflows/analytics-personal.yml) → `data/analytics_personal.json`, `*-personal.md`. Map: [`START_HERE`](START_HERE.md#two-channels-two-probes) · detail: [`PERSONAL_ANALYTICS`](PERSONAL_ANALYTICS.md).
- **Catalog channel (in progress):** New `content_catalog.json` rows from `youtube_upload.py` can carry **`channel`: `brand` \| `personal`** when `--catalog-channel` / `CONTENT_CATALOG_CHANNEL` is set (workflows wired). Historic rows omit the field — optional backfill later. **ADR:** [`decisions/0002-content-catalog-channel-field.md`](decisions/0002-content-catalog-channel-field.md).

## Goal (last phase — done)

- **Personal analytics v1** in CI (token scopes, `analytics_personal.json`, `*-personal.md`, Studio cross-read).
- **Brand + personal push race** fixed (`git pull --rebase origin main` before `git push` in both analytics workflows).
- **Weekly reports** include **Analytics window** line ([`agent/report.py`](../agent/report.py)); merge on `main`.

## Goal (this phase — in flight)

- **Catalog / channel:** land optional **`channel`** on new catalog rows + ADR; then (optional) backfill or consumers (audit, tooling) that filter by channel.
- **Iron out cross-read:** brand vs personal reports + same `date_range` as Studio when sanity-checking totals.

## Facts

- **Audit join (brand):** `audit-*.md` still uses **brand** `analytics.json` only; catalog rows tagged **`personal`** clarify which uploads are not in that join until personal-aware audit exists.
- **Human-in-the-loop:** no auto-production from suggestions yet.

## Next actions (pick one thread when ready)

1. **Post-merge verify:** spot-check **catalog `channel`** on new rows (one personal + one brand upload path); [`ADR 0002`](decisions/0002-content-catalog-channel-field.md).
2. **Consumers (later):** filter `audit_channel` / reports by **`channel`**, or **`generations.json`** `channel` when added — follow ADR; do **not** blend correlate rows across channels.
3. **Personal parity (optional):** `suggestions_personal.json`, personal-aware audit/join — [`PERSONAL_ANALYTICS.md`](PERSONAL_ANALYTICS.md) roadmap.
4. **Framework generalization (later):** multi-channel **channel profile** template (reusable workflow / config) — [`START_HERE`](START_HERE.md) checklist.
5. **Optional automation (safe):** **`scripts/plan_run_intent.py`** (gated planner v0) reads `suggestions.json` → **`data/run_intent.json`** or **`data/reports/run-intent-blocked.md`** ([`spec/contracts/production-run-intent.md`](spec/contracts/production-run-intent.md)); **next:** workflow consumer validates + maps to `batch_generate` / `youtube_upload` (static `workflow_dispatch` stays the **human smoke** door—[`COHESION_ROADMAP.md`](COHESION_ROADMAP.md) Phase 6 *Two doors*).
6. **Phase 2.5 + inference hygiene:** extend **`correlate.py`** with CIs / z-scores / effect sizes **and** Step Summary + doc language that **CIs address noise, not confounders** (title/thumbnail/CTR vs params — **`AGENT.md`** § *Confounders & packaging*).
7. **Packaging telemetry (later slice):** joinable **fingerprints** on ledger/catalog **before** CTR-heavy automation; optional ADR if schema grows.
8. **Spec phases:** **`AGENT.md`** Phase **3** when volume **and** interpretation guardrails justify it; **`COHESION_ROADMAP.md`** Phase **6** only after joins/trust feel right.
9. **Title / packaging (defer):** same **mood × duration × dual** matrix on **brand + personal** reuses templates → **identical `video_title` strings** on two channels (different `video_id`s). Fine for smoke; before **high volume** or sharp **channel positioning**, tweak metadata (e.g. per-channel suffix or description line), rotation policy, or later **run intent** rules so packs are not unintentional clones — [`START_HERE.md`](START_HERE.md) checklist.

## Risks / open questions

- **Art Creator** uploads with `--no-update-catalog` still skip the catalog; ledger-only path unchanged.
