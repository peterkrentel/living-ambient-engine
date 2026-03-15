#!/usr/bin/env python3
"""
Batch Video Generator - Content Factory
Generates multiple videos across moods and durations for YouTube automation.
"""

import click
import os
import sys
import re
import json
from datetime import datetime
from pathlib import Path
import yaml

from orchestrator.orchestrator import Orchestrator


def load_moods(config_dir: str = "config") -> list:
    """Load all available moods from config."""
    moods_path = Path(config_dir) / "moods.yaml"
    with open(moods_path, 'r') as f:
        moods = yaml.safe_load(f)
    return list(moods.keys())


def parse_duration(duration_str: str) -> int:
    """Parse duration string like '1h', '30m', '2h', '10min', '1.5h' to seconds.

    Supports: 30s, 5sec, 10m, 10min, 1h, 1hr, 1hour, 1.5h, plain integers (seconds)
    """
    duration_str = duration_str.strip().lower()

    # Regex pattern: optional float/int followed by unit
    match = re.match(r'^(\d+(?:\.\d+)?)\s*(h|hr|hour|hours|m|min|mins|minutes|s|sec|secs|seconds)?$', duration_str)

    if not match:
        raise ValueError(f"Invalid duration format: '{duration_str}'. Use formats like: 30s, 10min, 1h, 1.5h")

    value = float(match.group(1))
    unit = match.group(2) or 's'  # Default to seconds if no unit

    if unit in ('h', 'hr', 'hour', 'hours'):
        return int(value * 3600)
    elif unit in ('m', 'min', 'mins', 'minutes'):
        return int(value * 60)
    elif unit in ('s', 'sec', 'secs', 'seconds'):
        return int(value)
    else:
        return int(value)


def generate_single(mood: str, duration: int, output_dir: str, seed: int = None, dual: bool = False) -> dict:
    """Generate a single video or dual videos (for parallel execution)."""
    try:
        orchestrator = Orchestrator()
        if dual:
            result = orchestrator.generate_dual(mood=mood, duration=duration, output_dir=output_dir, seed=seed)
            # Return info about both versions
            return {
                "status": "success",
                "mood": mood,
                "duration": duration,
                "dual": True,
                "seed": result['ambience']['metadata']['seed'],
                "result": result['ambience'],  # Primary result for manifest
                "result_ambience": result['ambience'],
                "result_melody": result['melody']
            }
        else:
            result = orchestrator.generate(mood=mood, duration=duration, output_dir=output_dir, seed=seed)
            return {"status": "success", "mood": mood, "duration": duration, "dual": False, "seed": result['metadata']['seed'], "result": result}
    except Exception as e:
        return {"status": "error", "mood": mood, "duration": duration, "error": str(e)}


