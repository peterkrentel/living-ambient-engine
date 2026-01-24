# Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTENT FACTORY                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │  Config  │───▶│  Engine  │───▶│  Output  │              │
│  │moods.yaml│    │          │    │  .mp4    │              │
│  └──────────┘    │ ┌──────┐ │    │  .json   │              │
│                  │ │Visual│ │    │  .png    │              │
│                  │ └──────┘ │    └────┬─────┘              │
│                  │ ┌──────┐ │         │                    │
│                  │ │Audio │ │         ▼                    │
│                  │ └──────┘ │    ┌──────────┐              │
│                  │ ┌──────┐ │    │ YouTube  │              │
│                  │ │Render│ │    │ Upload   │              │
│                  │ └──────┘ │    └──────────┘              │
│                  └──────────┘                              │
└─────────────────────────────────────────────────────────────┘
```

## Pipeline Flow

```
Trigger (Cron/Manual)
        │
        ▼
┌───────────────────┐
│  GitHub Actions   │
│  content-factory  │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ batch_generate.py │  ← Generates N videos
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ youtube_upload.py │  ← Uploads with SEO
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│    YouTube        │  ← Revenue 💰
└───────────────────┘
```

## Brainwave Mapping

| State | Hz Range | Mood | Effect |
|-------|----------|------|--------|
| Delta | 0.5-4 | sleep | Deep sleep |
| Theta | 4-8 | trance, ceremony | Meditation |
| Alpha | 8-14 | chill, study | Relaxed focus |
| Beta | 14-30 | energize, warrior | Active focus |
| Gamma | 30-100 | deep_focus | Peak performance |

## Solfeggio Frequencies

| Hz | Name | Used In |
|----|------|---------|
| 174 | Pain relief | sleep |
| 432 | Natural calm | study, deep_focus |
| 528 | Love/healing | sleep, trance |
| 639 | Harmony | chill |
| 741 | Awakening | energize, warrior |

## File Structure

```
living-ambient-engine/
├── run_job.py           # Single video CLI
├── batch_generate.py    # Batch generation
├── youtube_upload.py    # YouTube upload
│
├── audio/
│   └── generator.py     # Drums, binaural, solfeggio
│
├── visuals/
│   └── generator.py     # Fractals, geometry, effects
│
├── render/
│   └── renderer.py      # FFmpeg pipeline
│
├── orchestrator/
│   └── orchestrator.py  # Coordinates all modules
│
├── youtube/
│   └── uploader.py      # YouTube API client
│
├── config/
│   ├── moods.yaml       # 8 mood presets
│   └── defaults.yaml    # Resolution, FPS, etc.
│
└── .github/workflows/
    └── content-factory.yml  # CI/CD automation
```

## GitHub Secrets Required

| Secret | Description |
|--------|-------------|
| `YOUTUBE_TOKEN_B64` | Base64-encoded OAuth token |
| `GOOGLE_CLIENT_ID` | OAuth client ID (optional) |
| `GOOGLE_CLIENT_SECRET` | OAuth client secret (optional) |

