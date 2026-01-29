# Content Library

The Content Library is an automated catalog system that tracks all generated videos with YouTube links, metadata, and identifiers. It's automatically updated when new content is uploaded to YouTube.

## Overview

After running the Content Factory workflow:
1. Videos are generated and uploaded to YouTube
2. The catalog is automatically updated with YouTube links and metadata
3. The catalog is committed back to the repository
4. A markdown summary (`CONTENT_LIBRARY.md`) is generated for easy browsing

## Files

- **`content_catalog.json`** - Persistent JSON catalog with all video metadata
- **`CONTENT_LIBRARY.md`** - Human-readable markdown export of the catalog

## Catalog Entry Structure

Each video in the catalog contains:

```json
{
  "catalog_id": "video_0001_20240129_142305",
  "youtube_id": "dQw4w9WgXcQ",
  "youtube_url": "https://youtube.com/watch?v=dQw4w9WgXcQ",
  "title": "Deep Focus | Taiko | 1 Hour",
  "mood": "deep_focus",
  "duration": 3600,
  "duration_str": "1 Hour",
  "seed": 1234567890,
  "version": "standard",
  "rhythm": "taiko",
  "rhythm_name": "Taiko",
  "uploaded_at": "2024-01-29T14:23:05",
  "generated_at": "2024-01-29T14:15:30",
  "metadata": { /* full generation metadata */ }
}
```

## CLI Usage

### View Statistics

```bash
python library_cli.py stats
```

Shows:
- Total number of videos
- Total duration in hours
- Average duration
- Videos by mood

### Search Videos

```bash
# Search by mood
python library_cli.py search --mood deep_focus

# Search by duration range
python library_cli.py search --min-duration 1800 --max-duration 7200

# Search by rhythm
python library_cli.py search --rhythm taiko

# Search by version
python library_cli.py search --version pure_ambience

# Combine filters
python library_cli.py search --mood sleep --min-duration 3600 --json-output
```

### List Videos

```bash
# List all videos
python library_cli.py list

# List by mood
python library_cli.py list --mood trance
```

### Get Video Details

```bash
python library_cli.py get <youtube_id>
```

### Export as Markdown

```bash
python library_cli.py export --output MY_VIDEOS.md
```

## Programmatic Usage

```python
from library import ContentLibrary

# Initialize library
library = ContentLibrary()

# Get statistics
stats = library.get_stats()
print(f"Total videos: {stats['total_videos']}")

# Search videos
focus_videos = library.search(mood="deep_focus", min_duration=3600)

# Get videos by mood
sleep_videos = library.get_by_mood("sleep")

# Export markdown
library.export_markdown("MY_CATALOG.md")
```

## Automatic Updates

The Content Library is automatically updated when:

1. **Using the GitHub Action workflow**: The `content-factory.yml` workflow automatically:
   - Generates videos
   - Uploads to YouTube
   - Updates the catalog with YouTube links
   - Commits catalog changes back to the repository

2. **Manual uploads with catalog update**:
   ```bash
   # Single video
   python youtube_upload.py --video output/video.mp4 --update-catalog
   
   # Batch upload
   python youtube_upload.py --batch ./batch_output --update-catalog
   ```

3. **Disable catalog updates** (if needed):
   ```bash
   python youtube_upload.py --batch ./batch_output --no-update-catalog
   ```

## Key Features

### 📊 Statistics & Analytics
- Track total videos and duration
- View distribution by mood, rhythm, version
- Calculate averages and trends

### 🔍 Advanced Search
- Filter by mood, rhythm, duration, version
- Combine multiple filters
- Export results as JSON

### 🔗 YouTube Integration
- Stores YouTube video IDs and URLs
- No local video files stored (just metadata)
- Direct links to watch videos

### 📝 Markdown Export
- Human-readable catalog
- Organized by mood
- Includes all metadata and links

### 🤖 Automated Tracking
- No manual updates needed
- Integrated with CI/CD workflow
- Git-tracked for history

## Use Cases

### Content Management
Browse all your generated videos, filter by criteria, and track what you've created.

### Analytics
Understand your content library composition - which moods you've focused on, total duration, etc.

### Planning
Search for gaps in your content (e.g., "need more 3-hour videos for 'trance' mood").

### Sharing
Export markdown catalog to share your video library with others.

### Reproducibility
Every video includes its generation seed, allowing exact reproduction if needed.

## Example Workflow

```bash
# 1. Generate and upload content (happens in GitHub Action)
python batch_generate.py --moods sleep,focus --durations 1h,3h --dual
python youtube_upload.py --batch ./batch_output  # auto-updates catalog

# 2. View your library
python library_cli.py stats

# 3. Search for specific content
python library_cli.py search --mood sleep --min-duration 3600

# 4. Export for sharing
python library_cli.py export --output MY_VIDEOS.md
```

## Catalog Persistence

The catalog is stored in the repository:
- **Version controlled**: Full history of all uploads
- **Shared**: Available to all collaborators
- **Persistent**: Never lost, always accessible
- **No external dependencies**: Just Git

## Best Practices

1. **Let the workflow handle updates**: The GitHub Action automatically updates the catalog
2. **Don't manually edit** `content_catalog.json` - use the CLI or API
3. **Export markdown regularly** for human-readable snapshots
4. **Use search/filter** to find specific videos instead of browsing manually
5. **Track your seeds** if you want to reproduce exact videos

## Troubleshooting

### Catalog not updating
- Ensure `--update-catalog` flag is used (default: true)
- Check GitHub Action has write permissions to repository
- Verify catalog path is correct

### Missing videos in catalog
- Only uploaded videos are tracked
- Check that upload completed successfully
- Verify YouTube API credentials are valid

### Duplicate entries
- The catalog automatically prevents duplicates by YouTube ID
- If you see duplicates, it may be a bug - please report

## Future Enhancements

Potential additions to the content library:
- Analytics dashboard (view counts, watch time)
- Playlist management
- Content recommendations based on gaps
- Export to other formats (CSV, database)
- Integration with YouTube Analytics API
