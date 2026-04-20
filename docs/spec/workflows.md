# GitHub Workflows Specification

> **Owner:** `.github/workflows/` directory
> **Canonical Spec:** [SYSTEM.md](./SYSTEM.md)
> **Contract Version:** 1.0

## Overview

Twelve workflow files automate video generation, YouTube deployment, analytics, and testing. Use the **Workflow Index** below as the map; YAML is the source of truth when this table drifts.

**Each workflow YAML file MUST include a spec reference comment:**

```yaml
# Spec: docs/spec/workflows.md#workflow-name
```

## Workflow Index

| ID | Workflow | Trigger | Purpose | Channel |
|----|----------|---------|---------|---------|
| WF-CF | `content-factory.yml` | Manual (cron **commented out** in YAML; strategy TBD) | Batch generation + upload | Personal |
| WF-CFLPB | `content-factory-personal-long-batch.yml` | Manual + schedule (daily 09:00 UTC; 6h runner cap) | 24×1h personal pressure batch; pick → generate → **upload on schedule** (dispatch upload gated by `upload`) | Personal |
| WF-CFB | `content-factory-brand.yml` | Manual only | Batch generation + upload | Brand |
| WF-CFBATCH | `content-factory-brand-batch.yml` | Manual (+ optional schedule) | Mood rotation (SEO; cron may be off) | Brand |
| WF-CFBMICRO | `content-factory-brand-micro-batch.yml` | Manual + schedule (daily 08:00 UTC) | 4× short brand/day + **upload on schedule** (like brand batch); dispatch `upload` for manual runs | Brand |
| WF-ART | `art-creator.yml` | Manual / workflow_call | Single custom video | Brand (optional) |
| WF-BATCH | `art-creator-batch.yml` | Manual (+ optional schedule) | Matrix generation (cron may be off) | Brand |
| WF-PIANO | `piano-batch.yml` | Manual only | Batch piano videos + upload | Brand |
| WF-TEST | `test-art-creator.yml` | Manual + PR (path filter) | CI: spec validation + contract tests + 7× `art-creator` matrix (no production upload) | None |
| WF-AGENT | `analytics-agent.yml` | Schedule (weekly) + Manual | Fetch YouTube stats, reports, correlate, **plan run intent**, channel audit, **`run-next` v0**, optional **dual LLM advisory** (Gemini API + runner GGUF via `scripts/agent_dual_advisory.py`) | Brand |
| WF-AGENT-P | `analytics-personal.yml` | Schedule (weekly) + Manual | Fetch personal stats + report + `analyze_data` + audit + correlate → `suggestions_personal.json` + **plan intent** (`run_intent_personal.json` / blocked) + `run-next-*-personal.md` + optional **dual LLM advisory** (never writes brand `suggestions.json`) | Personal |
| WF-RIC | `run-intent-consumer.yml` | Manual only | Validate intent JSON (default `data/run_intent.json`; personal: `data/run_intent_personal.json`) → `batch_generate` → optional gated `youtube_upload` (brand or personal per intent `channel`) | Brand or personal |

## Gating Rules

| Event | Required Checks | Blocks |
|-------|-----------------|--------|
| PR to `main` | All jobs in `Test Art Creator - All Combinations` workflow | Merge |
| Push to `main` | None (protected by PR) | N/A |
| Schedule | None | N/A (runs anyway) |
| Manual dispatch | None | N/A |

**PR check names as shown in GitHub UI:**

| Job ID | PR Check Name | Description |
|--------|---------------|-------------|
| `spec-validation` | `Test Art Creator - All Combinations / spec-validation` | Validates specs exist |
| `contract-tests` | `Test Art Creator - All Combinations / contract-tests` | Runs contract tests |
| `call-art-creator` | `Test Art Creator - All Combinations / call-art-creator (...)` | 7 matrix jobs |

**Matrix gating:** All 7 `call-art-creator` matrix jobs MUST pass. For matrix workflows, all matrix job variants MUST succeed for the workflow to be considered passing.

## Contract Enforcement

This spec is enforced at multiple levels:

| Level | Mechanism | What it catches |
|-------|-----------|-----------------|
| PR | Branch protection requires workflow green | Missing specs, broken contracts |
| CI | `spec-validation` job | Spec files missing, guardrails undocumented |
| Runtime | `clamp_to_guardrails()` | Invalid parameter values |

**Enforcement source of truth:** GitHub repository settings → Branches → `main` branch protection rules. This document describes the *intent*; the branch protection configuration is the *actual gate*.

**Policy:** If the spec and workflow disagree, the workflow MUST be changed or the spec MUST be updated in the same PR—never leave them diverged.

**When changing workflows:**

