# System Guardrails

> **Hard limits and forbidden states that must never be violated.**
> These are non-negotiable constraints enforced across all components.

## Quick Reference - Numeric Parameters

| Parameter | Min | Max | Default | Enforcement |
|-----------|-----|-----|---------|-------------|
| `tempo` | 20 | 200 | 60 | Clamp |
| `visual_speed` | 0.01 | 1.5 | 0.5 | Clamp |
| `visual_complexity` | 0.1 | 1.0 | 0.7 | Clamp |
| `brainwave_frequency` | 1 | 50 | 10 | Clamp |
| `solfeggio_frequency` | 174 | 963 | 432 | Validate |
| `rhythm_volume` | 0.0 | 1.0 | 0.5 | Clamp |
| `ambient_volume` | 0.0 | 1.0 | 1.0 | Clamp |
| `duration` | 5s | 4h | 5min | Validate |
| `fps` | 15 | 60 | 15 | Validate |
| `resolution.width` | 640 | 3840 | 640 | Validate |
| `resolution.height` | 480 | 2160 | 480 | Validate |

## Valid Moods

Canonical list of valid mood identifiers. Source: `config/moods.yaml`

| Category | Valid Values |
|----------|--------------|
| **Nature** | `rain_sleep`, `ocean_waves`, `fireplace`, `forest_morning` |
| **Music** | `deep_focus`, `sleep`, `chill`, `study`, `energize`, `lofi_study`, `piano_relax` |
| **Tribal** | `warrior`, `ceremony`, `trance` |

**Special value:** `all` - expands to all 14 moods

**Enforcement:** Validate + Reject. Unknown mood causes immediate failure with error listing valid options.

**Adding new moods:**
1. Add to `config/moods.yaml`
2. Update this table
3. Workflows auto-discover from config (no workflow changes needed)

## Valid Durations (Workflow Inputs)

| Value | Seconds | Use Case |
|-------|---------|----------|
| `30s` | 30 | Test/preview |
| `5min` | 300 | Quick creation (art-creator default) |
| `10min` | 600 | Short session |
| `1h` | 3600 | Standard session |
| `3h` | 10800 | Extended session |
| `4h` | 14400 | Maximum allowed |

**Enforcement:** Dropdown selection in workflows (no free text = no typos)

## Valid Moods

Moods are defined in `config/moods.yaml`. Only these values are accepted:

| Category | Valid Moods | Description |
|----------|-------------|-------------|
| **Nature** | `rain_sleep`, `ocean_waves`, `fireplace`, `forest_morning` | Ambient nature sounds, no drums |
| **Music** | `deep_focus`, `sleep`, `chill`, `study`, `energize`, `lofi_study`, `piano_relax` | Musical ambient with optional rhythm |
| **Tribal** | `warrior`, `ceremony`, `trance` | Tribal drums and ceremonial sounds |

**Special value:** `all` - generates all 14 moods

**Enforcement:** Validate + Reject (unknown moods cause immediate failure with list of valid options)

## Forbidden States

These conditions must **never** occur. If detected, the system must halt with an error.

### 1. Security Violations

| Forbidden | Reason | Detection |
|-----------|--------|-----------|
| Secrets in logs | Credential exposure | Pre-commit hook, CI scan |
| Secrets in artifacts | Credential exposure | Artifact validation |
| Secrets in code | Credential exposure | Git-secrets, pre-commit |
| Arbitrary file write outside output dirs | Security | Path validation |
| Shell injection in config values | Security | Input sanitization |

### 2. Data Integrity Violations

| Forbidden | Reason | Detection |
|-----------|--------|-----------|
| Audio clipping (peaks > 1.0 or < -1.0) | Quality | Normalization check |
| Video with 0 frames | Corrupt output | Frame count validation |
| Mismatched audio/video duration (>2s) | Sync issues | Duration comparison |
| Empty output files | Corrupt output | File size check |
| Invalid UTF-8 in metadata | Encoding errors | Encoding validation |

### 3. Resource Violations

| Forbidden | Reason | Detection |
|-----------|--------|-----------|
| Memory usage > 8GB | OOM on runners | Pre-allocation check |
| Temp files > 50GB | Disk exhaustion | Disk space check |
| Single job > 6 hours | Workflow timeout | Duration limits |
| Infinite loops in generation | Hang | Timeout watchdog |

