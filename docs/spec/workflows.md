# GitHub Workflows Specification

> **Owner:** `.github/workflows/` directory
> **Canonical Spec:** [SYSTEM.md](./SYSTEM.md)

## Overview

Three workflows automate video generation and YouTube deployment.

## Workflow Index

| Workflow | Trigger | Purpose | Channel |
|----------|---------|---------|---------|
| `content-factory.yml` | Schedule + Manual | Batch generation + upload | Personal |
| `content-factory-brand.yml` | Manual | Batch generation + upload | Brand |
| `art-creator.yml` | Manual | Single custom video | Brand (optional) |

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
workflow_dispatch:  # Manual only
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

