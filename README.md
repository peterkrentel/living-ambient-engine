# Living Ambient Engine

**Automated hypnotic ambient video generation with procedural audio and visuals.**

Generate trance-inducing ambient videos designed to capture attention and induce flow states. Perfect for YouTube content, meditation, focus sessions, and more.

## ✨ Features

- 🎨 **Hypnotic Visuals**: Procedural animations using sacred geometry, fractals, Fibonacci spirals, and particle systems
- 🎵 **Ambient Audio**: Binaural beats, isochronic tones, and layered synthesis tuned to brainwave frequencies
- 🧠 **Psychological Design**: Patterns designed to trigger engagement and trance states
- ⚙️ **Configurable Moods**: Pre-built presets for deep_focus, sleep, chill, study, and energize
- 🚀 **Fully Automated**: One command generates complete MP4 with metadata and thumbnail

## 🎯 Mood Presets

- **deep_focus** - Deep concentration and flow state (40 Hz gamma waves, sacred geometry)
- **sleep** - Deep relaxation and sleep induction (2 Hz delta waves, slow waves)
- **chill** - Relaxed and peaceful state (10 Hz alpha waves, organic flow)
- **study** - Alert focus and learning (14 Hz beta waves, geometric patterns)
- **energize** - Energized and motivated (25 Hz high beta, fractal zoom)

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- FFmpeg (must be installed on your system)

**Install FFmpeg:**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/peterkrentel/living-ambient-engine.git
cd living-ambient-engine
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment (optional):**
```bash
cp .env.example .env
# Edit .env if you want to customize settings
```

### Usage

**List available moods:**
```bash
python run_job.py --list-moods
```

**Generate a video:**
```bash
# 5-minute deep focus video
python run_job.py --mood deep_focus --duration 300

# 10-minute sleep video
python run_job.py --mood sleep --duration 600

# Custom output directory
python run_job.py --mood chill --duration 180 --output ./my_videos
```

**Output:**
- `output/{mood}_{duration}s_{timestamp}.mp4` - Final video
- `output/{mood}_{duration}s_{timestamp}.json` - Metadata
- `output/{mood}_{duration}s_{timestamp}.png` - Thumbnail

## 📁 Project Structure

```
living-ambient-engine/
├── audio/              # Audio generation (binaural beats, synthesis)
├── visuals/            # Visual generation (fractals, sacred geometry)
├── render/             # FFmpeg rendering pipeline
├── orchestrator/       # Main coordination logic
├── config/             # Mood presets and defaults
│   ├── moods.yaml
│   └── defaults.yaml
├── run_job.py          # CLI entry point
├── requirements.txt
└── README.md
```

## 🎨 Customization

Edit `config/moods.yaml` to create your own mood presets or modify existing ones:

```yaml
my_custom_mood:
  description: "My custom mood"
  visual:
    type: "fibonacci_spiral"  # or sacred_geometry, fractal_zoom, etc.
    colors:
      primary: [R, G, B]
      secondary: [R, G, B]
      accent: [R, G, B]
    speed: 0.5
    complexity: 0.7
  audio:
    base_frequency: 40
    binaural_beat: 40
    layers:
      - type: "sine"
        frequency: 432
        amplitude: 0.3
```

## 🔧 Advanced Configuration

Edit `config/defaults.yaml` to change video resolution, FPS, codecs, and more.

## 🛣️ Roadmap

### ✅ Milestone 1 - MVP (Current)
- [x] Procedural visual generation
- [x] Procedural audio generation
- [x] FFmpeg rendering pipeline
- [x] CLI interface
- [x] 5 mood presets

### 🔜 Milestone 2 - YouTube Publishing
- [ ] YouTube Data API integration
- [ ] OAuth authentication
- [ ] Automated upload with scheduling
- [ ] Title/description templating

### 🔮 Milestone 3 - Shorts & Distribution
- [ ] Auto-cut Shorts from long videos
- [ ] Vertical crop and encode
- [ ] Shorts upload automation

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔒 Security

