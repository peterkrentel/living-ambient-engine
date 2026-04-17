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

### 1. After Video Upload (ledger on disk and on `main`)

**Canonical path today:** [`youtube_upload.py`](../../youtube_upload.py) calls `record_generation_upload` from [`agent/log_generation.py`](../../agent/log_generation.py) after a successful upload (batch and single). That updates **`data/generations.json`** in the working tree.

**On GitHub Actions**, writing the file on the runner is **not** enough: upload workflows **must commit and push** `data/generations.json` to `main` or channel audits will show **0% join** to analytics. Step list and per-workflow behavior: **[`docs/spec/workflows.md`](workflows.md) § Generations ledger**. Decision record: **[`docs/decisions/0001-persist-generations-json-on-ci.md`](../decisions/0001-persist-generations-json-on-ci.md)**.

**Optional alternate** (not mixed with the upload path today): standalone CLI after upload — example only:

```yaml
# Example only — prefer aligning with COHESION Phase 2b (single path)
- name: Log generation for analytics
  if: success()
  run: |
    python -m agent.log_generation \
      --video-id "$VIDEO_ID" \
      --workflow "${{ github.workflow }}" \
      --mood "$MOOD" \
      --duration 300
```

```
Workflow → Upload to YouTube → record_generation_upload → data/generations.json → git commit (CI) → main
```

**Backfill (catalog rows only):** Videos that reached **`content_catalog.json`** before the ledger existed can be appended once with [`scripts/backfill_generations_from_catalog.py`](../../scripts/backfill_generations_from_catalog.py) (run from repo root; `--dry-run` first). That restores **`uploaded_at`** from the catalog. It does **not** add rows for uploads that never hit the catalog (e.g. Art Creator with `--no-update-catalog`).

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

**Schema version:** 2 (added versioning, hashes, snapshots)

### generations.json

**Implemented:** `agent/log_generation.py` writes **schema_version 1** rows on successful upload via `youtube_upload.py` (batch + single). Increment **`schema_version`** when adding required fields.

**CI:** Persist updates on `main` per **[`workflows.md`](workflows.md) § Generations ledger** (same PR when changing upload YAML).

```json
{
  "schema_version": 2,
  "videos": [
    {
      "video_id": "dQw4w9WgXcQ",
      "generation_id": "uuid-v4-here",
      "generated_at": "2026-02-07T08:00:00Z",
      "uploaded_at": "2026-02-07T08:30:00Z",
      "workflow": "content-factory-brand-batch",
      "mood": "deep_focus",
      "duration_seconds": 300,
      "versioning": {
        "repo_sha": "abc123",
        "config_hash": "sha256:...",
        "seed": 42,
        "thumbnail_hash": "sha256:..."
      },
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
        "title_hash": "sha256:...",
        "tags": ["focus", "concentration", "study music"]
      }
    }
  ]
}
```

### analytics.json

**Note:** Uses snapshots to track metrics over time (not just latest).

```json
{
  "schema_version": 2,
  "videos": [
    {
      "video_id": "dQw4w9WgXcQ",
      "published_at": "2026-02-07T08:30:00Z",
      "title": "Deep Focus | 5 Minutes",
      "snapshots": [
        {
          "fetched_at": "2026-02-14T00:00:00Z",
          "window": {"start": "2026-02-07", "end": "2026-02-14"},
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
          "retention_features": {
            "drop_0_30s": 15.0,
            "drop_midpoint": 25.0,
            "area_under_curve": 0.72
          },
          "traffic_source_percent": {
            "browse": 40,
            "search": 30,
            "suggested": 25,
            "other": 5
          }
        }
      ]
    }
  ]
}
```

**Snapshot dedupe:** Unique key is `(video_id, window.start, window.end)`. If re-run, overwrite existing snapshot for same window.

**Window definition:** 7 days, inclusive start, exclusive end (standard analytics practice), aligned to cron (Sunday UTC). Example: `start: 2026-02-07, end: 2026-02-14` = [Feb 7, Feb 14).

**Why snapshots:** Distinguishes "spike then die" vs "slow burn" patterns.

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

