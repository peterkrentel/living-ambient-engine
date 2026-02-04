# Daily Art Creator - Automated Art Generation

This directory contains the data and scripts for the **Daily Art Creator** workflow, which automatically generates unique art pieces every day by cycling through curated combinations of Art Creator parameters.

## Overview

The Daily Art Creator workflow runs automatically every day at **1:10pm CST (19:10 UTC)** and:

1. ✅ Selects the next unused combination from the curated list
2. 📝 Updates tracking to mark the combination as used
3. 🎨 Triggers the Art Creator workflow with those specific parameters
4. 🔄 Continues daily until all combinations have been used

## Files

### `art-combinations.json`

Contains the curated list of all Art Creator parameter combinations to cycle through. Each combination includes:

- **id**: Unique identifier for the combination
- **name**: Descriptive name for the art piece
- **art_period**: Historical art period (e.g., "cave_art", "renaissance", "future")
- **visual_pattern**: Type of visual pattern (e.g., "fractal_zoom", "sacred_geometry")
- **visual_speed**: Speed of visual changes (0.1 to 1.5, or "auto")
- **visual_complexity**: Complexity level (0.1 to 1.0, or "auto")
- **color_palette**: Color scheme (e.g., "sunset", "ocean", "psychedelic")
- **music_style**: Music/rhythm style (e.g., "heartbeat", "gnawa", "taiko")
- **tempo**: Music tempo in BPM (20-200)
- **brainwave_frequency**: Brainwave entrainment frequency in Hz (1-50)
- **solfeggio_frequency**: Solfeggio healing frequency (174, 285, 396, 417, 528, 639, 741, 852, 963)
- **rhythm_volume**: Volume level for rhythm/drums (0.0-1.0)
- **ambient_volume**: Volume level for ambient sounds (0.0-1.0)
- **journey**: Dynamic evolution pattern (e.g., "awakening", "trance", "waves")
- **journey_intensity**: How dramatic the changes are ("subtle", "moderate", "dramatic")
- **duration**: Length of the video (e.g., "10min", "1h")

### `art-tracking.json`

Tracks the progress of the daily art generation:

- **current_index**: Index of the next combination to use
- **used_combinations**: Array of all combinations that have been used (with timestamps)
- **total_combinations**: Total number of combinations available
- **completed**: Boolean flag indicating if all combinations have been used
- **last_updated**: Timestamp of last update

## Adding or Modifying Combinations

### Add New Combinations

1. Edit `art-combinations.json`
2. Add new combination objects to the `combinations` array
3. Ensure each has a unique `id` and descriptive `name`
4. Update the tracking file's `total_combinations` count if needed

Example:
```json
{
  "id": 21,
  "name": "Mystic Ocean Journey",
  "art_period": "ancient",
  "visual_pattern": "flowing_waves",
  "visual_speed": "0.4",
  "visual_complexity": "0.7",
  "color_palette": "ocean",
  "music_style": "gamelan",
  "tempo": "65",
  "brainwave_frequency": "8",
  "solfeggio_frequency": "528",
  "rhythm_volume": "0.5",
  "ambient_volume": "1.0",
  "journey": "waves",
  "journey_intensity": "moderate",
  "duration": "10min"
}
```

### Modify Existing Combinations

Simply edit the desired combination in `art-combinations.json`. Changes will take effect for future (unused) combinations.

### Reset to Start Over

To restart from the beginning after all combinations have been used:

```bash
python3 ../.github/scripts/select_art_combo.py --reset
```

Or manually edit `art-tracking.json`:
```json
{
  "description": "Tracks which Art Creator combinations have been used",
  "last_updated": null,
  "current_index": 0,
  "used_combinations": [],
  "total_combinations": 20,
  "completed": false
}
```

## Manual Testing

### Check Current Status

```bash
python3 ../.github/scripts/select_art_combo.py --status
```

Output:
```
📊 Art Creator Combination Status
   Total combinations: 20
   Used: 5
   Remaining: 15
   Current index: 5
   Completed: False
   Last updated: 2024-01-15T19:10:00Z
```

### Test Selection (Dry Run)

Preview the next combination without updating tracking:

```bash
python3 ../.github/scripts/select_art_combo.py --dry-run
```

### Manually Select Next Combination

```bash
python3 ../.github/scripts/select_art_combo.py
```

This will:
- Select the next unused combination
- Update the tracking file
- Output parameters to `$GITHUB_OUTPUT` (when running in GitHub Actions)

## Workflow Configuration

The workflow is defined in `../.github/workflows/daily-art-creator.yml` and can be:

- **Triggered automatically**: Runs daily at 19:10 UTC (1:10pm CST)
- **Triggered manually**: Via GitHub Actions UI for testing
- **Modified**: Edit the cron schedule or workflow steps as needed

### Change Schedule

Edit the cron expression in the workflow file:

```yaml
schedule:
  - cron: '10 19 * * *'  # 19:10 UTC = 1:10pm CST
```

### Disable Automatic Running

Comment out or remove the `schedule` trigger in the workflow file.

## Completion Behavior

When all combinations have been used:

1. ✅ The workflow stops triggering art generation
2. 📋 An issue is automatically created to notify maintainers
3. 💬 Console output explains how to reset or add more combinations
4. ⏸️ Scheduled runs continue but do nothing until reset

## Troubleshooting

### Workflow Not Running

- Check that the workflow file is on the `main` branch
- Verify the repository has Actions enabled
- Check Actions tab for any error messages

### Combinations Out of Sync

If tracking seems wrong, reset it:

```bash
python3 ../.github/scripts/select_art_combo.py --reset
```

### Testing Locally

The Python script works standalone outside of GitHub Actions:

```bash
cd /path/to/repo
python3 .github/scripts/select_art_combo.py --dry-run
```

## Best Practices

1. **Curate meaningful combinations**: Each should represent a distinct artistic vision
2. **Test before committing**: Use `--dry-run` to preview selections
3. **Keep tracking file in git**: It should be committed to track progress
4. **Document new combinations**: Use descriptive names that explain the art piece
5. **Consider duration**: Longer videos take more resources; balance variety and generation time

## Architecture

```
Daily Art Creator Workflow
    │
    ├─→ Runs on schedule (daily at 19:10 UTC)
    │
    ├─→ select_art_combo.py
    │     ├─→ Reads: art-combinations.json
    │     ├─→ Reads: art-tracking.json
    │     ├─→ Selects next unused combination
    │     └─→ Updates: art-tracking.json
    │
    ├─→ Commits tracking file update
    │
    └─→ Triggers: art-creator.yml
          └─→ Generates art with selected parameters
```

## See Also

- [Art Creator Documentation](../../docs/ART_CREATOR.md)
- [Workflow Specification](../../docs/spec/workflows.md)
- Main Art Creator workflow: `../.github/workflows/art-creator.yml`
