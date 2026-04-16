# Markdown inventory

> **Purpose:** One place to see **what every `.md` is for** so cleanup and “what’s stale?” questions are faster.  
> **Rule:** **Do not** move or rename **`CONTENT_LIBRARY.md`** (repo root) or paths under **`data/reports/`** — workflows and tooling expect them.

## Entry points (read these first)

| Path | Role |
|------|------|
| [`README.md`](../README.md) | Project overview, links into `docs/` |
| [`docs/START_HERE.md`](START_HERE.md) | Doc map, handoff, workflow reality, post-audit questions |
| [`docs/HANDOFF.md`](HANDOFF.md) | Current branch / next actions (overwrite often) |
| [`.github/AGENT_INSTRUCTIONS.md`](../.github/AGENT_INSTRUCTIONS.md) | AI / contributor checklist |

## Specs and contracts (`docs/spec/`)

| Area | Files |
|------|--------|
| Core | `SYSTEM.md`, `GUARDRAILS.md`, `ENFORCEMENT.md`, `workflows.md`, `AGENT.md` |
| Contracts | `contracts/*.md` |

## Component specs (code-adjacent)

| Path |
|------|
| `audio/SPEC.md`, `visuals/SPEC.md`, `orchestrator/SPEC.md`, `youtube/SPEC.md`, `config/SPEC.md`, `render/SPEC.md` |

## Human guides (`docs/`)

| Examples |
|----------|
| `GETTING_STARTED.md`, `QUICK_REFERENCE.md`, `ART_CREATOR*.md`, `CONTENT_LIBRARY*.md`, `EXECUTION.md`, `FAQ.md`, `COHESION_ROADMAP.md`, `master-plan.md`, `architecture.md`, `WORKFLOW_ARCHITECTURE.md`, `youtube-auth.md`, `USE_CASES.md`, `PIANO_BATCH_GUIDE.md`, `PERSONAL_ANALYTICS.md`, `decisions/*.md` |

## CI / data outputs (generated or semi-generated — do not “archive”)

| Path | Notes |
|------|--------|
| `data/reports/*.md` | Analytics Agent weekly reports + audits — **committed by CI** |
| **`CONTENT_LIBRARY.md`** (repo root) | **Library export** — path fixed in `library/` and workflows |

## Archived playbooks

| Path |
|------|
| [`docs/archive/`](archive/) — see [`archive/README.md`](archive/README.md) |

## Tooling / IDE (optional)

| Path |
|------|
| `.ai/agent-rules.md`, `.ai/kickoff-prompt.md` |

## Repo root (non-archive)

| Path | Notes |
|------|--------|
| `README.md`, `CONTRIBUTING.md` | Canonical |
| `CONTENT_LIBRARY.md` | **Generated** export (large) — not the same as `docs/CONTENT_LIBRARY.md` (human guide) |

---

*To refresh this list: `find . -name '*.md' -not -path './.git/*' -not -path './venv/*' | sort`*
