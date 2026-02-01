# Master Plan

## Status Overview

| Milestone | Status | Notes |
|-----------|--------|-------|
| 1. MVP | ✅ DONE | Local pipeline works |
| 2. YouTube Publishing | ✅ DONE | Uploader + GitHub Actions |
| 3. Go Live | ✅ DONE | Pipeline tested, uploads work |
| 4. Production Channel | ✅ DONE | Brand account configured |
| 5. Spec-Driven Development | ✅ DONE | Specs, guardrails, contracts, enforcement |
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
- [ ] Review schedule timing (2AM UTC - is this optimal for target audience?)
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

Required secret: YOUTUBE_TOKEN_B64 (Base64-encoded OAuth token)

---

## Deployment: GitHub Actions

Using GitHub Actions (free tier):
- 2000 min/month for private repos
- Unlimited for public repos
- 6-hour job limit (enough for 2-4 hour videos)

Workflow: .github/workflows/content-factory.yml
- Cron: Daily 2 AM UTC
- Manual: workflow_dispatch with mood/duration inputs
