# Quick Reference Guide

## Essential Commands

### Generate Single Video
```bash
python run_job.py --mood <mood> --duration <seconds>
```

### Batch Generate
```bash
python batch_generate.py --moods <mood1,mood2> --durations <duration1,duration2>
```

### Upload to YouTube
```bash
python youtube_upload.py --file <path/to/video.mp4>
```

---

## Mood Options

| Mood | Use Case | Brainwave | Frequency |
|------|----------|-----------|-----------|
| `deep_focus` | Work, coding | 40Hz Gamma | 432Hz |
| `sleep` | Bedtime | 2Hz Delta | 528Hz |
| `chill` | Relaxation | 10Hz Alpha | 639Hz |
| `study` | Learning | 12Hz Alpha | 432Hz |
| `trance` | Meditation | 6Hz Theta | 528Hz |
| `energize` | Morning boost | 25Hz Beta | 741Hz |
| `ceremony` | Spiritual | 7Hz Theta | 528Hz |
| `warrior` | Motivation | 20Hz Beta | 741Hz |

---

## Duration Formats

| Format | Meaning | Seconds |
|--------|---------|---------|
| `30s` | 30 seconds | 30 |
| `5m` | 5 minutes | 300 |
| `30m` | 30 minutes | 1800 |
| `1h` | 1 hour | 3600 |
| `2h30m` | 2.5 hours | 9000 |

Or use raw seconds: `--duration 600`

---

## Journey Presets (Art Creator)

Dynamic audio-visual evolution over time:

| Journey | Effect |
|---------|--------|
| `steady` | Constant tempo/speed (default) |
| `awakening` | Gradual rise from stillness to energy |
| `deep_dive` | Descending into calm (sleep prep) |
| `breathing` | Rhythmic oscillation (breathing sync) |
| `crescendo` | Build to peak then release |
| `trance` | Slow hypnotic build |
| `waves` | Long slow swells like ocean |

**Intensity Options:** `subtle` (±10%), `moderate` (±20%), `dramatic` (±30%)

---

## Common Examples

### Quick Test (30 seconds)
```bash
python run_job.py --mood trance --duration 30
```

### Standard Video (1 hour)
```bash
python run_job.py --mood deep_focus --duration 3600
```

### Long Form (2 hours)
```bash
python run_job.py --mood sleep --duration 7200
```

### Generate All Moods (1 hour each)
```bash
python batch_generate.py --moods all --durations 1h
```

### Multiple Durations
```bash
python batch_generate.py --moods sleep,study --durations 30m,1h,2h
```

---

## File Locations

### Input
- `config/moods.yaml` - Mood configurations
- `audio/` - Audio synthesis code
- `visuals/` - Visual generation code
- `render/` - FFmpeg rendering

### Output (default)
- `output/video_<timestamp>.mp4` - Generated video
- `output/thumbnail_<timestamp>.png` - Thumbnail
- `output/metadata_<timestamp>.json` - Metadata

### Batch Output
- `batch_output/<mood>_<duration>/` - Per-video folders

---

## CLI Options

### run_job.py
```bash
python run_job.py [OPTIONS]

Options:
  --mood TEXT           Mood preset (required)
  --duration INTEGER    Duration in seconds (required)
  --output PATH         Output directory (default: ./output)
  --verbose            Enable detailed logging
  --dry-run            Test without rendering
  --help               Show help message
```

### batch_generate.py
```bash
python batch_generate.py [OPTIONS]

Options:
  --moods TEXT          Comma-separated moods or "all" (required)
  --durations TEXT      Comma-separated durations (required)
  --output PATH         Output directory (default: ./batch_output)
  --parallel INTEGER    Number of parallel jobs (default: 1)
  --help               Show help message
```

### youtube_upload.py
```bash
python youtube_upload.py [OPTIONS]

Options:
  --auth                Authenticate with YouTube
  --file PATH           Video file to upload
  --batch PATH          Batch directory to upload
  --title TEXT          Custom video title
  --description TEXT    Custom description
  --category ID         YouTube category ID (default: 10)
  --privacy TEXT        Privacy status (public/private/unlisted)
  --help               Show help message
```

---

## Troubleshooting Quick Fixes

### "FFmpeg not found"
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Permission denied"
```bash
chmod +x run_job.py batch_generate.py youtube_upload.py
```

### Clear output directory
```bash
rm -rf output/*
rm -rf batch_output/*
```

---

## Performance Tips

### Speed Up Rendering
- Use shorter durations for testing (`--duration 30`)
- Lower resolution in config (720p instead of 1080p)
- Reduce framerate (24fps instead of 30fps)

### Save Disk Space
- Delete old videos: `rm output/*.mp4`
- Compress with higher CRF: Edit FFmpeg settings in `render/`
- Use batch folders: Automatic organization

### Batch Efficiently
```bash
# Generate overnight
nohup python batch_generate.py --moods all --durations 1h,2h &

# Check progress
tail -f nohup.out
```

---

## Environment Variables

Create `.env` file in project root:

```bash
# YouTube API (optional)
YOUTUBE_CLIENT_SECRETS_FILE=client_secrets.json
YOUTUBE_TOKEN_FILE=youtube_token.json

# Output settings
DEFAULT_OUTPUT_DIR=./output
DEFAULT_RESOLUTION=1280x720
DEFAULT_FPS=30

# Render settings
FFMPEG_THREADS=4
FFMPEG_CRF=23
```

---

## Git Commands

### Check Status
```bash
git status
git log --oneline -10
```

### Update Repository
```bash
git pull origin main
```

### Create Branch
```bash
git checkout -b feature/my-feature
```

---

## One-Liners

### Generate and upload immediately
```bash
python run_job.py --mood sleep --duration 3600 && python youtube_upload.py --file output/*.mp4
```

### Batch all moods, short durations
```bash
python batch_generate.py --moods all --durations 5m
```

### Test all moods quickly
```bash
for mood in deep_focus sleep chill study trance energize ceremony warrior; do
  python run_job.py --mood $mood --duration 30
done
```

---

## Keyboard Shortcuts

When running scripts:
- `Ctrl+C` - Stop current job
- `Ctrl+Z` - Pause job (then `bg` to resume)
- `Ctrl+D` - Exit interactive prompt

---

## Resources

- [Full Documentation](GETTING_STARTED.md)
- [Architecture](architecture.md)
- [YouTube Setup](youtube-auth.md)
- [Master Plan](master-plan.md)
- [GitHub Repo](https://github.com/peterkrentel/living-ambient-engine)

---

**Pro Tip:** Bookmark this page for quick command lookup! 🔖
