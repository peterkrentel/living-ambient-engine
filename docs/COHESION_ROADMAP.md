# Cohesion Roadmap

> **Purpose:** Unify the narrative (art → production → data), clarify **where truth lives**, and sequence technical work without breaking active automation.  
> **Companion docs:** [Master Plan](master-plan.md) (milestones), [Analytics Agent spec](spec/AGENT.md) (data loop phases), [Architecture](architecture.md) (diagrams).

## One-line summary

Unify story and systems: **three ledgers** (YouTube / `data/` / catalog), then close **video_id ↔ generation metadata**, then catalog policy, honest **stats vs ML** naming, portfolio wording, and later **human-in-the-loop** recommendations before any auto-queue.

---

## Principles

1. **Do not destabilize CI mid-flight** — Finish the current **Content Factory Brand Batch** rotation before changing `content-factory-brand-batch.yml`, unless changes are strictly **post-success** and **additive**.
2. **One spine, many modes** — Same engine: **art exploration**, **batch production**, **measurement**, (future) **recommendations**. Not one slogan; one **through-line**.
3. **Truth over hype** — Today = ingestion, reports, **statistical** correlation with gates. Reserve “ML” for trained models when they exist; “LLM planner” only after human-in-the-loop works.
4. **Metadata is the gold** — Each render produces a sidecar JSON with **seed** and **visual/audio configs** ([orchestrator](../orchestrator/orchestrator.py)). The cohesive win is **joining `video_id` ↔ that record**, not relying only on title parsing.
5. **Run via venv or CI** — Do not depend on ad-hoc system Python for project commands. Local work uses an **activated project virtualenv**; production and scheduled jobs run in **GitHub Actions**. See [EXECUTION.md](EXECUTION.md).

**Framing:** Crossing from **content automation** → **data system** is where many projects stall; the **join** is the unlock for honest correlation and any future ML—not more commentary alone.

---

## The three ledgers

| Ledger | What it is | Typical update path |
|--------|------------|---------------------|
| **YouTube** | Canonical public inventory + real-time stats | Upload workflows |
| **`data/*`** | Performance snapshots in git (`analytics.json`, `reports/`, `suggestions.json`) | [Analytics Agent](../.github/workflows/analytics-agent.yml) weekly / manual |
| **`content_catalog.json`** (+ optional `CONTENT_LIBRARY.md`) | Repo-side publishing catalog | Some upload workflows commit; **brand batch** historically did not — **policy choice** (see Phase 3) |

**Ephemeral (not a ledger):** [Content Factory Brand Batch](../.github/workflows/content-factory-brand-batch.yml) stores `./generated/` as a **GitHub Actions artifact** with **short retention** (~7 days). You cannot recover historical **generation params** from CI after that. YouTube keeps the video; **Phase 2** is what makes params durable in git.

---

## Phase 0 — Now: land brand batch

- Let **Content Factory Brand Batch** complete its mood rotation.
- Avoid editing that workflow until done (or accept re-runs).
- Optional: personal note of day index / moods / failures so “done” is explicit.

**Phase 0 complete (checklist — use what matches your intent):**

- [ ] Each of the **14** moods in the workflow list has appeared at least once from **scheduled** runs (rotation), **or** you explicitly accept stopping early / gaps from `day_override` / missed days.
- [ ] No undocumented **P0** generation or upload failures for that workflow (or failures are written down).
- [ ] Optional: snapshot **day index** / mood triples / quota stops so “done” is auditable later.

**Versioning (optional):** Git tag e.g. `pre-cohesion-2026` on `main` as a snapshot before ledger work.

---

## Phase 1 — Narrative cohesion (docs only)

**Goal:** Readable in ~5 minutes: **origins → today → next**.

| Deliverable | Notes |
|-------------|--------|
| This file + links | Single place for integration sequencing |
| Short **“Origins → Evolution → Roadmap”** blurb | Can live in [SYSTEM.md](spec/SYSTEM.md) intro or README if you want it more visible |
| **Three ledgers** (table above) | Stops “which source of truth?” confusion |

