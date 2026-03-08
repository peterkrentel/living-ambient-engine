# 🎹 Piano Batch Generator - Quick Start Guide

## What It Does

Automatically generates **6 piano relaxation videos** in one click:

| Duration | Versions | Total |
|----------|----------|-------|
| 1 hour   | Ambience + Melody | 2 videos |
| 3 hours  | Ambience + Melody | 2 videos |
| 4 hours  | Ambience + Melody | 2 videos |
| **TOTAL** | | **6 videos** |

## Video Titles Generated

- ✅ "Let Go of Stress | 1 Hour Soft Piano | Gently Evolving Melodies"
- ✅ "Let Go of Stress | 1 Hour Soft Piano [Pure Ambience]"
- ✅ "Let Go of Stress | 3 Hours Soft Piano | Gently Evolving Melodies"
- ✅ "Let Go of Stress | 3 Hours Soft Piano [Pure Ambience]"
- ✅ "Let Go of Stress | 4 Hours Soft Piano | Gently Evolving Melodies"
- ✅ "Let Go of Stress | 4 Hours Soft Piano [Pure Ambience]"

## How to Run (100% Automated)

### Step 1: Go to GitHub Actions

1. Open your browser to: `https://github.com/peterkrentel/living-ambient-engine/actions/workflows/piano-batch.yml`
2. Click the **"Run workflow"** button (top right)
3. Leave "Upload to YouTube" **checked** ✅
4. Click **"Run workflow"** (green button)

### Step 2: Wait for Completion

The workflow will automatically:
- ✅ Generate all 6 videos (1-2 hours total)
- ✅ Upload them to YouTube
- ✅ Apply SEO-optimized titles, descriptions, and tags
- ✅ Update your content catalog
- ✅ Commit the catalog to your repository

### Step 3: Done!

Your videos will be live on YouTube, ready to publish!

## What Each Video Contains

### Audio Features
- 🎹 Soft piano melodies (Lydian scale - dreamy, peaceful)
- 🧠 Theta waves (6 Hz) for deep relaxation
- 🎵 Very slow tempo (50 BPM)
- ✨ Never-repeating, evolving soundscape
- 🔇 No percussion/drums

### Visual Features
- 🌌 Deep blue starfield
- 💫 Slow, gentle movement
- 🎨 Calming colors
- 📺 640x480 resolution (optimized for ambient)

### SEO Optimization
- **Tags**: #PianoMusic #RelaxingPiano #StressRelief #PeacefulMusic #CalmPiano #Meditation
- **Description**: Professional, SEO-optimized with call-to-action
- **Category**: Music

## Expected Timeline

| Phase | Duration |
|-------|----------|
| Setup | ~2 minutes |
| 1h videos (2x) | ~15-20 minutes |
| 3h videos (2x) | ~30-40 minutes |
| 4h videos (2x) | ~40-50 minutes |
| Upload | ~10-15 minutes |
| **TOTAL** | **~1.5-2 hours** |

## Monitoring Progress

1. Click on the running workflow in GitHub Actions
2. Watch the live logs for each step
3. See the summary at the end with all video titles

## Troubleshooting

### If the workflow fails:
1. Check the error logs in GitHub Actions
2. Verify your YouTube credentials are set up correctly
3. Ensure you have enough YouTube API quota

### If you want to generate without uploading:
1. Uncheck "Upload to YouTube" when running the workflow
2. Videos will be saved as artifacts (downloadable for 7 days)

## Customization

Want different durations? Edit `.github/workflows/piano-batch.yml`:

```yaml
# Line 60: Change durations here
--durations 1h,3h,4h \
```

Change to any combination:
- `30s` - Quick test
- `10min` - Short video
- `1h` - 1 hour
- `3h` - 3 hours
- `4h` - 4 hours (maximum)

Example: `--durations 1h,2h,3h,4h` would generate 8 videos (4 durations × 2 versions)

## Next Steps

After your videos are uploaded:
1. Check your YouTube channel
2. Review the titles and descriptions
3. Publish the videos (they're uploaded as unlisted by default)
4. Monitor performance in YouTube Analytics

## Support

Questions? Check:
- Main docs: `docs/spec/workflows.md`
- Mood config: `config/moods.yaml`
- Workflow file: `.github/workflows/piano-batch.yml`

