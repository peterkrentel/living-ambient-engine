#!/usr/bin/env python3
"""Verify content_catalog.json youtube_ids match data/generations.json video_ids.

Exit 0 when sets match. Exit 1 on mismatch (prints missing in each direction).
Also prints workflow counts on the ledger (spot missing personal rows).

Usage (repo root):
  python scripts/verify_ledger_catalog.py

After a CI push failure, if YouTube has the video but git does not, add a row with:
  python -m agent.log_generation --video-id VIDEO_ID --workflow \"Content Factory (Personal)\" ...
See docs/spec/AGENT.md § Generation logger.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]


def main() -> int:
    cat_path = _REPO / "content_catalog.json"
    gen_path = _REPO / "data" / "generations.json"
    for p in (cat_path, gen_path):
        if not p.exists():
            print(f"❌ missing file: {p.relative_to(_REPO)}")
            return 1

    with open(cat_path) as f:
        catalog = json.load(f)
    with open(gen_path) as f:
        generations = json.load(f)

    cat_ids = {v.get("youtube_id") for v in catalog.get("videos", []) if v.get("youtube_id")}
    gen_ids = {v.get("video_id") for v in generations.get("videos", []) if v.get("video_id")}

    missing_in_gen = sorted(cat_ids - gen_ids)
    missing_in_cat = sorted(gen_ids - cat_ids)

    wf = Counter(v.get("workflow") for v in generations.get("videos", []))
    print("Ledger workflow counts:")
    for name, n in wf.most_common():
        print(f"  {n:4d}  {name!r}")

    personal_rows = sum(
        1 for v in generations.get("videos", []) if v.get("workflow") == "Content Factory (Personal)"
    )
    if personal_rows == 0:
        print(
            "\n⚠️  No ledger rows with workflow 'Content Factory (Personal)'. "
            "If you uploaded from the personal workflow, the row may never have reached "
            "`main` (e.g. push rejected); use `python -m agent.log_generation` with the "
            "Studio video id, or re-run the workflow after fixing CI push."
        )

    print(f"\nCatalog youtube_id count: {len(cat_ids)}")
    print(f"Generations video_id count: {len(gen_ids)}")

    if not missing_in_gen and not missing_in_cat:
        print("✅ Catalog and generations video id sets match.")
        return 0

    if missing_in_gen:
        print(f"\n❌ In catalog but NOT in generations ({len(missing_in_gen)}):")
        for vid in missing_in_gen[:50]:
            print(f"   {vid}")
        if len(missing_in_gen) > 50:
            print(f"   ... and {len(missing_in_gen) - 50} more")
    if missing_in_cat:
        print(f"\n❌ In generations but NOT in catalog ({len(missing_in_cat)}):")
        for vid in missing_in_cat[:50]:
            print(f"   {vid}")
        if len(missing_in_cat) > 50:
            print(f"   ... and {len(missing_in_cat) - 50} more")
    return 1


if __name__ == "__main__":
    sys.exit(main())
