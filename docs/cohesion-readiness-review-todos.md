# Cohesion readiness review — parked todos

> **Purpose:** Preserve a **risk / readiness** audit (code-first, not roadmap brainstorming) so work can resume **one item at a time** after a break.  
> **Origin:** Repo assessment prompt (VS Code / Copilot style), executed against the codebase **April 2026**.  
> **How to use:** Work **CR-1** → **CR-6** in order unless a dependency says otherwise; check boxes when merged to `main`. Lower items (**CR-L***) are optional polish.

**Related:** [`HANDOFF.md`](HANDOFF.md) · [`START_HERE.md` § Plan checklist](START_HERE.md#plan-checklist-living-as-of-2026-04) · [`COHESION_ROADMAP.md`](COHESION_ROADMAP.md)

---

## Execution queue (do one at a time)

| ID | Task | Effort |
|----|------|--------|
| [ ] **CR-1** | Extend **`tests/contracts/test_workflow_metadata_consistency.py`** `UPLOAD_WORKFLOWS` (or auto-discover) so **every** workflow that runs `python youtube_upload.py` is covered — include at least `content-factory-brand-batch.yml`, `piano-batch.yml`, `content-factory-personal-long-batch.yml` (grep `.github/workflows` for `youtube_upload.py` and reconcile list). | S |
| [ ] **CR-2** | Remove or narrow **`|| true`** after `scripts/ci_merge_main_after_data_commit.sh` in **`content-factory-brand-micro-batch.yml`** and **`content-factory-personal-long-batch.yml`** (and any other occurrence); fail the step or explicitly log + exit non-zero when merge/push must succeed. | S–M |
| [ ] **CR-3** | Add **direct tests** for **`scripts/correlate.py`** (fixture JSON → stable output shape / join behavior) and **`agent/log_generation.py`** `record_generation_upload` / upsert semantics (`generation_id`, `video_id`, optional `channel`). | M |
| [ ] **CR-4** | Fix **`docs/spec/AGENT.md`** **Data Schemas** drift: header/examples say **schema_version 2** while **`agent/log_generation.py`** implements **`SCHEMA_VERSION = 1`** — align docs to truth or split “target vs implemented.” | S |
| [ ] **CR-5** | **`analytics-agent.yml`** commit step: **`git add … || true`** — remove or scope so failures are visible; align with **`analytics-personal.yml`** (no `|| true` on required adds). | S |
| [ ] **CR-6** | **Optional:** Improve **visibility** when dual-advisory Gemini writes an error stub (e.g. 503) — e.g. `GITHUB_STEP_SUMMARY` line or job annotation so green runs are not misread as “full Gemini prose.” | S |

### Optional follow-ups (lower priority)

- [ ] **CR-L1** — `scripts/verify_ledger_catalog.py`: optional **`channel`**-aware set comparison (catalog + ledger) to reduce noise across lanes.
- [ ] **CR-L2** — Periodic check that **`.github/AGENT_INSTRUCTIONS.md`**, **`.cursor/rules/*.mdc`**, and **`docs/START_HERE.md`** stay aligned on branch/PR and verification policy.
- [ ] **CR-L3** — Optional **pre-commit** secret scan or team rule: never `git add -f` logs / key dumps; keep keys in GitHub **Secrets** only.

---

## 1. Findings (by severity)

### Critical

**None identified** in sampled paths (workflows, ledger, contracts, tests, `.gitignore`, `.devcontainer`). Routine discipline: do not commit API keys or `*key*.log` content.

### High

**H1 — Upload contract tests omit some upload workflows**

- **Why it matters:** Forbidden inline-upload patterns could regress on high-volume lanes while CI stays green.
- **Evidence:** `tests/contracts/test_workflow_metadata_consistency.py` — `UPLOAD_WORKFLOWS` lists five YAML files; other workflows still invoke `python youtube_upload.py` (e.g. `content-factory-brand-batch.yml`, `piano-batch.yml`, `content-factory-personal-long-batch.yml`).
- **Operational impact:** Metadata / cohesion upload path drift undetected.
- **Suggested fix:** **CR-1**.

### Medium

**M2 — `|| true` after merge/push helper**

- **Why:** Swallows merge/push failure; job can look healthy while `main` lags.
- **Evidence:** `content-factory-brand-micro-batch.yml`, `content-factory-personal-long-batch.yml` — `bash scripts/ci_merge_main_after_data_commit.sh || true`.
- **Suggested fix:** **CR-2**.

**M3 — `AGENT.md` schema narrative vs code**

- **Evidence:** `docs/spec/AGENT.md` — “Schema version: 2” and JSON examples vs `agent/log_generation.py` `SCHEMA_VERSION = 1`.
- **Suggested fix:** **CR-4**.

**M4 — No direct tests for correlate / ledger upsert**

- **Evidence:** No `tests/` matches for `correlate` / `log_generation` / `record_generation` join paths.
- **Suggested fix:** **CR-3**.

**M5 — Brand analytics `git add … || true`**

- **Evidence:** `.github/workflows/analytics-agent.yml` commit step; personal workflow uses plain `git add`.
- **Suggested fix:** **CR-5**.

**M6 — Dual advisory “fail soft” (e.g. Gemini 503)**

- **Why:** Green job + stub markdown is easy to miss if you only watch Actions.
- **Suggested fix:** **CR-6** (optional visibility).

### Low

**L1** — `verify_ledger_catalog.py` full-set diff without `channel` split — optional **CR-L1**.  
**L2** — `.devcontainer` minimal vs CI feature parity — document or accept.  
**L3** — Secret hygiene = `.gitignore` + discipline — **CR-L3**.  
**L4** — Multiple governance surfaces — **CR-L2**.

---

## 2. Strengths (evidence)

1. **Canonical agent read order** — `.github/AGENT_INSTRUCTIONS.md` (governance table).
2. **Upload metadata contract tests** — `tests/contracts/test_workflow_metadata_consistency.py`.
3. **Run-intent consumer + strict schema** — `tests/test_consume_run_intent.py`; `scripts/consume_run_intent.py` (`schema_version` check).
4. **Deterministic `run-next` tests** — `tests/test_run_next_report.py`.
5. **Dual-advisory tests** — `tests/test_agent_dual_advisory.py`.
6. **Analytics push race mitigation** — `analytics-agent.yml` / `analytics-personal.yml` — `git pull --rebase origin main` before push.
7. **Multi-lane audit join** — `scripts/audit_channel.py` — `_ledger_row_identity` + identity-aligned join stats.
8. **Intentional catalog policy** — Art Creator `--no-update-catalog` documented in `docs/spec/workflows.md`, `HANDOFF.md`, `youtube_upload.py`.

---

## 3. Cohesion maturity verdict

| Dimension | Verdict |
|-----------|---------|
| Architecture coherence | **Strong** |
| Operational reliability | **Moderate** (`|| true`, Gemini soft-fail) |
| Data contract rigor | **Moderate** (doc/schema drift; Art Creator policy explicit) |
| Test coverage sufficiency | **Moderate** (contracts + run-next + consumer; thin on correlate + ledger) |
| Security / secret hygiene | **Moderate** (ignore rules good; human discipline) |

**Overall: B** — Solid spine and partial guardrails; finish **CR-1**–**CR-3** before treating automation / joins as “fully trusted.”

---

## 4. Release readiness checklist (pass / fail)

Use before treating a release or “cohesion loop complete” as trusted.

| # | Criterion | Pass if |
|---|-----------|--------|
| 1 | Upload path | Every upload job uses **`python youtube_upload.py`**; contract test list **matches** all such workflows. |
| 2 | Post-commit push | No silent **`|| true`** on merge/push unless explicitly justified and logged. |
| 3 | Ledger on `main` | Upload workflows update **`data/generations.json`** as documented; Art Creator catalog exception understood. |
| 4 | Analytics window | Report **`date_range`** matches how you compare to Studio. |
| 5 | Run intent | `run_intent*.json` or blocked md; consumer behavior unchanged if relied on. |
| 6 | Dual advisory | Stubs acceptable **or** summary marks Gemini failure. |
| 7 | CI tests | `pytest` + contracts green; correlate/ledger tests present if claiming join safety. |
| 8 | Secrets | No keys in repo; GitHub Secrets only. |
| 9 | Docs vs code | **`generations.json`** schema story matches **`log_generation.py`**. |
| 10 | Lane isolation | Personal workflows do not overwrite brand `analytics.json` / `suggestions.json`. |

---

## When this doc shrinks

After each **CR-*** ships, update this file (check the box, move finding to a one-line “Done” note) or delete resolved sections and keep only open items. Optionally add a **Done** row to [`START_HERE.md` § Plan checklist](START_HERE.md#plan-checklist-living-as-of-2026-04) when the whole queue is cleared.
