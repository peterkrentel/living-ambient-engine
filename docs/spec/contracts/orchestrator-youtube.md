# Contract: Orchestrator/Workflow → YouTube Uploader

> Defines the interface for uploading videos to YouTube.
> See also: [GUARDRAILS.md](../GUARDRAILS.md) for parameter limits.

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

## Pre-Conditions

> **Must be true BEFORE calling the interface.**

### `YouTubeUploader.__init__`

| Condition | Check | Violation Handling |
|-----------|-------|-------------------|
| Token available | Env var or file exists | Raise `AuthenticationError` |
| Token valid | OAuth token not expired | Raise `AuthenticationError` |
| Token has scopes | `youtube.upload` scope | Raise `AuthenticationError` |

### `YouTubeUploader.upload`

| Condition | Check | Violation Handling |
|-----------|-------|-------------------|
| `video_path` exists | `Path(video_path).exists()` | Raise `ValueError` |
| `video_path` is file | `Path(video_path).is_file()` | Raise `ValueError` |
| `video_path` is MP4 | Valid MP4 header | Raise `ValueError` |
| `video_path` readable | Read permission | Raise `IOError` |
| `title` non-empty | `len(title.strip()) > 0` | Raise `ValueError` |
| `title` length | `len(title) <= 100` | Truncate with warning |
| `description` length | `len(description) <= 5000` | Truncate with warning |
| `tags` total length | `sum(len(t) for t in tags) <= 500` | Truncate list |
| `category_id` valid | Valid YouTube category | Use "10" (Music) |
| `privacy_status` valid | `in ['public', 'private', 'unlisted']` | Use 'public' |

## Post-Conditions

> **Must be true AFTER the interface returns successfully.**

### `YouTubeUploader.upload`

| Condition | Verification |
|-----------|--------------|
| Video ID returned | `len(video_id) == 11` (YouTube ID format) |
| Video accessible | `GET /videos?id={video_id}` returns data |
| Metadata matches | Title/description/tags match input |
| Privacy matches | Video has correct privacy status |

## Invariants

> **Must ALWAYS be true during execution.**

| Invariant | Description |
|-----------|-------------|
| **Quota tracking** | Track API units used, pause at 90% daily limit |
| **Idempotency** | Same title in 24h → return existing ID, don't re-upload |
| **Retry bounded** | Max 3 retries with exponential backoff |
| **Token refresh** | Auto-refresh expired tokens before failure |
| **No secrets logged** | Token/credentials never appear in logs |
| **Resumable upload** | Use resumable upload for files > 5MB |

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

## Error Handling

| Error | Behavior | Exit Code |
|-------|----------|-----------|
| No credentials | Raise `AuthenticationError` | 2 |
| Token expired | Attempt refresh, then raise `AuthenticationError` | 2 |
| Quota exceeded | Retry with backoff, then raise `QuotaExceededError` | 3 |
| Invalid video | Raise `ValueError` with details | 4 |
| Network error | Retry 3 times with backoff, then raise `UploadError` | 1 |
| Duplicate detected | Return existing video ID (idempotent) | 0 |
| Rate limited | Wait and retry (up to 5 min) | 1 if timeout |

## Metadata Schema

```python
metadata = {
    'title': str,           # Required, max 100 chars
    'description': str,     # Required, max 5000 chars
    'tags': List[str],      # Optional, total max 500 chars
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
| 1 | General error (network, timeout) |
| 2 | Authentication error |
| 3 | Quota exceeded |
| 4 | Invalid input |

## Contract Test

```python
def test_upload_contract():
    """Verify all contract conditions."""
    from pathlib import Path
    import pytest

    # Pre-condition: file must exist
    uploader = YouTubeUploader()
    with pytest.raises(ValueError, match="not found"):
        uploader.upload('/nonexistent.mp4', 'Title', 'Desc', [])

    # Pre-condition: title must be non-empty
    with pytest.raises(ValueError, match="title"):
        uploader.upload('/valid.mp4', '', 'Desc', [])

    # Pre-condition: title length
    long_title = 'x' * 150
    # Should truncate to 100, not raise

    # Pre-condition: valid privacy status
    with pytest.raises(ValueError, match="privacy"):
        uploader.upload('/valid.mp4', 'Title', 'Desc', [], privacy_status='invalid')

def test_idempotency():
    """Verify duplicate uploads return existing ID."""
    uploader = YouTubeUploader()

    # First upload
    id1 = uploader.upload('/test.mp4', 'Unique Title 123', 'Desc', [])

    # Second upload with same title within 24h
    id2 = uploader.upload('/test.mp4', 'Unique Title 123', 'Desc', [])

    assert id1 == id2, "Duplicate upload should return same ID"
```