1. Update this contract (`docs/spec/workflows.md`) in the same PR
2. If adding inputs/outputs, add to the relevant section
3. If changing concurrency, update the Concurrency section
4. Run `test-art-creator.yml` to validate

## Permissions Summary

| Workflow | `contents` | `actions` | Why |
|----------|------------|-----------|-----|
| `content-factory.yml` | write | - | Catalog + generations ledger commit |
| `content-factory-brand.yml` | write | - | Catalog + generations ledger commit |
| `content-factory-brand-batch.yml` | write | read | Generations ledger commit after upload |
| `run-intent-consumer.yml` | write | - | Catalog + generations ledger commit after gated upload |
| `piano-batch.yml` | write | - | Catalog + generations ledger commit |
| `art-creator.yml` | read (default); **upload** job sets `write` | read | Upload job pushes `data/generations.json` only |
| `test-art-creator.yml` | **write** | read | Must allow `art-creator.yml`’s **upload** job `contents: write` (GitHub validates reusable-workflow permissions at parse time; test matrix skips upload via inputs) |

### Generations ledger (`data/generations.json`)

[`youtube_upload.py`](../../youtube_upload.py) calls `record_generation_upload` after a successful upload. On GitHub Actions that update must be **committed and pushed** or the ledger stays empty on `main` and analytics audits show **0% join** to `analytics.json`.

| Workflow | When `data/generations.json` is committed |
|----------|-------------------------------------------|
| `content-factory.yml`, `content-factory-brand.yml`, `piano-batch.yml` | Same step as catalog: `git add` includes `data/generations.json` when present |
| `content-factory-brand-batch.yml` | Dedicated **Commit generations ledger** step after upload |
| `run-intent-consumer.yml` | **upload** job: same pattern as Content Factory — catalog / `CONTENT_LIBRARY.md` / `data/generations.json` + `ci_merge_main_after_data_commit.sh` |
| `art-creator.yml` | **upload** job: `permissions.contents: write`, commit `data/generations.json` after upload (`--no-update-catalog` unchanged) |

**Push race on `main`:** After the automated data `git commit`, upload workflows run **`scripts/ci_merge_main_after_data_commit.sh`**: `git merge origin/main`, then `git push`. If the merge conflicts on **`content_catalog.json`**, **`data/generations.json`**, and/or **`CONTENT_LIBRARY.md`**, **`scripts/merge_data_snapshot_conflicts.py`** performs an append-style **union** (by `youtube_id` / `video_id`) and regenerates **`CONTENT_LIBRARY.md`** from the merged catalog so parallel lanes (e.g. personal + piano) do not fail the job on rebase conflicts.

**Verify:** `python scripts/verify_ledger_catalog.py` — catalog `youtube_id` set must equal ledger `video_id` set; warns when no `Content Factory (Personal)` rows exist.

**Precision runs:** Large or agent-driven matrices should use the **validated run intent** contract ([`contracts/production-run-intent.md`](./contracts/production-run-intent.md)) consumed by CI—not unbounded extra `workflow_dispatch` inputs alone. **Consumer:** [`run-intent-consumer.yml`](../../.github/workflows/run-intent-consumer.yml) (`workflow_dispatch`; optional `validate_only`).

## content-factory.yml

### Trigger

**As in repo today:** `schedule` is **commented out** (personal channel on hold). Only **`workflow_dispatch`** runs until cron is re-enabled in `.github/workflows/content-factory.yml`.

**When schedule is enabled**, the intended cron is:

```yaml
# schedule:
#   - cron: '0 2 * * *'  # Daily 2AM UTC
workflow_dispatch:      # Manual trigger (always)
```

### Concurrency

```yaml
concurrency:
  group: content-factory
  cancel-in-progress: false  # Never cancel long-running generation
```

### Inputs (Manual)

| Input | Type | Default | Valid Values | Description |
|-------|------|---------|--------------|-------------|
| `moods` | string | `rain_sleep,deep_focus,ocean_waves` | See CONTENT_LIBRARY.md | Comma-separated moods |
| `duration` | choice | `1h` | `30s`, `10min`, `1h`, `3h`, `4h` | Video duration |
| `dual` | boolean | `true` | `true`, `false` | Generate both ambience + melody versions |
| `upload` | boolean | `true` | `true`, `false` | Upload to YouTube |

### Secrets Required

| Secret | Purpose |
|--------|---------|
| `YOUTUBE_TOKEN_PICKLE` | Personal channel OAuth token |

### Permissions

```yaml
permissions:
  contents: write  # Required for catalog commit
```

### Outputs

- Video artifacts in `./generated/` (7-day retention)
- `manifest.json` with generation metadata
- Upload results in job summary
- `data/generations.json` updates committed with the catalog when uploads succeed (see **Generations ledger** above)

## content-factory-brand.yml

Same as `content-factory.yml` except:

| Difference | content-factory | content-factory-brand |
|------------|-----------------|----------------------|
| Trigger | **Manual** (personal cron **off** in YAML until re-enabled) | **Manual only** |
| Secret | `YOUTUBE_TOKEN_PICKLE` | `YOUTUBE_TOKEN_PICKLE_BRAND` |
| Channel | Personal | Brand |
| Concurrency group | `content-factory` | `content-factory-brand` |

## content-factory-brand-batch.yml

### Purpose

Scheduled batch generation that rotates through ALL 14 moods with SEO-optimized metadata.
Runs daily, generating 3 videos (5 min each), uploading to brand channel.

**Strategy: Human Search SEO**

Unlike art-creator-batch which uses parameter-based variety for algorithm discovery,
content-factory-batch uses **SEO-optimized metadata from moods.yaml** for human search discovery:

| Approach | Why It Works |
|----------|--------------|
| 14 SEO-optimized moods | Targets high-volume search queries ("focus music", "rain for sleep") |
| moods.yaml metadata | Carefully crafted titles, descriptions, tags |
| Full mood coverage | 3 moods/day = ~5 days for complete rotation |

**Full coverage:**
- 14 moods total
- 3 videos/day = **~5 days for complete coverage**

### Trigger

```yaml
# schedule may be commented out in the workflow file during audit / strategy pauses
schedule:
  - cron: '0 8 * * *'  # Daily at 8 AM UTC (when enabled)
workflow_dispatch:      # Manual with day override (always available)
```

### Concurrency

```yaml
concurrency:
  group: content-factory-batch
  cancel-in-progress: false
```

### Inputs (Manual)

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `day_override` | string | '' | Day number 0-13 (overrides auto-counter) |
| `dry_run` | boolean | `false` | Generate but don't upload |

### Rotation Logic

Each day generates 3 moods, rotating through all 14:

| Day | Moods |
|-----|-------|
| 0 | deep_focus, sleep, chill |
| 1 | study, energize, trance |
| 2 | ceremony, warrior, rain_sleep |
| 3 | fireplace, ocean_waves, lofi_study |
| 4 | piano_relax, forest_morning, deep_focus |

### Secrets Required

| Secret | Purpose |
|--------|---------|
| `YOUTUBE_TOKEN_PICKLE_BRAND` | Brand channel OAuth |
| `YOUTUBE_CLIENT_SECRETS` | OAuth client config |

### Permissions

```yaml
permissions:
  contents: write
```

## content-factory-brand-micro-batch.yml

**Purpose:** Brand **micro** batch v1: **20 short** videos (5s / 10s / 30s) from **`data/brand_micro_batch_v1.json`**, each slot bound to a **`micro_*`** mood in **`config/moods.yaml`**. **`pick`** → **`generate`** → **`upload`**. **Scheduled** runs (**08:00 UTC**) upload after successful generate (same spirit as **`content-factory-brand-batch.yml`** upload job: not blocked by a dispatch-only gate). **`workflow_dispatch`:** set **`upload`: true** (and not **`dry_run`**) to upload. **Daily mode** runs **4 slots per calendar day** (days 1–5) and advances **`next_day`** in the state file when **`advance_state`** applies. **`run_full_batch`** runs all 20 in one job (no state advance). **`pick`** skips when **`data/brand_micro_batch_state.json`** has **`completed: true`** until **`reset_state`**. Runner: **`scripts/run_brand_micro_batch.py`** → `./generated/manifest.json`; **`youtube_upload.py --batch ./generated --catalog-channel brand`**.

**Inputs:** `day_override` (1–5), `reset_state`, `run_full_batch`, `dry_run`, `upload`.

*Future:* declarative **template + vars** for moods (see [COHESION_ROADMAP.md](../COHESION_ROADMAP.md) § Mood config templates) — **not** required for this batch; current `micro_*` entries are static YAML.

## content-factory-personal-long-batch.yml

**Purpose:** Personal **long-form pressure** batch v1: **24×1h** videos from **`data/personal_long_batch_pressure_v1.json`** (moods **`piano_deep_calm`**, **`ceremony`**, **`energize`**, **`deep_focus`** only; slots **interleaved** 6/day × 4 days). **`pick`** → **`generate`** → **`upload`**. **Scheduled** runs (**09:00 UTC**, staggered vs brand micro) **upload** after successful generate. **`workflow_dispatch`:** **`upload`: true** (and not **`dry_run`**) to upload. **`pick`** skips when **`data/personal_long_batch_pressure_state.json`** has **`completed: true`** until **`reset_state`**. Runner: **`scripts/run_personal_long_batch.py`**; **`youtube_upload.py --batch ./generated --catalog-channel personal`**. **Title hooks** for the four moods: **`config/moods.yaml`** `title_template` only.

