# YouTube Uploader Specification

> **Owner:** `youtube/` directory
> **Canonical Spec:** [docs/spec/SYSTEM.md](../docs/spec/SYSTEM.md)
> **Contract:** [docs/spec/contracts/orchestrator-youtube.md](../docs/spec/contracts/orchestrator-youtube.md)

## Purpose

Upload generated videos to YouTube with proper metadata, supporting both personal and brand channels with OAuth2 authentication.

## Public Interface

```python
class YouTubeUploader:
    def __init__(self, credentials_file=None, token_file=None)
    
    def authenticate(self) -> bool
    def upload(self, video_path, title, description, tags, 
               category_id="10", privacy_status="public") -> str
```

## Authentication Flow

### Local Development
1. Run `python youtube_upload.py --auth`
2. Browser opens for OAuth consent
3. Token saved to `youtube_token.pickle`

### GitHub Actions
1. Token stored as base64 in `YOUTUBE_TOKEN_PICKLE` secret
2. Decoded at runtime, no browser needed

### Dual Channel Support
| Channel | Token Secret | Token File |
|---------|--------------|------------|
| Personal | `YOUTUBE_TOKEN_PICKLE` | `youtube_token.pickle` |
| Brand | `YOUTUBE_TOKEN_PICKLE_BRAND` | `youtube_token_brand.pickle` |

## Metadata Defaults

```python
{
    'category_id': '10',        # Music
    'privacy_status': 'public',
    'made_for_kids': False,
    'default_language': 'en',
}
```

## SEO Optimization

Titles and descriptions are optimized for YouTube search:
- Keywords in first 60 characters of title
- Hashtags in description
- Relevant tags array
- Timestamps for long videos

## Acceptance Criteria

- [ ] Successful upload returns YouTube video ID
- [ ] Quota exceeded triggers retry with backoff
- [ ] Duplicate detection prevents re-upload
- [ ] Metadata (title, description, tags) applied correctly
- [ ] Privacy status respected
- [ ] Exit code 0 on success, non-zero on failure

## Error Handling

| Error | Exit Code | Behavior |
|-------|-----------|----------|
| Success | 0 | Return video ID |
| Auth failure | 2 | Clear message, suggest re-auth |
| Quota exceeded | 3 | Retry 3x with backoff, then fail |
| Invalid video | 4 | Validate before upload attempt |
| Network error | 1 | Retry 3x, then fail |

## Quota Management

YouTube API quota: 10,000 units/day
- Upload: ~1,600 units per video
- Safe limit: ~6 videos/day

Workflow handles quota:
```yaml
- name: Check quota before upload
  run: |
    # Skip if quota likely exceeded
    if [ "$VIDEOS_TODAY" -gt 5 ]; then
      echo "Quota limit approaching, skipping upload"
      exit 0
    fi
```

## Idempotency

To prevent duplicate uploads:
1. Check for existing video with same title in last 24h
2. If found, return existing video ID
3. If not found, proceed with upload

## Files

| File | Purpose |
|------|---------|
| `uploader.py` | YouTubeUploader class |
| `__init__.py` | Package exports |

## CLI Usage

```bash
# Authenticate (one-time)
python youtube_upload.py --auth

# Upload single video
python youtube_upload.py --file output/video.mp4 --title "My Video"

# Upload batch
python youtube_upload.py --batch ./batch_output

# Upload to brand channel
python youtube_upload.py --file video.mp4 --brand
```

## Testing

```bash
# Test auth (requires credentials)
python youtube_upload.py --auth

# Dry run (validates without uploading)
python youtube_upload.py --file video.mp4 --dry-run
```

## Security Notes

- Never commit `client_secrets.json` or `*.pickle` files
- Token files are in `.gitignore`
- GitHub secrets are encrypted at rest
- Tokens expire and auto-refresh

