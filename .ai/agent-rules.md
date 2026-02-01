# Agent Rules

Normative rules for any AI agent working on this codebase.

## MUST

1. Read `docs/spec/GUARDRAILS.md` before making any changes
2. Read `.github/AGENT_INSTRUCTIONS.md` for workflow guidance
3. Extract requirements explicitly from specs before implementing
4. Validate changes against acceptance criteria in specs
5. Update specs when changing behavior (same commit)
6. Use `clamp_to_guardrails()` for any new parameter validation
7. Run contract tests after changes: `pytest tests/contracts/ -v`

## MUST NOT

1. Invent behavior not defined in specs
2. Add parameters without defining limits in GUARDRAILS.md
3. Bypass validation/clamping in generators
4. Change interfaces without updating contracts
5. Commit code changes without corresponding spec updates

## Parameter Limits (Quick Reference)

| Parameter | Min | Max | Default |
|-----------|-----|-----|---------|
| tempo | 20 | 200 | 60 |
| visual_speed | 0.01 | 1.5 | 0.5 |
| visual_complexity | 0.1 | 1.0 | 0.7 |
| duration | 5s | 4h | 5min |
| fps | 15 | 60 | 15 |

## Enforcement

These rules are enforced at multiple levels:
- **Runtime**: `clamp_to_guardrails()` auto-corrects violations
- **CI**: `spec-validation` job blocks PRs with missing specs
- **Tests**: 18+ contract tests validate schemas

Violations that bypass specs will be caught and corrected automatically.

