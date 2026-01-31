# Spec Enforcement Rule

**MANDATORY for all code changes in this repository.**

## Before Making ANY Code Changes

1. **READ FIRST** - Always read these files before making any edits:
   - `.github/AGENT_INSTRUCTIONS.md` - Step-by-step guide for AI agents
   - `docs/spec/GUARDRAILS.md` - All parameter limits and forbidden states

2. **CONFIRM** - Before proceeding with edits, confirm you have read the specs by stating:
   > "I have read AGENT_INSTRUCTIONS.md and GUARDRAILS.md."

3. **CHECK LIMITS** - For any parameter changes, verify the new value is within guardrails:
   - tempo: 20-200 BPM
   - visual_speed: 0.01-1.5
   - visual_complexity: 0.1-1.0
   - duration: 10s-4h
   - fps: 15-60

4. **UPDATE SPECS** - Any behavior change requires a spec update in the same commit

## Common Mistakes to Avoid

- ❌ Making changes without reading GUARDRAILS.md first
- ❌ Adding parameters without defining limits
- ❌ Changing interfaces without updating contracts
- ❌ Skipping spec review "just this once"

## Why This Matters

This project uses spec-driven development. The specs are enforced at:
- **Runtime**: `clamp_to_guardrails()` in generators
- **CI**: spec-validation job on every PR
- **Tests**: 18+ contract tests

If you skip the specs, you may introduce bugs that are silently corrected at runtime.

