# Living Ambient Engine

Automated hypnotic video factory for YouTube monetization.

> **New User?** Start here: [📚 Getting Started Guide](docs/GETTING_STARTED.md) | [⚡ Quick Reference](docs/QUICK_REFERENCE.md) | [❓ FAQ](docs/FAQ.md)

## What It Does

Generates ambient videos with:
- 🌀 **Fractal visuals** - Mandelbrot/Julia zooms with psychedelic color cycling
- 🥁 **Tribal rhythms** - 8 authentic patterns (Bamboula, Kuku, Gnawa, etc.)
- 🧠 **Brainwave entrainment** - Binaural beats tuned to Delta/Theta/Alpha/Beta/Gamma
- 🎵 **Solfeggio frequencies** - 432Hz, 528Hz, 639Hz healing tones

## Quick Start

```bash
# Clone and setup
git clone https://github.com/peterkrentel/living-ambient-engine.git
cd living-ambient-engine
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Try interactive examples
python examples.py

# Or generate a video directly
python run_job.py --mood trance --duration 60
```

**Or use GitHub Codespaces** - click "Code" → "Codespaces" → "Create codespace"

## Commands

```bash
# Single video
python run_job.py --mood deep_focus --duration 300

# Batch generation  
python batch_generate.py --moods all --durations 1h,2h

# Upload to YouTube
python youtube_upload.py --batch ./batch_output
```

## 8 Mood Presets

| Mood | Brainwave | Frequency | Rhythm |
|------|-----------|-----------|--------|
| `deep_focus` | 40Hz Gamma | 432Hz | Taiko |
| `sleep` | 2Hz Delta | 528Hz | Heartbeat |
| `chill` | 10Hz Alpha | 639Hz | Gamelan |
| `study` | 12Hz Alpha | 432Hz | Taiko |
| `trance` | 6Hz Theta | 528Hz | Gnawa |
| `energize` | 25Hz Beta | 741Hz | Kuku |
| `ceremony` | 7Hz Theta | 528Hz | Candomble |
| `warrior` | 20Hz Beta | 741Hz | Burundi |

## Content Factory (CI/CD)

Automated pipeline via GitHub Actions:
1. **Scheduled generation** - Daily at 2 AM UTC
2. **Batch processing** - Multiple moods x durations
3. **Auto-upload** - Direct to YouTube with SEO

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for diagrams.

## Project Structure

```
run_job.py           # Single video CLI
batch_generate.py    # Batch generation
youtube_upload.py    # YouTube upload CLI
audio/               # Audio synthesis
visuals/             # Fractal/geometry generation  
render/              # FFmpeg pipeline
config/moods.yaml    # Mood presets
.github/workflows/   # CI/CD automation
```

## Setup YouTube API (one-time)

1. Go to console.cloud.google.com
2. Create project, enable "YouTube Data API v3"
3. Create OAuth2 credentials (Desktop app)
4. Download client_secrets.json to project root
5. Run: python youtube_upload.py --auth
6. Add token to GitHub Secrets as YOUTUBE_TOKEN_B64

See [docs/youtube-auth.md](docs/youtube-auth.md) for detailed instructions.

## Documentation

- 📚 **[Getting Started Guide](docs/GETTING_STARTED.md)** - Complete tutorial with examples
- ⚡ **[Quick Reference](docs/QUICK_REFERENCE.md)** - Command cheat sheet
- ❓ **[FAQ](docs/FAQ.md)** - Common questions answered
- 💡 **[Use Cases](docs/USE_CASES.md)** - Real-world applications
- 🏗️ **[Architecture](docs/architecture.md)** - System design and diagrams
- 📺 **[YouTube Setup](docs/youtube-auth.md)** - Authentication guide
- 🗺️ **[Master Plan](docs/master-plan.md)** - Roadmap and milestones
- 🤝 **[Contributing](CONTRIBUTING.md)** - How to contribute

## What Can I Do With This?

**Living Ambient Engine helps you:**
- ✅ Generate professional ambient videos for YouTube
- ✅ Create content for meditation, focus, sleep niches
- ✅ Automate video production with CI/CD
- ✅ Monetize through YouTube Partner Program
- ✅ Build a passive income content library

**Perfect for:**
- Content creators looking to scale
- Meditation/wellness creators
- YouTube automation enthusiasts
- Anyone interested in algorithmic art

👉 **[See What You Can Create →](docs/GETTING_STARTED.md#examples-gallery)**

## License

MIT - See LICENSE

