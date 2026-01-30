# Configuration Specification

> **Owner:** `config/` directory
> **Canonical Spec:** [docs/spec/SYSTEM.md](../docs/spec/SYSTEM.md)

## Purpose

Define all configuration for video generation including mood presets, default values, and journey curves.

## Files

| File | Purpose |
|------|---------|
| `defaults.yaml` | System-wide defaults |
| `moods.yaml` | 8 mood presets |
| `journeys.py` | 7 journey curve definitions |

## defaults.yaml Schema

```yaml
video:
  resolution:
    width: 1920
    height: 1080
  fps: 30
  codec: "libx264"
  crf: 23

audio:
  sample_rate: 44100
  channels: 2
  format: "wav"

output:
  directory: "./output"
  filename_pattern: "{mood}_{duration}s_{timestamp}"
```

## moods.yaml Schema

```yaml
mood_name:
  # Audio settings
  audio:
    tempo: 60
    binaural_freq: 10
    sine_freq: 432
    rhythm_pattern: "gnawa"
    rhythm_volume: 0.5
    drone_volume: 1.0
    melody_enabled: true
    arpeggio_enabled: true
  
  # Visual settings
  visual:
    pattern: "fractal_zoom"
    speed: 0.5
    complexity: 0.7
    symmetry: 4
    colors:
      primary: [100, 100, 200]
      secondary: [50, 50, 100]
      accent: [200, 150, 255]
  
  # Journey (optional)
  journey: "steady"
  journey_intensity: "moderate"
  
  # Metadata
  metadata:
    title_template: "{mood} - {duration} Ambient"
    description_template: "..."
    tags: ["ambient", "meditation", ...]
```

## journeys.py Schema

```python
JOURNEY_PRESETS = {
    'preset_name': {
        'name': 'Human Readable Name',
        'description': 'What this journey does',
        'tempo': lambda base: (lambda t: curve_function(t, base)),
        'speed': lambda base: (lambda t: curve_function(t, base)),
        'complexity': lambda base: (lambda t: curve_function(t, base)),
    }
}
```

## Available Journeys

| Journey | Tempo Curve | Speed Curve | Complexity Curve |
|---------|-------------|-------------|------------------|
| `steady` | Constant | Constant | Constant |
| `awakening` | 60%→130% | 40%→120% | 50%→100% |
| `deep_dive` | 110%→70% | 100%→30% | 100%→60% |
| `breathing` | ±30% sine | ±30% sine | Constant |
| `crescendo` | 70%→140%→80% | Arc | Arc |
| `trance` | 85%→115% | Slow rise | Slow rise |
| `waves` | ±25% slow | ±25% slow | ±15% slow |

## Config Resolution Order

1. **Runtime args** - Highest priority
2. **Workflow inputs** - GitHub Actions inputs
3. **Mood preset** - From moods.yaml
4. **Defaults** - From defaults.yaml

## Art Period Presets (Workflow)

Art Creator workflow defines additional presets:

| Period | Colors | Speed | Complexity | Pattern |
|--------|--------|-------|------------|---------|
| `cave_art` | Earth tones | 0.25 | 0.4 | sacred_geometry |
| `ancient` | Gold/jewel | 0.35 | 0.5 | sacred_geometry |
| `medieval` | Deep rich | 0.3 | 0.6 | geometric_morph |
| `renaissance` | Warm natural | 0.4 | 0.7 | fibonacci_spiral |
| `baroque` | Dramatic | 0.55 | 0.8 | geometric_morph |
| `impressionist` | Soft pastel | 0.45 | 0.6 | particle_flow |
| `modern` | Bold | 0.5 | 0.7 | fractal_zoom |
| `contemporary` | Mixed | 0.6 | 0.75 | particle_flow |
| `future` | Neon | 0.7 | 0.85 | fractal_zoom |

## Validation Rules

| Field | Valid Range | Default |
|-------|-------------|---------|
| `tempo` | 20-200 BPM | 60 |
| `binaural_freq` | 0.5-100 Hz | 10 |
| `sine_freq` | 100-1000 Hz | 432 |
| `speed` | 0.1-1.0 | 0.5 |
| `complexity` | 0.1-1.0 | 0.7 |
| `rhythm_volume` | 0.0-1.0 | 0.5 |
| `drone_volume` | 0.0-1.0 | 1.0 |

## Adding a New Mood

1. Add entry to `moods.yaml`
2. Test with `python run_job.py --mood new_mood --duration 30`
3. Update docs if public-facing

## Adding a New Journey

1. Add entry to `journeys.py` JOURNEY_PRESETS
2. Define tempo, speed, complexity curves
3. Test with Art Creator workflow
4. Update `docs/ART_CREATOR.md`

