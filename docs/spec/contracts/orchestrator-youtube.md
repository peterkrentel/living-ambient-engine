# Contract: Orchestrator/Workflow → YouTube Uploader

> Defines the interface for uploading videos to YouTube.

## Interface

```python
from youtube.uploader import YouTubeUploader

uploader = YouTubeUploader(
    credentials_file: str = None,    # Path to client_secrets.json
    token_file: str = None           # Path to token pickle file
)

video_id = uploader.upload(
    video_path: str,          # Path to MP4 file
    title: str,               # Video title (max 100 chars)
    description: str,         # Video description (max 5000 chars)
    tags: List[str],          # Video tags
    category_id: str = "10",  # YouTube category (10 = Music)
    privacy_status: str = "public"  # public/private/unlisted
)
```

## Authentication

### Token Sources (in order of precedence)
1. Environment variable `YOUTUBE_TOKEN_PICKLE` (base64 encoded)
2. Environment variable `YOUTUBE_TOKEN_PICKLE_BRAND` (for brand channel)
3. File path specified in constructor
4. Default file `youtube_token.pickle` in repo root

### Secrets Required (GitHub Actions)
| Secret | Purpose |
|--------|---------|
| `YOUTUBE_TOKEN_PICKLE` | Personal channel OAuth token |
| `YOUTUBE_TOKEN_PICKLE_BRAND` | Brand channel OAuth token |

## Guarantees

### Caller Guarantees
1. Video file exists and is valid MP4
2. Title is non-empty, ≤100 characters
3. Description is ≤5000 characters
4. Category ID is valid YouTube category

### Uploader Guarantees
1. Returns YouTube video ID on success
2. Respects API quota limits (retries with backoff)
3. Idempotent - won't create duplicates if video with same title exists in last 24h
4. Raises descriptive exception on failure

## Error Handling

| Error | Behavior |
|-------|----------|
| No credentials | Raise `AuthenticationError` |
| Quota exceeded | Retry with exponential backoff, then raise `QuotaExceededError` |
| Invalid video | Raise `ValueError` |
| Network error | Retry 3 times, then raise `UploadError` |
| Duplicate detected | Return existing video ID (idempotent) |

## Metadata Schema

```python
metadata = {
    'title': str,           # Required
    'description': str,     # Required
    'tags': List[str],      # Optional, default []
    'category_id': str,     # Optional, default "10"
    'privacy_status': str,  # Optional, default "public"
    'made_for_kids': bool,  # Optional, default False
}
```

## Workflow Integration

In GitHub Actions, the uploader is called via `youtube_upload.py`:

```yaml
- name: Upload to YouTube
  env:
    YOUTUBE_TOKEN_PICKLE: ${{ secrets.YOUTUBE_TOKEN_PICKLE }}
  run: |
    python youtube_upload.py \
      --file "$VIDEO_PATH" \
      --title "$TITLE" \
      --description "$DESCRIPTION"
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Authentication error |
| 3 | Quota exceeded |
| 4 | Invalid input |

## Testing Contract

```python
def test_upload_contract():
    # Mock test - actual upload requires credentials
    uploader = YouTubeUploader()
    
    # Verify validation
    with pytest.raises(ValueError):
        uploader.upload('/nonexistent.mp4', 'Title', 'Desc', [])
    
    with pytest.raises(ValueError):
        uploader.upload('/valid.mp4', '', 'Desc', [])  # Empty title
```

