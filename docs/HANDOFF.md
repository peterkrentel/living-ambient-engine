# Handoff (active work snapshot)

> **[Doc map →](START_HERE.md)** · keep this file **short**; **overwrite** when state moves (no diary here).

## Updated

2026-04-15

## Branch / PR

- **Branch:** `main` (ledger + doc sync landed)
- **Last merge:** PR #48 — `fix/ci-commit-generations-ledger` → `main`
- **Open PR:** _(none for this track — add when you open the next one)_

## Anchor

- **Commit:** `9936cff` — Merge pull request #48 (generations ledger CI, `test-art-creator` path + permissions fixes, doc map / archive)

## Goal (done for this PR)

Upload workflows **commit and push `data/generations.json`** on successful uploads; **`test-art-creator.yml`** valid for `workflow_call` into `art-creator.yml`.

## Facts (point to paths, do not paste essays)

- Latest weekly report: `data/reports/2026-W16.md`
- Latest channel audit: `data/reports/audit-2026-W16.md` _(re-run audit after a production upload to confirm join > 0 for new `video_id`s)_
- Spec / ADR: **`docs/START_HERE.md`** · **`docs/MARKDOWN_INDEX.md`** · **`docs/spec/workflows.md`** § Generations ledger · **`docs/decisions/0001-persist-generations-json-on-ci.md`**

## Next actions

1. **Smoke:** Run one real upload path you use (e.g. `workflow_dispatch` on brand factory or piano batch); confirm **`main`** picks up **`data/generations.json`** (and catalog if that path commits it).
2. Optional: PR **`feat/analytics-dual-metrics`** if it is still not on `main` (see `docs/START_HERE.md` checklist).
3. Next analytics weekly run: spot-check **`data/reports/audit-*.md`** join line after (1).

## Risks / open questions

- Fork PRs: `contents: write` on `test-art-creator` is required for YAML validity; token may still be limited on fork runs (same-repo PRs unaffected).
