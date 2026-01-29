# Content Library Quick Start

## What is the Content Library?

A persistent catalog of all your generated videos with:
- 🔗 YouTube links (not local files)
- 📅 Upload dates and generation timestamps
- 🎲 Seeds for reproducibility
- 🎨 Full metadata (mood, duration, rhythm, etc.)
- 🤖 Automatic updates via GitHub Actions

## Quick Commands

```bash
# View statistics
python library_cli.py stats

# Search videos
python library_cli.py search --mood deep_focus
python library_cli.py search --min-duration 3600

# List all videos
python library_cli.py list

# Export to markdown
python library_cli.py export
```

## How It Works

1. **Generate videos**: Run batch generation
2. **Upload to YouTube**: `python youtube_upload.py --batch ./output`
3. **Catalog updates automatically**: YouTube links saved to `content_catalog.json`
4. **Browse your library**: Use CLI or read `CONTENT_LIBRARY.md`

## GitHub Actions Integration

When the Content Factory workflow runs:
1. Generates videos
2. Uploads to YouTube
3. Updates catalog with YouTube links
4. Commits catalog back to repository
5. You see all your videos in `CONTENT_LIBRARY.md`

## Files

- **`content_catalog.json`** - JSON catalog (machine-readable)
- **`CONTENT_LIBRARY.md`** - Markdown export (human-readable)

Both files are automatically updated and committed by the GitHub Action.

## Example Catalog Entry

```json
{
  "catalog_id": "video_0001_20240129_142305",
  "youtube_url": "https://youtube.com/watch?v=dQw4w9WgXcQ",
  "title": "Deep Focus | Taiko | 1 Hour",
  "mood": "deep_focus",
  "duration": 3600,
  "seed": 1234567890
}
```

## Benefits

✅ **No local storage** - Only YouTube links, not video files  
✅ **Automatic updates** - CI/CD handles everything  
✅ **Version controlled** - Git tracks all changes  
✅ **Searchable** - Filter by mood, duration, rhythm, etc.  
✅ **Reproducible** - Seeds allow exact video recreation  
✅ **Shareable** - Markdown export for easy browsing  

## See Also

- Full documentation: [docs/CONTENT_LIBRARY.md](CONTENT_LIBRARY.md)
- CLI help: `python library_cli.py --help`
