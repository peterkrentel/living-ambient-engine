# Start here (documentation map)

> **Who this is for:** You, collaborators, and **AI assistants** working across sessions.  
> **Rule:** If something matters beyond one chat, it belongs **in git** (this tree), not only in IDE memory.

## First session message (copy pattern)

Use a short opener so nobody re-derives context from scratch:

1. **Mode:** Planning only / Implement / Review only  
2. **Goal:** One sentence (verifiable outcome)  
3. **Ground:** `@docs/HANDOFF.md` and, for behavior changes, the spec files below  

## Where truth lives (do not duplicate long explanations)

| Layer | File | What it answers |
|-------|------|-----------------|
| **Right now** | [`HANDOFF.md`](HANDOFF.md) | Branch, anchor commit, next 1–3 actions, pointers to latest `data/reports/*`. **Overwrite** when state moves. |
| **Strategic arc** | [`COHESION_ROADMAP.md`](COHESION_ROADMAP.md) | Ledgers, Phase 0–6, *why* sequencing (batch → join → catalog policy → …). |
| **Analytics / data loop** | [`spec/AGENT.md`](spec/AGENT.md) | Schemas, phases 1–2.5, correlation, suggestions — *what the agent measures*. |
| **CI/CD contract** | [`spec/workflows.md`](spec/workflows.md) | **Exact** workflow behavior: triggers, steps, **including** [`§ Generations ledger`](spec/workflows.md) (commit `data/generations.json` after upload). |
| **Governance** | [`spec/SYSTEM.md`](spec/SYSTEM.md) | Spec-first, file ownership, **session continuity** (handoff + chat limits). |
| **Decisions (why X not Y)** | [`decisions/`](decisions/) | ADRs — short, dated; link from `HANDOFF` when relevant. |
| **Execution** | [`EXECUTION.md`](EXECUTION.md) | venv + Actions only; no ad-hoc system Python. |
| **Guardrails** | [`spec/GUARDRAILS.md`](spec/GUARDRAILS.md) | Parameter limits — **check before changing generation**. |

## What is *not* a durable source of truth

| Thing | Use instead |
|-------|-------------|
| Long chat threads | Update **`HANDOFF.md`** + commit; attach `@docs/HANDOFF.md` next time. |
| Cursor plan files under `~/.cursor/plans/` | Optional; **cloneable** record = this repo (`HANDOFF`, ADRs, specs). |
| PR intent only in your head | **PR description** + optional `CHANGELOG.md` on merge. |

## Implementation vs narrative

- **Changing behavior** (workflows, upload, correlate): **code + `docs/spec/workflows.md`** (and `AGENT.md` / contracts if data shape changes). Same PR per [`SYSTEM.md`](spec/SYSTEM.md).  
- **Changing direction** (milestones, phases): **`COHESION_ROADMAP.md`** / **`master-plan.md`**.  
- **Recording a one-off decision** (branch strategy, tradeoff): **`docs/decisions/`** ADR.

## After this file

[`.github/AGENT_INSTRUCTIONS.md`](../.github/AGENT_INSTRUCTIONS.md) — ordered checklist (includes GUARDRAILS before generation changes). **Continuing work?** Open [`HANDOFF.md`](HANDOFF.md) first.

## Humans

- Onboarding flow: [`GETTING_STARTED.md`](GETTING_STARTED.md) · [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md)  
- Art Creator: [`ART_CREATOR.md`](ART_CREATOR.md)  

---

*If a fact is not findable from the table above, add it to the right file rather than relying on the next chat.*
