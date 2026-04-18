#!/usr/bin/env python3
"""Run personal long-form pressure batch from JSON spec (default: data/personal_long_batch_pressure_v1.json).

Spec-driven: slots_per_day, total_slots, default_dual, slots[]. CI helpers match brand micro batch:
  --pick-for-ci, --advance-day, --reset-state, --mode all|daily, --day N, optional --max-count.

Usage:
  python scripts/run_personal_long_batch.py --dry-run --mode daily --day 1
  python scripts/run_personal_long_batch.py --output ./generated --mode all
  python scripts/run_personal_long_batch.py --pick-for-ci --state-file data/personal_long_batch_pressure_state.json
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

DEFAULT_SPEC = _REPO / "data" / "personal_long_batch_pressure_v1.json"
DEFAULT_STATE = _REPO / "data" / "personal_long_batch_pressure_state.json"


def _github_output(name: str, value: str) -> None:
    path = os.environ.get("GITHUB_OUTPUT")
    if not path:
        return
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(f"{name}={value}\n")


def load_spec(spec_path: Path) -> dict:
    with open(spec_path, encoding="utf-8") as f:
        return json.load(f)


def spec_dims(spec: dict) -> tuple[int, int, str, bool]:
    slots = spec.get("slots") or []
    spd = int(spec.get("slots_per_day") or 0)
    tot = int(spec.get("total_slots") or 0)
    name = str(spec.get("name") or "personal_long_batch")
    dual = bool(spec.get("default_dual", False))
    if spd < 1 or tot < 1 or tot % spd != 0:
        raise SystemExit(f"Invalid slots_per_day/total_slots in spec: {spd!r}, {tot!r}")
    if len(slots) != tot:
        raise SystemExit(f"Expected {tot} slots in spec, got {len(slots)}")
    return spd, tot, name, dual


def load_slots(spec_path: Path) -> tuple[list[dict], dict]:
    spec = load_spec(spec_path)
    spd, tot, batch_name, default_dual = spec_dims(spec)
    slots = spec["slots"]
    for s in slots:
        if "slot" not in s or "mood" not in s or "duration_s" not in s:
            raise SystemExit(f"Each slot needs slot, mood, duration_s: {s!r}")
    return slots, {
        "spec": spec,
        "slots_per_day": spd,
        "total_slots": tot,
        "max_day": tot // spd,
        "batch_name": batch_name,
        "default_dual": default_dual,
    }


def slots_for_day(all_slots: list[dict], day: int, slots_per_day: int, max_day: int) -> list[dict]:
    if day < 1 or day > max_day:
        raise SystemExit(f"day must be 1..{max_day}, got {day}")
    lo = (day - 1) * slots_per_day + 1
    hi = day * slots_per_day
    return [s for s in all_slots if lo <= int(s["slot"]) <= hi]


def load_state(path: Path, meta: dict) -> dict:
    if not path.exists():
        return {
            "schema_version": 1,
            "batch": meta["batch_name"],
            "next_day": 1,
            "completed": False,
            "slots_per_day": meta["slots_per_day"],
            "total_slots": meta["total_slots"],
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


def cmd_pick_for_ci(state_file: Path, spec_path: Path) -> None:
    override = os.environ.get("DAY_OVERRIDE", "").strip()
    dry = os.environ.get("PICK_DRY_RUN", "").strip().lower() in ("1", "true", "yes")
    full = os.environ.get("RUN_FULL_BATCH", "").strip().lower() in ("1", "true", "yes")
    _, meta = load_slots(spec_path)
    max_day = meta["max_day"]

    if full:
        _github_output("mode", "all")
        _github_output("day_num", "0")
        _github_output("should_run", "true")
        _github_output("advance_state", "false")
        print("pick-for-ci: mode=all should_run=true advance_state=false")
        return

    state = load_state(state_file, meta)

    if override:
        day = int(override)
        if day < 1 or day > max_day:
            raise SystemExit(f"DAY_OVERRIDE must be 1..{max_day}, got {day}")
        should = "true"
        advance = "false"
    elif state.get("completed"):
        should = "false"
        day = 0
        advance = "false"
    else:
        day = int(state.get("next_day", 1))
        if day < 1 or day > max_day:
            raise SystemExit(f"Invalid next_day in state: {day!r}")
        should = "true"
        advance = "false" if dry else "true"

    _github_output("mode", "daily")
    _github_output("day_num", str(day))
    _github_output("should_run", should)
    _github_output("advance_state", advance)
    print(f"pick-for-ci: mode=daily day_num={day} should_run={should} advance_state={advance}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Personal long-form slot batch generator")
    ap.add_argument("--output", "-o", default="./generated", help="Output directory")
    ap.add_argument("--spec", type=Path, default=DEFAULT_SPEC, help="Batch JSON spec path")
    ap.add_argument("--state-file", type=Path, default=DEFAULT_STATE, help="Progress JSON for daily mode")
    ap.add_argument("--dry-run", action="store_true", help="Print plan only")
    ap.add_argument("--mode", choices=("all", "daily"), default="all", help="all=entire spec; daily=one day slice")
    ap.add_argument("--day", type=int, default=None, metavar="N", help="Day index (1 .. total_slots/slots_per_day)")
    ap.add_argument(
        "--max-count",
        type=int,
        default=None,
        metavar="N",
        help="Process at most N slots (prefix of slice; CI smoke)",
    )
    ap.add_argument(
        "--advance-day",
        type=int,
        default=None,
        metavar="N",
        help="Mark daily day N complete in state file",
    )
    ap.add_argument("--pick-for-ci", action="store_true", help="Emit GITHUB_OUTPUT for workflow pick job")
    ap.add_argument("--reset-state", action="store_true", help="Reset state file from spec dims")
    args = ap.parse_args()

    slots_all, meta = load_slots(args.spec)
    spd, tot, batch_name, default_dual = (
        meta["slots_per_day"],
        meta["total_slots"],
        meta["batch_name"],
        meta["default_dual"],
    )
    max_day = meta["max_day"]

    if args.pick_for_ci:
        cmd_pick_for_ci(args.state_file, args.spec)
        return

    if args.advance_day is not None:
        if args.advance_day < 1 or args.advance_day > max_day:
            raise SystemExit(f"--advance-day must be 1..{max_day}")
        state = load_state(args.state_file, meta)
        state["next_day"] = args.advance_day + 1
        if args.advance_day >= max_day:
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
                "batch": batch_name,
                "next_day": 1,
                "completed": False,
                "slots_per_day": spd,
                "total_slots": tot,
            },
        )
        print(f"Reset state: {args.state_file}")
        return

    out_dir = Path(args.output)
    os.makedirs(out_dir, exist_ok=True)

    if args.mode == "daily":
        if args.day is None:
            raise SystemExit("--mode daily requires --day N")
        slots_today = slots_for_day(slots_all, args.day, spd, max_day)
    else:
        slots_today = slots_all

    if args.max_count is not None and args.max_count >= 0:
        slots_today = slots_today[: args.max_count]

    if args.dry_run:
        print(f"Personal long batch {batch_name} (dry run) mode={args.mode}\n")
        if args.mode == "daily" and args.day is not None:
            print(f"  Day {args.day}/{max_day} — {len(slots_today)} slot(s)\n")
        for s in slots_today:
            du = s.get("dual", default_dual)
            print(f"  slot {int(s['slot']):2d}  {s['mood']}  {int(s['duration_s'])}s  dual={du}  [{s.get('bucket', '')}]")
        print(f"\nWould write/append manifest under {out_dir / 'manifest.json'}")
        return

    from batch_generate import generate_single  # noqa: E402

    results: list[dict] = []
    for s in slots_today:
        mood = s["mood"]
        dur = int(s["duration_s"])
        dual = bool(s.get("dual", default_dual))
        print(f"\n=== Slot {s['slot']} | {mood} @ {dur}s dual={dual} ===")
        r = generate_single(mood, dur, str(out_dir), dual=dual)
        results.append(r)
        if r["status"] != "success":
            print(f"❌ Failed: {r.get('error')}")
            sys.exit(1)
        print(f"✅ {r['result']['video_path']}")

    manifest_videos = []
    for r, s in zip(results, slots_today):
        if r["status"] == "success":
            entry = extract_video_info(r["result"], r["mood"], r["duration"], r["seed"])
            entry["batch_slot"] = int(s["slot"])
            entry["bucket"] = s.get("bucket", "")
            entry["dual"] = bool(s.get("dual", default_dual))
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
        "batch": batch_name,
    }
    meta_runs = meta_runs + [run_meta]

    manifest = {
        "generated_at": datetime.now().isoformat(),
        "batch": batch_name,
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
