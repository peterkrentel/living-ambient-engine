# AI Agent Instructions

> **Read this file before making any changes to this codebase.**
> **⚠️ MANDATORY: Check GUARDRAILS.md for every change!**

This project uses **spec-driven development**. Specifications are the source of truth for behavior.

## Git: always branch + PR

Do **not** push completed work directly to `main`. Create a **feature branch** from up-to-date `main`, push it, and open a **pull request**. See [`CONTRIBUTING.md`](../CONTRIBUTING.md) § *Git workflow: branch + pull request*. The only routine direct commits on `main` are **automated `data/`** updates from Actions (analytics, etc.)—that exception does not apply to code, specs, or workflow YAML you edit.

## Before Coding

1. **`docs/START_HERE.md`** — what belongs where (do not duplicate that map elsewhere). If continuing a thread: **`docs/HANDOFF.md`**.
2. **`docs/spec/GUARDRAILS.md`** — before any generation-parameter or mood work (**mandatory**).
3. **`docs/EXECUTION.md`** — how jobs run in **venv vs GitHub Actions** (implementation). **Verification for the maintainer** is **CI / GitHub UI first**—see *After Coding* below.
4. **Read only what you will change:** `docs/spec/SYSTEM.md`; relevant `*/SPEC.md`; `docs/spec/contracts/` for interfaces; **`docs/spec/workflows.md`** for any `.github/workflows/` edit.

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

