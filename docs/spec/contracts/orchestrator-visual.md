# Contract: Orchestrator → Visual Generator

> Defines the interface between the Orchestrator and Visual Generator components.
> See also: [GUARDRAILS.md](../GUARDRAILS.md) for parameter limits.

## Interface

```python
from visuals.generator import VisualGenerator

generator = VisualGenerator(
    config: Dict,                    # Visual configuration
    width: int = 1920,               # Video width
    height: int = 1080,              # Video height
    fps: int = 30,                   # Frames per second
    journey: str = 'steady',         # Journey preset name
    journey_intensity: str = 'moderate'  # Journey intensity
)

generator.generate(
    duration: float,    # Duration in seconds
    output_path: str    # Path to write MP4 file
)
```

## Pre-Conditions

> **Must be true BEFORE calling the interface.**

### `VisualGenerator.__init__`

| Condition | Check | Violation Handling |
|-----------|-------|-------------------|
| `config` is dict | `isinstance(config, dict)` | Raise `TypeError` |
| `colors` exists | `'colors' in config` | Raise `KeyError` |
| `colors.primary` valid | `len(primary) == 3, all 0-255` | Clamp values |
| `colors.secondary` valid | `len(secondary) == 3, all 0-255` | Clamp values |
| `colors.accent` valid | `len(accent) == 3, all 0-255` | Clamp values |
| `width` in range | `640 <= width <= 3840` | Clamp to range |
| `height` in range | `480 <= height <= 2160` | Clamp to range |
| `fps` in range | `15 <= fps <= 60` | Clamp to range |
| `journey` valid | `journey in JOURNEY_PRESETS` | Use 'steady' |
| `journey_intensity` valid | `intensity in ['subtle', 'moderate', 'dramatic']` | Use 'moderate' |

### `VisualGenerator.generate`

| Condition | Check | Violation Handling |
|-----------|-------|-------------------|
| `duration` positive | `duration > 0` | Raise `ValueError` |
| `duration` reasonable | `duration <= 14400` (4h) | Raise `ValueError` |
| `output_path` dir exists | `Path(output_path).parent.exists()` | Raise `IOError` |
| `output_path` writable | Write permission check | Raise `IOError` |
| Sufficient disk space | `free_space > estimated_size` | Raise `IOError` |

## Post-Conditions

> **Must be true AFTER the interface returns successfully.**

### `VisualGenerator.generate`

| Condition | Verification |
|-----------|--------------|
| File exists | `Path(output_path).exists()` |
| File non-empty | `Path(output_path).stat().st_size > 0` |
| Duration matches | `abs(actual_duration - requested) < 0.1` |
| Valid MP4 format | `ffprobe` succeeds |
| Resolution correct | `ffprobe` shows `width x height` |
| FPS correct | `ffprobe` shows expected fps |
| No audio track | Video-only MP4 |

## Invariants

> **Must ALWAYS be true during execution.**

| Invariant | Description |
|-----------|-------------|
| **Speed bounds** | `0.01 <= effective_speed <= 1.5` at all times |
| **Complexity bounds** | `0.1 <= effective_complexity <= 1.0` at all times |
| **Color bounds** | `0 <= R,G,B <= 255` for all pixels |
| **Frame continuity** | No duplicate or skipped frame indices |
| **Cumulative state** | Animation state accumulates (no jumps) |
| **Deterministic** | Same seed + config = identical output |
| **Memory bounded** | Peak memory < 8GB |

## Config Schema

```yaml
# Required
colors:
  primary: [R, G, B]      # 0-255 each
  secondary: [R, G, B]
  accent: [R, G, B]

# Optional with defaults
pattern: "fractal_zoom"   # Pattern generator name
speed: 0.5                # Base animation speed (0.01-1.5)
complexity: 0.7           # Visual complexity (0.1-1.0)
symmetry: 4               # Rotational symmetry (1-12)
zoom_speed: 0.001         # Fractal zoom rate
```

## Error Handling

| Error | Behavior | Exit |
|-------|----------|------|
| Invalid config | Raise `ValueError` with descriptive message | Immediate |
| Invalid pattern | Fall back to 'fractal_zoom' with warning | Continue |
| Invalid journey | Fall back to 'steady' with warning | Continue |
| Write failure | Raise `IOError` | Immediate |
| Duration ≤ 0 | Raise `ValueError` | Immediate |
| Memory exhaustion | Raise `MemoryError` | Immediate |
| FFmpeg failure | Raise `RuntimeError` with stderr | Immediate |

## Pattern Types

| Pattern | Description | Journey-Aware | Complexity-Aware |
|---------|-------------|---------------|------------------|
| `fractal_zoom` | Mandelbrot/Julia zoom | ✅ Speed | ❌ |
| `sacred_geometry` | Flower of life, metatron | ✅ Speed | ❌ |
| `fibonacci_spiral` | Golden ratio spiral | ✅ Speed | ✅ |
| `particle_flow` | Flowing particles | ✅ Speed | ✅ |
| `geometric_morph` | Morphing shapes | ✅ Speed | ❌ |
| `platonic_solids` | 3D rotating solids | ✅ Speed | ❌ |
| `slow_waves` | Organic wave motion | ✅ Speed | ❌ |
| `starfield` | Space journey | ❌ | ❌ |
| `rain_window` | Rain effect | ❌ | ❌ |
| `fireplace` | Fire effect | ❌ | ❌ |

## Journey Integration

The visual generator samples journey curves per-frame:

```python
progress = frame_index / total_frames  # 0.0 to 1.0
speed = self._get_journey_speed_at(progress, base_speed)
complexity = self._get_journey_complexity_at(progress, base_complexity)

# Post-journey clamping (invariant enforcement)
speed = max(0.01, min(1.5, speed))
complexity = max(0.1, min(1.0, complexity))
```

**Cumulative tracking** ensures smooth animation:

```python
# CORRECT: Accumulate changes
cumulative_rotation += speed * dt

# WRONG: Would cause jumps when speed changes
rotation = speed * elapsed_time
```

## Contract Test

```python
def test_visual_contract():
    """Verify all contract conditions."""
    import subprocess
    from pathlib import Path

    config = {
        'colors': {'primary': [100,100,100], 'secondary': [50,50,50], 'accent': [200,200,200]},
        'speed': 0.5,
        'complexity': 0.7
    }
    output = '/tmp/test_contract.mp4'

    gen = VisualGenerator(config, width=640, height=480, fps=30, journey='deep_dive')

    # Pre-condition: duration positive
    with pytest.raises(ValueError):
        gen.generate(-1, output)

    # Execute
    gen.generate(5.0, output)

    # Post-conditions
    assert Path(output).exists(), "File must exist"
    assert Path(output).stat().st_size > 0, "File must be non-empty"

    # Verify with ffprobe
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
         '-show_entries', 'stream=width,height,r_frame_rate',
         '-show_entries', 'format=duration',
         '-of', 'json', output],
        capture_output=True, text=True
    )
    import json
    info = json.loads(result.stdout)

    duration = float(info['format']['duration'])
    assert abs(duration - 5.0) < 0.1, "Duration must match"

    stream = info['streams'][0]
    assert stream['width'] == 640, "Width must match"
    assert stream['height'] == 480, "Height must match"
```

