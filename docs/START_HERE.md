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

## Root-level `*.md` (caution)

Files next to `README.md` (e.g. [`TESTING_PLAN.md`](../TESTING_PLAN.md), `IMPLEMENTATION_SUMMARY.md`, `INTEGRATION_STATUS.md`) are often **time- and branch-specific** playbooks. Treat them as **optional smoke notes**, not current status: check **named branch**, **date**, **paths** (GitHub Actions uses `/home/runner/...`; locally use your **repo root**), and **line numbers** into large YAML — those go stale.

**Merge / contract truth:** [`spec/workflows.md`](spec/workflows.md) and the workflows it references (including PR gate [`test-art-creator.yml`](../.github/workflows/test-art-creator.yml)).

## Implementation vs narrative

- **Changing behavior** (workflows, upload, correlate): **code + `docs/spec/workflows.md`** (and `AGENT.md` / contracts if data shape changes). Same PR per [`SYSTEM.md`](spec/SYSTEM.md).  
- **Changing direction** (milestones, phases): **`COHESION_ROADMAP.md`** / **`master-plan.md`**.  
- **Recording a one-off decision** (branch strategy, tradeoff): **`docs/decisions/`** ADR.

## Workflows: how they got here (reality)

`.github/workflows/` did **not** start as one grand design. They **accreted**: Content Factory (personal → brand) → Art Creator (separate palette, then optional brand upload + many YAML fixes) → scheduled **batches** (SEO mood rotation vs art×music discovery) → **Analytics Agent** → **Piano batch** → **audit-window pauses** → **ledger on `main`**. That is normal for a working channel + CI setup.

- **Design intent (one slice):** [`WORKFLOW_ARCHITECTURE.md`](WORKFLOW_ARCHITECTURE.md) — Art Creator vs Content Factory; may be **stale** on details (check [`spec/workflows.md`](spec/workflows.md) + YAML).
- **Evidence of evolution:** `git log --oneline -- .github/workflows/`

You usually **do not need a new workflow** unless there is a **new job-to-be-done**; prefer **editing existing YAML** and **moving logic into Python/orchestrator** so workflows stay thin triggers.

## Post-audit: questions that force the next answer

Answer these in **`HANDOFF.md`** (or an **ADR** if the choice is hard to reverse). Until they are answered, “next production run” stays ambiguous.

1. **Primary production lane for the next stretch:** SEO mood batch (`content-factory-brand-batch`), algorithm batch (`art-creator-batch`), manual brand factory (`content-factory-brand`), and/or hand runs (`art-creator`) — **which one leads**, and which stay **off** or **occasional**?
2. **Schedules:** Re-enable **cron** on which workflows, and when — or stay **manual-only** until another milestone?
3. **Personal channel:** Still **paused** (`content-factory.yml`); is **TBD** still correct, or **retire / repurpose**?
4. **Catalog model:** Heading toward **Cohesion B** (YouTube canonical, repo = generation + analysis) or **A/hybrid** — does the next run need **catalog commits** every time?
5. **Art Creator:** Is it **R&D only** (occasional uploads) or a **first-class production door** — does investment go to **inputs/UX/metadata** here vs batch YAML only?

## Once you pick a step in the plan (tackle in order)

Use this as a **checklist**, not a new doc layer. Skip items that do not apply.

1. **Ledger on `main`:** merge the PR that makes upload jobs **commit `data/generations.json`**; smoke one upload; confirm audit join **>0** for new `video_id`s.
2. **Doc drift:** fix any workflow doc that disagrees with YAML (e.g. [`WORKFLOW_ARCHITECTURE.md`](WORKFLOW_ARCHITECTURE.md) vs current Art Creator upload behavior).
3. **Turn production back on:** `workflow_dispatch` first, then **un-pause cron** only for the lane you chose in question (1)–(2).
4. **Evolve Art Creator (optional):** parameters, titles, upload path — **after** (1) so experiments **show up** in `generations.json` on `main`.
5. **Dual-metrics / correlate:** if `feat/analytics-dual-metrics` is not on `main`, merge when ready so CI matches [`spec/AGENT.md`](spec/AGENT.md) Phase 2.

## After this file

[`.github/AGENT_INSTRUCTIONS.md`](../.github/AGENT_INSTRUCTIONS.md) — ordered checklist (includes GUARDRAILS before generation changes). **Continuing work?** Open [`HANDOFF.md`](HANDOFF.md) first.

## Humans

- Onboarding flow: [`GETTING_STARTED.md`](GETTING_STARTED.md) · [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md)  
- Art Creator: [`ART_CREATOR.md`](ART_CREATOR.md)  

---

*If a fact is not findable from the table above, add it to the right file rather than relying on the next chat.*
