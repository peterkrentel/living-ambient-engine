# Handoff (active work snapshot)

> **[Doc map →](START_HERE.md)** · keep this file **short**; **overwrite** when state moves (no diary here).

## Updated

2026-04-16

## Branch / PR

- **Branch:** `main`
- **Open PR:** _(none)_

## Anchor

- **Commit:** `f9e9401` — latest **Analytics Agent** data push (`data/analytics.json`, reports, audit, `suggestions.json`)

## Goal (this phase — done)

- **Ledger on `main`** + **CI commits** + **catalog backfill** (`scripts/backfill_generations_from_catalog.py`) → **`data/generations.json`** now **68** rows.
- **Dual-metrics correlate** on `main` (retention + watch minutes) + **Analytics Agent** re-run so outputs match.
- **Docs:** two-channel / two-probe (`START_HERE`), brand-only analytics vs mixed catalog gap, **`fetch_analytics.py`** scope note.

## Facts

- **Audit join (brand):** **`audit-*.md`** reports **~22 / 314** — ledger rows that **also** appear in **brand** `analytics.json` (personal-only ledger rows do not count here). See **`START_HERE`** § *Two channels* + *Gap*.
- **Human-in-the-loop:** still the operating mode; no auto-production from suggestions yet.

## Next actions (pick one thread when ready)

1. **Product / data model:** split or **`channel`**-tag **`content_catalog.json`** (or separate files) so brand join and personal uploads do not share one ambiguous bucket — **ADR** if the choice is hard to reverse.
2. **Optional automation (safe):** a **gated planner** job that reads `suggestions.json` + thresholds and outputs **either** a proposed `workflow_dispatch` payload **or** a **“BLOCKED — insufficient signal”** report (no renders until you promote it).
3. **Personal analytics:** implement path in **`docs/PERSONAL_ANALYTICS.md`** when you want parity with brand (`analytics_personal.json`, etc.).
4. **Spec phases:** **`docs/spec/AGENT.md`** Phase **2.5** (rigor) → **3** when volume justifies; **`COHESION_ROADMAP.md`** Phase **6** only after joins/trust feel right.

## Risks / open questions

- **Art Creator** uploads still skip **`content_catalog.json`** (`--no-update-catalog`); ledger gaps for those unless you add logging or catalog there.
