# Master Plan

> **Reality check (2026-04):** Ledger + CI + **dual-metrics** correlate + **catalog backfill** are on **`main`**. **Brand** analytics (`data/analytics.json`) vs **mixed** `content_catalog.json` is documented in [`START_HERE.md`](START_HERE.md). Next product forks: **channel-tagged / split catalog**, optional **gated production planner**, **personal** analytics — see [`HANDOFF.md`](HANDOFF.md).

## Status Overview

| Milestone | Status | Notes |
|-----------|--------|-------|
| 1. MVP | ✅ DONE | Local pipeline works |
| 2. YouTube Publishing | ✅ DONE | Uploader + GitHub Actions |
| 3. Go Live | ✅ DONE | Pipeline tested, uploads work |
| 4. Production Channel | ✅ DONE | Brand account configured |
| 5. Spec-Driven Development | ✅ DONE | Specs, guardrails, contracts, enforcement |
| 5b. Brand data loop (ledger + analytics) | 🔄 In progress | `generations.json` on `main`, CI commits, `correlate.py` retention + watch min, backfill from catalog; audit join = **brand overlap** until catalog split / personal fetch |
| 6. SEO & Scheduling | ⬜ TODO | Optimize titles/moods for search, smarter schedule |
| 7. Content Quality | ⬜ TODO | Better audio/visuals, smaller files |
| 8. AI Melody Agent | ⬜ TODO | AI-generated ambient melodies |
| 9. Shorts | ⬜ TODO | Auto-cut from long videos |

---

## Milestone 1 — MVP ✅

- [x] Public repo + MIT license + .gitignore + .env.example
- [x] Visual generator (fractals, sacred geometry)
- [x] Audio generator (tribal drums, binaural beats, solfeggio)
- [x] FFmpeg render to final.mp4
- [x] CLI: run_job.py --mood deep_focus --duration 120
- [x] Metadata JSON + thumbnail PNG

## Milestone 2 — YouTube Publishing ✅

- [x] YouTube uploader module (OAuth via secrets)
- [x] Title/description/SEO templating
- [x] batch_generate.py for bulk generation
- [x] GitHub Actions workflow (daily 2AM UTC + manual)
- [x] Codespaces config for cloud dev

## Milestone 3 — Go Live ✅

- [x] Google Cloud project + OAuth2 credentials
- [x] Run youtube_upload.py --auth locally
- [x] Add YOUTUBE_TOKEN_PICKLE + YOUTUBE_CLIENT_SECRETS to GitHub Secrets
- [x] Test GitHub Actions with manual trigger
- [x] First test upload (30s × 3 moods)

## Milestone 4 — Production Channel ✅

- [x] Create brand account / dedicated channel
- [x] Add new email as test user in GCP
- [x] Re-run OAuth flow with new account
- [x] Update GitHub secrets with new token
- [x] Delete test videos from personal channel

## Milestone 5 — Spec-Driven Development ✅

- [x] Create specs for all components (`*/SPEC.md`)
- [x] Define guardrails (`docs/spec/GUARDRAILS.md`)
- [x] Add contract tests (`tests/contracts/`)
- [x] CI enforcement (`spec-validation`, `contract-tests` jobs)
- [x] Workflow contract (`docs/spec/workflows.md`)
- [x] Memory guardrail to prevent OOM

## Milestone 6 — SEO & Scheduling ⬜

Optimize for discoverability and consistent publishing.

- [ ] Research high-volume ambient/sleep/focus search terms
- [ ] Map moods to SEO-optimized titles (e.g., "rain sleep" → "Rain Sounds for Deep Sleep | 3 Hours")
- [ ] Review schedule timing (2AM UTC when personal `content-factory` cron is re-enabled — is it optimal for target audience?)
- [ ] Consider upload frequency vs. quality tradeoff
- [ ] Add tags/keywords based on search data

## Milestone 7 — Content Quality ⬜

- [ ] Optimize file size (720p, lower framerate, CRF tuning)
- [ ] Improve visuals (colors, patterns, smoother animation)
- [ ] Improve audio (layering, textures, fade in/out)
- [ ] Add CLI progress bar (tqdm)

## Milestone 8 — AI Melody Agent ⬜

- [ ] Research AI music generation (Suno, MusicGen, etc.)
- [ ] Integrate melody generation into pipeline
- [ ] Layer melodies with binaural beats
- [ ] Mood-specific musical themes

## Milestone 9 — Shorts ⬜

- [ ] Auto-cut 15-60s clips from long videos
- [ ] Vertical crop + encode (9:16)
- [ ] Shorts upload with linking

---

## Secrets Policy

Hard rule: Secrets never enter git history.

| Environment | Method |
|-------------|--------|
| Local | .env file (gitignored) |
| GitHub Actions | Repository Secrets |
| Codespaces | Environment Secrets |

Required secrets (see repo Settings → Secrets): **`YOUTUBE_CLIENT_SECRETS`**, **`YOUTUBE_TOKEN_PICKLE`** (personal), **`YOUTUBE_TOKEN_PICKLE_BRAND`** (brand). Tokens are stored **base64-encoded** in GitHub — not a single `YOUTUBE_TOKEN_B64` name unless you named one that way locally.

---

## Deployment: GitHub Actions

Using GitHub Actions (free tier):
- 2000 min/month for private repos
- Unlimited for public repos
- 6-hour job limit (enough for 2-4 hour videos)

**Workflow map:** [`docs/spec/workflows.md`](spec/workflows.md) (eight files). In short:

| Workflow | Role |
|----------|------|
| `content-factory.yml` | Personal channel factory (**cron off** in YAML; manual) |
| `content-factory-brand.yml` | Brand factory (manual) |
| `content-factory-brand-batch.yml` | Brand SEO mood batch |
| `piano-batch.yml` | Piano batch (uses **personal** token today) |
| `art-creator.yml` / `art-creator-batch.yml` | Custom / matrix art → optional **brand** upload |
| `analytics-agent.yml` | **Brand** metrics → `data/analytics.json`, reports, correlate, audit |
| `test-art-creator.yml` | PR + manual CI gate |

---

*Last reviewed: 2026-04-16 — align with `START_HERE`, `HANDOFF`, and `spec/workflows.md`.*
