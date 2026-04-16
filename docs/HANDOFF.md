# Handoff (active work snapshot)

> **[Doc map →](START_HERE.md)** · keep this file **short**; **overwrite** when state moves (no diary here).

## Updated

2026-04-15

## Branch / PR

- **Branch:** `main`
- **Open PR:** _(none)_

## Anchor

- **Analytics lanes in repo:** **Brand** — `analytics-agent.yml` → `data/analytics.json`, weekly `data/reports/YYYY-WW.md`, `suggestions.json`, `audit-*.md`. **Personal (v1)** — `analytics-personal.yml` → `data/analytics_personal.json`, `data/reports/YYYY-WW-personal.md` (no correlate/audit/suggestions yet). Map: [`START_HERE`](START_HERE.md#two-channels-two-probes), detail: [`PERSONAL_ANALYTICS`](PERSONAL_ANALYTICS.md).

## Goal (last phase — done)

- **Ledger on `main`** + **CI commits** + **catalog backfill** → **`data/generations.json`** populated.
- **Dual-metrics correlate** on `main` + **Analytics Agent** outputs aligned.
- **Docs:** two-channel / two-probe, brand-only analytics vs mixed catalog, `fetch_analytics.py` scope.

## Goal (this phase — in flight)

- **Prove the personal lane in CI:** run **Analytics Agent (Personal)** once on `main`; confirm `analytics_personal.json` + `*-personal.md` land and stay isolated from brand files.
- **Iron out cross-read:** same week label, two JSON shapes comparable; note anything missing for “what next” (e.g. CTR — see `PERSONAL_ANALYTICS.md`).
- **Defer abstraction:** multi-channel “template” (reusable workflow / channel profiles) only after this feels boring or a third channel is real — captured in plan checklist ([`START_HERE`](START_HERE.md) table + [`PERSONAL_ANALYTICS`](PERSONAL_ANALYTICS.md) roadmap).

## Facts

- **Audit join (brand):** **`audit-*.md`** counts ledger rows against **brand** `analytics.json` only; personal snapshots do not change that metric until catalog/channel tagging improves. See **`START_HERE`** § *Two channels* + *Gap*.
- **Human-in-the-loop:** still the operating mode; no auto-production from suggestions yet.

## Next actions (pick one thread when ready)

1. **Ops:** trigger **`analytics-personal.yml`** (`workflow_dispatch`) and verify secrets/scopes; skim first `*-personal.md` vs same-week brand report.
2. **Product / data model:** split or **`channel`**-tag **`content_catalog.json`** (or separate files) so brand join and personal intent stay aligned — **ADR** if the choice is hard to reverse.
3. **Personal parity (when you want it):** `suggestions_personal.json`, personal-aware audit/join, or parameterize `correlate.py` — see **`PERSONAL_ANALYTICS.md`** roadmap (do **not** blend brand + personal rows in one correlate run until dimensions are explicit).
4. **Framework generalization (later):** one **channel profile** template (OAuth secret name, `ANALYTICS_JSON_PATH`, report suffix, optional correlate flag) via reusable workflow or small config — **after** steps 1–3 stabilize; goal is add channel *N* without duplicating YAML logic.
5. **Optional automation (safe):** gated planner from `suggestions.json` → plan JSON or **BLOCKED** report (no blind renders).
6. **Spec phases:** **`AGENT.md`** Phase **2.5** → **3** when volume justifies; **`COHESION_ROADMAP.md`** Phase **6** only after joins/trust feel right.

## Risks / open questions

- **Art Creator** uploads still skip **`content_catalog.json`** (`--no-update-catalog`); ledger gaps for those unless you add logging or catalog there.