### 4. Metadata Consistency Violations

| Forbidden | Reason | Detection |
|-----------|--------|-----------|
| Inline metadata generation in workflows | Inconsistent SEO, bypasses moods.yaml | Contract test + code review |
| Hardcoded tags/description in workflow YAML | Single source of truth violation | Contract test |
| Upload without metadata.json | Missing SEO optimization | Pre-upload validation |

**Enforcement:**
- All workflows that upload to YouTube MUST use `youtube_upload.py`
- All metadata (title, description, tags) MUST originate from `moods.yaml` → `metadata.json` → `youtube_upload.py`
- Inline Python in workflows MUST NOT generate YouTube metadata directly

**Exception: art-creator.yml and art-creator-batch.yml**

These workflows use a **different metadata strategy** intentionally:

| Workflow | Strategy | Why |
|----------|----------|-----|
| content-factory-brand | SEO-optimized (moods.yaml) | Human search discovery ("focus music") |
| art-creator-batch | Parameter-based variety | Algorithm discovery (volume/variety) |

art-creator generates titles from parameters (`"Ambient {art_period} | {duration} | Evolving {music_style} Soundscape"`)
rather than moods.yaml. This is intentional - the goal is 81 unique title combinations to maximize
algorithm recommendation chances, not individual title SEO optimization.

**This exception applies ONLY to art-creator workflows. All other workflows MUST use moods.yaml.**

Contract test: `tests/contracts/test_workflow_metadata_consistency.py`

**Memory Enforcement via Chunked Generation:**

Audio generation uses **streaming/chunked writes** to stay within memory limits, enabling
4+ hour videos on systems with limited RAM (e.g., 7GB GitHub Actions runners).

```python
# AudioGenerator.generate() uses chunked streaming instead of pre-allocation
# Chunk size: 30 seconds (~10MB per chunk for stereo float32)
chunk_duration = 30  # seconds
chunk_size = chunk_duration * sample_rate

with sf.SoundFile(output_path, 'w', sample_rate, channels) as f:
    for chunk_start in range(0, num_samples, chunk_size):
        chunk = generate_chunk(chunk_start, chunk_size)  # ~10MB
        f.write(chunk)
```

**Why chunked:** A 4-hour video at 44100 Hz stereo float32 would require ~10GB RAM if
pre-allocated. Chunked generation uses only ~10-15MB regardless of video duration.

Contract test: `tests/contracts/test_audio_contract.py::TestAudioContractGuardrails::test_memory_guardrail_enforced`

## Enforcement Levels

### Level 1: Clamp (Silent Correction)
Values outside range are silently clamped to nearest valid value.
```python
tempo = max(20, min(200, tempo))  # Clamp to 20-200
```

### Level 2: Warn + Fallback
Invalid values trigger a warning and use a safe default.
```python
if journey not in JOURNEY_PRESETS:
    warnings.warn(f"Unknown journey '{journey}', using 'steady'")
    journey = 'steady'
```

### Level 3: Validate + Reject
Invalid values cause immediate failure with descriptive error.
```python
if duration <= 0:
    raise ValueError(f"Duration must be positive, got {duration}")
```

### Level 4: Halt (Critical)
Forbidden states that require immediate termination.
```python
if secret_detected_in_output:
    raise SecurityError("Secret detected in output - aborting")
```

## Parameter Validation Rules

### Audio Parameters

```python
# Tempo: BPM for rhythm and melody timing
tempo: int
  min: 20      # Below this is imperceptible rhythm
  max: 200     # Above this is too fast for ambient
  default: 60
  enforcement: CLAMP

# Brainwave frequency: Hz for binaural beats
brainwave_frequency: float
  min: 1       # Delta waves
  max: 50      # Gamma waves
  default: 10  # Alpha waves (relaxation)
  enforcement: CLAMP

# Solfeggio frequencies: Must be valid healing frequencies
solfeggio_frequency: int
  valid: [174, 285, 396, 417, 432, 528, 639, 741, 852, 963]
  default: 432
  enforcement: VALIDATE (reject invalid)

# Volume levels
rhythm_volume: float
  min: 0.0
  max: 1.0
  default: 0.5
  enforcement: CLAMP

ambient_volume: float
  min: 0.0
  max: 1.0
  default: 1.0
  enforcement: CLAMP
```

### Visual Parameters

