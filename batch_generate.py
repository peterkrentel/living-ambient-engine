#!/usr/bin/env python3
"""
Batch Video Generator - Content Factory
Generates multiple videos across moods and durations for YouTube automation.
"""

import click
import os
import json
from datetime import datetime
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import yaml

from orchestrator.orchestrator import Orchestrator


def load_moods(config_dir: str = "config") -> list:
    """Load all available moods from config."""
    moods_path = Path(config_dir) / "moods.yaml"
    with open(moods_path, 'r') as f:
        moods = yaml.safe_load(f)
    return list(moods.keys())


def parse_duration(duration_str: str) -> int:
    """Parse duration string like '1h', '30m', '2h', '10min' to seconds."""
    duration_str = duration_str.strip().lower()
    if duration_str.endswith('h') or duration_str.endswith('hr') or duration_str.endswith('hour'):
        return int(duration_str.rstrip('hour').rstrip('hr').rstrip('h')) * 3600
    elif duration_str.endswith('min'):
        return int(duration_str[:-3]) * 60
    elif duration_str.endswith('m'):
        return int(duration_str[:-1]) * 60
    elif duration_str.endswith('s') or duration_str.endswith('sec'):
        return int(duration_str.rstrip('sec').rstrip('s'))
    else:
        return int(duration_str)


def generate_single(mood: str, duration: int, output_dir: str, seed: int = None) -> dict:
    """Generate a single video (for parallel execution)."""
    try:
        orchestrator = Orchestrator()
        result = orchestrator.generate(mood=mood, duration=duration, output_dir=output_dir, seed=seed)
        return {"status": "success", "mood": mood, "duration": duration, "seed": result['metadata']['seed'], "result": result}
    except Exception as e:
        return {"status": "error", "mood": mood, "duration": duration, "error": str(e)}


@click.command()
@click.option('--moods', '-m', default='all', help='Comma-separated moods or "all"')
@click.option('--durations', '-d', default='1h,2h', help='Comma-separated durations (e.g., "30m,1h,2h,4h")')
@click.option('--output', '-o', default='./batch_output', help='Output directory')
@click.option('--parallel', '-p', default=1, type=int, help='Parallel jobs (default: 1, use with caution)')
@click.option('--dry-run', is_flag=True, help='Show what would be generated without generating')
@click.option('--list-moods', '-l', is_flag=True, help='List available moods')
def main(moods: str, durations: str, output: str, parallel: int, dry_run: bool, list_moods: bool):
    """
    Batch Video Generator - Content Factory
    
    Generate multiple videos for YouTube automation.
    
    Examples:
        # Generate all moods at 1h and 2h durations
        python batch_generate.py --moods all --durations 1h,2h
        
        # Generate specific moods
        python batch_generate.py --moods deep_focus,sleep,trance --durations 30m,1h
        
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
                click.echo(f"❌ Unknown mood: {m}")
                click.echo(f"Available: {', '.join(available_moods)}")
                return
    
    # Parse durations
    duration_list = [parse_duration(d.strip()) for d in durations.split(',')]
    
    # Calculate total jobs
    jobs = [(mood, dur) for mood in selected_moods for dur in duration_list]
    total_jobs = len(jobs)
    
    click.echo(f"\n🏭 CONTENT FACTORY - Batch Generator")
    click.echo(f"{'='*50}")
    click.echo(f"📋 Moods: {len(selected_moods)} ({', '.join(selected_moods[:3])}{'...' if len(selected_moods) > 3 else ''})")
    click.echo(f"⏱️  Durations: {', '.join(durations.split(','))}")
    click.echo(f"📦 Total videos: {total_jobs}")
    click.echo(f"📁 Output: {output}")
    
    if dry_run:
        click.echo(f"\n🔍 DRY RUN - Would generate:")
        for mood, dur in jobs:
            dur_str = f"{dur//3600}h" if dur >= 3600 else f"{dur//60}m"
            click.echo(f"  - {mood} @ {dur_str}")
        return
    
    # Create output directory
    os.makedirs(output, exist_ok=True)
    
    # Generate videos
    click.echo(f"\n🚀 Starting generation...")
    results = []
    
    for i, (mood, dur) in enumerate(jobs, 1):
        dur_str = f"{dur//3600}h" if dur >= 3600 else f"{dur//60}m"
        click.echo(f"\n[{i}/{total_jobs}] Generating {mood} @ {dur_str}...")
        
        result = generate_single(mood, dur, output)
        results.append(result)
        
        if result["status"] == "success":
            click.echo(f"  ✅ Done: {result['result']['video_path']}")
        else:
            click.echo(f"  ❌ Error: {result['error']}")
    
    # Summary
    success = sum(1 for r in results if r["status"] == "success")
    click.echo(f"\n{'='*50}")
    click.echo(f"✨ BATCH COMPLETE: {success}/{total_jobs} videos generated")
    
    # Save manifest
    manifest = {
        "generated_at": datetime.now().isoformat(),
        "total": total_jobs,
        "success": success,
        "videos": [r for r in results if r["status"] == "success"]
    }
    manifest_path = Path(output) / "manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2, default=str)
    click.echo(f"📄 Manifest saved: {manifest_path}")


if __name__ == "__main__":
    main()

