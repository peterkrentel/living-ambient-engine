# Component Contracts

> Internal contracts defining interfaces between components.
> Changes to these contracts require updates to both sides of the interface.

## Contract Index

| Contract | Components | Description |
|----------|------------|-------------|
| [orchestrator-audio](./orchestrator-audio.md) | Orchestrator → Audio | Audio generation interface |
| [orchestrator-visual](./orchestrator-visual.md) | Orchestrator → Visual | Visual generation interface |
| [orchestrator-youtube](./orchestrator-youtube.md) | Workflow → YouTube | Upload interface |
| [production-run-intent](./production-run-intent.md) | Planner / human → CI | Versioned JSON for moods, duration, dual, upload, channel (precision path; workflow consumer TBD) |

## Contract Rules

1. **Both sides must agree** - Changes require updates to caller and callee
2. **Backward compatible when possible** - Add optional params, don't remove required ones
3. **Version in spec** - Major interface changes get a version bump note
4. **Test the contract** - Each contract includes a test example

## How to Update a Contract

1. Propose change in PR description
2. Update the contract markdown file
3. Update both components to match
4. Update/add tests that verify the contract
5. Get review from owners of both components

## Contract Template

When adding a new contract:

```markdown
# Contract: Component A → Component B

> One-line description

## Interface
\`\`\`python
# Function/class signature
\`\`\`

## Guarantees
### Caller Guarantees
### Callee Guarantees

## Error Handling

## Testing Contract
```

