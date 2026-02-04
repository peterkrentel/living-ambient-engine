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

## test-art-creator.yml

### Purpose

Tests all input combinations for `art-creator.yml` by triggering it via `workflow_call`.

**Three modes:**
1. **Schedule** - Daily cron run with pattern rotation and uploads (respects 10 uploads/24hr limit)
2. **PR** - All 7 patterns in parallel, 5-second videos, no upload
3. **Manual** - Configurable pattern set, duration, and upload

### Trigger

```yaml
schedule:
  - cron: '0 3 * * *'  # Daily 3AM UTC - rotates pattern sets
workflow_dispatch:      # Manual trigger with options
pull_request:          # Auto-trigger on workflow/core code changes
  paths:
    - '.github/workflows/art-creator.yml'
    - '.github/workflows/test-art-creator.yml'
    - 'audio/**'
    - 'visuals/**'
    - 'orchestrator/**'
    - 'config/**'
    - 'render/**'
```

### Inputs (Manual)

| Input | Type | Default | Valid Values | Description |
|-------|------|---------|--------------|-------------|
| `pattern_set` | choice | `auto` | `auto`, `all`, `set1`, `set2`, `set3` | Pattern subset to test |
| `duration` | choice | `5s` | `5s`, `5min`, `10min` | Video duration |
| `upload_to_brand` | boolean | `false` | `true`, `false` | Upload to Brand YouTube |
| `reason` | string | - | - | Test run description |

### Pattern Rotation Strategy

Scheduled runs rotate through pattern subsets to stay under YouTube upload quota:

| Day(s) | Pattern Set | Test IDs | Upload Count |
|--------|-------------|----------|--------------|
| Mon, Thu, Sun | `set1` | 1-3 | 3 videos |
| Tue, Fri | `set2` | 4-5 | 2 videos |
| Wed, Sat | `set3` | 6-7 | 2 videos |

**Rationale:** Max 3 videos/day << 10 uploads/24hr quota limit

See: [docs/CRON_PATTERN_TESTING.md](../CRON_PATTERN_TESTING.md) for detailed schedule

### Job Sequence

```text
spec-validation → contract-tests → determine-pattern-set → call-art-creator (filtered matrix)
```

1. **spec-validation** - Validates specs exist and are consistent
2. **contract-tests** - Runs `tests/contracts/test_validation_contract.py`
3. **determine-pattern-set** - Decides which patterns to run based on trigger type and inputs
4. **call-art-creator** - Calls art-creator.yml with filtered matrix items

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

Parameters vary by trigger type:

**PR runs (validation):**
- `pattern_set: 'all'` - All 7 patterns
- `duration: '5s'` - Minimum per GUARDRAILS.md
- `skip_artifact_upload: 'true'` - No artifact storage
- `upload: false` - No YouTube upload

**Scheduled runs (production testing):**
- `pattern_set: auto` - Rotates by day (set1/set2/set3)
- `duration: '5min'` - Quality test video
- `skip_artifact_upload: 'false'` - Save artifacts
- `upload: true` - Upload to Brand YouTube

**Manual runs:**
- Configurable via workflow_dispatch inputs
- `test_id: ${{ matrix.test_id }}` - **Required for parallel execution**

### Outputs

**PR runs:**
- No artifacts saved
- No YouTube upload
- Failure in any test case blocks PR merge

**Scheduled/Manual with upload:**
- Artifacts saved (7-day retention)
- Videos uploaded to Brand YouTube channel
- Catalog updates committed

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

