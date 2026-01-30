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
| `art-creator.yml` | Manual + workflow_call | Single custom video | Brand (optional) |
| `test-art-creator.yml` | Manual | Test art-creator with matrix | None (test only) |

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
workflow_call:      # Can be called by test-art-creator
```

### Execution Modes

**Manual (workflow_dispatch):**
- Runs with user-provided inputs
- Executes only test_id 1 from matrix (for validation)
- Can upload to YouTube if enabled

**Test Mode (workflow_call):**
- Triggered by test-art-creator workflow
- Runs all 5 matrix test combinations
- Never uploads to YouTube
- Tests journey presets and parameter combinations

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

### Test Matrix

The workflow includes a matrix strategy for comprehensive testing:

| Test ID | Art Period | Visual Pattern | Music Style | Solfeggio | Journey | Intensity |
|---------|------------|----------------|-------------|-----------|---------|-----------|
| 1 | modern | fractal_zoom | gnawa | 528 Hz | steady | moderate |
| 2 | cave_art | organic_flow | heartbeat | 174 Hz | awakening | subtle |
| 3 | renaissance | fibonacci_spiral | taiko | 639 Hz | deep_dive | moderate |
| 4 | future | starfield | none | 963 Hz | crescendo | dramatic |
| 5 | impressionist | flowing_waves | gamelan | 417 Hz | waves | moderate |

**Journey Coverage:** Tests 5 of 7 journey presets:
- ✅ `steady` - Traditional constant tempo
- ✅ `awakening` - Gradual energy rise
- ✅ `deep_dive` - Descending into calm
- ✅ `crescendo` - Build to peak then release
- ✅ `waves` - Ocean-like swells
- ⚠️ `breathing` - Not in matrix (similar to waves)
- ⚠️ `trance` - Not in matrix (similar to awakening)

## test-art-creator.yml

### Purpose
Automated testing workflow that triggers the art-creator workflow with matrix expansion to validate all parameter combinations including journey presets.

### Trigger
```yaml
workflow_dispatch:  # Manual only
```

### How It Works
1. Calls `art-creator.yml` using `workflow_call`
2. Art-creator runs all 5 matrix test combinations in parallel
3. Each test generates a 10-second video
4. No uploads occur (test mode)
5. Artifacts saved for inspection

### Use Cases
- **Pre-release validation:** Test all combinations before merging changes
- **Journey preset validation:** Ensure all journey curves work correctly
- **Configuration testing:** Validate art period and color palette mappings
- **Integration testing:** Test orchestrator with various input combinations

### Running Tests
```bash
# Via GitHub UI
Actions → Test Art Creator - All Combinations → Run workflow

# Enter optional reason for test run
```

### Test Duration
- Each test: ~2-3 minutes (10s video generation + setup)
- Total: ~10-15 minutes (parallel execution)

### Test Artifacts
Each matrix test produces:
- Video file (10s MP4)
- Creation metadata JSON
- Retention: 30 days

### Adding Test Cases

To add a new test combination to the matrix:

1. Edit `.github/workflows/art-creator.yml`
2. Add new entry to `matrix.include`
3. Ensure journey preset is specified
4. Update this spec with new test case
5. Update total count in `test-art-creator.yml` comments

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