**Risk:** None (documentation). Can run **in parallel** with Phase 2; do **not** let narrative work **delay** the join for long—otherwise you accumulate analytics you can’t fully attribute.

---

## Phase 2 — Technical: params ↔ YouTube (the core dataset)

**Goal:** Correlation and future models use **real inputs**, not only parsed titles. **This phase is the main technical priority** after Phase 0 (batch) is stable.

| Step | Action |
|------|--------|
| 2a | Persist each run with **`generation_id`** + **generation params** (sidecar: seed, mood, configs, workflow, `GITHUB_SHA`); set / update **`video_id`** after successful upload (see **Data contract rules** below). **`data/generations.json`** per [AGENT.md](spec/AGENT.md). |
| 2b | **Pick one code path:** either **`python -m agent.log_generation`** from workflows **or** append inside [`youtube_upload.py`](../youtube_upload.py) only — avoid splitting logic across both. Same commit as [AGENT.md](spec/AGENT.md) updates so spec matches code. **Implemented path:** `youtube_upload.py` → `record_generation_upload`. |
| 2c | **CI must persist the ledger on `main`:** every workflow that runs `youtube_upload.py` **commits and pushes** `data/generations.json` when it changes (not only the catalog). Otherwise audits show **0% join** forever. Canonical step list: [workflows.md](spec/workflows.md) § **Generations ledger**. ADR: [decisions/0001](decisions/0001-persist-generations-json-on-ci.md). |
| 2d | Evolve **`scripts/correlate.py`**: join analytics rows by **`video_id`** to **`generations.json`** and use **params**; **else** fallback to title parsing (backward compatibility). **Dual engagement metrics:** correlate on **`average_view_percentage`** (retention) and **`watch_time_minutes`** (minutes in fetch window per video — growth signal); see [AGENT.md](spec/AGENT.md) Phase 2. |
| 2e | **Inference hygiene (Phase 2.5):** add uncertainty stats **with** documented limits—**title/thumbnail/CTR confound** param–outcome stories; confidence intervals **do not** remove that. Canonical copy: [AGENT.md](spec/AGENT.md) § *Confounders & packaging* + Phase 2.5. Optional **2f** (later): packaging **fingerprints** on ledger rows joinable to analytics. |

**Schema risk:** `generations.json` becomes the **central join table**—lock fields and **`schema_version`** early; bump version when fields change. Use a stable **internal** id distinct from YouTube’s id: **`generation_id`** (UUID) = one generation/upload *event*; **`video_id`** = external join after publish (may be missing until upload succeeds; retries re-link the same `generation_id`).

#### Data contract rules (`generations.json`)

1. **Identity:** **`generation_id`** is mandatory and stable for the lifecycle of that render/upload attempt. **`video_id`** is the **external** join key to YouTube and analytics; optional until upload succeeds.
2. **Updates vs append:** **Append** a new record when a **new** generation run starts. **Update in place** the same **`generation_id`** when upload **retries** succeed (set `video_id`, timestamps)—avoid duplicate rows for the same logical generation. (If you ever need an audit log of every attempt, use a separate `attempts[]` sub-array or a second file; don’t blur “one row per generation” without documenting it.)
3. **Fallback precedence for analysis:** **`generations.json` params** (by `video_id`) → **title parsing** → `"unknown"` / skip. Document this in [AGENT.md](spec/AGENT.md) when implemented.
4. **Schema bumps:** Increment **`schema_version`** when required fields or semantics change; migrations or one-time scripts for old rows if needed.
5. **One row per uploaded asset:** Each record that reaches YouTube should map to **one** **`video_id`**. If batch tooling uses **`--dual`** (ambience + melody), expect **two rows** (two **`generation_id`**s, two **`video_id`**s) for one render job. Optionally link them with a shared **`batch_run_id`** or **`parent_generation_id`**—pick one approach and document it in [AGENT.md](spec/AGENT.md).

Example **minimum** shape (extend per [AGENT.md](spec/AGENT.md)):

