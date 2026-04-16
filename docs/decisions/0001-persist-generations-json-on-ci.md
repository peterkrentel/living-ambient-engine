# ADR 0001: Persist `data/generations.json` from CI upload workflows

- **Status:** Accepted  
- **Date:** 2026-04-15  
- **Context:** Channel audit (`data/reports/audit-2026-W16.md`) showed **`generations.json` join 0 / 306** vs `analytics.json`. Code already called `record_generation_upload` from `youtube_upload.py` on the runner, but **no workflow committed `data/generations.json` to `main`**, so the ledger never became the join source for analytics.  
- **Decision:** Every GitHub Actions workflow that runs `youtube_upload.py` must **stage, commit, and push** `data/generations.json` when it changes (same commit as catalog where catalog is committed; dedicated step where there is no catalog commit). Art Creator `upload` job grants `contents: write` only on that job for the push.  
- **Consequences:** Non-zero join for **new** uploads after merge; historic videos remain unjoined until optional backfill. Merge conflicts possible if two upload jobs finish close together — same class of risk as catalog commits; mitigate with usual pull/rebase patterns if needed.  
- **Spec:** [`docs/spec/workflows.md`](../spec/workflows.md) § Generations ledger (canonical step list).
