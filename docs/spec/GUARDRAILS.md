# System Guardrails

> **Hard limits and forbidden states that must never be violated.**
> These are non-negotiable constraints enforced across all components.

## Quick Reference

| Parameter | Min | Max | Default | Enforcement |
|-----------|-----|-----|---------|-------------|
| `tempo` | 20 | 200 | 60 | Clamp |
| `visual_speed` | 0.01 | 1.5 | 0.5 | Clamp |
| `visual_complexity` | 0.1 | 1.0 | 0.7 | Clamp |
| `brainwave_frequency` | 1 | 50 | 10 | Clamp |
| `solfeggio_frequency` | 174 | 963 | 432 | Validate |
| `rhythm_volume` | 0.0 | 1.0 | 0.5 | Clamp |
| `ambient_volume` | 0.0 | 1.0 | 1.0 | Clamp |
| `duration` | 10s | 4h | 5min | Validate |
| `fps` | 15 | 60 | 24 | Validate |
| `resolution.width` | 640 | 3840 | 1280 | Validate |
| `resolution.height` | 480 | 2160 | 720 | Validate |

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
| Memory usage > 8GB | OOM on runners | Memory monitoring |
| Temp files > 50GB | Disk exhaustion | Disk space check |
| Single job > 6 hours | Workflow timeout | Duration limits |
| Infinite loops in generation | Hang | Timeout watchdog |

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

# Resolution
width: int
  min: 640     # Minimum for YouTube
  max: 3840    # 4K maximum
  default: 1280
  enforcement: VALIDATE

height: int
  min: 480
  max: 2160
  default: 720
  enforcement: VALIDATE

# Frame rate
fps: int
  min: 15      # Minimum for smooth video
  max: 60      # Maximum for ambient (no need higher)
  default: 24
  enforcement: VALIDATE
```

### Duration Parameters

```python
# Video duration
duration: str | int
  min: "10s"   # Minimum useful length
  max: "4h"    # Maximum for workflow timeout
  default: "5min"
  enforcement: VALIDATE

# Workflow timeout
workflow_timeout: int (minutes)
  max: 360     # 6 hours GitHub Actions limit
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

## Adding New Guardrails

When adding new parameters or features:

1. **Define bounds** - What are the min/max/default values?
2. **Choose enforcement** - Clamp, warn+fallback, validate, or halt?
3. **Document here** - Add to appropriate section
4. **Implement validation** - Add to workflow and/or code
5. **Add tests** - Contract tests for boundary conditions

