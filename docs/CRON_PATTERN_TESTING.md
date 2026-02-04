# Cron Pattern Testing Schedule

## Overview

The `test-art-creator.yml` workflow now runs daily on a cron schedule to automatically test different pattern combinations. This automated testing respects the YouTube API upload limit of 10 uploads per 24 hours by rotating through different pattern subsets each day.

## Schedule

**Cron:** `0 3 * * *` (Daily at 3:00 AM UTC)

## Pattern Rotation Strategy

The workflow automatically rotates through three pattern sets based on the day of the week:

| Day(s) | Pattern Set | Test IDs | Patterns Tested | Upload Count |
|--------|-------------|----------|----------------|--------------|
| Mon, Thu, Sun | **Set 1** | 1-3 | Cave Art, Renaissance, Modern | 3 videos |
| Tue, Fri | **Set 2** | 4-5 | Future, Impressionist | 2 videos |
| Wed, Sat | **Set 3** | 6-7 | Baroque, Medieval | 2 videos |

**Total weekly uploads:** 3×3 + 2×2 + 2×2 = 17 videos/week (~2.4/day average)

This rotation ensures:
- All 7 pattern combinations are tested weekly
- Daily uploads stay well under the 10 uploads/24hr limit
- Different combinations are tested at different times

## Pattern Details

### Set 1 (Patterns 1-3)
1. **Cave Art** - Organic flow, heartbeat rhythm, awakening journey
2. **Renaissance** - Fibonacci spiral, gnawa rhythm, breathing journey
3. **Modern** - Geometric morph, gamelan rhythm, trance journey

### Set 2 (Patterns 4-5)
4. **Future** - Starfield, no percussion, deep dive journey
5. **Impressionist** - Flowing waves, candomble rhythm, waves journey

### Set 3 (Patterns 6-7)
6. **Baroque** - Julia fractal, taiko drums, crescendo journey
7. **Medieval** - Sacred geometry, burundi drums, steady journey

## Automatic vs. Manual Control

### Automatic Mode (Scheduled Runs)
- **Trigger:** Cron schedule at 3 AM UTC
- **Pattern Set:** Rotates by day of week
- **Duration:** 5 minutes (testing quality)
- **Upload:** Yes (to Brand channel)

### Manual Mode (workflow_dispatch)
You can override the automatic behavior:

1. **Pattern Set Options:**
   - `auto` - Use day-of-week rotation (default)
   - `all` - Run all 7 patterns (no upload, for testing)
   - `set1` - Run only patterns 1-3
   - `set2` - Run only patterns 4-5
   - `set3` - Run only patterns 6-7

2. **Duration Options:**
   - `5s` - Fast validation (default for manual)
   - `5min` - Quality test video
   - `10min` - Extended test video

3. **Upload Control:**
   - Check `upload_to_brand` to enable YouTube upload
   - Unchecked by default for manual runs

### Pull Request Mode
- **Pattern Set:** All 7 patterns
- **Duration:** 5 seconds (fast validation)
- **Upload:** No upload

## How It Works

1. **Determine Pattern Set Job**
   - Checks event type (schedule vs. manual vs. PR)
   - For scheduled runs: calculates day of week (1-7)
   - Assigns pattern set based on day
   - Sets duration and upload flag

2. **Call Art Creator Job**
   - Matrix defines all 7 pattern combinations
   - Each matrix item tagged with its pattern set (set1, set2, or set3)
   - `if` condition filters matrix items based on determined pattern set
   - Only matching patterns execute

3. **Upload Process**
   - When upload=true, generated videos upload to Brand YouTube channel
   - Uses existing art-creator.yml upload functionality
   - Respects all YouTube API guardrails

## Monitoring

Check workflow runs:
```
GitHub → Actions → Test Art Creator - All Combinations
```

**Success criteria:**
- All selected patterns complete successfully
- Videos upload to YouTube (scheduled runs)
- No upload quota exceeded errors

## Benefits

1. **Continuous Testing** - Automated daily validation of all pattern combinations
2. **Quota Compliant** - Respects 10 uploads/24hr limit with room to spare
3. **Content Generation** - Creates diverse test content for Brand channel
4. **Early Detection** - Catches breaking changes before they reach production
5. **Flexible Control** - Manual override for specific pattern testing

## Troubleshooting

**If a scheduled run fails:**
1. Check which pattern set was running (Mon/Thu/Sun=set1, etc.)
2. Run that specific set manually with workflow_dispatch
3. Use `pattern_set` input to select failing set
4. Disable upload to test without consuming quota

**To skip a day's upload:**
- Manually cancel the scheduled workflow run before it completes

**To test a specific pattern:**
- Use content-factory.yml or art-creator.yml directly
- test-art-creator.yml is designed for combination testing

## Related Documentation

- [Art Creator Guide](ART_CREATOR.md)
- [Workflow Specification](spec/workflows.md)
- [System Guardrails](spec/GUARDRAILS.md)
