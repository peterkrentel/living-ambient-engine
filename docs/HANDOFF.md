# Handoff (active work snapshot)

> **[Doc map →](START_HERE.md)** · keep this file **short**; **overwrite** when state moves (no diary here).

## Updated

2026-04-16

## Branch / PR

- **Branch:** `main`
- **Open PR:** _(none — add when you open the next one)_

## Anchor

- **Commit:** `9df537a` — merge **`feat/analytics-dual-metrics`** (correlate: retention + watch minutes)

## Goal (current)

Prove **ledger join** and **analytics loop** on **brand** after factory uploads; **`correlate.py`** now emits **dual engagement** suggestions on **`main`**.

## Facts

- **Brand smoke done:** `data/generations.json` has **8** new rows (4 moods × dual, **600s**), committed with catalog (`dbeaa46` area); see `git log --oneline -- data/generations.json`.
- Weekly report / audit on disk may still be **pre-smoke** until **Analytics Agent** runs again: `data/reports/2026-W16.md`, `audit-2026-W16.md`.
- Two-lane strategy (personal vs brand; analytics = brand today): **`docs/START_HERE.md`** § **Two channels, two probes**.

## Next actions (in order)

1. **Run Analytics Agent** (`workflow_dispatch` is enough) so **`data/analytics.json`**, **`data/reports/`**, **`audit-*.md`**, and **`suggestions.json`** include the new **`video_id`s** — then open the latest **audit** and confirm **generations join** moved off **0%** for those rows (historic 306 may still be 0 without backfill).
2. **Overwrite this file** when (1) finishes with the new report week + one-line “join looks like X”.

## Risks / open questions

- Old channel videos **without** ledger rows will keep audit denominator high until you accept that or backfill.
