# Audio Generator Specification

> **Owner:** `audio/` directory
> **Canonical Spec:** [docs/spec/SYSTEM.md](../docs/spec/SYSTEM.md)
> **Contract:** [docs/spec/contracts/orchestrator-audio.md](../docs/spec/contracts/orchestrator-audio.md)

## Purpose

Generate ambient audio with layered synthesis including tribal rhythms, binaural beats, solfeggio tones, melodies, and arpeggios. Supports dynamic tempo evolution via journey system.

## Public Interface

```python
class AudioGenerator:
    def __init__(self, config, sample_rate=44100, channels=2,
                 rhythm_volume_override=None, drone_volume_override=None,
                 journey='steady', journey_intensity='moderate')
    
    def generate(self, duration: float, output_path: str) -> None
```

## Audio Layers

| Layer | Description | Config Key |
|-------|-------------|------------|
| **Binaural Beat** | Stereo frequency difference for brainwave entrainment | `binaural_freq` |
| **Solfeggio Tone** | Healing frequency sine wave | `sine_freq` |
| **Tribal Rhythm** | Procedural drum patterns | `rhythm_pattern` |
| **Drone** | Ambient pad/texture | `drone_volume` |
| **Melody** | Pentatonic melodic phrases | `melody_enabled` |
| **Arpeggio** | Flowing note sequences | `arpeggio_enabled` |

## Rhythm Patterns

| Pattern | Origin | Character |
|---------|--------|-----------|
| `heartbeat` | Universal | Primal, grounding |
| `taiko` | Japan | Powerful, focused |
| `gamelan` | Indonesia | Ethereal, layered |
| `gnawa` | Morocco | Deep, meditative |
| `bamboula` | Caribbean | Hypnotic groove |
| `candomble` | Brazil | Sacred polyrhythms |
| `burundi` | East Africa | Intense, energizing |
| `kuku` | West Africa | Joyful, celebratory |
| `none` | - | No percussion |

## Journey Integration

Journey affects tempo dynamically over the duration:

```python
def _get_journey_tempo_at(self, t: float, base_tempo: float) -> float:
    """
    t: progress 0.0 to 1.0
    Returns: tempo at this point in the journey
    """
```

**Affected components:**
- Melody note timing
- Arpeggio speed

**Not yet affected (future):**
- Rhythm BPM (currently static)

## Phase System

Audio evolves through phases every 3-7 minutes:

1. **Settle** - Establish the mood
2. **Drift** - Subtle variations
3. **Deepen** - Intensity builds
4. **Resolve** - Return to calm

## Acceptance Criteria

- [ ] Output WAV duration matches requested ±1 second
- [ ] No audio clipping (peaks within -1.0 to 1.0)
- [ ] Binaural beat frequency difference is accurate ±0.1 Hz
- [ ] Rhythm patterns are recognizable and on-beat
- [ ] Journey tempo changes are smooth (no sudden jumps)
- [ ] All layers blend without harsh frequencies

## Error Handling

| Condition | Behavior |
|-----------|----------|
| Invalid tempo (<20 or >200) | Clamp to valid range |
| Unknown rhythm pattern | Fall back to 'gnawa' |
| Unknown journey | Fall back to 'steady' |
| Write failure | Raise IOError |

## Dependencies

- `numpy` - Audio synthesis
- `scipy` - Signal processing, WAV output
- `numba` - JIT compilation for performance

## Files

| File | Purpose |
|------|---------|
| `generator.py` | Main AudioGenerator class |
| `__init__.py` | Package exports |

## Testing

```bash
# Quick test
python -c "
from audio.generator import AudioGenerator
ag = AudioGenerator({'tempo': 60}, journey='awakening')
ag.generate(10, '/tmp/test.wav')
print('✓ Audio generated')
"
```

## Future Enhancements

- [ ] Journey-aware rhythm BPM
- [ ] More rhythm patterns
- [ ] Harmonic progression system
- [ ] Real-time streaming output

