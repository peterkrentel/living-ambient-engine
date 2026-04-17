# AI Agent Instructions

> **Read this file before making any changes to this codebase.**
> **⚠️ MANDATORY: Check GUARDRAILS.md for every change!**

**Maintainer verification default:** **GitHub Actions + github.com only** — do **not** instruct the maintainer to run local `git` / venv / `python …` for smoke or “did it work?” unless they **explicitly** ask for local steps (see [`.cursor/rules/ci-only-verification.mdc`](../.cursor/rules/ci-only-verification.mdc) and *After Coding*).

This project uses **spec-driven development**. Specifications are the source of truth for behavior.

## Governance stack and read order

**Why this section exists:** Git does not execute docs. Until this list, **no single file defined the sequence**—truth was spread across `START_HERE`, `GUARDRAILS`, contracts, workflows, and Cursor rules. Assistants guessed from fragments. **This heading is the canonical order** for a normal change; keep it in sync if you add layers.

**Read in this order** (stop when you have enough context for the task):

| Step | Read | What it answers |
|------|------|-----------------|
| 1 | [`docs/START_HERE.md`](../docs/START_HERE.md) | Where each kind of truth lives—**do not duplicate** that map in chat. |
| 2 | [`docs/HANDOFF.md`](../docs/HANDOFF.md) | **Only if** continuing in-repo work (branch, next actions, pointers). |
| 3 | [`docs/spec/GUARDRAILS.md`](../docs/spec/GUARDRAILS.md) | **Before** generation-parameter, mood, duration, or limit changes—hard caps. |
| 4 | [`docs/spec/SYSTEM.md`](../docs/spec/SYSTEM.md), the relevant `*/SPEC.md`, and [`docs/spec/contracts/`](../docs/spec/contracts/) | Behavior and interfaces you are changing. |
| 5 | [`docs/spec/workflows.md`](../docs/spec/workflows.md) | **Only if** editing `.github/workflows/*.yml`. |
| 6 | [`.cursor/rules/*.mdc`](../.cursor/rules/) | Cursor-only maintainer preferences (e.g. CI-first verification). |

**Then:** branch + PR (below); ship spec/contract/doc updates **in the same change** as code; verify via **GitHub Actions** and the **github.com** UI unless the maintainer asks for local steps.

## Git: always branch + PR

Do **not** push completed work directly to `main`. Create a **feature branch** from up-to-date `main`, push it, and open a **pull request**. See [`CONTRIBUTING.md`](../CONTRIBUTING.md) § *Git workflow: branch + pull request*. The only routine direct commits on `main` are **automated `data/`** updates from Actions (analytics, etc.)—that exception does not apply to code, specs, or workflow YAML you edit.

## Before Coding

Follow **Governance stack and read order** above. In addition:

- **`docs/EXECUTION.md`** — how jobs run in **venv vs GitHub Actions** (implementation detail). Maintainer verification: **CI / GitHub UI first**—see *After Coding*.
- **Narrow reading:** open only the specs and contracts that touch files you will edit—do not re-read the whole tree every time.

## While Coding

- **Honor contracts**: Component interfaces must match their contract definitions
- **Follow patterns**: Match existing code style and patterns in the component
- **Preserve invariants**: Don't break guarantees listed in specs

## After Coding

1. **Update specs**: Any behavior change requires a spec update in the same commit
2. **Update contracts**: Interface changes require contract updates
3. **Update docs**: User-facing changes need doc updates
4. **Test / verify:** Prefer **GitHub Actions** (`workflow_dispatch`), PR checks, and the **github.com** file/commit view. **Do not** instruct the maintainer to run local git, venv, or CLI verification unless they **explicitly** ask for local steps. Optional venv smoke for contributors who use it: `docs/EXECUTION.md`.

## Quick Reference

| Change Type | Specs to Update |
|-------------|-----------------|
| **Any parameter change** | `docs/spec/GUARDRAILS.md` + component spec |
| New audio feature | `audio/SPEC.md`, `docs/spec/GUARDRAILS.md` |
| New visual pattern | `visuals/SPEC.md`, `docs/spec/GUARDRAILS.md` |
| New workflow input | `docs/spec/workflows.md`, `docs/spec/GUARDRAILS.md` |
| New mood preset | `config/SPEC.md` |
| Interface change | `docs/spec/contracts/*.md` + both component specs |
| New journey preset | `config/SPEC.md`, `audio/SPEC.md`, `visuals/SPEC.md` |

## Common Mistakes to Avoid

- ❌ **NOT checking GUARDRAILS.md before making changes**
- ❌ Adding features without updating specs
- ❌ Changing interfaces without updating contracts
- ❌ Assuming behavior from code alone (read the spec!)
- ❌ Creating new files when editing existing ones would work
- ❌ Adding dependencies without using package manager
- ❌ Adding parameters without defining limits in GUARDRAILS.md
- ❌ Bypassing validation/clamping in generators
- ❌ **Telling the maintainer to “run locally”** (git, venv, `python …`) as the default verification path—use **Actions + GitHub UI** unless they ask for local steps

## Testing Commands

Optional for contributors using a **local venv** (not the default verification story for CI-only maintainers):

```bash
# Quick smoke test (30 seconds)
python run_job.py --mood trance --duration 30

# Test specific mood
python run_job.py --mood deep_focus --duration 30

# Test batch generation
python batch_generate.py --moods rain_sleep,ocean_waves --durations 30s

# Validate YAML configs
python -c "import yaml; yaml.safe_load(open('config/moods.yaml'))"

# Test journey curves
python -c "from config.journeys import JOURNEY_PRESETS; print(list(JOURNEY_PRESETS.keys()))"
```

## Project Structure

```
docs/spec/
├── SYSTEM.md           # Start here - system overview
├── contracts/          # Cross-component interfaces
│   ├── orchestrator-audio.md
│   ├── orchestrator-visual.md
│   └── orchestrator-youtube.md
└── workflows.md        # GitHub Actions specs

audio/SPEC.md           # Audio generator
visuals/SPEC.md         # Visual generator
orchestrator/SPEC.md    # Pipeline coordinator
youtube/SPEC.md         # YouTube uploader
config/SPEC.md          # Configuration
render/SPEC.md          # FFmpeg wrapper
```

## When in Doubt

1. Ask the user for clarification
2. Read the spec again
3. Check history for similar changes (GitHub **Commits** / **Blame** on the file, or `git log` only when working in a clone)
4. Look at existing tests for expected behavior