**Personal channel (separate experiment):** [`analytics-personal.yml`](../../.github/workflows/analytics-personal.yml) runs `fetch_analytics --channel personal` and `report` with `ANALYTICS_JSON_PATH=data/analytics_personal.json` (see `docs/PERSONAL_ANALYTICS.md`). It does not update `data/analytics.json`, `suggestions.json`, or brand audit files.

## Success Metrics

| Metric | Target | Purpose |
|--------|--------|---------|
| Data completeness | 100% videos logged | No gaps in generation data |
| Analytics freshness | Updated weekly | Recent performance data |
| Report generation | Automated | No manual intervention |
| Correlation accuracy | Best/worst identified | Actionable insights |

## Data Quality Checks

Run these checks before trusting any analysis:

| Check | What it catches | Action |
|-------|-----------------|--------|
| Missing analytics | Videos with no metrics | Flag in report |
| Mismatched IDs | video_id not in generations | Investigate |
| Low-view videos | views < 20 | Exclude from retention correlation (keep for CTR analysis) |
| Outlier detection | 10x above/below mean | Flag for review |
| Sample size | See actionability gates below | Filter appropriately |

**Actionability Gates (consistent sample size rules):**

| Threshold | Classification | Action |
|-----------|----------------|--------|
| n ≥ 5 AND group_views ≥ 200 | **Actionable** | Generate increase/decrease suggestions |
| n ≥ 3 (but fails above) | **Exploratory** | Show as "observation", not actionable |
| n < 3 | **Ignore** | Too noisy, don't report |

## Failure Modes & Mitigations

| Failure | Impact | Mitigation |
|---------|--------|------------|
| YouTube API quota exhausted | No new data | Use cached analytics, alert |
| Corrupted JSON | Script crashes | Validate schema, keep backups |
| Missing retention curves | Incomplete analysis | Fall back to basic metrics |
| Git push conflicts | Data not saved | Retry with rebase, alert |
| Token expiry | Auth fails | Refresh token, alert |

**Failure behavior:**
- Fetch fails → Report runs with last-known analytics
- Report fails → Job fails (alerts via GitHub)
- Correlation fails → Job continues, logs warning

## Confounders to Track

**Warning:** Your generator params might matter less than these:

| Confounder | Why it matters | How to track |
|------------|----------------|--------------|
| Title/thumbnail | Dominates CTR | Store `title_hash`, `thumbnail_hash` |
| Upload time | Algorithm timing | Store `uploaded_at` with timezone |
| Traffic source | Browse vs Search vs Suggested | Store `traffic_source` breakdown |
| Audience size | Returning vs new viewers | Store `new_vs_returning` if available |
| Video age | Older videos have more views | Normalize by `days_since_upload` |

**Rule:** Never credit tempo/mood for a better thumbnail.

## ML Learning Path

Your phased approach to learning MLOps:

```
┌───────────────────────────────────────────────────────────────────────────────────────┐
│                              ML LEARNING JOURNEY                                      │
├───────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                       │
│  Phase 1       Phase 1.5      Phase 2        Phase 2.5      Phase 3       Phase 4   │
│  ─────────     ──────────     ─────────      ──────────     ─────────     ─────────  │
│  Data          Aggregation    Correlation    Statistical    Predictive    Optimize   │
│  Pipeline                                    Rigor          Modeling                 │
│                                                                                       │
│  ✅ DONE       ✅ DONE        ✅ CORE        ⏳ NEXT        ⏳ 100+ vids  ⏳ 500+    │
│                                                                                       │
│  • Cron        • Group by     • Find         • Confidence   • Linear      • Bayesian │
│  • Fetch API     category       patterns       intervals      regression  • Multi-obj│
│  • Store JSON  • Rank by      • Std dev      • Z-scores     • Random      • Reinforce│
│  • Reports       metric       • Sample n     • Effect size    forest        learning │
│                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────┘
```

| Phase | What You Learn | Key Files | Status |
|-------|----------------|-----------|--------|
| **1** | Data pipelines, API integration | `fetch_analytics.py`, `report.py` | ✅ Done |
| **1.5** | Aggregation, feature extraction | `analyze_data.py` | ✅ Done |
| **2** | Correlation (retention % + watch min), suggestions | `correlate.py`, `suggestions.json` | ✅ Shipped on `main` (see **Confounders & packaging**; **2.5** for uncertainty, not causality) |
| **2.5** | CIs, z-scores, effect sizes **+** inference limits in docs / summaries | `correlate.py` + spec | ⏳ Next |
| **3** | Predictive modeling (100+ videos) | sklearn models | ⏳ Future |
| **4** | Optimization, recommendations | Bayesian/RL | ⏳ Future |

