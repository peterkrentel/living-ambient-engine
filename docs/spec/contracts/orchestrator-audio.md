# Contract: Orchestrator → Audio Generator

> Defines the interface between the Orchestrator and Audio Generator components.

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

## Config Schema

```yaml
# Required
tempo: 60                    # Base BPM (20-200)

# Optional with defaults
binaural_freq: 10            # Brainwave frequency Hz
sine_freq: 432               # Solfeggio frequency Hz
rhythm_pattern: "gnawa"      # Tribal rhythm name or "none"
rhythm_volume: 0.5           # 0.0-1.0
drone_volume: 1.0            # 0.0-1.0
melody_enabled: true         # Enable melodic elements
arpeggio_enabled: true       # Enable arpeggios
```

## Guarantees

### Orchestrator Guarantees
1. Config dict contains at minimum `tempo` key
2. Duration is positive number in seconds
3. Output path directory exists and is writable
4. Journey is valid preset name from `config/journeys.py`

### Audio Generator Guarantees
1. Output WAV file duration matches requested ±1 second
2. Sample rate is exactly as specified
3. Output is valid WAV format, 16-bit PCM
4. No clipping (audio normalized to -1.0 to 1.0)
5. Journey tempo evolution is smooth (no sudden jumps)

## Error Handling

| Error | Behavior |
|-------|----------|
| Invalid config | Raise `ValueError` with descriptive message |
| Invalid journey | Fall back to 'steady' with warning |
| Write failure | Raise `IOError` |
| Duration ≤ 0 | Raise `ValueError` |

## Journey Integration

The audio generator samples the journey curve at each note/beat:

```python
progress = current_time / total_duration  # 0.0 to 1.0
tempo = self._get_journey_tempo_at(progress, base_tempo)
```

Journey affects:
- Melody note timing
- Arpeggio speed
- (Rhythm BPM is currently static - future enhancement)

## Testing Contract

```python
def test_audio_contract():
    config = {'tempo': 60}
    gen = AudioGenerator(config, journey='awakening')
    gen.generate(10.0, '/tmp/test.wav')
    
    # Verify duration
    import wave
    with wave.open('/tmp/test.wav') as w:
        duration = w.getnframes() / w.getframerate()
        assert abs(duration - 10.0) < 1.0
```