**Ops:** GitHub-hosted jobs are **capped at 6 hours**; six sequential **1h** renders often exceed that — prefer **local / self-hosted** or a larger runner when needed.

**Inputs:** `day_override` (1–4), `reset_state`, `run_full_batch`, `dry_run`, `upload` (required **true** on dispatch to upload; schedule uploads automatically when generation succeeds).

### Planned follow-ups (not in this workflow)

| Phase | Scope |
|-------|--------|
| **P1** | **Thumbnail differentiation:** post-render overlay or visual presets rotated per slot (today thumbnails are video frame grabs — see `render/renderer.py`). |
| **P2** | **`title_hook` / `title_override`:** first-phrase rotation or per-slot titles from batch JSON, logged in manifest for joins. |

## run-intent-consumer.yml

**Purpose:** Validate committed run intent JSON (defaults **`data/run_intent.json`** + blocked report **`data/reports/run-intent-blocked.md`**) against [`contracts/production-run-intent.md`](./contracts/production-run-intent.md) v1, then run **`batch_generate.py`** with the same flags Content Factory would use (`--moods`, `--durations`, optional `--dual`). Optionally upload via **`youtube_upload.py --batch`** with **`--catalog-channel`** set from intent `channel`. **Personal lane:** dispatch with **`intent_path`** = `data/run_intent_personal.json` and **`blocked_report_path`** = `data/reports/run-intent-blocked-personal.md` (pair produced by [`analytics-personal.yml`](../../.github/workflows/analytics-personal.yml)). **Planner v0** still commits **`upload`: false**; uploads require intent **`upload`: true** *and* dispatcher **`confirm_upload`** (double gate).

**Spec:** [`contracts/production-run-intent.md`](./contracts/production-run-intent.md) · Validator: [`scripts/consume_run_intent.py`](../../scripts/consume_run_intent.py)

### Trigger

```yaml
on:
  workflow_dispatch:
    inputs:
      validate_only: boolean   # default false — if true, only parse/validate + Step Summary
      confirm_upload: boolean  # default false — required (with intent.upload) to run upload job
      intent_path: string       # default data/run_intent.json — use data/run_intent_personal.json for personal lane
      blocked_report_path: string  # default data/reports/run-intent-blocked.md — pair with intent_path
```

When **`validate_only`** is true, `parse` passes **`--allow-planner-blocked`**: missing the chosen intent file but present the paired **`blocked_report_path`** exits **0** (expected after analytics gate) and writes a Step Summary — not a red failure. Full runs (generate) do **not** pass that flag: missing intent remains **exit 1**.

### Jobs

| Job | Purpose |
|-----|---------|
| `parse` | Checkout; `pip install pyyaml`; run `consume_run_intent.py --intent "$INTENT_PATH" --blocked-report "$BLOCKED_PATH" --emit-github-output` (adds **`--allow-planner-blocked`** when `validate_only`). Validates intent or records planner BLOCKED; sets outputs when intent exists. |
| `generate` | Skipped when `validate_only`; else FFmpeg + `requirements.txt`, `batch_generate.py`, artifact `run-intent-generated-{channel}`. |
| `upload` | Skipped unless `validate_only` is false **and** `confirm_upload` **and** `parse.outputs.upload == 'true'`; restores **brand** or **personal** OAuth secret by `channel`; `youtube_upload.py --batch ./generated --catalog-channel …`; commits catalog / ledger via `scripts/ci_merge_main_after_data_commit.sh`. |

### Secrets

| Secret | When |
|--------|------|
| `YOUTUBE_TOKEN_PICKLE_BRAND` | Upload job, `channel=brand` |
| `YOUTUBE_TOKEN_PICKLE` | Upload job, `channel=personal` |
| `YOUTUBE_CLIENT_SECRETS` | Upload job (both lanes) |

### Permissions

```yaml
permissions:
  contents: write
```

## art-creator.yml

### Trigger

```yaml
workflow_dispatch:  # Manual trigger
workflow_call:      # Called by test-art-creator.yml
```

### Concurrency

```yaml
concurrency:
  group: art-creator-${{ github.run_id }}-${{ inputs.test_id || 'manual' }}
  cancel-in-progress: false
```

**CRITICAL:** The concurrency group MUST include `test_id` when called from test-art-creator.yml.
This allows 7 parallel test jobs to run without cancelling each other.

**Example concurrency group values:**

| Scenario | Group Value |
|----------|-------------|
| Manual run (run_id=123) | `art-creator-123-manual` |
| Test matrix job 1 (run_id=456) | `art-creator-456-1` |
| Test matrix job 7 (run_id=456) | `art-creator-456-7` |

See: `tests/contracts/` for enforcement via `spec-validation` job.

