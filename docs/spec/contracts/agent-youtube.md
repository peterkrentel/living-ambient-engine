# Contract: Analytics Agent → YouTube Analytics API

> Defines the interface for fetching video performance data from YouTube.
> See also: [GUARDRAILS.md](../GUARDRAILS.md) for rate limits.

## Interface

```python
from agent.fetch_analytics import AnalyticsFetcher

fetcher = AnalyticsFetcher(
    credentials_file: str = None,    # Path to client_secrets.json
    token_file: str = None           # Path to token pickle file
)

# Fetch analytics for specific videos
analytics = fetcher.fetch(
    video_ids: List[str],            # YouTube video IDs
    start_date: date = None,         # Default: 28 days ago
    end_date: date = None            # Default: yesterday
)

# Fetch analytics for all channel videos
analytics = fetcher.fetch_all(
    start_date: date = None,
    end_date: date = None,
    max_results: int = 50            # Limit for API quota
)
```

## Pre-Conditions

| Condition | Check | Violation Handling |
|-----------|-------|-------------------|
| Token available | Env var or file exists | Raise `AuthenticationError` |
| Token valid | OAuth token not expired | Raise `AuthenticationError` |
| Token has scopes | `youtube.readonly`, `yt-analytics.readonly` | Raise `AuthenticationError` |
| `video_ids` non-empty | `len(video_ids) > 0` | Raise `ValueError` |
| `start_date` <= `end_date` | Date order valid | Raise `ValueError` |
| `start_date` not future | Can't fetch future data | Raise `ValueError` |

## Post-Conditions

| Condition | Verification |
|-----------|--------------|
| Analytics returned | Non-empty dict for valid videos |
| Metrics present | views, watch_time, ctr populated |
| Data saved | `data/analytics.json` updated |

## Return Schema

```python
{
    "fetched_at": str,               # ISO 8601 timestamp
    "videos": [
        {
            "video_id": str,         # YouTube video ID (11 chars)
            "metrics": {
                "views": int,
                "watch_time_minutes": float,
                "average_view_duration_seconds": float,
                "average_view_percentage": float,
                "impressions": int,
                "ctr": float,        # Click-through rate (%)
                "subscribers_gained": int,
                "subscribers_lost": int,
                "likes": int,
                "dislikes": int,
                "comments": int,
                "shares": int
            },
            "retention_curve": List[float]  # 0-100% at intervals
        }
    ]
}
```

## YouTube Analytics API Dimensions/Metrics

### Metrics Used

| API Metric | Our Field | Description |
|------------|-----------|-------------|
| `views` | `views` | Total views |
| `estimatedMinutesWatched` | `watch_time_minutes` | Total watch time |
| `averageViewDuration` | `average_view_duration_seconds` | Avg seconds watched |
| `averageViewPercentage` | `average_view_percentage` | Avg % of video watched |
| `annotationClickThroughRate` | `ctr` | Click-through rate |
| `subscribersGained` | `subscribers_gained` | New subs from video |
| `subscribersLost` | `subscribers_lost` | Unsubs from video |
| `likes` | `likes` | Like count |
| `dislikes` | `dislikes` | Dislike count |
| `comments` | `comments` | Comment count |
| `shares` | `shares` | Share count |

### Retention Curve

Uses `audienceRetention` report with relative retention data points.

## Rate Limits & Quotas

| Limit | Value | Handling |
|-------|-------|----------|
| Daily quota | 10,000 units | Track usage, stop at 90% |
| Queries per 100 seconds | 100 | Rate limit requests |
| Reports per query | 1 | Batch efficiently |

**Cost per query:**
- Analytics query: 1 unit
- Video list: 1 unit per 50 videos

## Error Handling

| Error | Behavior | Exit Code |
|-------|----------|-----------|
| No credentials | Raise `AuthenticationError` | 2 |
| Token expired | Attempt refresh, then raise | 2 |
| Quota exceeded | Stop gracefully, save partial | 3 |
| Video not found | Skip, log warning | 0 |
| API error | Retry 3x with backoff | 1 |

## Invariants

| Invariant | Description |
|-----------|-------------|
| **Quota tracking** | Never exceed 90% daily quota |
| **Incremental fetch** | Only fetch data newer than last fetch |
| **Graceful degradation** | Save partial data on errors |
| **No secrets logged** | Credentials never in logs/output |
| **Idempotent storage** | Re-running doesn't duplicate data |

## Authentication

### Required OAuth Scopes

```
https://www.googleapis.com/auth/youtube.readonly
https://www.googleapis.com/auth/yt-analytics.readonly
```

### Token Sources (in order)

1. `YOUTUBE_TOKEN_PICKLE` environment variable (base64)
2. `YOUTUBE_TOKEN_PICKLE_BRAND` environment variable
3. Constructor parameter
4. Default file `youtube_token.pickle`

### Token Usage by Workflow

| Workflow | Token | Notes |
|----------|-------|-------|
| Analytics Agent | `YOUTUBE_TOKEN_PICKLE_BRAND` | Brand channel analytics |
| Content Factory | `YOUTUBE_TOKEN_PICKLE` | Personal account uploads |

## Contract Test

```python
def test_fetch_contract():
    """Verify all contract conditions."""
    from agent.fetch_analytics import AnalyticsFetcher
    import pytest
    
    fetcher = AnalyticsFetcher()
    
    # Pre-condition: video_ids must be non-empty
    with pytest.raises(ValueError, match="video_ids"):
        fetcher.fetch([])
    
    # Pre-condition: date order
    with pytest.raises(ValueError, match="date"):
        fetcher.fetch(['abc'], start_date=date(2026, 2, 1), end_date=date(2026, 1, 1))
    
    # Post-condition: valid response structure
    result = fetcher.fetch(['dQw4w9WgXcQ'])
    assert 'fetched_at' in result
    assert 'videos' in result
    assert isinstance(result['videos'], list)
```