```json
{
  "schema_version": 1,
  "videos": [
    {
      "generation_id": "uuid-v4",
      "video_id": "string-or-null-until-upload",
      "uploaded_at": "ISO8601-or-null",
      "workflow": "content-factory-brand.yml",
      "commit_sha": "optional",
      "mood": "string",
      "seed": 0,
      "params": {
        "visual_config": {},
        "audio_config": {}
      }
    }
  ]
}
```

**Rule once join exists:** Prefer **joined params** for mood/art_period/music_style; do **not** treat title parsing as primary for new analysis.

**Rollout:** Test on **one** workflow first (e.g. manual brand upload), not brand batch, until JSON is correct.

**Risk:** Low if gated on upload success and tested on one workflow first.

### Cleanup debt (while you’re in Phase 2 / analytics code)

These **reconciliation bugs** can quietly distort trust in the analysis layer—fix when touching `correlate` / `analyze_data`:

- **`correlate`** reports mood **`study`** “missing” while weekly report tables show **study** videos — title-classification vs report column mismatch.
- **`analyze_data.py`** “best retention” summary line vs **by-type table** (e.g. lofi_study) — reconcile definitions or remove the misleading line.

### Historic videos and backfill

Videos published **before** `generations.json` exists have **no** joined params in the repo. For them, analysis continues to use **title parsing** (and description) unless you later:

- Accept **partial attribution** for the long tail, or
- Run an **optional one-time backfill** (e.g. align `video_id` with catalog exports, recovered sidecars, or a curated sheet). **Do not** block Phase 2 on backfill design—define schema and forward logging first; script the past when the format is stable.

### Phase 2 implementation notes (detail in the Phase 2 PR)

- **Concurrent writers:** Multiple CI jobs or local runs appending one shared JSON file invite **git merge conflicts**. Prefer a **single writer** (e.g. only the upload step on `main`), or **sharded files** / NDJSON merged in a dedicated step—decide when implementing **2b**.
- **Tests:** When implementing **2d** (correlate), add a minimal check: fixture **`analytics` + `generations`** → correlate uses **joined params** for a known **`video_id`** (harness shape left to that PR).

---

## Phase 3 — Catalog / library parity (strategic)

**Goal:** Decide what the **repo catalog** is for—then align workflows.

**Two valid models:**

| Model | Idea | Tradeoff |
|-------|------|----------|
| **A — Repo + catalog as audit trail** | Every upload path commits `content_catalog.json` / `CONTENT_LIBRARY.md` | Reproducibility ↑, friction ↑ |
| **B — YouTube as canonical inventory** | Channel = ground truth; repo = **generation + analysis** (`data/*`, code); catalog **optional or derived** | Faster, fewer merge commits; less “browse in git without API” |

**Recommendation:** **Default to B** for this codebase (production engine + analytics loop, not a CMS). **Revisit A** only if **audit / compliance** or “must browse inventory without YouTube API” becomes a hard requirement, or **after** `generations.json` + analytics join is stable and you still want git-mirrored publishing history. Hybrid remains valid (e.g. catalog commits on manual brand only).

| Step | Action |
|------|--------|
| 3a | **Choose A, B, or hybrid** — if undecided, **start with B** and document; add catalog commits later if needed. |
| 3b | If **A**: add the **same commit block** as manual [Content Factory (Brand)](../.github/workflows/content-factory-brand.yml) to **brand batch** after upload (post batch completion). If **B**: document that catalog commits are **optional** and how to regenerate if needed. |
| 3c | Declare **one canonical** human doc for library workflow (root vs `docs/` duplicates). |

---

## Phase 4 — Naming & honest ML line

| Step | Action |
|------|--------|
| 4a | Workflow step names / `correlate.py` header: **“statistical correlation”** vs **“ML”** where accurate. |
| 4b | Align **AGENT.md** phase thresholds (e.g. 100 vs 500 videos) with code comments. |
| 4c | Optional: dedupe **`parse_video_type`** / `parse_type` into one shared helper. |

---

## Phase 5 — Career / portfolio wording

| Step | Action |
|------|--------|
| 5a | README (or personal site): one paragraph — **data flywheel**, guardrails, phased automation, **human approval** before auto-queue. |
| 5b | Resume: **ingestion, structured metrics, correlation + gates, spec-driven CI** — accurate today. |