See [SECURITY.md](SECURITY.md) for information on how secrets are handled.

---

— Build + Deploy Plan (with Public Repo)
0) Repo strategy (Day 0)
Repos

Public: living-ambient-engine

Contains all generation + rendering + upload code (no secrets)

Private (recommended): living-ambient-deploy

Infra as code, environment configs, runbooks, CI secrets references

If you want only one repo, keep it public and put infra in /deploy but do not commit any cloud creds or OAuth tokens.

License

MIT (default)

(Optional) Apache 2.0 if you want patent language

Secrets policy (hard rule)

Secrets never enter git history.

Provide .env.example and use:

Local: .env

Prod: cloud secret manager / GitHub Actions secrets

Public repo includes:

.gitignore that blocks .env, token files, credential JSON, output videos.

1) MVP goals (Weeks 1–2)
Ship the first automated end-to-end run locally

Inputs: mood + duration
Outputs: final.mp4 + metadata JSON + thumbnail PNG

Pipeline:

Generate audio (MVP model/API)

Generate visuals (procedural)

Render final MP4 (FFmpeg)

Write metadata (prompts, seed, duration)

(Manual upload for MVP)

2) Automation & publishing (Week 3)
YouTube upload automation (no secrets in repo)

YouTube Data API uploader module

OAuth creds stored in secret manager / GitHub secrets

Support scheduled publish

Modes:

--approve (generate everything, require manual upload/approval)

--auto (auto-upload + schedule)

3) Distribution without spam (Week 4)

Add Shorts pipeline:

Auto-cut 15–60s clips from final

Vertical crop + encode

Upload as Shorts

Explicitly out of scope:

DM-blasting / “poke friends” automation
(spam/ToS risk, account bans, reputation damage)

4) Public repo structure (in the plan)
living-ambient-engine/ (PUBLIC)
├─ README.md
├─ LICENSE (MIT)
├─ architecture/
│  └─ diagram.png
├─ config/
│  ├─ moods.yaml
│  ├─ schedules.yaml
│  └─ defaults.yaml
├─ orchestrator/
├─ audio/
├─ visuals/
├─ render/
├─ upload/
├─ shorts/
├─ scripts/
├─ docker/
├─ .env.example
├─ .gitignore
└─ SECURITY.md (how secrets are handled)

living-ambient-deploy/ (PRIVATE, recommended)
├─ terraform/ or bicep/ or pulumi/
├─ github-actions/
├─ runbooks/
└─ env/

5) GitHub workflow baked in
Issue templates (public repo)

Bug

Feature

“New mood preset”

“Renderer quality”

Project board (optional)

Columns:

Backlog → In Progress → Review → Done

Branch strategy

main protected

PRs required

Releases tagged (v0.1, v0.2)

6) Work breakdown (Augment-ready tickets)
Milestone 1 — Public repo MVP

Create public repo + MIT license + .gitignore + .env.example

Implement job schema + artifact layout

Visual generator (procedural) producing visual.mp4

Audio generator producing audio.wav/mp3

FFmpeg render to final.mp4

CLI: run_job --mood deep_focus --duration 120

Store artifacts + metadata JSON

Milestone 2 — YouTube publishing

YouTube uploader module (OAuth handled via secrets)

Title/description/thumbnail templating

Optional approval gate

Retry/backoff + logging

Milestone 3 — Scheduling + Shorts

Scheduler integration (cloud or GitHub Actions cron)

Shorts cutter + vertical encode

Shorts upload + linking back to long video

7) Deployment options (stays in plan)

Recommended: container + managed scheduler

AWS (ECS/Fargate + EventBridge)

Azure (Container Apps + scheduled job)

GCP (Cloud Run + Cloud Scheduler)

Secrets:

Stored in cloud secret manager and injected at runtime.

Artifacts:

Stored in object storage (S3/Blob/GCS).

If you want, I can also draft the README.md + SECURITY.md + initial GitHub issues list as text you can paste straight into the repo.