---

### Phase 1.5: Aggregation & Learning ✅

**Goal:** Learn MLOps fundamentals by building a simple feedback loop.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  COLLECT    │ ──► │  ANALYZE    │ ──► │  ADJUST     │
│             │     │             │     │             │
│  Weekly     │     │  Group by   │     │  Human      │
│  analytics  │     │  type, rank │     │  reviews &  │
│  fetch      │     │  by metric  │     │  tunes      │
└─────────────┘     └─────────────┘     └─────────────┘
     ✅ Auto           ✅ Auto            📝 Manual
```

**What runs automatically:**
- `agent/fetch_analytics.py` → collects YouTube data
- `agent/report.py` → generates markdown report
- `scripts/analyze_data.py` → groups by type, ranks by retention %

**What you learn:**
| MLOps Concept | How We're Doing It |
|---------------|-------------------|
| **Data Pipeline** | Weekly cron fetches data → JSON |
| **Feature Extraction** | Parse mood/type from video title |
| **Metric Tracking** | Retention %, views, watch time |
| **Aggregation** | Group by type, calculate averages |
| **Feedback Loop** | Data → Report → Human Decision → Config Change |

---

### Phase 2: Statistical Correlation 🔄

**Goal:** Automatically find patterns and suggest optimizations.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  COLLECT    │ ──► │  CORRELATE  │ ──► │  SUGGEST    │
│             │     │             │     │             │
│  analytics  │     │  ML finds   │     │  Output to  │
│  .json      │     │  patterns   │     │  Step Sum   │
└─────────────┘     └─────────────┘     └─────────────┘
     ✅ Auto           ✅ Auto            ✅ Auto
                                              │
                                              ▼
                                         📝 Human
                                         reviews &
                                         decides
```

**Components:**
| File | Purpose |
|------|---------|
| `scripts/correlate.py` | ML correlation analysis |
| `data/suggestions.json` | Machine-readable suggestions |
| GitHub Step Summary | Human-readable suggestions |

**Engagement signals (Phase 2):** Correlation runs on **two** metrics already stored in `analytics.json`:
- **`average_view_percentage`** — quality per play (how much of the video people watch, on average, among videos with enough views).
- **`watch_time_minutes`** (YouTube `estimatedMinutesWatched` per video in the fetch window) — **growth / attention**: mean minutes per video in a bucket vs channel mean. High values often reflect reach × hold, not “better art” alone.

Use retention for “stickiness”; use watch minutes for “this bucket fed the channel in this period.” **Impressions / CTR** remain Studio-first until added to `fetch_analytics` (future).

#### Confounders & packaging (read before trusting suggestions)

**CTR and impression mix** often move because of **title, thumbnail, browse vs search surface, Shorts vs long-form routing, and seasonality**—not because mood/tempo “caused” a win. **Do not** treat bucket-level correlation as proof that generation **params** drove an outcome when **packaging** differed across rows.

**Phase 2.5** (confidence intervals, z-scores, effect sizes) answers **“is this signal plausibly noise?”** It does **not** remove confounding. Ship **2.5** together with **explicit warnings** in Step Summary / consumer docs so humans and any future automation do not overfit.

**Before using correlation to justify CTR or packaging bets:** extend **`fetch_analytics`** where the API allows (see `docs/PERSONAL_ANALYTICS.md`), add **joinable packaging fingerprints** (e.g. title + thumbnail hash at publish time, or stable asset ids) on ledger or catalog rows, and keep **matrix levers** (retention, watch minutes from joined params) mentally separate from **packaging experiments**.

**What it outputs (suggestions.json):**
```json
{
  "overall_avg_retention": 12.0,
  "overall_avg_watch_minutes_per_video": 5.31,
  "suggestions": [
    {
      "action": "increase",
      "type": "music_style",
      "name": "none",
      "reason": "+3.3% vs channel avg (n=6, views=303)",
      "confidence": "medium",
      "actionable": true,
      "sample_size": 6,
      "group_views": 303,
      "metric": "average_view_percentage"
    },
    {
      "action": "increase",
      "type": "art_period",
      "name": "ancient",
      "reason": "+12.5 min vs channel avg (n=5, views=400)",
      "metric": "watch_time_minutes"
    }
  ],
  "all_stats": [],
  "all_stats_watch_time": []
}
```

