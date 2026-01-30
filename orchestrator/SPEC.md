# Orchestrator Specification

> **Owner:** `orchestrator/` directory
> **Canonical Spec:** [docs/spec/SYSTEM.md](../docs/spec/SYSTEM.md)

## Purpose

Coordinate the complete video generation pipeline: load config, generate audio, generate visuals, combine with FFmpeg, create thumbnails, and produce final output.

## Public Interface

```python
class Orchestrator:
    def __init__(self, config_path: str = None)
    
    def generate(self,
                 mood: str,
                 duration: int,
                 output_dir: str = "./output",
                 seed: int = None,
                 rhythm_volume: float = None,
                 drone_volume: float = None) -> Dict
```

## Pipeline Flow

```
1. Load Config
   ├── Read defaults.yaml
   ├── Read moods.yaml
   └── Merge with runtime overrides

2. Setup
   ├── Create temp directory
   ├── Initialize seed (random or provided)
   └── Extract journey parameters

3. Generate Components (parallel-capable)
   ├── AudioGenerator.generate() → audio.wav
   └── VisualGenerator.generate() → visual.mp4

4. Combine
   └── FFmpeg merge audio + video → final.mp4

5. Post-process
   ├── Generate thumbnail
   ├── Write metadata JSON
   └── Cleanup temp files

6. Return
   └── Dict with paths and metadata
```

## Config Resolution

Priority (highest to lowest):
1. Runtime parameters (function arguments)
2. Mood preset (`config/moods.yaml`)
3. Defaults (`config/defaults.yaml`)

## Journey Parameter Flow

```python
# Extract from mood config
journey = mood_config.get('journey', 'steady')
journey_intensity = mood_config.get('journey_intensity', 'moderate')

# Pass to generators
AudioGenerator(..., journey=journey, journey_intensity=journey_intensity)
VisualGenerator(..., journey=journey, journey_intensity=journey_intensity)
```

## Output Structure

```python
{
    'video_path': '/path/to/output/mood_duration_timestamp.mp4',
    'thumbnail_path': '/path/to/output/mood_duration_timestamp.png',
    'metadata_path': '/path/to/output/mood_duration_timestamp.json',
    'seed': 1234567890,
    'duration': 300,
    'mood': 'deep_focus'
}
```

## Acceptance Criteria

- [ ] Final video has both audio and video tracks
- [ ] Video duration matches requested
- [ ] Thumbnail is generated and valid PNG
- [ ] Metadata JSON contains all generation parameters
- [ ] Temp files are cleaned up on success
- [ ] Seed is recorded for reproducibility

## Error Handling

| Condition | Behavior |
|-----------|----------|
| Unknown mood | Raise ValueError |
| Audio generation fails | Raise, cleanup temp |
| Visual generation fails | Raise, cleanup temp |
| FFmpeg fails | Raise with FFmpeg error |
| Disk full | Raise IOError |

## Dependencies

- `audio.generator.AudioGenerator`
- `visuals.generator.VisualGenerator`
- `render.renderer` (FFmpeg wrapper)
- `PyYAML` - Config loading

## Files

| File | Purpose |
|------|---------|
| `orchestrator.py` | Main Orchestrator class |
| `__init__.py` | Package exports |

## Testing

```bash
# Quick test (30 second video)
python run_job.py --mood trance --duration 30

# Verify output
ls -la output/
```

## Future Enhancements

- [ ] Parallel audio/visual generation
- [ ] Progress callbacks
- [ ] Resume from checkpoint
- [ ] Streaming output

