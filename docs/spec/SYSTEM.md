# System Specification

> **Canonical spec for Living Ambient Engine.** All component specs reference this document.
> Changes to cross-component behavior require updates here first.

## Overview

**Living Ambient Engine** is a procedural ambient audiovisual generator that produces long-form, continuously evolving, non-repeating videos for YouTube monetization.

### Core Value Proposition

- **Automated content generation** - No manual editing required
- **Infinite uniqueness** - Every video is procedurally unique
- **YouTube-optimized** - Metadata, thumbnails, SEO built-in
- **Dual-channel support** - Personal and brand channel workflows

## Glossary

| Term | Definition |
|------|------------|
| **Mood** | A preset configuration defining audio/visual parameters (e.g., `deep_focus`, `sleep`) |
| **Journey** | Dynamic evolution of tempo/speed/complexity over time |
| **Art Period** | Historical art style preset defining colors, patterns, complexity |
| **Binaural Beat** | Audio frequency difference between ears for brainwave entrainment |
| **Solfeggio** | Ancient healing frequency (174Hz, 432Hz, 528Hz, etc.) |
| **Phase** | Audio evolution stage (settle → drift → deepen → resolve) |
| **Seed** | Random seed for reproducible generation |

## Component Boundaries

```
┌─────────────────────────────────────────────────────────────────┐
│                        ENTRY POINTS                              │
│  run_job.py │ batch_generate.py │ GitHub Actions Workflows       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATOR                                │
│  orchestrator/orchestrator.py                                    │
│  - Coordinates all generation                                    │
│  - Applies mood/journey config                                   │
│  - Manages temp files and output                                 │
└───────┬─────────────────┬─────────────────┬────────────────────┘
        │                 │                 │
        ▼                 ▼                 ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│    AUDIO      │ │    VISUAL     │ │    RENDER     │
│ audio/        │ │ visuals/      │ │ render/       │
│ - Drums       │ │ - Fractals    │ │ - FFmpeg      │
│ - Binaural    │ │ - Geometry    │ │ - Thumbnails  │
│ - Melody      │ │ - Particles   │ │               │
│ - Journey     │ │ - Journey     │ │               │
└───────────────┘ └───────────────┘ └───────────────┘
        │                 │                 │
        └─────────────────┴─────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                       YOUTUBE                                    │
│  youtube/uploader.py                                             │
│  - OAuth2 authentication                                         │
│  - Upload with metadata                                          │
│  - Dual channel support                                          │
└─────────────────────────────────────────────────────────────────┘
```

## Invariants (Must Always Be True)

1. **No hardcoded secrets** - All credentials via environment variables or GitHub secrets
2. **Reproducible with seed** - Same seed + config = identical output
3. **Graceful degradation** - Missing optional features don't crash generation
4. **Idempotent uploads** - Re-running with same content doesn't create duplicates
5. **Exit codes** - Non-zero exit on failure for CI/CD compatibility

## Data Flow Contracts

### Config → Orchestrator
- Input: mood name OR full config dict
- Orchestrator merges with `config/defaults.yaml` and `config/moods.yaml`
- Journey params flow through to audio/visual generators

### Orchestrator → Audio Generator
- Input: `audio_config` dict, `duration`, `journey`, `journey_intensity`
- Output: WAV file path
- Contract: Audio length matches requested duration ±1 second

### Orchestrator → Visual Generator  
- Input: `visual_config` dict, `duration`, `journey`, `journey_intensity`
- Output: MP4 file path (video only, no audio)
- Contract: Video length matches requested duration, FPS matches config

### Render → Final Output
- Input: Video MP4 + Audio WAV
- Output: Combined MP4 with audio
- Contract: Output is valid MP4, playable in standard players

### YouTube Uploader
- Input: MP4 file, metadata dict, channel selection
- Output: YouTube video ID or error
- Contract: Respects quota limits, retries on transient failures

## File Ownership

| Path | Owner | Spec Location |
|------|-------|---------------|
| `audio/` | Audio Generator | `audio/SPEC.md` |
| `visuals/` | Visual Generator | `visuals/SPEC.md` |
| `orchestrator/` | Orchestrator | `orchestrator/SPEC.md` |
| `youtube/` | YouTube Uploader | `youtube/SPEC.md` |
| `config/` | Configuration | `config/SPEC.md` |
| `render/` | FFmpeg Renderer | `render/SPEC.md` |
| `.github/workflows/` | CI/CD | `docs/spec/workflows.md` |

## Branch Strategy

| Branch | Purpose | Deploys To |
|--------|---------|------------|
| `main` | Production-ready code | YouTube (via workflows) |
| `feature/*` | Feature development | None (PR required) |

## Change Management

### Spec-First Rule
> **Any change to cross-component behavior requires a spec update in the same PR.**

Examples requiring spec updates:
- New config parameters that affect multiple components
- Changes to data flow between components
- New invariants or removal of existing ones
- Workflow input/output changes

### PR Checklist
See `CONTRIBUTING.md` for the required checklist including spec verification.

## Related Specs

- [Audio Generator Spec](../../audio/SPEC.md)
- [Visual Generator Spec](../../visuals/SPEC.md)
- [Orchestrator Spec](../../orchestrator/SPEC.md)
- [YouTube Uploader Spec](../../youtube/SPEC.md)
- [Configuration Spec](../../config/SPEC.md)
- [Workflow Spec](./workflows.md)
- [Contracts](./contracts/)

