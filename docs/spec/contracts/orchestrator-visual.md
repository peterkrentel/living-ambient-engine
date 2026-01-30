# Contract: Orchestrator → Visual Generator

> Defines the interface between the Orchestrator and Visual Generator components.

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

## Config Schema

```yaml
# Required
colors:
  primary: [R, G, B]      # 0-255 each
  secondary: [R, G, B]
  accent: [R, G, B]

# Optional with defaults
pattern: "fractal_zoom"   # Pattern generator name
speed: 0.5                # Base animation speed (0.1-1.0)
complexity: 0.7           # Visual complexity (0.1-1.0)
symmetry: 4               # Rotational symmetry
zoom_speed: 0.001         # Fractal zoom rate
```

## Guarantees

### Orchestrator Guarantees
1. Config dict contains `colors` with primary/secondary/accent
2. Duration is positive number in seconds
3. Output path directory exists and is writable
4. Journey is valid preset name from `config/journeys.py`

### Visual Generator Guarantees
1. Output MP4 duration matches requested duration exactly
2. Resolution matches width × height specified
3. Frame rate matches fps specified
4. Output is valid MP4 (H.264), no audio track
5. Journey speed/complexity evolution is smooth (cumulative phase tracking)
6. No visual artifacts at journey transitions

## Error Handling

| Error | Behavior |
|-------|----------|
| Invalid config | Raise `ValueError` with descriptive message |
| Invalid pattern | Fall back to 'fractal_zoom' with warning |
| Invalid journey | Fall back to 'steady' with warning |
| Write failure | Raise `IOError` |
| Duration ≤ 0 | Raise `ValueError` |

## Pattern Types

| Pattern | Description | Journey-Aware |
|---------|-------------|---------------|
| `fractal_zoom` | Mandelbrot/Julia zoom | ✅ Speed |
| `sacred_geometry` | Flower of life, metatron | ✅ Speed |
| `fibonacci_spiral` | Golden ratio spiral | ✅ Speed, Complexity |
| `particle_flow` | Flowing particles | ✅ Speed, Complexity |
| `geometric_morph` | Morphing shapes | ✅ Speed |
| `platonic_solids` | 3D rotating solids | ✅ Speed |
| `slow_waves` | Organic wave motion | ✅ Speed |
| `starfield` | Space journey | ❌ |
| `rain_window` | Rain effect | ❌ |
| `fireplace` | Fire effect | ❌ |

## Journey Integration

The visual generator samples journey curves per-frame:

```python
progress = frame_index / total_frames  # 0.0 to 1.0
speed = self._get_journey_speed_at(progress, base_speed)
complexity = self._get_journey_complexity_at(progress, base_complexity)
```

**Cumulative tracking** ensures smooth animation:
```python
cumulative_rotation += speed * dt  # Not: rotation = speed * t
```

## Testing Contract

```python
def test_visual_contract():
    config = {
        'colors': {'primary': [100,100,100], 'secondary': [50,50,50], 'accent': [200,200,200]},
        'speed': 0.5,
        'complexity': 0.7
    }
    gen = VisualGenerator(config, width=640, height=480, fps=30, journey='deep_dive')
    gen.generate(5.0, '/tmp/test.mp4')
    
    # Verify with ffprobe
    import subprocess
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 
                            'format=duration', '-of', 'csv=p=0', '/tmp/test.mp4'],
                           capture_output=True, text=True)
    duration = float(result.stdout.strip())
    assert abs(duration - 5.0) < 0.1
```