### Input Categories

**Visual:**

- `art_period` - Historical style preset (see ART_CREATOR.md)
- `visual_pattern` - Pattern algorithm
- `visual_speed` - Animation speed (auto or 0.1-1.0)
- `visual_complexity` - Detail level (auto or 0.1-1.0)
- `color_palette` - Color preset or custom

**Audio:**

- `music_style` - Rhythm pattern
- `tempo` - BPM (auto or 40-120)
- `brainwave_frequency` - Binaural Hz
- `solfeggio_frequency` - Healing Hz
- `rhythm_volume` - Drum level
- `ambient_volume` - Drone level

**Journey:**

- `journey` - Dynamic evolution preset
- `journey_intensity` - Variation magnitude

**Generation:**

- `duration` - Video length (5s-4h per GUARDRAILS.md)
- `seed` - Reproducibility seed
- `title` - Custom title
- `upload_to_brand` - Upload toggle
- `test_id` - **Required for parallel tests** (passed by test-art-creator.yml)
- `skip_artifact_upload` - Skip artifact upload (for tests)

### Secrets Required

| Secret | Purpose |
|--------|---------|
| `YOUTUBE_TOKEN_PICKLE_BRAND` | Brand channel OAuth (if uploading) |

### Permissions

Workflow default (tight):

```yaml
permissions:
  contents: read
  actions: read
```

The **`upload`** job (when `upload_to_brand` is true) sets `permissions: contents: write` so it can push **`data/generations.json`** after `youtube_upload.py` runs with `--no-update-catalog` (no catalog commit from this workflow).

## art-creator-batch.yml

### Purpose

Scheduled batch generation that systematically covers ALL parameter combinations.
Runs daily, generating 3 videos (5 min each), uploading to brand channel.

**Strategy: Algorithm Discovery (not human search SEO)**

Unlike content-factory-brand which targets human search queries ("focus music", "rain for sleep"),
art-creator-batch uses a **volume/variety strategy** for YouTube algorithm discovery:

| Approach | Why It Works |
|----------|--------------|
| 81 unique title combinations | More videos = more chances for algorithm recommendation |
| Distinct art_period × music_style pairs | Each combo attracts different audience segments |
| Parameter-based titles | Variety signals fresh content to algorithm |
| Never-repeating content | Algorithm favors unique over duplicate |

**Title format:** `"Ambient {art_period} | {duration_str} | Evolving {music_style} Soundscape"`

This is intentionally different from moods.yaml SEO templates. The goal is casting a wide net
for algorithm discovery, not optimizing individual titles for human search.

**Full matrix coverage:**
- 9 art_periods × 9 music_styles = 81 unique title combinations
- 3 videos/day = **27 days for complete coverage**
- Also rotates: visual_pattern (14), color_palette (10), journey (7), solfeggio (9)

### Trigger

```yaml
# schedule may be commented out in the workflow file during audit / strategy pauses
schedule:
  - cron: '0 6 * * *'  # Daily at 6 AM UTC (when enabled)
workflow_dispatch:      # Manual with day override (always available)
```

### Concurrency

```yaml
concurrency:
  group: art-creator-batch
  cancel-in-progress: false
```

### Inputs (Manual)

| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `day_override` | string | '' | Day number 0-80 (overrides auto-counter) |
| `dry_run` | boolean | `false` | Generate but don't upload |

### Rotation Logic

Each video gets a **unique art_period × music_style combination** (no duplicate titles).

| Parameter | Options | Rotation |
|-----------|---------|----------|
| art_period | 9 | Sequential through 81 combos |
| music_style | 9 | Sequential through 81 combos |
| visual_pattern | 14 | Cycles every 14 videos |
| color_palette | 10 | Cycles every 10 videos |
| journey | 7 | Cycles every 7 videos |
| solfeggio | 9 | Cycles every 9 videos |

Day counter uses days since epoch (mod 81) for consistent sequencing across runs.

### Job Sequence

```text
schedule → generate-1, generate-2, generate-3 (parallel) → summary
```

### Secrets Required

| Secret | Purpose |
|--------|---------|
| `YOUTUBE_TOKEN_PICKLE_BRAND` | Brand channel OAuth |

### Permissions

```yaml
permissions:
  contents: write
```

## test-art-creator.yml

### Purpose

Tests all input combinations for `art-creator.yml` by triggering it via `workflow_call`.
Runs 7 test cases **in parallel** with 5-second videos (minimum per GUARDRAILS.md).

### Trigger

```yaml
workflow_dispatch:  # Manual trigger
pull_request:       # Auto-trigger on workflow/core code changes
  paths:
    - '.github/workflows/**'   # Any workflow edit (not only art-creator / content-factory)
    - 'audio/**'
    - 'visuals/**'
    - 'orchestrator/**'
    - 'config/**'
    - 'render/**'
    - 'youtube_upload.py'
    - 'youtube/**'
    - 'tests/contracts/**'
    - 'docs/spec/**'
```

