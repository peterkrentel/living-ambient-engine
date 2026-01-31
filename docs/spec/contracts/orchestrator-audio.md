# Contract: Orchestrator → Audio Generator

> Defines the interface between the Orchestrator and Audio Generator components.
> See also: [GUARDRAILS.md](../GUARDRAILS.md) for parameter limits.

## Interface

```python
from audio.generator import AudioGenerator

generator = AudioGenerator(
    config: Dict,                    # Audio configuration
    sample_rate: int = 44100,        # Audio sample rate
    channels: int = 2,               # Stereo
    rhythm_volume_override: float = None,  # Optional volume override
    drone_volume_override: float = None,   # Optional volume override
    journey: str = 'steady',         # Journey preset name
    journey_intensity: str = 'moderate'  # Journey intensity
)

generator.generate(
    duration: float,    # Duration in seconds
    output_path: str    # Path to write WAV file
)
```

## Pre-Conditions

> **Must be true BEFORE calling the interface.**

### `AudioGenerator.__init__`
| Condition | Check | Violation Handling |
|-----------|-------|-------------------|
| `config` is dict | `isinstance(config, dict)` | Raise `TypeError` |
| `config['tempo']` exists | `'tempo' in config` | Raise `KeyError` |
| `tempo` in range | `20 <= tempo <= 200` | Clamp to range |
| `sample_rate` valid | `sample_rate in [22050, 44100, 48000]` | Use 44100 |
| `channels` valid | `channels in [1, 2]` | Use 2 |
| `journey` valid | `journey in JOURNEY_PRESETS` | Use 'steady' |
| `journey_intensity` valid | `intensity in ['subtle', 'moderate', 'dramatic']` | Use 'moderate' |

### `AudioGenerator.generate`
| Condition | Check | Violation Handling |
|-----------|-------|-------------------|
| `duration` positive | `duration > 0` | Raise `ValueError` |
| `duration` reasonable | `duration <= 14400` (4h) | Raise `ValueError` |
| `output_path` dir exists | `Path(output_path).parent.exists()` | Raise `IOError` |
| `output_path` writable | Write permission check | Raise `IOError` |

## Post-Conditions

> **Must be true AFTER the interface returns successfully.**

### `AudioGenerator.generate`
| Condition | Verification |
|-----------|--------------|
| File exists | `Path(output_path).exists()` |
| File non-empty | `Path(output_path).stat().st_size > 0` |
| Duration matches | `abs(actual_duration - requested) < 1.0` |
| Valid WAV format | `wave.open()` succeeds |
| Sample rate correct | `wav.getframerate() == sample_rate` |
| Channels correct | `wav.getnchannels() == channels` |
| No clipping | `max(abs(samples)) <= 1.0` |

## Invariants

> **Must ALWAYS be true during execution.**

| Invariant | Description |
|-----------|-------------|
| **Tempo bounds** | `20 <= effective_tempo <= 200` at all times |
| **Volume bounds** | `0.0 <= volume <= 1.0` for all layers |
| **No NaN/Inf** | Audio samples never contain NaN or Infinity |
| **Monotonic time** | Sample index always increases |
| **Deterministic** | Same seed + config = identical output |

## Config Schema

```yaml
# Required
tempo: 60                    # Base BPM (20-200)

# Optional with defaults
binaural_freq: 10            # Brainwave frequency Hz (1-50)
sine_freq: 432               # Solfeggio frequency Hz
rhythm_pattern: "gnawa"      # Tribal rhythm name or "none"
rhythm_volume: 0.5           # 0.0-1.0
drone_volume: 1.0            # 0.0-1.0
melody_enabled: true         # Enable melodic elements
arpeggio_enabled: true       # Enable arpeggios
```

## Error Handling

| Error | Behavior | Exit |
|-------|----------|------|
| Invalid config | Raise `ValueError` with descriptive message | Immediate |
| Invalid journey | Fall back to 'steady' with warning | Continue |
| Invalid rhythm | Fall back to 'gnawa' with warning | Continue |
| Write failure | Raise `IOError` | Immediate |
| Duration ≤ 0 | Raise `ValueError` | Immediate |
| Memory exhaustion | Raise `MemoryError` | Immediate |

## Journey Integration

The audio generator samples the journey curve at each note/beat:

```python
progress = current_time / total_duration  # 0.0 to 1.0
tempo = self._get_journey_tempo_at(progress, base_tempo)

# Post-journey clamping (invariant enforcement)
tempo = max(20, min(200, tempo))
```

Journey affects:
- Melody note timing
- Arpeggio speed
- (Rhythm BPM is currently static - future enhancement)

## Contract Test

```python
def test_audio_contract():
    """Verify all contract conditions."""
    import wave
    import numpy as np
    from pathlib import Path

    config = {'tempo': 60}
    gen = AudioGenerator(config, journey='awakening')
    output = '/tmp/test_contract.wav'

    # Pre-condition: duration positive
    with pytest.raises(ValueError):
        gen.generate(-1, output)

    # Execute
    gen.generate(10.0, output)

    # Post-conditions
    assert Path(output).exists(), "File must exist"
    assert Path(output).stat().st_size > 0, "File must be non-empty"

    with wave.open(output) as w:
        duration = w.getnframes() / w.getframerate()
        assert abs(duration - 10.0) < 1.0, "Duration must match ±1s"
        assert w.getframerate() == 44100, "Sample rate must match"
        assert w.getnchannels() == 2, "Channels must match"
```

