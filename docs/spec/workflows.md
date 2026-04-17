# GitHub Workflows Specification

> **Owner:** `.github/workflows/` directory
> **Canonical Spec:** [SYSTEM.md](./SYSTEM.md)
> **Contract Version:** 1.0

## Overview

Nine workflow files automate video generation, YouTube deployment, analytics, and testing. Use the **Workflow Index** below as the map; YAML is the source of truth when this table drifts.

**Each workflow YAML file MUST include a spec reference comment:**

```yaml
# Spec: docs/spec/workflows.md#workflow-name
```

## Workflow Index

| ID | Workflow | Trigger | Purpose | Channel |
|----|----------|---------|---------|---------|
| WF-CF | `content-factory.yml` | Manual (cron **commented out** in YAML; strategy TBD) | Batch generation + upload | Personal |
| WF-CFB | `content-factory-brand.yml` | Manual only | Batch generation + upload | Brand |
| WF-CFBATCH | `content-factory-brand-batch.yml` | Manual (+ optional schedule) | Mood rotation (SEO; cron may be off) | Brand |
| WF-ART | `art-creator.yml` | Manual / workflow_call | Single custom video | Brand (optional) |
| WF-BATCH | `art-creator-batch.yml` | Manual (+ optional schedule) | Matrix generation (cron may be off) | Brand |
| WF-PIANO | `piano-batch.yml` | Manual only | Batch piano videos + upload | Brand |
| WF-TEST | `test-art-creator.yml` | Manual + PR (path filter) | CI: spec validation + contract tests + 7× `art-creator` matrix (no production upload) | None |
| WF-AGENT | `analytics-agent.yml` | Schedule (weekly) + Manual | Fetch YouTube stats, reports, correlate, channel audit | Brand |
| WF-AGENT-P | `analytics-personal.yml` | Schedule (weekly) + Manual | Fetch personal stats + weekly `*-personal.md` report only | Personal |

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
| `piano-batch.yml` | write | - | Catalog + generations ledger commit |
| `art-creator.yml` | read (default); **upload** job sets `write` | read | Upload job pushes `data/generations.json` only |
| `test-art-creator.yml` | **write** | read | Must allow `art-creator.yml`’s **upload** job `contents: write` (GitHub validates reusable-workflow permissions at parse time; test matrix skips upload via inputs) |

### Generations ledger (`data/generations.json`)

[`youtube_upload.py`](../../youtube_upload.py) calls `record_generation_upload` after a successful upload. On GitHub Actions that update must be **committed and pushed** or the ledger stays empty on `main` and analytics audits show **0% join** to `analytics.json`.

| Workflow | When `data/generations.json` is committed |
|----------|-------------------------------------------|
| `content-factory.yml`, `content-factory-brand.yml`, `piano-batch.yml` | Same step as catalog: `git add` includes `data/generations.json` when present |
| `content-factory-brand-batch.yml` | Dedicated **Commit generations ledger** step after upload |
| `art-creator.yml` | **upload** job: `permissions.contents: write`, commit `data/generations.json` after upload (`--no-update-catalog` unchanged) |

**Push race on `main`:** After `git commit` and before `git push`, workflows that update the repo run `git pull --rebase origin main` so another job (analytics, another upload lane) advancing `main` does not cause a non-fast-forward rejection.

**Verify:** `python scripts/verify_ledger_catalog.py` — catalog `youtube_id` set must equal ledger `video_id` set; warns when no `Content Factory (Personal)` rows exist.

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
8. Run channel coverage audit (`scripts/audit_channel.py`) — read-only markdown from committed analytics; summarizes 14-mood and 9×9 art×music grid coverage plus generations ledger join stats (no API calls)
9. Commit and push data files — after `git commit`, run `git pull --rebase origin main` then `git push` so a concurrent push on `main` (e.g. the other analytics workflow) does not cause the job to fail

### Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Analytics data | `data/analytics.json` | YouTube performance metrics |
| Weekly report | `data/reports/YYYY-WW.md` | Human-readable summary |
| ML suggestions | `data/suggestions.json` | Bucket suggestions tagged by `metric` (`average_view_percentage` and/or `watch_time_minutes`); Step Summary lists both |
| Channel audit | `data/reports/audit-YYYY-WW.md` | Coverage vs target grids + ledger join share (CI-generated) |

### Secrets Required

| Secret | Purpose |
|--------|---------|
| `YOUTUBE_TOKEN_PICKLE` | YouTube API authentication |

### Guardrails

- **Rate limits:** Stop at 90% daily quota (9,000 units)
- **Data retention:** All data kept indefinitely in repo
- **Privacy:** No PII logged, no viewer data stored
- **Writes:** Only to `data/` directory

See: [GUARDRAILS.md](./GUARDRAILS.md) § Analytics Agent Guardrails

---

## analytics-personal.yml

**Purpose:** Same *family* of metrics as the brand fetcher, but as a **separate experiment**: personal OAuth only, `data/analytics_personal.json`, and reports named `data/reports/YYYY-WW-personal.md`. Does **not** run correlate, audit, or `suggestions.json` (those remain brand-scoped until explicitly parameterized).

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
| `analyze-personal` | Fetch with `--channel personal`, generate report with `ANALYTICS_CHANNEL=personal` |

### Outputs

| Output | Location |
|--------|----------|
| Analytics | `data/analytics_personal.json` |
| Weekly report | `data/reports/YYYY-WW-personal.md` |

### Secrets

| Secret | Purpose |
|--------|---------|
| `YOUTUBE_TOKEN_PICKLE` | Personal channel OAuth (same as Content Factory personal) |

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

