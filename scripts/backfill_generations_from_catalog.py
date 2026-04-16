#!/usr/bin/env python3
"""Append missing generations.json rows from content_catalog.json.

Videos uploaded before ledger + CI commits only hit YouTube + catalog.
This script joins catalog → ledger for correlate / audit join rate.

Does NOT cover catalog-less uploads (e.g. Art Creator with --no-update-catalog);
those need a separate path (title parse, manifests, or manual rows).

Usage (repo root):
  python scripts/backfill_generations_from_catalog.py --dry-run
  python scripts/backfill_generations_from_catalog.py
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from agent.log_generation import load_generations, record_generation_upload  # noqa: E402


def _version_to_variant(version: str | None) -> str:
    if version == "pure_ambience":
        return "ambience"
    if version == "with_music":
        return "melody"
    return "full"


def main() -> int:
    parser = argparse.ArgumentParser(description="Backfill generations.json from content_catalog.json")
    parser.add_argument("--dry-run", action="store_true", help="Print actions only; do not write")
    parser.add_argument(
        "--catalog",
        default="content_catalog.json",
        help="Path to content catalog JSON",
    )
    args = parser.parse_args()

    catalog_path = _REPO_ROOT / args.catalog
    if not catalog_path.exists():
        print(f"❌ Catalog not found: {catalog_path}")
        return 1

    with open(catalog_path) as f:
        catalog = json.load(f)

    data = load_generations()
    have = {r.get("video_id") for r in data.get("videos", []) if r.get("video_id")}

    added = 0
    skipped = 0
    for row in catalog.get("videos", []):
        vid = row.get("youtube_id")
        if not vid:
            skipped += 1
            continue
        if vid in have:
            skipped += 1
            continue

        mood = row.get("mood")
        dur = row.get("duration")
        if dur is None:
            meta = row.get("metadata") or {}
            dur = meta.get("duration")
        duration_seconds = int(dur or 300)

        seed = row.get("seed")
        variant = _version_to_variant(row.get("version"))

        uploaded_at = row.get("uploaded_at")
        generated_at = row.get("generated_at")
        if isinstance(generated_at, str) and "T" not in generated_at and len(generated_at) == 15:
            # e.g. 20260130_013712 — use catalog uploaded_at for generated when ambiguous
            generated_at = uploaded_at or generated_at

        title = row.get("title") or (row.get("metadata") or {}).get("video_title", "")

        params_extra = {
            "backfill": True,
            "catalog_id": row.get("catalog_id"),
        }

        if args.dry_run:
            print(f"would add {vid} mood={mood} dur={duration_seconds}s variant={variant} title={title[:50]!r}")
            added += 1
            have.add(vid)
            continue

        record_generation_upload(
            video_id=vid,
            workflow="catalog_backfill",
            mood=mood,
            duration_seconds=duration_seconds,
            seed=seed,
            variant=variant,
            params=params_extra,
            metadata={"title": title, "video_title": title},
            generated_at=str(generated_at) if generated_at else None,
            uploaded_at=str(uploaded_at) if uploaded_at else None,
        )
        have.add(vid)
        added += 1

    if args.dry_run:
        print(f"\nDry run: would add {added} rows, skip {skipped}")
        return 0

    print(f"✅ Added {added} ledger rows from catalog (skipped {skipped})")
    try:
        with open(_REPO_ROOT / "data" / "analytics.json") as f:
            a_ids = {v.get("video_id") for v in json.load(f).get("videos", []) if v.get("video_id")}
        overlap = len(have & a_ids)
        print(
            f"ℹ️  Ledger video_ids also present in data/analytics.json: {overlap} / {len(have)} "
            f"(brand fetch only — personal-only catalog rows will not match until personal analytics exists)."
        )
    except OSError:
        pass
    return 0


if __name__ == "__main__":
    os.chdir(_REPO_ROOT)
    raise SystemExit(main())
