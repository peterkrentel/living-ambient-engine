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

1. **Merge + verify:** PR for **catalog `channel`** wiring; spot-check one personal + one brand upload path still commits catalog as expected.
2. **Consumers (later):** filter `audit_channel` / reports by `channel`, or **`generations.json`** `channel` — follow ADR; do not blend correlate rows across channels.
3. **Personal parity (optional):** `suggestions_personal.json`, personal audit — [`PERSONAL_ANALYTICS.md`](PERSONAL_ANALYTICS.md) roadmap.
4. **Framework generalization (later):** multi-channel analytics **template** (reusable workflow) — [`START_HERE`](START_HERE.md) checklist.
5. **Optional automation (safe):** gated planner from `suggestions.json`.
6. **Spec phases:** [`AGENT.md`](spec/AGENT.md) Phase **2.5** → **3** when volume justifies.

## Risks / open questions

- **Art Creator** uploads with `--no-update-catalog` still skip the catalog; ledger-only path unchanged.
