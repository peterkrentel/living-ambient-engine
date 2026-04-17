# Contract: Production run intent (CI / planner → batch & upload)

> **Purpose:** One **versioned JSON** shape for “what to run next” so **humans**, a **gated planner**, or a future **LLM** can target moods, duration, dual, and upload flags **without** relying on an ever-growing set of static `workflow_dispatch` form fields alone. **Today:** contract + roadmap only; **workflow consumer** is implemented when Phase 6 / planner work starts.

## Consumers (planned)

| Consumer | Role |
|----------|------|
| GitHub Actions workflow (TBD) | Read intent path or inline JSON → validate → invoke `batch_generate` / `youtube_upload` with equivalent flags (`--catalog-channel`, etc.). |
| Gated planner / human PR | Writes or edits intent under `data/` or a path passed to `workflow_dispatch`. |

## Schema version 1 (`schema_version: 1`)

| Field | Type | Required | Notes |
|-------|------|----------|--------|
| `schema_version` | `integer` | yes | Bump when breaking semantics. |
| `channel` | `"brand"` \| `"personal"` | yes | Must match secrets / workflow lane. |
| `moods` | `string[]` | yes | Subset of factory-valid moods or agreed alias list; empty forbidden. |
| `duration` | `string` | yes | Labels aligned with factory CLI (e.g. `30s`, `10min`, `1h`, …). |
| `dual` | `boolean` | yes | Ambience + melody when true. |
| `upload` | `boolean` | yes | If false, generate only (dry path). |
| `max_videos` | `integer` \| `null` | no | Optional safety cap for automation. |

**Validation (non-negotiable):** Invalid JSON or unknown mood/duration → **fail the job** (no partial upload). Confounder / packaging rules from [`AGENT.md`](../AGENT.md) Phase 2 still apply when interpreting analytics that *fed* the intent.

## Example (illustrative)

```json
{
  "schema_version": 1,
  "channel": "brand",
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
- **Analytics loop:** [`AGENT.md`](../AGENT.md) — suggestions inform the planner; they do not bypass this contract once automation consumes intent.