```python
# Speed: Animation rate multiplier
visual_speed: float
  min: 0.01    # Nearly static
  max: 1.5     # Fast but not jarring
  default: 0.5
  enforcement: CLAMP

# Complexity: Detail level
visual_complexity: float
  min: 0.1     # Minimal detail
  max: 1.0     # Maximum detail
  default: 0.7
  enforcement: CLAMP

# Resolution (smaller is better for ambient YouTube)
width: int
  min: 640     # Minimum for YouTube
  max: 3840    # 4K maximum
  default: 640 # Use minimum - smaller files, faster renders
  enforcement: VALIDATE

height: int
  min: 480
  max: 2160
  default: 480 # Use minimum - smaller files, faster renders
  enforcement: VALIDATE

# Frame rate (lower is fine for ambient)
fps: int
  min: 15      # Minimum for smooth video
  max: 60      # Maximum for ambient (no need higher)
  default: 15  # Use minimum - smaller files, faster renders
  enforcement: VALIDATE
```

### Duration Parameters

```python
# Video duration
duration: str | int
  min: "5s"    # Minimum for tests (allows 2s fade in/out + content)
  max: "4h"    # Maximum for workflow timeout
  default: "5min"
  enforcement: VALIDATE

# Workflow timeout
workflow_timeout: int (minutes)
  create_art: 300   # 5 hours for 4h video generation + processing
  upload: 30        # Upload step timeout
  max: 360          # 6 hours GitHub Actions limit
  enforcement: VALIDATE

# Concurrency group (art-creator.yml)
concurrency_group: str
  format: "art-creator-{run_id}-{test_id}"
  requirement: Must include test_id to allow parallel matrix jobs
  enforcement: VALIDATE
```

## Journey System Guardrails

Journey curves must stay within safe bounds:

```python
# After applying journey curves, clamp results
tempo = max(20, min(200, tempo))
speed = max(0.05, min(1.5, speed))
complexity = max(0.1, min(1.0, complexity))
```

**Invariant:** Journey curves cannot produce values outside clamped ranges.

## File System Guardrails

### Allowed Write Paths
```
./output/          # Final outputs
./artifacts/       # Build artifacts
./temp/            # Temporary files (auto-cleaned)
/tmp/              # System temp (CI runners)
```

### Forbidden Write Paths
```
./                 # Repository root (except allowed subdirs)
../*               # Parent directories
/etc/, /usr/, etc  # System directories
~/.ssh/, ~/.aws/   # Credential directories
```

## YouTube API Guardrails

| Limit | Value | Handling |
|-------|-------|----------|
| Daily upload quota | 10,000 units | Track usage, pause if near limit |
| Video title length | 100 chars | Truncate with ellipsis |
| Description length | 5000 chars | Truncate |
| Tags total length | 500 chars | Prioritize important tags |
| Upload retries | 3 | Exponential backoff |

## Monitoring & Alerting

### Metrics to Track
- Generation time per minute of video
- Memory high-water mark
- Disk usage during generation
- Upload success rate
- Workflow failure rate

### Alert Conditions
- Generation time > 2x baseline
- Memory > 6GB
- Disk usage > 40GB
- Upload failure rate > 20%
- Workflow failure rate > 10%

## Runtime Enforcement

**Status: ✅ ENFORCED**

Guardrails are enforced at runtime in generators:

| Component | Enforcement | File |
|-----------|-------------|------|
| AudioGenerator | `clamp_to_guardrails('audio_config')` | `audio/generator.py` |
| VisualGenerator | `clamp_to_guardrails('visual_config')` | `visuals/generator.py` |
| Workflow | PR validation job | `.github/workflows/test-art-creator.yml` |

```python
# How enforcement works in generators:
from config.validator import clamp_to_guardrails

class AudioGenerator:
    def __init__(self, config, ...):
        # GUARDRAILS ENFORCEMENT (Level 1: Clamp)
        config = clamp_to_guardrails(config, 'audio_config')
        self.config = config
```

## Adding New Guardrails

When adding new parameters or features:

1. **Define bounds** - What are the min/max/default values?
2. **Choose enforcement** - Clamp, warn+fallback, validate, or halt?
3. **Document here** - Add to appropriate section
4. **Implement validation** - Add to workflow and/or code
5. **Add to JSON schema** - Update `config/schemas/*.json`
6. **Add tests** - Contract tests for boundary conditions

