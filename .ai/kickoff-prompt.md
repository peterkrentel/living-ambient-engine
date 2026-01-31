# Agent Kickoff Prompt

Copy and paste this at the start of any AI agent session for this repo.

---

## Prompt

```
I'm working on the living-ambient-engine repository.

Before making any changes, I need you to:

1. Read the specs:
   - docs/spec/GUARDRAILS.md (parameter limits, forbidden states)
   - .github/AGENT_INSTRUCTIONS.md (workflow guidance)
   - docs/spec/SYSTEM.md (system overview)

2. For any component you'll modify, read its spec:
   - audio/SPEC.md
   - visuals/SPEC.md
   - orchestrator/SPEC.md
   - config/SPEC.md

3. Confirm you've read the relevant specs before proceeding.

4. Summarize the requirements you extracted from the specs that are relevant to the task.
   - Cite the spec file and section for each requirement.

5. If any spec is missing, unclear, or contradictory, stop and ask for clarification before making changes.

6. Any behavior change requires updating the spec in the same commit.

Before finishing:
- Verify changes comply with all relevant specs
- Map changes back to spec sections
- Ensure existing or new tests validate the behavior

The repo uses spec-driven development with runtime enforcement.
Invalid parameters are auto-clamped. CI validates specs on every PR.
```

---

## Why This Exists

This prompt ensures any AI agent (ChatGPT, Claude, Gemini, Copilot, etc.)
follows the same rules as Augment agents who get `.augment/rules/` injected.

For Augment users: this is already automatic via `.augment/rules/spec-enforcement.md`

For other tools: paste this prompt to achieve the same effect.