**Required fields per suggestion:**
| Field | Purpose |
|-------|---------|
| `action`, `type`, `name` | What to lean toward |
| `reason` | Human-readable delta vs channel average |
| `metric` | `average_view_percentage` or `watch_time_minutes` |
| `confidence` | low/medium/high based on n |
| `actionable` | Passes n ≥ 5 and group_views ≥ 200 |
| `ci_low`, `ci_high` | Confidence interval (optional until Phase 2.5) |

**How correlation works (simple stats, no neural nets):**
1. Group videos by type (mood, art_period, music_style)
2. For **each metric**, among videos with **views ≥ 20**, compute group mean (`average_view_percentage` or `watch_time_minutes` per video)
3. Calculate std dev per group (retention path)
4. Compare each group mean to the **channel mean** for that metric (all videos with any views in the window)
5. Rank by delta; suggest increase/decrease when |delta| clears a threshold (2 percentage points retention, 1 minute watch time)
6. Apply actionability gates (n ≥ 5 AND group_views ≥ 200 = actionable; n ≥ 3 exploratory)
7. Merge both metric families into `suggestions` (each item tagged with `metric`); keep `all_stats` (retention) and `all_stats_watch_time` separate for tables

**MLOps concepts learned:**
| Concept | Implementation |
|---------|----------------|
| **Feature engineering** | Extract mood/style from title |
| **Aggregation** | Group by category, calc averages |
| **Uncertainty quantification** | Std dev, sample size, CI |
| **Model output** | Structured suggestions (JSON) |
| **Human-in-the-loop** | You review before acting |

**When to move to Phase 3:**
- Suggestions are consistently accurate
- Most groups have n ≥ 10 (high confidence)
- You trust the patterns

### Phase 3: Agent Optimization (Future)

**Goal:** Agent acts on suggestions automatically.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  SUGGEST    │ ──► │  AGENT      │ ──► │  PR         │
│             │     │             │     │             │
│  suggestions│     │  Reads JSON │     │  Auto-create│
│  .json      │     │  edits YAML │     │  for review │
└─────────────┘     └─────────────┘     └─────────────┘
     ✅ Auto           ✅ Auto            ✅ Auto
                                              │
                                              ▼
                                         📝 Human
                                         approves PR