@click.command()
@click.option('--moods', '-m', default='all', help='Comma-separated moods or "all"')
@click.option('--durations', '-d', default='1h,2h', help='Comma-separated durations (e.g., "30m,1h,2h,4h,1.5h")')
@click.option('--output', '-o', default='./batch_output', help='Output directory')
@click.option('--dual', is_flag=True, help='Generate BOTH ambience-only and melody versions for each video')
@click.option('--dry-run', is_flag=True, help='Show what would be generated without generating')
@click.option('--list-moods', '-l', is_flag=True, help='List available moods')
@click.option('--append-manifest', is_flag=True, help='Append to existing manifest.json instead of overwriting')
def main(moods: str, durations: str, output: str, dual: bool, dry_run: bool, list_moods: bool, append_manifest: bool):
    """
    Batch Video Generator - Generative Ambient Art Engine

    Generate multiple videos for publishing.

    Examples:
        # Generate all moods at 1h and 2h durations
        python batch_generate.py --moods all --durations 1h,2h

        # Generate specific moods
        python batch_generate.py --moods deep_focus,sleep,trance --durations 30m,1h

        # Generate DUAL output (both ambience and melody versions)
        python batch_generate.py --moods rain_sleep,ocean_waves --durations 3h --dual

        # Dry run to see what would be generated
        python batch_generate.py --moods all --durations 1h,2h,4h --dry-run
    """
    available_moods = load_moods()

    if list_moods:
        click.echo("Available moods:")
        for mood in available_moods:
            click.echo(f"  - {mood}")
        return

    # Parse moods
    if moods.lower() == 'all':
        selected_moods = available_moods
    else:
        selected_moods = [m.strip() for m in moods.split(',')]
        # Validate moods
        for m in selected_moods:
            if m not in available_moods:
                click.echo(f"❌ Unknown mood: {m}", err=True)
                click.echo(f"Available: {', '.join(available_moods)}", err=True)
                sys.exit(1)

    # Parse durations
    try:
        duration_list = [parse_duration(d.strip()) for d in durations.split(',')]
    except ValueError as e:
        click.echo(f"❌ {e}", err=True)
        sys.exit(1)
    
    # Calculate total jobs
    jobs = [(mood, dur) for mood in selected_moods for dur in duration_list]
    total_jobs = len(jobs)
    total_videos = total_jobs * 2 if dual else total_jobs

    mode_str = "DUAL (Ambience + Melody)" if dual else "SINGLE"
    click.echo(f"\n🏭 CONTENT FACTORY - Batch Generator ({mode_str})")
    click.echo(f"{'='*60}")
    click.echo(f"📋 Moods: {len(selected_moods)} ({', '.join(selected_moods[:3])}{'...' if len(selected_moods) > 3 else ''})")
    click.echo(f"⏱️  Durations: {', '.join(durations.split(','))}")
    click.echo(f"📦 Total jobs: {total_jobs}")
    if dual:
        click.echo(f"🔀 Mode: DUAL - generating {total_videos} videos (2 per job)")
    click.echo(f"📁 Output: {output}")

    if dry_run:
        click.echo(f"\n🔍 DRY RUN - Would generate:")
        for mood, dur in jobs:
            dur_str = f"{dur//3600}h" if dur >= 3600 else f"{dur//60}m"
            if dual:
                click.echo(f"  - {mood} @ {dur_str} (AMBIENCE + MELODY)")
            else:
                click.echo(f"  - {mood} @ {dur_str}")
        return

    # Create output directory
    os.makedirs(output, exist_ok=True)

    # Generate videos
    click.echo(f"\n🚀 Starting generation...")
    results = []

    for i, (mood, dur) in enumerate(jobs, 1):
        dur_str = f"{dur//3600}h" if dur >= 3600 else f"{dur//60}m"
        mode_label = " (DUAL)" if dual else ""
        click.echo(f"\n[{i}/{total_jobs}] Generating {mood} @ {dur_str}{mode_label}...")

        result = generate_single(mood, dur, output, dual=dual)
        results.append(result)

        if result["status"] == "success":
            if dual:
                click.echo(f"  ✅ Ambience: {result['result_ambience']['video_path']}")
                click.echo(f"  ✅ Melody:   {result['result_melody']['video_path']}")
            else:
                click.echo(f"  ✅ Done: {result['result']['video_path']}")
        else:
            click.echo(f"  ❌ Error: {result['error']}")

    # Summary
    success = sum(1 for r in results if r["status"] == "success")
    videos_generated = success * 2 if dual else success
    click.echo(f"\n{'='*60}")
    click.echo(f"✨ BATCH COMPLETE: {success}/{total_jobs} jobs successful ({videos_generated} videos)")

    # Save manifest - only upload-relevant fields (slim format)
    def extract_video_info(result_obj, mood, duration, seed, variant="full"):
        """Extract only upload-relevant fields from generation result."""
        metadata = result_obj.get("metadata", {})
        return {
            "mood": mood,
            "duration": duration,
            "seed": seed,
            "variant": variant,  # "ambience" or "melody" or "full"
            "video_path": result_obj.get("video_path"),
            "thumbnail_path": result_obj.get("thumbnail_path"),
            "metadata_path": result_obj.get("metadata_path"),
            "title": metadata.get("video_title", "Unknown"),
            "description": metadata.get("description", ""),
            "tags": metadata.get("tags", []),
            "created_at": datetime.now().isoformat(),
            "upload_status": "pending",
            "video_id": None  # Filled after upload
        }

    manifest_videos = []
    for r in results:
        if r["status"] == "success":
            if r.get("dual"):
                # Add both versions to manifest
                manifest_videos.append(extract_video_info(
                    r["result_ambience"], r["mood"], r["duration"], r["seed"], "ambience"
                ))
                manifest_videos.append(extract_video_info(
                    r["result_melody"], r["mood"], r["duration"], r["seed"], "melody"
                ))
            else:
                manifest_videos.append(extract_video_info(
                    r["result"], r["mood"], r["duration"], r["seed"], "full"
                ))

    # Load existing manifest if appending
    manifest_path = Path(output) / "manifest.json"
    if append_manifest and manifest_path.exists():
        click.echo(f"📄 Loading existing manifest to append...")
        with open(manifest_path, 'r') as f:
            existing_manifest = json.load(f)

        # Merge videos
        existing_videos = existing_manifest.get("videos", [])
        manifest_videos = existing_videos + manifest_videos

        # Update totals
        total_jobs += existing_manifest.get("total_jobs", 0)
        success += existing_manifest.get("successful_jobs", 0)
        click.echo(f"  ✅ Appended {len(manifest_videos) - len(existing_videos)} new videos to existing {len(existing_videos)} videos")

    manifest = {
        "generated_at": datetime.now().isoformat(),
        "total_jobs": total_jobs,
        "successful_jobs": success,
        "failed_jobs": total_jobs - success,
        "dual_mode": dual,
        "total_videos": len(manifest_videos),
        "videos": manifest_videos
    }
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2, default=str)
    click.echo(f"📄 Manifest saved: {manifest_path} ({len(manifest_videos)} total videos)")


if __name__ == "__main__":
    main()

