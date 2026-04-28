# Handoff (active work snapshot)

> **[Doc map →](START_HERE.md)** · keep this file **short**; **overwrite** when state moves (no diary here). **Record of what shipped:** not deleted bullets here — add or keep a **`Done`** row in [`START_HERE` § Plan checklist](START_HERE.md#plan-checklist-living-as-of-2026-04) (those rows **stay on purpose**), plus **ADRs** / **git + PRs** when it was a decision or merge.

## Updated

2026-04-28

## Branch / PR

- **Policy:** All **code and docs** ship via **new feature branch (from pulled `main`) → pull request → merge to `main`** (humans + agents). **Exception:** Actions may commit **`data/`** (analytics) or **`content_catalog.json`** (upload bots) on `main`.
- **Dual-advisory human compare (done):** merged on `main` — playbook [`spec/DUAL_ADVISORY_COMPARE.md`](spec/DUAL_ADVISORY_COMPARE.md) via **PR #90**; horizon checklist / roadmap commits (`fc4c211`, `1dc1117`) are ancestors of `main`. Remote branch `docs/horizon-dual-advisory-compare` may still exist but is **behind** `main`; safe to delete after you confirm on GitHub.

## Parked backlog (preserved when taking a break)

- **Cohesion readiness review (risk / readiness audit):** full findings, maturity verdict, release checklist, and **ordered execution queue** (`CR-1` …) — [`cohesion-readiness-review-todos.md`](cohesion-readiness-review-todos.md). Tackle **one `CR-*` item per PR**; check boxes there when done.

## Anchor

- **Analytics (two lanes):** **Brand** — [`analytics-agent.yml`](../.github/workflows/analytics-agent.yml) → `data/analytics.json`, `data/reports/YYYY-WW.md`, `suggestions.json`, `audit-*.md`, `run_intent.json` / blocked, `run-next-*.md` (commit step uses `git pull --rebase` before push). **Personal** — [`analytics-personal.yml`](../.github/workflows/analytics-personal.yml) → `data/analytics_personal.json`, `*-personal.md`, `audit-*-personal.md`, `suggestions_personal.json`, `run_intent_personal.json` / blocked-personal, `run-next-*-personal.md`. Map: [`START_HERE`](START_HERE.md#two-channels-two-probes) · detail: [`PERSONAL_ANALYTICS`](PERSONAL_ANALYTICS.md).
- **Catalog channel:** New `content_catalog.json` rows from `youtube_upload.py` carry **`channel`: `brand` \| `personal`** (both values already on `main` in the catalog). Historic rows may omit the field — optional backfill later. **ADR:** [`decisions/0002-content-catalog-channel-field.md`](decisions/0002-content-catalog-channel-field.md).

## Goal (last phase — done)

- **Personal analytics v1** in CI (token scopes, `analytics_personal.json`, `*-personal.md`, Studio cross-read).
- **Brand + personal push race** fixed (`git pull --rebase origin main` before `git push` in both analytics workflows).
- **Weekly reports** include **Analytics window** line ([`agent/report.py`](../agent/report.py)); pipe-table cells sanitize **`|`** / newlines so Top 5 and mood tables render on GitHub; merge on `main`.
- **`run-next` v0:** [`scripts/run_next_report.py`](../scripts/run_next_report.py) on **brand + personal** workflows → `run-next-YYYY-WW.md` / `run-next-YYYY-WW-personal.md` (deterministic; **actionable** vs **exploratory**; packaging caveat). **Next:** validators → optional LLM → automation — [`COHESION_ROADMAP.md`](COHESION_ROADMAP.md) Phase 6.

## Goal (this phase — in flight)

- **Catalog / channel:** **`channel`** on new rows + ADR are **landed**; remaining work is optional **backfill** and **consumers** (audit, tooling) that filter by channel.
- **Iron out cross-read:** brand vs personal reports + same `date_range` as Studio when sanity-checking totals.
- **Dual advisory runner (Qwen) contract (done):** both lanes now reliably emit a **non-stub** `agent-insight-*-runner.md` with the five required `##` sections and deterministic totals anchored to JSON (guardrail retry + grounding retry + deterministic totals injection when needed).

## Facts

- **Catalog `channel` (done):** `content_catalog.json` on `main` already shows **`brand`** and **`personal`** on newer rows ([`ADR 0002`](decisions/0002-content-catalog-channel-field.md)); no further “post-merge spot-check” needed unless upload wiring changes.
- **Audit join (brand):** `audit-*.md` still uses **brand** `analytics.json` only; catalog rows tagged **`personal`** clarify which uploads are not in that join until personal-aware audit exists.
- **Human-in-the-loop:** no auto-production from suggestions yet.
- **Surface / packaging strategy:** platforms often surface **similar niche + slight packaging variation** (title/thumbnail) well before you can claim **param causality** from correlate alone — see [`spec/AGENT.md`](spec/AGENT.md) § *Confounders & packaging*. **[`piano-batch.yml`](../.github/workflows/piano-batch.yml)** is a deliberate example (incl. cross-read of the **personal** lane before running). Per-channel **positioning** / dedup when the *same* strings hit two channels stays open — **#8** below.

## Next actions (pick one thread when ready)

1. **Consumers (later):** filter `audit_channel` / reports by **`channel`**, or **`generations.json`** `channel` when added — follow ADR; do **not** blend correlate rows across channels.
2. **Personal parity (optional):** same analytics steps as brand (incl. **`plan_run_intent`** → `run_intent_personal.json` / blocked + consumer path inputs); remaining: personal-aware **audit/join filtering** on catalog when needed — [`PERSONAL_ANALYTICS.md`](PERSONAL_ANALYTICS.md).
3. **Framework generalization (later):** multi-channel **channel profile** template (reusable workflow / config) — [`START_HERE`](START_HERE.md) checklist.
4. **Optional automation (safe):** **Shipped:** [`run-intent-consumer.yml`](../.github/workflows/run-intent-consumer.yml) + [`scripts/consume_run_intent.py`](../scripts/consume_run_intent.py) validate **`data/run_intent.json`** → **`batch_generate`** / double-gated **`youtube_upload`** ([`spec/contracts/production-run-intent.md`](spec/contracts/production-run-intent.md)); planner v0 still defaults **`upload`: false**. **Next (optional):** personal-lane planner, richer intent→flags mapping, or LLM overrides — [`COHESION_ROADMAP.md`](COHESION_ROADMAP.md) Phase 6 *Two doors*.
5. **Phase 2.5 + inference hygiene:** extend **`correlate.py`** with CIs / z-scores / effect sizes **and** Step Summary + doc language that **CIs address noise, not confounders** (title/thumbnail/CTR vs params — **`AGENT.md`** § *Confounders & packaging*).
6. **Packaging telemetry (later slice):** joinable **fingerprints** on ledger/catalog **before** CTR-heavy automation; optional ADR if schema grows.
7. **Spec phases:** **`AGENT.md`** Phase **3** when volume **and** interpretation guardrails justify it; **`COHESION_ROADMAP.md`** Phase **6** only after joins/trust feel right.
8. **Title / packaging (defer):** same **mood × duration × dual** matrix on **brand + personal** reuses templates → **identical `video_title` strings** on two channels (different `video_id`s). Fine for smoke; before **high volume** or sharp **channel positioning**, tweak metadata (e.g. per-channel suffix or description line), rotation policy, or later **run intent** rules so packs are not unintentional clones — [`START_HERE.md`](START_HERE.md) checklist.

9. **Autonomy next step (recommended):** move from advisory prose toward **validated structured intent**: add **validators** for `run-next` / inputs (numbers match JSON; cited evidence), then expand/strengthen the **`run_intent*.json`** door (contract + consumer) so it can safely drive **generation/upload** with caps — see [`COHESION_ROADMAP.md`](COHESION_ROADMAP.md) Phase 6 *Two doors* and *Autonomy horizon*.
10. **`run-next` + dual-advisory (quality phase):** wiring is shipped; next is **quality + validators**, not more plumbing: remove runner WIR placeholder residue, enforce minimum Insight count / concreteness, and add numeric parity validators before anything consumes prose.
11. **Autonomy horizon (north star):** after trust gates, move from advisory prose toward **validated structured intent** → consumer → generate → publish → complete catalog/ledger feedback; supervised **Phase 3** models only when data justify them — [`COHESION_ROADMAP.md`](COHESION_ROADMAP.md) Phase 6 **Autonomy horizon (post-trust north star)**.

## Risks / open questions

- **Art Creator** uploads with `--no-update-catalog` still skip the catalog; ledger-only path unchanged.
