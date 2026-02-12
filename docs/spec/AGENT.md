# Analytics Agent System Specification

> **Purpose:** Track video generation parameters, fetch YouTube Analytics, correlate performance with inputs, and surface learnings for optimization.

## Overview

The Analytics Agent is a **data collection and reporting system** that creates a feedback loop between video generation and YouTube performance. Phase 1 is observation-only (no automated optimization).

```
┌─────────────────────────────────────────────────────────────────────┐
│                        ANALYTICS AGENT LOOP                         │
│                                                                     │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐         │
│   │   Generate   │───▶│   Upload     │───▶│   Log Params │         │
│   │   (existing) │    │   (existing) │    │   (standalone)│         │
│   └──────────────┘    └──────────────┘    └──────────────┘         │
│                              │                    │                 │
│                              ▼                    ▼                 │
│                           YouTube          data/generations.json    │
│                              │                                      │
│   ┌──────────────┐    ┌──────────────┐           │                 │
│   │   Report     │◀───│ Fetch Stats  │◀──────────┘                 │
│   │   (weekly)   │    │   (weekly)   │                             │
│   └──────────────┘    └──────────────┘                             │
│          │                    │                                     │
│          ▼                    ▼                                     │
│   data/reports/        data/analytics.json                         │
└─────────────────────────────────────────────────────────────────────┘
```

## Design Principle: Standalone Service

The agent is a **standalone service** that does NOT modify existing working code:

- ✅ `youtube_upload.py` - **UNCHANGED** (no risk to uploads)
- ✅ Workflows call agent **after** upload succeeds
- ✅ Agent failure does NOT affect video generation/upload
- ✅ Logging is optional per-workflow

## Components

| Component | File | Purpose |
|-----------|------|---------|
| Generation Logger | `agent/log_generation.py` | Records video parameters after generation |
| Analytics Fetcher | `agent/fetch_analytics.py` | Pulls YouTube Analytics API data |
| Report Generator | `agent/report.py` | Creates performance reports |

## Phase 1 Scope (Current)

| Feature | Status | Description |
|---------|--------|-------------|
| Log generation parameters | ✅ Build | Save all params to JSON after each generation |
| Fetch YouTube Analytics | ✅ Build | Pull views, CTR, retention, watch time |
| Generate weekly report | ✅ Build | Human-readable performance summary |
| Correlate params → performance | ✅ Build | Simple analysis (best/worst performers) |
| ML optimization | ❌ Future | Automated parameter tuning |
| Agent decision-making | ❌ Future | Goal-directed generation |

## Data Flow

### 1. After Video Upload (per-workflow step)

Workflows call the logger CLI **after** a successful upload:

```yaml
# Example workflow step (added after upload step)
- name: Log generation for analytics
  if: success()  # Only if upload succeeded
  run: |
    python -m agent.log_generation \
      --video-id "$VIDEO_ID" \
      --workflow "${{ github.workflow }}" \
      --mood "$MOOD" \
      --duration 300
```

```
Workflow (art-creator, content-factory)
    → Upload to YouTube (existing)
    → python -m agent.log_generation (standalone CLI)
    → data/generations.json
```

### 2. Weekly Analytics Fetch

```
analytics-agent.yml (cron: weekly)
    → agent/fetch_analytics.py
    → YouTube Analytics API
    → data/analytics.json
```

### 3. Weekly Report

```
analytics-agent.yml
    → agent/report.py
    → data/reports/YYYY-WW.md
```

## Data Schemas

### generations.json

```json
{
  "videos": [
    {
      "video_id": "dQw4w9WgXcQ",
      "generated_at": "2026-02-07T08:00:00Z",
      "uploaded_at": "2026-02-07T08:30:00Z",
      "workflow": "content-factory-brand-batch",
      "mood": "deep_focus",
      "duration_seconds": 300,
      "params": {
        "art_period": null,
        "music_style": "gnawa",
        "tempo": 60,
        "visual_speed": 0.5,
        "visual_complexity": 0.7,
        "journey": "steady",
        "rhythm_volume": 0.5
      },
      "metadata": {
        "title": "Deep Focus | 5 Minutes | Gnawa Drums for Concentration",
        "tags": ["focus", "concentration", "study music"]
      }
    }
  ]
}
```

### analytics.json

```json
{
  "fetched_at": "2026-02-14T00:00:00Z",
  "videos": [
    {
      "video_id": "dQw4w9WgXcQ",
      "metrics": {
        "views": 1234,
        "watch_time_minutes": 5678,
        "average_view_duration_seconds": 180,
        "average_view_percentage": 60.0,
        "impressions": 10000,
        "ctr": 12.34,
        "subscribers_gained": 5,
        "likes": 50,
        "comments": 3
      },
      "retention_curve": [100, 95, 90, 85, 80, 75, 70, 65, 60]
    }
  ]
}
```

## Workflow: analytics-agent.yml

```yaml
name: Analytics Agent

on:
  schedule:
    - cron: '0 0 * * 0'  # Every Sunday at midnight UTC
  workflow_dispatch:      # Manual trigger

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Fetch YouTube Analytics
        env:
          YOUTUBE_TOKEN_PICKLE: ${{ secrets.YOUTUBE_TOKEN_PICKLE }}
        run: python -m agent.fetch_analytics
      
      - name: Generate Report
        run: python -m agent.report
      
      - name: Commit Data
        run: |
          git add data/
          git commit -m "chore: update analytics [skip ci]" || true
          git push
```

## Success Metrics

| Metric | Target | Purpose |
|--------|--------|---------|
| Data completeness | 100% videos logged | No gaps in generation data |
| Analytics freshness | Updated weekly | Recent performance data |
| Report generation | Automated | No manual intervention |
| Correlation accuracy | Best/worst identified | Actionable insights |

## Future Phases

### Phase 2: ML Correlation
- Train model on params → performance data
- Identify which parameters correlate with high retention
- Suggest parameter adjustments

### Phase 3: Agent Optimization
- Goal-directed generation ("optimize for retention")
- Automated parameter tuning based on ML predictions
- A/B testing of parameter variations

## Related Specs

- [GUARDRAILS.md](./GUARDRAILS.md) - Agent-specific constraints
- [contracts/agent-youtube.md](./contracts/agent-youtube.md) - YouTube Analytics API interface
- [workflows.md](./workflows.md) - analytics-agent.yml specification