### Job Sequence

```text
spec-validation → contract-tests → call-art-creator (7 parallel jobs)
```

1. **spec-validation** - Validates specs exist and are consistent
2. **contract-tests** - Runs `tests/contracts/test_validation_contract.py`
3. **call-art-creator** - Calls art-creator.yml 7 times with matrix inputs

### Test Matrix Coverage

| Test | Art Period | Pattern | Journey | Intensity |
|------|------------|---------|---------|-----------|
| 1 | cave_art | organic_flow | awakening | subtle |
| 2 | renaissance | fibonacci_spiral | breathing | moderate |
| 3 | modern | geometric_morph | trance | dramatic |
| 4 | future | starfield | deep_dive | moderate |
| 5 | impressionist | flowing_waves | waves | subtle |
| 6 | baroque | julia | crescendo | dramatic |
| 7 | medieval | sacred_geometry | steady | moderate |

### Test Parameters

All 7 jobs use:

- `duration: '5s'` - Minimum per GUARDRAILS.md
- `skip_artifact_upload: 'true'` - No artifact storage
- `test_id: ${{ matrix.test_id }}` - **Required for parallel execution**

### Outputs

- No artifacts saved
- No YouTube upload
- Failure in any test case blocks PR merge

## Invariants

1. **All workflows exit non-zero on failure** - CI/CD compatibility
2. **Artifacts always saved** - Even if upload fails
3. **Idempotent uploads** - Re-runs don't create duplicates
4. **Quota awareness** - Graceful handling of API limits
5. **Metadata consistency** - ALL uploads use `youtube_upload.py` with `metadata.json`

### Metadata Consistency Rule

**MANDATORY:** All workflows that upload to YouTube MUST:

1. Generate `metadata.json` via orchestrator (or compatible generator)
2. Call `python youtube_upload.py --batch <directory>` — CI factory workflows pass **`--catalog-channel personal`** or **`--catalog-channel brand`** so new `content_catalog.json` rows are tagged ([ADR 0002](../decisions/0002-content-catalog-channel-field.md))
3. NOT generate title/description/tags inline in workflow YAML

**Rationale:** Single source of truth for SEO optimization. Tags and descriptions are defined in `moods.yaml` and flow through the pipeline:

```
moods.yaml → orchestrator → metadata.json → youtube_upload.py → YouTube
```

**Exception: art-creator.yml / art-creator-batch.yml**

These workflows use parameter-based metadata generation (not moods.yaml) intentionally.
See [GUARDRAILS.md](./GUARDRAILS.md) § Metadata Consistency Violations for rationale.

**Enforcement:**
- Contract test: `tests/contracts/test_workflow_metadata_consistency.py`
- See: [GUARDRAILS.md](./GUARDRAILS.md) § Metadata Consistency Violations
- See: [orchestrator-youtube.md](./contracts/orchestrator-youtube.md) § Workflow Integration

## analytics-agent.yml

**Purpose:** Fetch YouTube Analytics data and generate performance reports.

**Spec:** [AGENT.md](./AGENT.md)

### Trigger

```yaml
on:
  schedule:
    - cron: '0 0 * * 0'  # Every Sunday at midnight UTC
  workflow_dispatch: {}   # Manual trigger
```

### Jobs

| Job | Purpose | Depends On |
|-----|---------|------------|
| `analyze` | Fetch analytics + generate report | None |

### Job: analyze

**Steps:**

