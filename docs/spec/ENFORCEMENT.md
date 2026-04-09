# Enforcement Architecture

> **Three-layer control system for spec-driven development.**
> Ensures specs are followed by humans, AI agents, and automated systems.

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    LAYER 3: AGENT BIAS                      │
│         "Bias agents toward reading specs first"            │
├─────────────────────────────────────────────────────────────┤
│  .github/AGENT_INSTRUCTIONS.md        → Cursor / any agent  │
│  .ai/agent-rules.md                  → Any AI agent        │
│  .ai/kickoff-prompt.md               → Manual paste        │
│  README.md notice                    → First thing seen    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   LAYER 2: ENFORCEMENT                      │
│            "Catch violations automatically"                 │
├─────────────────────────────────────────────────────────────┤
│  clamp_to_guardrails()               → Runtime auto-fix    │
│  spec-validation job                 → PR blocks           │
│  contract tests                      → CI blocks           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    LAYER 1: TRUTH                           │
│              "Single source of truth"                       │
├─────────────────────────────────────────────────────────────┤
│  docs/spec/GUARDRAILS.md             → Parameter limits    │
│  docs/spec/SYSTEM.md                 → System overview     │
│  docs/spec/contracts/*.md            → Interfaces          │
│  */SPEC.md                           → Component specs     │
└─────────────────────────────────────────────────────────────┘
```

## How It Works

### Layer 1: Truth (Specs)

The specs define what the system should do. They are:
- **Versioned** in git
- **Reviewable** in PRs
- **Authoritative** - code follows specs, not vice versa

| File | Purpose |
|------|---------|
| `docs/spec/GUARDRAILS.md` | Parameter limits, forbidden states |
| `docs/spec/SYSTEM.md` | System architecture overview |
| `docs/spec/contracts/*.md` | Cross-component interfaces |
| `*/SPEC.md` | Component-level specifications |

### Layer 2: Enforcement (Validators)

Automated systems that catch violations:

| Mechanism | When | Action |
|-----------|------|--------|
| `clamp_to_guardrails()` | Runtime | Auto-corrects invalid values |
| `spec-validation` job | Every PR | Blocks merge if specs missing |
| Guardrail↔Contract check | Every PR | Blocks merge if guardrails lack tests |
| Contract tests | Every PR | Blocks merge if schemas violated |

**Key insight**: Even if an agent ignores specs, Layer 2 catches it.

**Guardrail↔Contract alignment** (added to prevent OOM-style bugs):
```yaml
# In .github/workflows/test-art-creator.yml spec-validation job
- name: Validate guardrails have contract tests
  run: |
    # Each forbidden state in GUARDRAILS.md must have a contract test
    if ! grep -q "test_memory_guardrail" tests/contracts/test_audio_contract.py; then
      exit 1  # Block merge
    fi
```

### Layer 3: Agent Bias (Rules)

Nudges AI agents to read specs before coding:

| File | Tool | Injection |
|------|------|-----------|
| `.github/AGENT_INSTRUCTIONS.md` | Cursor / Copilot / etc. | Read first (README links it) |
| `.cursor/rules/*.md` | Cursor | Optional project rules (if present) |
| `.ai/agent-rules.md` | Any AI | Reference |
| `.ai/kickoff-prompt.md` | Any AI | Manual paste |
| `README.md` notice | Any AI | First thing seen |

**Key insight**: This layer is "best effort" - if it fails, Layer 2 catches it.

## Failure Modes

| Scenario | Layer 3 | Layer 2 | Layer 1 | Outcome |
|----------|---------|---------|---------|---------|
| Agent reads specs | ✅ | ✅ | ✅ | Perfect |
| Agent skips specs | ❌ | ✅ | ✅ | Caught by validators |
| Bad value in config | ❌ | ✅ | ✅ | Auto-clamped at runtime |
| Missing spec update | ❌ | ✅ | ✅ | PR blocked by CI |
| All layers fail | ❌ | ❌ | ✅ | Spec documents intent for fix |

## Design Principles

1. **Stateless agents, stateful intent** - Agents don't need memory; specs are in git
2. **Defense in depth** - Multiple layers catch different failure modes
3. **Fail safe** - Invalid values are corrected, not rejected
4. **Portable** - Works with any AI tool or editor
5. **Versioned** - All rules are in git, not tool settings

## Adding New Enforcement

When adding new parameters or features:

1. **Define in Layer 1** - Add to GUARDRAILS.md with limits
2. **Enforce in Layer 2** - Add to JSON schema + validator
3. **Document in Layer 3** - Update agent-rules.md if needed

## References

- [GUARDRAILS.md](./GUARDRAILS.md) - All parameter limits
- [SYSTEM.md](./SYSTEM.md) - System architecture
- [AGENT_INSTRUCTIONS.md](../../.github/AGENT_INSTRUCTIONS.md) - AI agent guide
- [agent-rules.md](../../.ai/agent-rules.md) - Normative rules for any AI