```

**What it does:**
- Reads `data/suggestions.json`
- Modifies `config/moods.yaml` (adjust variations, weights)
- Creates PR with changes
- You approve/reject

**Production execution (future, two doors):** (1) **Small `workflow_dispatch`** on factory workflows for smoke and deliberate one-offs. (2) **Run intent JSON** — [`contracts/production-run-intent.md`](contracts/production-run-intent.md) — validated in CI and mapped to batch/upload flags; a gated planner or LLM (later) emits **only** that structured shape so targeting moods/duration/dual/upload does not depend on static form fields alone.

**MLOps concepts:**
- Automated model deployment
- Continuous learning
- A/B testing of parameter variations
- Experiment tracking

---

## ⚠️ Important: What This Is (and Isn't)

### What You're Learning (Real MLOps)

| Concept | Your Implementation | Why It Matters |
|---------|---------------------|----------------|
| **Data Pipeline** | Cron → API → JSON | Most courses skip this |
| **Feature Engineering** | Extract mood/tempo/style from videos | Core ML skill |
| **Feedback Loops** | Data → Analysis → Human Decision → Config | How real products work |
| **Experiment Tracking** | `generations.json`, `analytics.json` | Production ML requirement |
| **Human-in-the-loop** | You review before acting | Prevents bad automation |

### What Phase 2 Is NOT (Yet)

Phase 2 correlation is **statistics**, not machine learning:
- No model learning weights
- No loss minimization
- No prediction of unseen samples
- No generalization

**And that's fine.** You shouldn't jump to ML without enough data.

### The Biggest Risks

| Risk | Problem | Mitigation |
|------|---------|------------|
| **Too little data** | 5-20 videos = noise | Wait for 100+ videos |
| **False confidence** | "Gnawa +12%!" (but n=2) | Track sample size, require n≥5 |
| **Correlation ≠ causation** | Is it tempo? Or title? Or algorithm? | Stay skeptical |

### Data Volume Reality

| Videos | Signal Quality |
|--------|----------------|
| 5 | Noise |
| 20 | Mostly noise |
| 100+ | Patterns stabilize |
| 500+ | Real insights |

---

## Phase 2.5: Statistical Rigor (Before Real ML)

Before adding predictive models, tighten **uncertainty quantification** and **how results are described**—not only the numbers.

| Measure | Purpose | Status |
|---------|---------|--------|
| Sample size threshold | n ≥ 5 actionable, 3–4 exploratory, fewer than 3 ignore | ✅ Added |
| Standard deviation | Spread within groups | ✅ Added |
| Confidence intervals | Interval estimates for bucket vs mean | ⏳ Future |
| Z-score vs global mean | Standardized distance from channel mean | ⏳ Future |
| Effect size (e.g. Cohen's d) | Practical significance vs noise | ⏳ Future |
| Summary / JSON **disclaimers** | Confounders (§ Phase 2); CIs **≠** causality | ⏳ Ship with 2.5 |

**Why this matters:** You learn to distrust small samples and variance **before** sklearn—and you avoid mistaking **statistical** confidence for **causal** claims about params when **packaging** is unmodeled.

**Parallel track (not a substitute for 2.5):** **Packaging telemetry** (hashes or ids joinable to `video_id`) is its own milestone; schedule it when CTR-driven narratives or automation need defensible joins (optional ADR if schema impact is large).

---

## Phase 3: Predictive Modeling (Future - 100+ videos)

**Trigger:** Move here when you have 100+ videos with views.

When you have enough data, move from:
> "What performed best historically?"

To:
> "Given these parameters, what retention will this video likely get?"

**Models to try (in order):**

| Model | Complexity | When to use |
|-------|------------|-------------|
| Linear regression | Simple | First attempt, baseline |
| Random forest | Medium | Better with non-linear patterns |
| Gradient boosting | Complex | Best accuracy, needs more data |

```python
X = [tempo, visual_speed, complexity, duration, mood_encoded]
y = average_view_percentage

# Train regression model
# Predict expected retention
# Optimize inputs
```

**What you'll learn:**
- Train/test split
- Overfitting
- Feature importance
- Cross-validation

---

## Phase 4: Optimization (Future - 500+ videos)

**Trigger:** Move here when predictive models are accurate.

Turn predictions into optimization:
- Predict retention for parameter combinations
- Search parameter space
- Recommend optimal settings

This is where it becomes a **mini-recommender system**.

**Advanced concepts:**

| Technique | What it does |
|-----------|--------------|
| Bayesian optimization | Efficiently search parameter space |
| Multi-objective optimization | Balance retention vs. other goals |
| Reinforcement learning | Learn from ongoing experiments |

---

## 🎯 Why This Approach Works

> "It's better than 90% of ML courses because it forces you to build the infrastructure and thinking that ML actually depends on."

**Your plan is:**
- ✅ Realistic
- ✅ Technically sound
- ✅ Aligned with real MLOps
- ✅ Phased correctly
- ✅ Grounded in data
- ✅ Designed for learning the right things in the right order

**It's not "ML" yet — but it's the correct path to ML.**

You're building a **tiny YouTube experimentation platform** - that's closer to:
- Growth engineering
- Experimentation platforms
- Recommender optimization

Which is how YouTube itself operates.

---

## Future: Experiment Registry (Placeholder)

When the system matures, add formal experiment tracking:

| Component | Purpose |
|-----------|---------|
| Experiment ID | Unique identifier for each test |
| Parameter set | Frozen config snapshot |
| Model version | Which correlation/prediction model |
| Evaluation metrics | What we measured |
| Outcome | Did it improve? |

This enables:
- Reproducible experiments
- A/B test tracking
- Model versioning
- Rollback capability

**Not building yet** - but acknowledging it shows foresight.

## Related Specs

- [GUARDRAILS.md](./GUARDRAILS.md) - Agent-specific constraints
- [contracts/agent-youtube.md](./contracts/agent-youtube.md) - YouTube Analytics API interface
- [workflows.md](./workflows.md) - analytics-agent.yml specification

