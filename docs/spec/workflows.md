# GitHub Workflows Specification

> **Owner:** `.github/workflows/` directory
> **Canonical Spec:** [SYSTEM.md](./SYSTEM.md)

## Overview

Four workflows automate video generation, YouTube deployment, and testing.

## Workflow Index

| Workflow | Trigger | Purpose | Channel |
|----------|---------|---------|---------|
| `content-factory.yml` | Schedule + Manual | Batch generation + upload | Personal |
| `content-factory-brand.yml` | Manual | Batch generation + upload | Brand |
| `art-creator.yml` | Manual / workflow_call | Single custom video | Brand (optional) |
| `test-art-creator.yml` | Manual | Test all input combinations | None (artifacts only) |

## content-factory.yml

### Trigger
```yaml
schedule:
  - cron: '0 2 * * *'  # Daily 2AM UTC
workflow_dispatch:      # Manual trigger
```

### Inputs (Manual)
| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `moods` | string | `all` | Comma-separated moods |
| `durations` | string | `1h` | Comma-separated durations |
| `upload` | boolean | `true` | Upload to YouTube |

### Secrets Required
| Secret | Purpose |
|--------|---------|
| `YOUTUBE_TOKEN_PICKLE` | Personal channel OAuth token |

### Outputs
- Video artifacts (7-day retention)
- Upload results in job summary

## content-factory-brand.yml

Same as `content-factory.yml` but uses:
- `YOUTUBE_TOKEN_PICKLE_BRAND` secret
- Uploads to brand channel

## art-creator.yml

### Trigger
```yaml
workflow_dispatch:  # Manual trigger
workflow_call:      # Called by test-art-creator.yml
```

### Input Categories

**Visual:**
- `art_period` - Historical style preset
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
- `duration` - Video length
- `seed` - Reproducibility seed
- `title` - Custom title
- `upload_to_brand` - Upload toggle

### Secrets Required
| Secret | Purpose |
|--------|---------|
| `YOUTUBE_TOKEN_PICKLE_BRAND` | Brand channel OAuth (if uploading) |

## test-art-creator.yml

### Purpose
Tests all input combinations for `art-creator.yml` by triggering it via `workflow_call`.
The test matrix is defined in this workflow and calls art-creator.yml 7 times with different inputs.
Runs 7 test cases in parallel with 5-second videos (minimum per GUARDRAILS.md) - fast validation without YouTube upload or artifact storage.

### Trigger
```yaml
workflow_dispatch:  # Manual only
```

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

### Usage
```bash
# Via GitHub UI: Actions → Test Art Creator - All Combinations → Run workflow
```

### Outputs
- No artifacts saved (tests use `skip_artifact_upload: true`)
- No YouTube upload (skipped for tests)
- Failure in any test case reported in job summary

## Invariants

1. **All workflows exit non-zero on failure** - CI/CD compatibility
2. **Artifacts always saved** - Even if upload fails
3. **Idempotent uploads** - Re-runs don't create duplicates
4. **Quota awareness** - Graceful handling of API limits

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

