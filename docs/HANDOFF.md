# Handoff (active work snapshot)

> **[Doc map →](START_HERE.md)** · keep this file **short**; **overwrite** when state moves (no diary here).

## Updated

2026-04-15

## Branch / PR

- **Branch:** `fix/ci-commit-generations-ledger` _(replace when you switch)_
- **Tracking / pushed:** _(fill after `git push -u`)_
- **Open PR:** _(link or “none”)_

## Anchor

- **Commit:** _(paste output of `git log -1 --oneline` on your branch)_

## Goal

Land upload workflows that **commit and push `data/generations.json`** so analytics audits show a non-zero **generations join** for new uploads; keep `docs/spec/workflows.md` aligned.

## Facts (point to paths, do not paste essays)

- Latest weekly report: `data/reports/2026-W16.md`
- Latest channel audit: `data/reports/audit-2026-W16.md` _(join was 0/306 until ledger is persisted from CI)_
- Spec / ADR pointers: **`docs/START_HERE.md`** (map + **post-audit questions** + production checklist); **`docs/MARKDOWN_INDEX.md`** (all `.md`); **`docs/archive/`** (old root playbooks); this work: `docs/spec/workflows.md` § Generations ledger; `docs/decisions/0001-persist-generations-json-on-ci.md`

## Next actions

1. `git push origin fix/ci-commit-generations-ledger` → open PR to `main`.
2. Run one manual upload workflow; confirm `main` includes an update to `data/generations.json`.
3. After merge, optional: `feat/analytics-dual-metrics` PR if still not on `main`.

## Risks / open questions

- _(Short list, optional)_
