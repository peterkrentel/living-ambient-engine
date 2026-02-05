# GitHub Workflows Specification

> **Owner:** `.github/workflows/` directory
> **Canonical Spec:** [SYSTEM.md](./SYSTEM.md)
> **Contract Version:** 1.0

## Overview

Four workflows automate video generation, YouTube deployment, and testing.

**Each workflow YAML file MUST include a spec reference comment:**

```yaml
# Spec: docs/spec/workflows.md#workflow-name
```

## Workflow Index

| ID | Workflow | Trigger | Purpose | Channel |
|----|----------|---------|---------|---------|
| WF-CF | `content-factory.yml` | Schedule + Manual | Batch generation + upload | Personal |
| WF-CFB | `content-factory-brand.yml` | Manual only | Batch generation + upload | Brand |
| WF-ART | `art-creator.yml` | Manual / workflow_call | Single custom video | Brand (optional) |
| WF-BATCH | `art-creator-batch.yml` | Schedule + Manual | Daily matrix generation | Brand |
| WF-TEST | `test-art-creator.yml` | Manual + PR (path filter) | Test all input combinations | None (test only) |

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
| `content-factory.yml` | write | - | Catalog commit |
| `content-factory-brand.yml` | write | - | Catalog commit |
| `art-creator.yml` | write | - | Catalog commit |
| `test-art-creator.yml` | read | read | Read-only tests |

## content-factory.yml

### Trigger

```yaml
schedule:
  - cron: '0 2 * * *'  # Daily 2AM UTC
workflow_dispatch:      # Manual trigger
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

## content-factory-brand.yml

Same as `content-factory.yml` except:

| Difference | content-factory | content-factory-brand |
|------------|-----------------|----------------------|
| Trigger | Schedule + Manual | **Manual only** |
| Secret | `YOUTUBE_TOKEN_PICKLE` | `YOUTUBE_TOKEN_PICKLE_BRAND` |
| Channel | Personal | Brand |
| Concurrency group | `content-factory` | `content-factory-brand` |

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

```yaml
permissions:
  contents: write  # Required for catalog commit
```

## art-creator-batch.yml

### Purpose

Scheduled batch generation that systematically covers all art_period × music_style combinations.
Runs daily, generating 3 videos (5 min each), uploading to brand channel.

**Full matrix coverage:** 8 art periods × 9 music styles = 72 combinations over ~24 days.

### Trigger

```yaml
schedule:
  - cron: '0 6 * * *'  # Daily at 6 AM UTC
workflow_dispatch:      # Manual with day override
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
| `day_override` | string | '' | Override day of week (0-7, 0=Sunday) |
| `dry_run` | boolean | `false` | Generate but don't upload |

### Daily Rotation Schedule

| Day | Art Period | Music Styles |
|-----|------------|--------------|
| 0 (Sun) | modern | gnawa, taiko, gamelan |
| 1 (Mon) | renaissance | burundi, kuku, candomble |
| 2 (Tue) | baroque | bamboula, heartbeat, none |
| 3 (Wed) | impressionist | gnawa, taiko, gamelan |
| 4 (Thu) | cave_art | burundi, kuku, candomble |
| 5 (Fri) | ancient | bamboula, heartbeat, none |
| 6 (Sat) | medieval | gnawa, taiko, gamelan |
| 7 | future | burundi, kuku, candomble |

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
    - '.github/workflows/art-creator.yml'
    - '.github/workflows/test-art-creator.yml'
    - 'audio/**'
    - 'visuals/**'
    - 'orchestrator/**'
    - 'config/**'
    - 'render/**'
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
2. Call `python youtube_upload.py --batch <directory>`
3. NOT generate title/description/tags inline in workflow YAML

**Rationale:** Single source of truth for SEO optimization. Tags and descriptions are defined in `moods.yaml` and flow through the pipeline:

```
moods.yaml → orchestrator → metadata.json → youtube_upload.py → YouTube
```

**Enforcement:**
- Contract test: `tests/contracts/test_workflow_metadata_consistency.py`
- See: [GUARDRAILS.md](./GUARDRAILS.md) § Metadata Consistency Violations
- See: [orchestrator-youtube.md](./contracts/orchestrator-youtube.md) § Workflow Integration

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

