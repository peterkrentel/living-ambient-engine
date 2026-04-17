# ADR 0002: Optional `channel` on `content_catalog.json` rows

## Status

Accepted (implementation: new writes only; historic rows unchanged).

## Context

- `content_catalog.json` is a **single** file that can list uploads from **both** YouTube identities (personal + brand).
- Brand analytics and audit join use **`data/analytics.json`** (brand channel only), so catalog rows without context are ambiguous for tooling and docs (“gap” in [`START_HERE.md`](../START_HERE.md)).
- Splitting into two files (`content_catalog_brand.json` / `content_catalog_personal.json`) would touch every reader/writer and complicate workflows.

## Decision

1. Add an optional string field **`channel`** on each **video** object in the catalog, with allowed values **`brand`** | **`personal`**.
2. **New** rows written by `youtube_upload.py` set `channel` when the upload is invoked with **`--catalog-channel`** (or env **`CONTENT_CATALOG_CHANNEL`**, same values). The same upload path sets optional **`channel`** on matching **`data/generations.json`** rows for analytics / audit joins.
3. **Existing** rows remain valid **without** `channel` (unknown / legacy). Optional later: backfill from workflow provenance or heuristics.
4. Do **not** change the top-level `catalog_version` in this ADR; treat `channel` as additive schema.

## Consequences

- **Pros:** Single file preserved; analytics and audit code can gradually filter; explicit for new uploads.
- **Cons:** Mixed population until backfill; consumers must treat missing `channel` as unknown.
- **Alternatives deferred:** split catalog files; derive channel only from `generations.json` (still valuable but does not label catalog-only rows).

## References

- [`library/catalog.py`](../../library/catalog.py) — `add_video(..., channel=...)`
- [`youtube_upload.py`](../../youtube_upload.py) — `--catalog-channel`
- Workflows: `content-factory.yml` (personal), `content-factory-brand.yml`, `content-factory-brand-batch.yml`, `piano-batch.yml` (personal token → personal).
