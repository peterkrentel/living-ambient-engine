# Contract: Production run intent (CI / planner → batch & upload)

> **Purpose:** One **versioned JSON** shape for “what to run next” so **humans**, a **gated planner**, or a future **LLM** can target moods, duration, dual, and upload flags **without** relying on an ever-growing set of static `workflow_dispatch` form fields alone. **Workflow consumer** (validate → `batch_generate` / optional `youtube_upload`) is implemented as [`run-intent-consumer.yml`](../../../.github/workflows/run-intent-consumer.yml) + [`scripts/consume_run_intent.py`](../../../scripts/consume_run_intent.py).

## Consumers

| Consumer | Role |
|----------|------|
| [`run-intent-consumer.yml`](../../../.github/workflows/run-intent-consumer.yml) | **`workflow_dispatch`:** validate committed intent (default `data/run_intent.json`; **personal:** set inputs to `data/run_intent_personal.json` + `data/reports/run-intent-blocked-personal.md`) → `batch_generate.py` → artifact; **YouTube** only if intent **`upload`: true** *and* dispatcher **`confirm_upload`** (double gate). **`validate_only`:** missing intent + paired blocked report → **green** (planner BLOCKED, not a failure). `--catalog-channel` matches intent `channel`. |
| [`scripts/plan_run_intent.py`](../../../scripts/plan_run_intent.py) | **v0 (shipped):** reads suggestions JSON → writes intent JSON **or** blocked markdown; **brand** defaults (`data/suggestions.json` → `data/run_intent.json` / `run-intent-blocked.md`); **personal** uses `--suggestions data/suggestions_personal.json` and `--intent-output data/run_intent_personal.json` / `--blocked-output …-personal.md`. `upload` defaults **false**. Optional `--force-moods` for smoke. Wired from `analytics-agent.yml` and `analytics-personal.yml` after correlate. |
| Gated planner / human PR | May edit intent JSON under `data/` before dispatching the consumer workflow. |

## Schema version 2 (`schema_version: 2`)

| Field | Type | Required | Notes |
|-------|------|----------|--------|
| `schema_version` | `integer` | yes | Bump when breaking semantics. |
| `channel` | `"brand"` \| `"personal"` | yes | Must match secrets / workflow lane. |
| `week` | `string` | yes | ISO week label `YYYY-Www` used to bind intent to an analytics run. |
| `generated_at` | `string` | yes | ISO8601 timestamp when the planner wrote this JSON. |
| `suggestions_generated_at` | `string` \| `null` | no | Optional correlate bundle timestamp for provenance. |
| `moods` | `string[]` | yes | Subset of factory-valid moods or agreed alias list; empty forbidden. |
| `duration` | `string` | yes | Labels aligned with factory CLI (e.g. `30s`, `10min`, `1h`, …). |
| `dual` | `boolean` | yes | Ambience + melody when true. |
| `upload` | `boolean` | yes | If false, generate only (dry path). |
| `max_videos` | `integer` \| `null` | no | Optional safety cap for automation. |

**Validation (non-negotiable):** Invalid JSON or unknown mood/duration → **fail the job** (no partial upload). Confounder / packaging rules from [`AGENT.md`](../AGENT.md) Phase 2 still apply when interpreting analytics that *fed* the intent.

## Example (illustrative)

```json
{
  "schema_version": 2,
  "channel": "brand",
  "week": "2026-W18",
  "generated_at": "2026-04-28T00:00:00+00:00",
  "suggestions_generated_at": "2026-04-28T00:00:00+00:00",
  "moods": ["trance", "sleep", "fireplace", "forest_morning"],
  "duration": "10min",
  "dual": true,
  "upload": true,
  "max_videos": null
}
```

## Relation to other docs

- **Human smoke:** keep using small **`workflow_dispatch`** inputs on [`content-factory-brand.yml`](../../.github/workflows/content-factory-brand.yml) / personal — no need to author JSON for one-off checks.
- **Roadmap:** [`COHESION_ROADMAP.md`](../../COHESION_ROADMAP.md) Phase 6 — agent / planner steps emit this artifact under gates.
- **LLM advisory vs this contract:** `agent-insight-*-gemini.md` / `*-runner.md` are **advisory only**; they **do not** trigger the consumer. Any future **Gemini + Qwen → production** path must still land as **validated intent JSON** (or blocked report), not raw markdown → `batch_generate` — see Phase 6 **LLM advisory → production (contract bridge)** in [`COHESION_ROADMAP.md`](../../COHESION_ROADMAP.md).
- **Analytics loop:** [`AGENT.md`](../AGENT.md) — suggestions inform the planner; they do not bypass this contract once automation consumes intent.
