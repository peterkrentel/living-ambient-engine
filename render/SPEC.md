# Render Specification

> **Owner:** `render/` directory
> **Canonical Spec:** [docs/spec/SYSTEM.md](../docs/spec/SYSTEM.md)

## Purpose

FFmpeg wrapper for combining audio and video tracks, plus thumbnail generation.

## Public Interface

```python
class Renderer:
    def combine(self, video_path: str, audio_path: str, output_path: str) -> None
    def generate_thumbnail(self, video_path: str, output_path: str, 
                          timestamp: float = None) -> None
```

## FFmpeg Command: Combine

```bash
ffmpeg -y \
  -i {video_path} \
  -i {audio_path} \
  -c:v copy \
  -c:a aac \
  -b:a 192k \
  -shortest \
  {output_path}
```

## FFmpeg Command: Thumbnail

```bash
ffmpeg -y \
  -i {video_path} \
  -ss {timestamp} \
  -vframes 1 \
  -q:v 2 \
  {output_path}
```

## Acceptance Criteria

- [ ] Output MP4 has both video and audio tracks
- [ ] Video codec is preserved (H.264)
- [ ] Audio is AAC at 192kbps
- [ ] Thumbnail is valid JPEG/PNG
- [ ] No FFmpeg errors in output
- [ ] Temp files are not left behind

## Error Handling

| Error | Behavior |
|-------|----------|
| FFmpeg not found | Raise with install instructions |
| Invalid input | Raise ValueError |
| Encoding failure | Raise with FFmpeg stderr |
| Disk full | Raise IOError |

## Dependencies

- `ffmpeg` (system binary, must be in PATH)
- `subprocess` (Python stdlib)

## Files

| File | Purpose |
|------|---------|
| `renderer.py` | Renderer class |
| `__init__.py` | Package exports |

## Installation Check

```bash
# Verify FFmpeg is available
ffmpeg -version

# macOS
brew install ffmpeg

# Ubuntu
sudo apt install ffmpeg
```

## Testing

```bash
# Test combine
python -c "
from render.renderer import Renderer
r = Renderer()
r.combine('video.mp4', 'audio.wav', 'output.mp4')
"

# Test thumbnail
python -c "
from render.renderer import Renderer
r = Renderer()
r.generate_thumbnail('video.mp4', 'thumb.png', timestamp=5.0)
"
```

## Performance Notes

- `-c:v copy` avoids re-encoding video (fast)
- Audio encoding is the main time cost
- Consider `-preset ultrafast` for testing

