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
| **All `.md` paths** | [`MARKDOWN_INDEX.md`](MARKDOWN_INDEX.md) | Grouped inventory (specs, reports, archive, root exports). |

## What is *not* a durable source of truth

| Thing | Use instead |
|-------|-------------|
| Long chat threads | Update **`HANDOFF.md`** + commit; attach `@docs/HANDOFF.md` next time. |
| Cursor plan files under `~/.cursor/plans/` | Optional; **cloneable** record = this repo (`HANDOFF`, ADRs, specs). |
| PR intent only in your head | **PR description** + optional `CHANGELOG.md` on merge. |

## Root-level `*.md` (caution)

**Exception:** [`CONTENT_LIBRARY.md`](../CONTENT_LIBRARY.md) at repo root is the **library export** (workflows + `library/` write there) — **do not move or rename**.

Other root markdown is often **time-specific**. Historical playbooks now live in **[`docs/archive/`](archive/)** (see [`archive/README.md`](archive/README.md)). Full inventory: **[`MARKDOWN_INDEX.md`](MARKDOWN_INDEX.md)**.

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

## Two channels, two probes

This is the **intentional** split so neither you nor an assistant “merges” the two stories by accident.

| Lane | Channel (OAuth) | What you are probing | Typical shape in practice |
|------|------------------|----------------------|---------------------------|
| **Personal** | `YOUTUBE_TOKEN_PICKLE` — [`content-factory.yml`](../.github/workflows/content-factory.yml) (and [`piano-batch.yml`](../.github/workflows/piano-batch.yml), same secret) | Longer **ambient / mood** exploration; how YouTube treats **depth / length** and calmer catalog | Multi-hour or long-form runs; not the “fill every grid cell” game |
| **Brand** | `YOUTUBE_TOKEN_PICKLE_BRAND` — brand factory, brand batch, Art Creator **brand** upload | Shorter clips, **preset + matrix** output; how YouTube treats **high variety / SEO + art×music** surface | Often **~5 min** and many distinct titles (factory + Art Creator rows in analytics) |

**Repo analytics today (`analytics-agent.yml`):** fetch, weekly **`.md`**, **`suggestions.json`**, **`audit-*.md`**, and **`data/analytics.json`** are **brand only** (workflow sets the brand token). Personal performance is still **Studio / ad hoc** until the plan in [`PERSONAL_ANALYTICS.md`](PERSONAL_ANALYTICS.md) lands (separate JSON + reports). That is not a bug — it is **scope**: one automated measurement spine on brand first.

**Gap to name explicitly:** **`content_catalog.json`** is a **single** repo file today and can include rows from **both** lanes (personal + brand uploads that update the catalog). **`data/analytics.json`** is **only the brand channel’s** video list and metrics. So **`audit-*.md` “generations join”** counts ledger `video_id`s that appear **in brand analytics** — personal-only catalog rows will **not** move that percentage until personal analytics exists or catalogs are split / tagged by channel.

## Post-audit: questions that force the next answer

Answer these in **`HANDOFF.md`** (or an **ADR** if the choice is hard to reverse). Until they are answered, “next production run” stays ambiguous.

1. **Primary production lane for the next stretch:** SEO mood batch (`content-factory-brand-batch`), algorithm batch (`art-creator-batch`), manual brand factory (`content-factory-brand`), and/or hand runs (`art-creator`) — **which one leads**, and which stay **off** or **occasional**?
2. **Schedules:** Re-enable **cron** on which workflows, and when — or stay **manual-only** until another milestone?
3. **Personal channel:** Still **paused** (`content-factory.yml`); is **TBD** still correct, or **retire / repurpose**?
4. **Catalog model:** Heading toward **Cohesion B** (YouTube canonical, repo = generation + analysis) or **A/hybrid** — does the next run need **catalog commits** every time?
5. **Art Creator:** Is it **R&D only** (occasional uploads) or a **first-class production door** — does investment go to **inputs/UX/metadata** here vs batch YAML only?

## Plan checklist (living — as of 2026-04)

Use this as a **checklist**, not a new doc layer. **Done** items stay for history; skip or replace when obsolete.

| Status | Item |
|--------|------|
| Done | **Ledger on `main`:** upload workflows commit **`data/generations.json`**; smoke + **Analytics Agent** re-run. |
| Done | **Catalog → ledger backfill:** [`scripts/backfill_generations_from_catalog.py`](../scripts/backfill_generations_from_catalog.py) + optional **`uploaded_at`** on historic rows ([`AGENT.md`](spec/AGENT.md) § ledger). |
| Done | **Dual-metrics correlate** on `main` (retention + watch minutes → **`suggestions.json`**). |
| Done | **Two-channel doc** + **brand-only analytics vs mixed catalog** gap named ([§ Two channels](#two-channels-two-probes)). |
| Open | **Catalog / channel model:** split file or **`channel`** field so audit join and production intent stay aligned. |
| Open | **Gated production helper (optional):** read `suggestions.json` + gates → **plan JSON** or **BLOCKED** report — no blind auto-render ([`COHESION_ROADMAP.md`](COHESION_ROADMAP.md) Phase 6 ordering). |
| Open | **Personal analytics** per [`PERSONAL_ANALYTICS.md`](PERSONAL_ANALYTICS.md). |
| Open | **Cron / lanes:** post-audit questions above — which workflow leads, when to un-pause schedules. |
| Open | **Art Creator ↔ catalog:** if you want full join, relax **`--no-update-catalog`** or add a parallel ledger path. |

## After this file

[`.github/AGENT_INSTRUCTIONS.md`](../.github/AGENT_INSTRUCTIONS.md) — ordered checklist (includes GUARDRAILS before generation changes). **Continuing work?** Open [`HANDOFF.md`](HANDOFF.md) first.

## Humans

- Onboarding flow: [`GETTING_STARTED.md`](GETTING_STARTED.md) · [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md)  
- Art Creator: [`ART_CREATOR.md`](ART_CREATOR.md)  

---

*If a fact is not findable from the table above, add it to the right file rather than relying on the next chat.*
