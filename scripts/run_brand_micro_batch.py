#!/usr/bin/env python3
"""Run brand micro batch v1 from data/brand_micro_batch_v1.json → ./generated/manifest.json.

Each slot: one mood key in config/moods.yaml (micro_* brand batch) + duration in seconds.
Titles and tags come from that mood definition (orchestrator metadata).

Usage:
  python scripts/run_brand_micro_batch.py --output ./generated
  python scripts/run_brand_micro_batch.py --output ./generated --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

DEFAULT_SPEC = _REPO / "data" / "brand_micro_batch_v1.json"


def load_slots(spec_path: Path) -> list[dict]:
    with open(spec_path, encoding="utf-8") as f:
        data = json.load(f)
    slots = data.get("slots") or []
    if len(slots) != 20:
        raise SystemExit(f"Expected 20 slots in spec, got {len(slots)}")
    return slots


def extract_video_info(result_obj: dict, mood: str, duration: int, seed: int) -> dict:
    metadata = result_obj.get("metadata", {})
    return {
        "generation_id": str(uuid.uuid4()),
        "mood": mood,
        "duration": duration,
        "seed": seed,
        "variant": "full",
        "video_path": result_obj.get("video_path"),
        "thumbnail_path": result_obj.get("thumbnail_path"),
        "metadata_path": result_obj.get("metadata_path"),
        "title": metadata.get("video_title", "Unknown"),
        "description": metadata.get("description", ""),
        "tags": metadata.get("tags", []),
        "created_at": datetime.now().isoformat(),
        "upload_status": "pending",
        "video_id": None,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Brand micro batch v1 generator")
    ap.add_argument("--output", "-o", default="./generated", help="Output directory")
    ap.add_argument("--spec", type=Path, default=DEFAULT_SPEC, help="Batch JSON spec path")
    ap.add_argument("--dry-run", action="store_true", help="Print plan only")
    args = ap.parse_args()

    slots = load_slots(args.spec)
    out_dir = Path(args.output)
    os.makedirs(out_dir, exist_ok=True)

    if args.dry_run:
        print("Brand micro batch v1 (dry run)\n")
        for s in slots:
            print(f"  slot {s['slot']:2d}  {s['mood']}  {s['duration_s']}s  [{s['bucket']}]  thumb:{s['thumbnail_text']}")
        print(f"\nWould write manifest to {out_dir / 'manifest.json'}")
        return

    from batch_generate import generate_single  # noqa: E402 — heavy deps; skip for dry-run

    results: list[dict] = []
    for s in slots:
        mood = s["mood"]
        dur = int(s["duration_s"])
        print(f"\n=== Slot {s['slot']} | {mood} @ {dur}s ===")
        r = generate_single(mood, dur, str(out_dir), dual=False)
        results.append(r)
        if r["status"] != "success":
            print(f"❌ Failed: {r.get('error')}")
            sys.exit(1)
        print(f"✅ {r['result']['video_path']}")

    manifest_videos = []
    for r, s in zip(results, slots):
        if r["status"] == "success":
            entry = extract_video_info(r["result"], r["mood"], r["duration"], r["seed"])
            entry["batch_slot"] = s["slot"]
            entry["bucket"] = s["bucket"]
            entry["thumbnail_text"] = s.get("thumbnail_text", "")
            manifest_videos.append(entry)

    manifest = {
        "generated_at": datetime.now().isoformat(),
        "batch": "brand_micro_batch_v1",
        "spec_path": str(args.spec.resolve()),
        "total_videos": len(manifest_videos),
        "videos": manifest_videos,
    }
    mp = out_dir / "manifest.json"
    with open(mp, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, default=str)
    print(f"\n📄 Manifest saved: {mp} ({len(manifest_videos)} videos)")


if __name__ == "__main__":
    main()