1. Checkout repository
2. Setup Python 3.11
3. Install dependencies (`pip install -r requirements.txt`)
4. Fetch YouTube Analytics (`python -m agent.fetch_analytics`)
5. Generate weekly report (`python -m agent.report`)
6. Run performance analysis (`scripts/analyze_data.py`)
7. Run ML correlation (`scripts/correlate.py`) — suggests bucket-level **increase/reduce** using **retention %** and **watch minutes per video** (in the fetch window); see [AGENT.md](./AGENT.md) Phase 2
8. Plan run intent (`scripts/plan_run_intent.py`) — gated v0: writes `data/run_intent.json` when actionable **mood** increases exist, else `data/reports/run-intent-blocked.md`; **`upload` defaults false**; execution is **manual** via [`run-intent-consumer.yml`](../../.github/workflows/run-intent-consumer.yml); see [`contracts/production-run-intent.md`](./contracts/production-run-intent.md)
9. Run channel coverage audit (`scripts/audit_channel.py`) — read-only markdown from committed analytics; summarizes 14-mood and 9×9 art×music grid coverage plus generations ledger join stats (no API calls)
10. Write **`run-next`** advisory (`scripts/run_next_report.py`) — deterministic markdown from **`suggestions.json`** + **`audit-YYYY-WW.md`** + optional personal-lane pointers (**no** LLM, **no** `batch_generate` / upload); same ISO week label as the brand audit
11. **Cache runner GGUF** — `actions/cache` on `~/.cache/living-agent` (default Qwen2.5-1.5B Instruct q4 GGUF path used by the script; cache key bumps when the default model file changes)
12. **Dual LLM advisory (optional v0):** `pip install llama-cpp-python`, then **`scripts/agent_dual_advisory.py --lane brand`** with the same ISO week as step 10. The script runs **Gemini (REST)** on the **full** bundle and **runner GGUF** on a **lean** bundle (run-next + compact suggestions/analytics + short reports) in **parallel threads**, writing `agent-insight-YYYY-WW-brand-gemini.md` and `agent-insight-YYYY-WW-brand-runner.md`. Job logs: expand the **Dual advisory** group; runner-side lines use prefix **`[runner-advisory]`** (bundle size estimate, `n_ctx`, load/inference timing). If `GEMINI_API_KEY` is unset, Gemini output is a short stub; if `llama-cpp-python` is missing, runner output is a stub (CI installs it).
13. Commit and push data files — after `git commit`, run `git pull --rebase origin main` then `git push` so a concurrent push on `main` (e.g. the other analytics workflow) does not cause the job to fail

**Roadmap (same week family):** **validators** (cited indices, numeric parity with JSON); richer **self-hosted** options later; **automation** only after outputs are trusted — [`COHESION_ROADMAP.md`](../COHESION_ROADMAP.md) Phase 6 · [`HANDOFF.md`](../HANDOFF.md). **Shipped (prototype):** dual advisory (Gemini API + runner GGUF on GitHub-hosted runners for comparison; default Qwen2.5-1.5B Instruct q4).

### Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Analytics data | `data/analytics.json` | YouTube performance metrics |
| Weekly report | `data/reports/YYYY-WW.md` | Human-readable summary |
| ML suggestions | `data/suggestions.json` | Bucket suggestions tagged by `metric` (`average_view_percentage` and/or `watch_time_minutes`); Step Summary lists both |
| Run intent (v0) | `data/run_intent.json` **or** `data/reports/run-intent-blocked.md` | Planner output; committed when present (intent often absent until gates pass) |
| Run-next (v0) | `data/reports/run-next-YYYY-WW.md` | Advisory “what next” from correlate + brand audit + personal pointers; validators / LLM layers tracked in roadmap above |
| Gemini advisory (v0) | `data/reports/agent-insight-YYYY-WW-brand-gemini.md` | API prose on the fixed bundle; stub if no `GEMINI_API_KEY` |
| Runner GGUF advisory (v0) | `data/reports/agent-insight-YYYY-WW-brand-runner.md` | Instruct GGUF on the workflow runner (default Qwen2.5-1.5B q4 path); stub if `llama-cpp-python` / model missing |
| Channel audit | `data/reports/audit-YYYY-WW.md` | Coverage vs target grids + ledger join share (CI-generated) |

### Secrets Required

| Secret | Purpose |
|--------|---------|
| `YOUTUBE_TOKEN_PICKLE_BRAND` | YouTube API authentication (brand token pickle) |
| `GEMINI_API_KEY` | Optional — enables Gemini half of dual advisory; omit for Gemini stub |

**Repository Variable (optional):** `GEMINI_MODEL` — set under *Settings → Secrets and variables → Actions → Variables*; both analytics workflows pass it as `env.GEMINI_MODEL`. When empty, [`agent_dual_advisory.py`](../../scripts/agent_dual_advisory.py) uses its built-in default.

**Optional env (runner GGUF, workflow or runner config):** `AGENT_GGUF_PATH`, `AGENT_GGUF_URL` (default Hugging Face Qwen2.5-1.5B Instruct q4), `AGENT_LLAMA_THREADS`.

### Guardrails

- **Rate limits:** Stop at 90% daily quota (9,000 units)
- **Data retention:** All data kept indefinitely in repo
- **Privacy:** No PII logged, no viewer data stored
- **Writes:** Only to `data/` directory

See: [GUARDRAILS.md](./GUARDRAILS.md) § Analytics Agent Guardrails

---

## analytics-personal.yml

**Purpose:** Same *family* of metrics as the brand fetcher, but as a **separate experiment**: personal OAuth only, `data/analytics_personal.json`, reports named `data/reports/YYYY-WW-personal.md`, and **`scripts/audit_channel.py`** with `ANALYTICS_JSON_PATH` / `ANALYTICS_CHANNEL=personal` / `ANALYTICS_REPORT_SUFFIX=-personal` → `data/reports/audit-YYYY-WW-personal.md`. Then **`scripts/correlate.py`** with `ANALYTICS_JSON_PATH` + **`SUGGESTIONS_JSON_PATH=data/suggestions_personal.json`** (never overwrites brand `data/suggestions.json`), then **`scripts/run_next_report.py --lane personal`** → `data/reports/run-next-YYYY-WW-personal.md`.

