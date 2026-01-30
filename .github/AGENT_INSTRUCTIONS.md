# AI Agent Instructions

> **Read this file before making any changes to this codebase.**

This project uses **spec-driven development**. Specifications are the source of truth for behavior.

## Before Coding

1. **Read the system spec**: `docs/spec/SYSTEM.md`
2. **Read component specs**: Check `*/SPEC.md` for any component you'll modify
   - `audio/SPEC.md` - Audio generation
   - `visuals/SPEC.md` - Visual generation
   - `orchestrator/SPEC.md` - Pipeline coordination
   - `youtube/SPEC.md` - YouTube uploads
   - `config/SPEC.md` - Configuration system
   - `render/SPEC.md` - FFmpeg rendering
3. **Check contracts**: `docs/spec/contracts/` for cross-component interfaces
4. **Check workflow specs**: `docs/spec/workflows.md` for CI/CD changes

## While Coding

- **Honor contracts**: Component interfaces must match their contract definitions
- **Follow patterns**: Match existing code style and patterns in the component
- **Preserve invariants**: Don't break guarantees listed in specs

## After Coding

1. **Update specs**: Any behavior change requires a spec update in the same commit
2. **Update contracts**: Interface changes require contract updates
3. **Update docs**: User-facing changes need doc updates
4. **Test**: Run `python run_job.py --mood trance --duration 30` to verify

## Quick Reference

| Change Type | Specs to Update |
|-------------|-----------------|
| New audio feature | `audio/SPEC.md` |
| New visual pattern | `visuals/SPEC.md` |
| New workflow input | `docs/spec/workflows.md`, relevant component spec |
| New mood preset | `config/SPEC.md` |
| Interface change | `docs/spec/contracts/*.md` + both component specs |
| New journey preset | `config/SPEC.md`, `audio/SPEC.md`, `visuals/SPEC.md` |

## Common Mistakes to Avoid

- ❌ Adding features without updating specs
- ❌ Changing interfaces without updating contracts
- ❌ Assuming behavior from code alone (read the spec!)
- ❌ Creating new files when editing existing ones would work
- ❌ Adding dependencies without using package manager

## Testing Commands

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
3. Check git history for similar changes: `git log --oneline --all -- <file>`
4. Look at existing tests for expected behavior