**Distinction:** [Master Plan](master-plan.md) **Milestone 8** = generative **melody** AI. Analytics **Phase 3–4** in [AGENT.md](spec/AGENT.md) = **predictive / optimization** — separate bullets in outward-facing text.

---

## Phase 6 — Future: “agent decides next step”

**Order (non-negotiable for safety):**

1. Workflow or script emits a **recommendation artifact** (markdown/JSON) from `data/*` — **no** auto-generation.
2. **`workflow_dispatch`** with suggested inputs — **human** runs.
3. Only later: optional auto-trigger with **caps**, **guardrails**, and **spec updates**.

**Two doors (keep both):** **(A)** Small manual **`workflow_dispatch`** on Content Factory workflows for smoke and hand-picked runs (fixed form fields). **(B) Precision path:** versioned **run intent JSON** — [`spec/contracts/production-run-intent.md`](spec/contracts/production-run-intent.md) — **validated in CI** then mapped to `batch_generate` / `youtube_upload` flags; a gated planner or future LLM emits **only** that shape (no ad-hoc shell, no unbounded growth of dropdown inputs). *Workflow reader:* [`run-intent-consumer.yml`](../.github/workflows/run-intent-consumer.yml) + [`scripts/consume_run_intent.py`](../scripts/consume_run_intent.py). **Planner v0:** [`scripts/plan_run_intent.py`](../scripts/plan_run_intent.py) (after brand correlate) writes intent or a **BLOCKED** report; execution is **manual** `workflow_dispatch` on the consumer workflow.

**Explainability:** Recommendations must cite **evidence** (e.g. “top retention cluster: `mood=X`, `tempo` band Y, *n*=…”) — not vague “make more calm stuff.” Otherwise you won’t trust the loop.

