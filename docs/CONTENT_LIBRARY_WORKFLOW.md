# Content Library - How It Works

## The Complete Workflow

### 1. Video Generation (GitHub Actions)
When the Content Factory workflow runs (daily at 2 AM UTC or manually triggered):

```yaml
# .github/workflows/content-factory.yml
- Generate videos (batch_generate.py)
- Upload to YouTube (youtube_upload.py --batch)
- Update catalog (automatic)
- Commit catalog to repo (automatic)
```

### 2. Catalog Update (Automatic)
After each successful YouTube upload:

```python
# youtube_upload.py captures the result
{
  "video_id": "ABC123XYZ",
  "url": "https://youtube.com/watch?v=ABC123XYZ",
  "title": "Deep Focus | Taiko | 1 Hour"
}

# Adds to content_catalog.json
library.add_video(
    youtube_id=result['video_id'],
    youtube_url=result['url'],
    title=result['title'],
    metadata=full_metadata
)
```

### 3. Repository Update (Automatic)
The workflow commits the updated catalog:

```bash
git add content_catalog.json CONTENT_LIBRARY.md
git commit -m "📚 Update content library catalog [automated]"
git push
```

### 4. Browse Your Library
You can now view all your videos:

```bash
# View statistics
python library_cli.py stats

# Search for videos
python library_cli.py search --mood deep_focus --min-duration 3600

# Export to markdown
python library_cli.py export
```

## What Gets Stored

### content_catalog.json
```json
{
  "catalog_version": "1.0",
  "created_at": "2024-01-29T10:00:00",
  "last_updated": "2024-01-29T14:30:00",
  "total_videos": 25,
  "videos": [
    {
      "catalog_id": "video_0001_20240129_103000_a1b2c3d4",
      "youtube_id": "ABC123XYZ",
      "youtube_url": "https://youtube.com/watch?v=ABC123XYZ",
      "title": "Deep Focus | Taiko | 1 Hour",
      "mood": "deep_focus",
      "duration": 3600,
      "duration_str": "1 Hour",
      "seed": 1234567890,
      "version": "standard",
      "rhythm": "taiko",
      "rhythm_name": "Taiko",
      "uploaded_at": "2024-01-29T10:30:00",
      "generated_at": "2024-01-29T10:15:00",
      "metadata": { /* full generation config */ }
    }
  ]
}
```

### CONTENT_LIBRARY.md
Human-readable markdown with:
- Statistics (total videos, duration, etc.)
- Videos organized by mood
- Direct YouTube links
- All metadata (seed, duration, rhythm, etc.)

## Manual Usage

### Generate and Upload Locally

```bash
# 1. Generate videos
python batch_generate.py --moods deep_focus,sleep --durations 1h

# 2. Upload to YouTube (catalog updates automatically)
python youtube_upload.py --batch ./batch_output

# 3. View your catalog
python library_cli.py stats
```

### Query the Catalog

```bash
# Find all long-form content
python library_cli.py search --min-duration 3600

# Find specific mood
python library_cli.py search --mood sleep

# Find pure ambience versions
python library_cli.py search --version pure_ambience

# Get details of specific video
python library_cli.py get ABC123XYZ
```

### Export for Sharing

```bash
# Create markdown export
python library_cli.py export --output MY_VIDEOS.md

# Share MY_VIDEOS.md with your team/audience
```

## Programmatic Access

```python
from library import ContentLibrary

# Load catalog
library = ContentLibrary()

# Get all videos for a mood
focus_videos = library.get_by_mood('deep_focus')

# Search with multiple filters
long_focus = library.search(
    mood='deep_focus',
    min_duration=3600,
    version='standard'
)

# Get statistics
stats = library.get_stats()
print(f"Total: {stats['total_videos']} videos")
print(f"Duration: {stats['total_duration_hours']} hours")

# Export
library.export_markdown('custom_export.md')
```

## File Locations

```
your-repo/
├── content_catalog.json       # Machine-readable catalog (tracked in git)
├── CONTENT_LIBRARY.md         # Human-readable export (tracked in git)
├── library/                   # Library module
│   ├── __init__.py
│   └── catalog.py
├── library_cli.py             # CLI tool
├── youtube_upload.py          # Upload script (updated)
└── .github/workflows/
    └── content-factory.yml    # Automated workflow (updated)
```

## Important Notes

### What IS stored:
✅ YouTube links and video IDs  
✅ Metadata (mood, duration, seed, etc.)  
✅ Upload dates and timestamps  
✅ Full generation configuration  

### What is NOT stored:
❌ Video files (.mp4)  
❌ Audio files (.wav)  
❌ Thumbnails (.png)  
❌ Any local artifacts  

### Why This Matters:
- **Small repository** - Only JSON/markdown, no large files
- **Fast operations** - No video processing needed
- **Easy sharing** - Just commit and push
- **Version controlled** - Full history in git

## Troubleshooting

### Catalog not updating
1. Check that `--update-catalog` is enabled (default: true)
2. Verify uploads completed successfully
3. Check GitHub Action logs for errors

### Missing videos
1. Ensure videos were actually uploaded
2. Check for upload errors in logs
3. Verify YouTube API credentials

### Corrupted catalog
Don't worry! The library automatically:
1. Detects corrupted JSON files
2. Creates a backup (.json.backup)
3. Starts fresh catalog

## Best Practices

1. **Let automation handle it** - The GitHub Action is the recommended way
2. **Don't edit manually** - Use CLI or API to modify catalog
3. **Review commits** - Check what was added after each run
4. **Export regularly** - Create markdown snapshots
5. **Use search** - Don't browse manually, use filters

## Next Steps

Now that you have a content library:
1. Run the Content Factory workflow
2. Videos will be generated and uploaded
3. Catalog will be updated automatically
4. Browse your library anytime with the CLI
5. Share CONTENT_LIBRARY.md with others

## Questions?

- 📚 Full documentation: [CONTENT_LIBRARY.md](CONTENT_LIBRARY.md)
- ⚡ Quick start: [CONTENT_LIBRARY_QUICKSTART.md](CONTENT_LIBRARY_QUICKSTART.md)
- 💻 Examples: `examples_library.py`
- ❓ CLI help: `python library_cli.py --help`
