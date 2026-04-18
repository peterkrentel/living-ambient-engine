#!/usr/bin/env python3
"""Run brand micro batch v1 from data/brand_micro_batch_v1.json → ./generated/manifest.json.

Modes:
  * --mode all (default): all 20 slots, fresh manifest (overwrites manifest videos list).
  * --mode daily --day N: slots for day N only (4 videos); appends to manifest when it already exists.

CI pick (GITHUB_OUTPUT):
  * --pick-for-ci: reads state + optional DAY_OVERRIDE env → day_num, should_run, advance_state.

State (after a successful daily generate, from CI only):
  * --advance-day N: bump next_day in state file (run in the same job step as git commit).

Usage:
  python scripts/run_brand_micro_batch.py --output ./generated --mode all
  python scripts/run_brand_micro_batch.py --output ./generated --mode daily --day 2
  python scripts/run_brand_micro_batch.py --pick-for-ci --state-file data/brand_micro_batch_state.json
  python scripts/run_brand_micro_batch.py --reset-state
  python scripts/run_brand_micro_batch.py --advance-day 2 --state-file data/brand_micro_batch_state.json
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
DEFAULT_STATE = _REPO / "data" / "brand_micro_batch_state.json"
SLOTS_PER_DAY = 4
TOTAL_SLOTS = 20
MAX_DAY = TOTAL_SLOTS // SLOTS_PER_DAY


def _github_output(name: str, value: str) -> None:
    path = os.environ.get("GITHUB_OUTPUT")
    if not path:
        return
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(f"{name}={value}\n")


def load_slots(spec_path: Path) -> list[dict]:
    with open(spec_path, encoding="utf-8") as f:
        data = json.load(f)
    slots = data.get("slots") or []
    if len(slots) != TOTAL_SLOTS:
        raise SystemExit(f"Expected {TOTAL_SLOTS} slots in spec, got {len(slots)}")
    return slots


def slots_for_day(all_slots: list[dict], day: int) -> list[dict]:
    if day < 1 or day > MAX_DAY:
        raise SystemExit(f"day must be 1..{MAX_DAY}, got {day}")
    lo = (day - 1) * SLOTS_PER_DAY + 1
    hi = day * SLOTS_PER_DAY
    return [s for s in all_slots if lo <= s["slot"] <= hi]


def load_state(path: Path) -> dict:
    if not path.exists():
        return {
            "schema_version": 1,
            "next_day": 1,
            "completed": False,
            "slots_per_day": SLOTS_PER_DAY,
            "total_slots": TOTAL_SLOTS,
        }
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


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


def cmd_pick_for_ci(state_file: Path) -> None:
    override = os.environ.get("DAY_OVERRIDE", "").strip()
    dry = os.environ.get("PICK_DRY_RUN", "").strip().lower() in ("1", "true", "yes")
    full = os.environ.get("RUN_FULL_BATCH", "").strip().lower() in ("1", "true", "yes")

    if full:
        _github_output("mode", "all")
        _github_output("day_num", "0")
        _github_output("should_run", "true")
        _github_output("advance_state", "false")
        print("pick-for-ci: mode=all should_run=true advance_state=false")
        return

    state = load_state(state_file)

    if override:
        day = int(override)
        if day < 1 or day > MAX_DAY:
            raise SystemExit(f"DAY_OVERRIDE must be 1..{MAX_DAY}, got {day}")
        should = "true"
        advance = "false"
    elif state.get("completed"):
        should = "false"
        day = 0
        advance = "false"
    else:
        day = int(state.get("next_day", 1))
        if day < 1 or day > MAX_DAY:
            raise SystemExit(f"Invalid next_day in state: {day!r}")
        should = "true"
        advance = "false" if dry else "true"

    _github_output("mode", "daily")
    _github_output("day_num", str(day))
    _github_output("should_run", should)
    _github_output("advance_state", advance)
    print(f"pick-for-ci: mode=daily day_num={day} should_run={should} advance_state={advance}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Brand micro batch v1 generator")
    ap.add_argument("--output", "-o", default="./generated", help="Output directory")
    ap.add_argument("--spec", type=Path, default=DEFAULT_SPEC, help="Batch JSON spec path")
    ap.add_argument("--state-file", type=Path, default=DEFAULT_STATE, help="Progress JSON for daily mode")
    ap.add_argument("--dry-run", action="store_true", help="Print plan only")
    ap.add_argument(
        "--mode",
        choices=("all", "daily"),
        default="all",
        help="all=20 videos; daily=4 for --day",
    )
    ap.add_argument("--day", type=int, default=None, metavar="N", help="Day 1..5 (daily mode)")
    ap.add_argument(
        "--advance-day",
        type=int,
        default=None,
        metavar="N",
        help="Mark daily day N complete: set next_day=N+1 and completed if N==5 (state file only)",
    )
    ap.add_argument("--pick-for-ci", action="store_true", help="Emit day_num / should_run / advance_state for GITHUB_OUTPUT")
    ap.add_argument("--reset-state", action="store_true", help="Reset state file to day 1 and exit")
    args = ap.parse_args()

    if args.pick_for_ci:
        cmd_pick_for_ci(args.state_file)
        return

    if args.advance_day is not None:
        if args.advance_day < 1 or args.advance_day > MAX_DAY:
            raise SystemExit(f"--advance-day must be 1..{MAX_DAY}")
        state = load_state(args.state_file)
        state["next_day"] = args.advance_day + 1
        if args.advance_day >= MAX_DAY:
            state["completed"] = True
        write_state(args.state_file, state)
        print(
            f"Advanced state after day {args.advance_day}: {args.state_file} → next_day={state['next_day']}, completed={state.get('completed')}"
        )
        return

    if args.reset_state:
        write_state(
            args.state_file,
            {
                "schema_version": 1,
                "next_day": 1,
                "completed": False,
                "slots_per_day": SLOTS_PER_DAY,
                "total_slots": TOTAL_SLOTS,
            },
        )
        print(f"Reset state: {args.state_file}")
        return

    slots_all = load_slots(args.spec)
    out_dir = Path(args.output)
    os.makedirs(out_dir, exist_ok=True)

    if args.mode == "daily":
        if args.day is None:
            raise SystemExit("--mode daily requires --day N (1..5)")
        slots_today = slots_for_day(slots_all, args.day)
    else:
        slots_today = slots_all

    if args.dry_run:
        print(f"Brand micro batch v1 (dry run) mode={args.mode}\n")
        if args.mode == "daily":
            print(f"  Day {args.day}/{MAX_DAY} — slots: {[s['slot'] for s in slots_today]}\n")
        for s in slots_today:
            print(
                f"  slot {s['slot']:2d}  {s['mood']}  {s['duration_s']}s  [{s['bucket']}]  thumb:{s['thumbnail_text']}"
            )
        print(f"\nWould write/append manifest under {out_dir / 'manifest.json'}")
        return

    from batch_generate import generate_single  # noqa: E402

    results: list[dict] = []
    for s in slots_today:
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
    for r, s in zip(results, slots_today):
        if r["status"] == "success":
            entry = extract_video_info(r["result"], r["mood"], r["duration"], r["seed"])
            entry["batch_slot"] = s["slot"]
            entry["bucket"] = s["bucket"]
            entry["thumbnail_text"] = s.get("thumbnail_text", "")
            manifest_videos.append(entry)

    mp = out_dir / "manifest.json"
    existing: list[dict] = []
    meta_runs: list[dict] = []
    if mp.exists() and args.mode == "daily":
        try:
            old = json.loads(mp.read_text(encoding="utf-8"))
            existing = old.get("videos", [])
            meta_runs = old.get("daily_runs", [])
        except (json.JSONDecodeError, OSError):
            existing = []

    run_meta = {
        "generated_at": datetime.now().isoformat(),
        "mode": args.mode,
        "day": args.day,
        "videos_in_run": len(manifest_videos),
    }
    meta_runs = meta_runs + [run_meta]

    manifest = {
        "generated_at": datetime.now().isoformat(),
        "batch": "brand_micro_batch_v1",
        "spec_path": str(args.spec.resolve()),
        "total_videos": len(existing) + len(manifest_videos),
        "videos": existing + manifest_videos,
        "daily_runs": meta_runs,
    }
    if args.mode == "daily" and args.day is not None:
        manifest["current_day"] = args.day

    with open(mp, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, default=str)
    print(f"\n📄 Manifest saved: {mp} ({len(manifest_videos)} new, {len(existing)} prior, {manifest['total_videos']} total)")


if __name__ == "__main__":
    main()