**Spec:** [PERSONAL_ANALYTICS.md](../PERSONAL_ANALYTICS.md), [AGENT.md](./AGENT.md)

### Trigger

```yaml
on:
  schedule:
    - cron: '0 2 * * 1'   # Monday 02:00 UTC (offset from brand Sunday run)
  workflow_dispatch: {}
```

### Jobs

| Job | Purpose |
|-----|---------|
| `analyze-personal` | Fetch with `--channel personal`, report + analyze + audit + correlate + plan intent + run-next (env-scoped paths) |

### Job: analyze-personal — steps (ordered)

1. Checkout
2. Setup Python + install deps
3. Fetch analytics (`python -m agent.fetch_analytics --channel personal`)
4. Weekly report (`python -m agent.report` with `ANALYTICS_JSON_PATH` / `ANALYTICS_CHANNEL` / `ANALYTICS_REPORT_SUFFIX`)
5. Performance analysis (`scripts/analyze_data.py` with `ANALYTICS_JSON_PATH=data/analytics_personal.json`)
6. Channel audit (`scripts/audit_channel.py` with same env as report)
7. ML correlation (`scripts/correlate.py` with `ANALYTICS_JSON_PATH` + `SUGGESTIONS_JSON_PATH=data/suggestions_personal.json`)
8. Plan run intent (`scripts/plan_run_intent.py` with `--suggestions data/suggestions_personal.json`, `--channel personal`, `--intent-output data/run_intent_personal.json`, `--blocked-output data/reports/run-intent-blocked-personal.md`)
9. Run-next advisory personal (`scripts/run_next_report.py --lane personal`)
10. **Cache runner GGUF** — same cache key family as brand (`~/.cache/living-agent`)
11. **Dual LLM advisory personal:** `pip install llama-cpp-python` + `scripts/agent_dual_advisory.py --lane personal` → `agent-insight-YYYY-WW-personal-gemini.md` and `agent-insight-YYYY-WW-personal-runner.md` (Gemini full bundle + runner lean bundle in parallel; logs **`[runner-advisory]`** in the folded **Dual advisory** group)
12. Commit + push (`git pull --rebase origin main` before `git push`; `git add` includes `agent-insight-*-personal-*.md` in addition to `*-personal.md`)

### Outputs

| Output | Location |
|--------|----------|
| Analytics | `data/analytics_personal.json` |
| Weekly report | `data/reports/YYYY-WW-personal.md` |
| Channel audit | `data/reports/audit-YYYY-WW-personal.md` |
| ML suggestions (personal) | `data/suggestions_personal.json` |
| Run intent (personal v0) | `data/run_intent_personal.json` **or** `data/reports/run-intent-blocked-personal.md` |
| Run-next (personal v0) | `data/reports/run-next-YYYY-WW-personal.md` |
| Gemini advisory (personal v0) | `data/reports/agent-insight-YYYY-WW-personal-gemini.md` |
| Runner GGUF advisory (personal v0) | `data/reports/agent-insight-YYYY-WW-personal-runner.md` |

### Secrets

| Secret | Purpose |
|--------|---------|
| `YOUTUBE_TOKEN_PICKLE` | Personal channel OAuth (same as Content Factory personal) |
| `GEMINI_API_KEY` | Optional — Gemini half of dual advisory; omit for Gemini stub |

**Repository Variable (optional):** `GEMINI_MODEL` — same as brand analytics (Actions Variables → `env.GEMINI_MODEL`).

**Guardrail:** This workflow must **not** set `YOUTUBE_TOKEN_PICKLE_BRAND`, so `fetch_analytics` never picks the brand token for personal runs.

---

## Adding a New Workflow Input

1. Add input definition in `workflow_dispatch.inputs`
2. Wire to environment variable in job
3. Pass through to Python config generation
4. Update this spec
5. Update `docs/ART_CREATOR.md` if user-facing

## Testing Workflows

```bash
# Local simulation (won't upload)
python run_job.py --mood trance --duration 30

# Trigger workflow manually via GitHub UI
# Actions → Select workflow → Run workflow
```

## Workflow Environment

| Variable | Value |
|----------|-------|
| Runner | `ubuntu-latest` |
| Python | `3.11` |
| FFmpeg | Pre-installed |

## Security Notes

- Secrets are masked in logs
- Token pickes are base64 encoded in secrets
- Never echo secrets or write to artifacts

