# Visual Generator Specification

> **Owner:** `visuals/` directory
> **Canonical Spec:** [docs/spec/SYSTEM.md](../docs/spec/SYSTEM.md)
> **Contract:** [docs/spec/contracts/orchestrator-visual.md](../docs/spec/contracts/orchestrator-visual.md)

## Purpose

Generate hypnotic procedural visuals including fractals, sacred geometry, particle systems, and organic patterns. Supports dynamic speed/complexity evolution via journey system.

## Public Interface

```python
class VisualGenerator:
    def __init__(self, config, width=1920, height=1080, fps=30,
                 journey='steady', journey_intensity='moderate')
    
    def generate(self, duration: float, output_path: str) -> None
```

## Pattern Types

| Pattern | Description | Journey-Aware |
|---------|-------------|---------------|
| `fractal_zoom` | Mandelbrot/Julia infinite zoom | ✅ Speed |
| `sacred_geometry` | Flower of life, metatron's cube | ✅ Speed |
| `fibonacci_spiral` | Golden ratio spiral | ✅ Speed, Complexity |
| `particle_flow` | Flowing organic particles | ✅ Speed, Complexity |
| `geometric_morph` | Morphing geometric shapes | ✅ Speed |
| `platonic_solids` | 3D rotating polyhedra | ✅ Speed |
| `slow_waves` | Organic wave motion | ✅ Speed |
| `starfield` | Space journey effect | ❌ Static |
| `rain_window` | Rain on glass | ❌ Static |
| `fireplace` | Flickering fire | ❌ Static |
| `human_silhouette` | Meditation figure | ❌ Static |
| `nature_frame` | Natural border elements | ❌ Static |

## Color Configuration

```yaml
colors:
  primary: [R, G, B]      # Main color (0-255)
  secondary: [R, G, B]    # Supporting color
  accent: [R, G, B]       # Highlight color
```

## Journey Integration

Journey affects speed and complexity dynamically:

```python
def _get_journey_speed_at(self, progress: float, base_speed: float) -> float
def _get_journey_complexity_at(self, progress: float, base_complexity: float) -> float
```

**Cumulative tracking** prevents jerky animation:
```python
# Correct: accumulate changes
cumulative_rotation += current_speed * dt

# Wrong: would cause jumps when speed changes
rotation = current_speed * elapsed_time
```

## Acceptance Criteria

- [ ] Output MP4 duration matches requested exactly
- [ ] Resolution matches width × height
- [ ] Frame rate matches fps
- [ ] No visual artifacts at journey transitions
- [ ] Colors match config (no unexpected color shifts)
- [ ] Patterns are smooth and hypnotic (no jarring motion)

## Error Handling

| Condition | Behavior |
|-----------|----------|
| Invalid pattern | Fall back to 'fractal_zoom' |
| Invalid journey | Fall back to 'steady' |
| Missing colors | Use default palette |
| Speed out of range | Clamp to 0.05-2.0 |
| Complexity out of range | Clamp to 0.1-1.0 |

## Dependencies

- `numpy` - Array operations
- `opencv-python` - Video encoding
- `numba` - JIT for fractal rendering
- `pillow` - Image processing

## Files

| File | Purpose |
|------|---------|
| `generator.py` | Main VisualGenerator class |
| `__init__.py` | Package exports |

## Performance Notes

- Fractal rendering uses Numba JIT for 10-50x speedup
- Frame generation is the bottleneck for long videos
- Consider reducing resolution for faster testing

## Testing

```bash
# Quick test
python -c "
from visuals.generator import VisualGenerator
config = {
    'colors': {'primary': [100,100,100], 'secondary': [50,50,50], 'accent': [200,200,200]},
    'speed': 0.5
}
vg = VisualGenerator(config, width=640, height=480, journey='waves')
vg.generate(5, '/tmp/test.mp4')
print('✓ Visual generated')
"
```

## Future Enhancements

- [ ] More pattern types
- [ ] Pattern blending/transitions
- [ ] Real-time preview mode
- [ ] GPU acceleration (CUDA/Metal)

