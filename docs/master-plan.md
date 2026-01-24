# Master Plan

## Status Overview

| Milestone | Status | Notes |
|-----------|--------|-------|
| 1. MVP | ✅ DONE | Local pipeline works |
| 2. YouTube Publishing | ✅ DONE | Uploader + GitHub Actions |
| 3. Go Live | 🔄 NEXT | YouTube API credentials needed |
| 4. Shorts | ⬜ TODO | Auto-cut from long videos |

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

## Milestone 3 — Go Live 🔄

- [ ] Google Cloud project + OAuth2 credentials
- [ ] Run youtube_upload.py --auth in Codespace
- [ ] Add YOUTUBE_TOKEN_B64 to GitHub Secrets
- [ ] Test GitHub Actions with manual trigger
- [ ] First production upload

## Milestone 4 — Shorts ⬜

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