**Advisory `run-next` (near-term, explicit):** add a **weekly** markdown artifact (path TBD, e.g. `data/reports/run-next-YYYY-WW.md`) or a **dedicated section** in the weekly report — **ranked** “what to try next,” mixing **strong** and **weak** signals with clear labels (same spirit as **actionable** vs **exploratory** in correlate). This is **separate** from the **strict** automation gate (`data/run_intent.json` / `run-intent-blocked.md`): humans read `run-next` for strategy; they run Content Factory / consumer only when ready. **Packaging / algorithm surface:** it is normal to exploit **same-franchise + slight title/thumb variation** when that matches how the feed clusters content — **[`piano-batch.yml`](../.github/workflows/piano-batch.yml)** is a repo example (strategy informed by **personal**-lane read). Still document **confounders** ([`AGENT.md`](spec/AGENT.md) § *Confounders & packaging*); per-channel **dedup / positioning** when two channels would share identical display titles stays a **later** polish ([`HANDOFF.md`](HANDOFF.md) next actions **#8**).

**`run-next` implementation order (agreed):**

1. **v0 deterministic** — step in [`analytics-agent.yml`](../.github/workflows/analytics-agent.yml) after audit: [`scripts/run_next_report.py`](../scripts/run_next_report.py) emits `run-next-*.md` from structured data; commit with weekly data. **No** LLM; **no** `batch_generate` / upload.
2. **Validators** — CI or script checks: every claim traceable to `suggestions.json` / audit; numeric parity; fail the step on drift.
3. **Optional LLM prose** — only after (1)(2) are boring: model consumes **fixed JSON bundle** + prompt from git; output still schema-validated. **Preferred:** open-weight on **self-hosted** runner or hardware you control (**MLOps / AI-ops**, no third-party inference). **Optional prototype:** vendor API (e.g. Gemini free tier) for speed **only** until a local path exists; document in `workflows.md` + secrets policy.
4. **Automation** — optional `workflow_run` / scheduled consumer, richer `run_intent`, etc., **only** after `run-next` is trusted; keep Phase 6 steps **2–3** (human dispatch → later caps).

---

## Versioning this project

| Layer | Suggestion |
|-------|------------|
| **Git** | Tags on `main`: e.g. `v2026.1.0` at milestones (“post–brand-batch cohesion”, “generations wired”). |
| **Changelog** | `CHANGELOG.md` — short **Added / Changed / Fixed** per tag. |
| **Data** | Bump **`schema_version`** in `generations.json` / related files when fields change ([AGENT.md](spec/AGENT.md)). |
| **Story** | Optional narrative “Engine v1 = batch + publish; v2 = joined analytics; v3 = recommendations” separate from semver. |

---

## Suggested order of next moves

1. **Phase 0:** Finish brand batch; don’t touch batch workflow until stable.  
2. **Immediately after:** Phase **2a–2b** — implement **`video_id` ↔ metadata** (`generations.json` + one logging path). This is the **first** code priority; Phase 1 narrative can run in parallel but must not block 2 for long.  
3. **Phase 2c** — **CI persistence** of `generations.json` on `main` (see [workflows.md](spec/workflows.md) § Generations ledger; [ADR 0001](decisions/0001-persist-generations-json-on-ci.md)).  
4. **Phase 2d** (correlate) + **2e** (2.5 stats + disclaimers) + lock **AGENT.md** schema (“data constitution”). Treat **2f** (packaging hashes) as a separate scheduling decision when CTR automation matters.  
5. **Phase 3** — confirm **B** (or A/hybrid) per section above.  
6. **Polish:** Phases **4–5**; Phase **6** when joins feel trustworthy.

**Stripped execution (first code sprint):** (1) minimal `generations.json` + `schema_version` + **`generation_id`** per run; (2) upload path **creates** row then **updates** `video_id` on success / retry; (3) workflows **commit** `data/generations.json` to `main`; (4) test on **manual** brand workflow; (5) correlate: join by `video_id` → title fallback; (6) Phase **2.5** + **confounder** language before trusting suggestions at scale ([AGENT.md](spec/AGENT.md)).

**Status on `main` (2026-04):** (1)–(4) **landed** (see [ADR 0001](decisions/0001-persist-generations-json-on-ci.md)); (5) **evolving** — `correlate.py` uses **dual engagement** metrics (retention + watch minutes); **catalog backfill** added ledger rows for historic **`content_catalog.json`** uploads; **brand-only** `analytics.json` vs **mixed** catalog is documented in [`START_HERE.md`](START_HERE.md). **Personal** snapshots: `analytics-personal.yml` → `analytics_personal.json` + `*-personal.md` ([`PERSONAL_ANALYTICS.md`](PERSONAL_ANALYTICS.md)). **Catalog `channel`:** new CI catalog rows carry optional **`channel`** (`brand` / `personal`) per [ADR 0002](decisions/0002-content-catalog-channel-field.md) once merged; historic rows may omit the field — optional backfill / audit filtering. **Next:** post-merge spot-check `channel` on upload paths; optional personal correlate/suggestions; **later** multi-channel **profile template** ([`HANDOFF.md`](HANDOFF.md), [`START_HERE`](START_HERE.md) checklist). Remaining: **Phase 2.5 + confounder language** ([AGENT.md](spec/AGENT.md)), **packaging fingerprints** before CTR-heavy automation, optional **gated production plan** before Phase 6 auto-trigger.

---

## Related paths

- **Doc map (start here):** [`START_HERE.md`](START_HERE.md) — where each kind of truth lives; **ADRs:** [`decisions/`](decisions/)
- Execution policy (venv + CI): [`EXECUTION.md`](EXECUTION.md)
- Personal channel (separate analytics plan): [`PERSONAL_ANALYTICS.md`](PERSONAL_ANALYTICS.md)
- Workflows: [.github/workflows/](../.github/workflows/)
- Analytics code: [`agent/`](../agent/), [`scripts/analyze_data.py`](../scripts/analyze_data.py), [`scripts/correlate.py`](../scripts/correlate.py)
- Generation spine: [`orchestrator/orchestrator.py`](../orchestrator/orchestrator.py), [`batch_generate.py`](../batch_generate.py)

---

*Last updated: 2026-04-16 — living document; adjust phases as the channel and codebase evolve.*
