#!/usr/bin/env python3
"""
Single Video Generator - Fine-grained control for individual videos.
Generate one video at a time with full parameter control and reproducibility.
"""

import click
import sys
import re
import yaml
from pathlib import Path
from orchestrator.orchestrator import Orchestrator


def load_moods(config_dir: str = "config") -> dict:
    """Load all mood configurations from ``config/moods.yaml``."""
    moods_path = Path(config_dir) / "moods.yaml"
    with open(moods_path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


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


@click.command()
@click.option('--mood', '-m', required=True, help='Mood preset name')
@click.option('--duration', '-d', required=True, help='Duration (e.g., 30s, 10min, 1h, 3h)')
@click.option('--seed', '-s', type=int, default=None, help='Random seed for reproducibility')
@click.option('--output', '-o', default='./output', help='Output directory')
@click.option('--rhythm-volume', type=float, default=None, help='Override rhythm volume (0.0-1.0)')
@click.option('--drone-volume', type=float, default=None, help='Override drone/ambient volume (0.0-1.0)')
@click.option('--dual', is_flag=True, help='Generate BOTH ambience-only and melody versions')
@click.option('--list-moods', '-l', is_flag=True, help='List all available moods')
@click.option('--show-params', '-p', is_flag=True, help='Show parameters for a mood')
def main(mood: str, duration: str, seed: int, output: str, rhythm_volume: float,
         drone_volume: float, dual: bool, list_moods: bool, show_params: bool):
    """
    Single Video Generator - Generate one video with full control.

    Examples:
        # Generate with random seed
        python generate_single.py --mood rain_sleep --duration 1h

        # Generate with specific seed (reproducible)
        python generate_single.py --mood rain_sleep --duration 1h --seed 12345

        # Generate BOTH ambience and melody versions (dual output)
        python generate_single.py --mood rain_sleep --duration 1h --dual

        # Reproduce a video from metadata
        python generate_single.py --mood rain_sleep --duration 1h --seed 987654321

        # Override volume settings
        python generate_single.py --mood deep_focus --duration 30min --rhythm-volume 0.3

        # Show all available moods
        python generate_single.py --list-moods

        # Show parameters for a mood
        python generate_single.py --mood rain_sleep --show-params
    """
    moods = load_moods()
    
    if list_moods:
        click.echo("\n🎭 Available Moods:")
        click.echo("=" * 60)
        for name, config in moods.items():
            desc = config.get('description', 'No description')
            click.echo(f"  {name:20} - {desc}")
        return
    
    if show_params:
        if mood not in moods:
            click.echo(f"❌ Unknown mood: {mood}", err=True)
            click.echo(f"Available: {', '.join(moods.keys())}", err=True)
            sys.exit(1)
        
        click.echo(f"\n🎛️  Parameters for '{mood}':")
        click.echo("=" * 60)
        config = moods[mood]
        click.echo(f"\nDescription: {config.get('description', 'N/A')}")
        click.echo(f"Title Template: {config.get('title_template', 'N/A')}")
        
        click.echo("\n📺 Visual Config:")
        for key, val in config.get('visual', {}).items():
            click.echo(f"  {key}: {val}")
        
        click.echo("\n🎵 Audio Config:")
        for key, val in config.get('audio', {}).items():
            if key == 'layers':
                click.echo(f"  layers:")
                for i, layer in enumerate(val):
                    click.echo(f"    [{i}] {layer}")
            else:
                click.echo(f"  {key}: {val}")
        return
    
    # Validate mood
    if mood not in moods:
        click.echo(f"❌ Unknown mood: {mood}", err=True)
        click.echo(f"Available: {', '.join(moods.keys())}", err=True)
        sys.exit(1)

    # Parse duration
    try:
        duration_seconds = parse_duration(duration)
    except ValueError as e:
        click.echo(f"❌ {e}", err=True)
        sys.exit(1)
    duration_display = f"{duration_seconds//3600}h" if duration_seconds >= 3600 else f"{duration_seconds//60}m" if duration_seconds >= 60 else f"{duration_seconds}s"

    mode_str = "DUAL OUTPUT (Ambience + Melody)" if dual else "SINGLE VIDEO"
    click.echo(f"\n🎬 {mode_str} GENERATOR")
    click.echo("=" * 60)
    click.echo(f"📋 Mood: {mood}")
    click.echo(f"⏱️  Duration: {duration_display} ({duration_seconds}s)")
    click.echo(f"🎲 Seed: {seed if seed else 'Auto-generated'}")
    click.echo(f"📁 Output: {output}")
    if dual:
        click.echo(f"🔀 Mode: Generating BOTH ambience-only and melody versions")
    if rhythm_volume is not None:
        click.echo(f"🥁 Rhythm Volume: {rhythm_volume}")
    if drone_volume is not None:
        click.echo(f"🎹 Drone Volume: {drone_volume}")
    click.echo("=" * 60)

    # Generate
    orchestrator = Orchestrator()

    if dual:
        # Generate both versions
        result = orchestrator.generate_dual(
            mood=mood,
            duration=duration_seconds,
            output_dir=output,
            seed=seed
        )

        click.echo(f"\n✨ DUAL VIDEOS GENERATED!")
        click.echo(f"\n🌧️  AMBIENCE VERSION (no melody - top YouTube performer):")
        click.echo(f"   📹 Video: {result['ambience']['video_path']}")
        click.echo(f"   📋 Metadata: {result['ambience']['metadata_path']}")
        click.echo(f"   🖼️  Thumbnail: {result['ambience']['thumbnail_path']}")
        click.echo(f"\n🎵 MELODY VERSION (with music):")
        click.echo(f"   📹 Video: {result['melody']['video_path']}")
        click.echo(f"   📋 Metadata: {result['melody']['metadata_path']}")
        click.echo(f"   🖼️  Thumbnail: {result['melody']['thumbnail_path']}")
        click.echo(f"\n🎲 Seed used: {result['ambience']['metadata']['seed']}")
        click.echo(f"   (Save this seed to reproduce these exact videos)")
    else:
        # Generate single version
        result = orchestrator.generate(
            mood=mood,
            duration=duration_seconds,
            output_dir=output,
            rhythm_volume=rhythm_volume,
            drone_volume=drone_volume,
            seed=seed
        )

        click.echo(f"\n✨ VIDEO GENERATED!")
        click.echo(f"📹 Video: {result['video_path']}")
        click.echo(f"📋 Metadata: {result['metadata_path']}")
        click.echo(f"🖼️  Thumbnail: {result['thumbnail_path']}")
        click.echo(f"\n🎲 Seed used: {result['metadata']['seed']}")
        click.echo(f"   (Save this seed to reproduce this exact video)")


if __name__ == "__main__":
    main()

