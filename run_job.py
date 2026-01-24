#!/usr/bin/env python3
"""
Living Ambient Engine - CLI Entry Point

Generate hypnotic ambient videos with procedural audio and visuals.

Usage:
    python run_job.py --mood deep_focus --duration 120
    python run_job.py --mood sleep --duration 600 --output ./my_videos
    python run_job.py --list-moods
"""

import click
from pathlib import Path
from dotenv import load_dotenv
from orchestrator import Orchestrator


# Load environment variables
load_dotenv()


@click.command()
@click.option('--mood', '-m', type=str, help='Mood preset (e.g., deep_focus, sleep, chill)')
@click.option('--duration', '-d', type=int, help='Duration in seconds')
@click.option('--output', '-o', type=str, help='Output directory (optional)')
@click.option('--list-moods', '-l', is_flag=True, help='List available mood presets')
@click.option('--config-dir', type=str, default='config', help='Config directory path')
@click.option('--rhythm-volume', '-r', type=float, help='Tribal drum volume 0.0-1.0 (default: from config)')
@click.option('--drone-volume', '-v', type=float, help='Drone/ambient volume 0.0-1.0 (default: 1.0)')
def main(mood, duration, output, list_moods, config_dir, rhythm_volume, drone_volume):
    """Living Ambient Engine - Generate hypnotic ambient videos."""
    
    # Initialize orchestrator
    orchestrator = Orchestrator(config_dir=config_dir)
    
    # List moods if requested
    if list_moods:
        click.echo("\n🎨 Available Mood Presets:\n")
        moods = orchestrator.list_moods()
        for mood_name, description in moods.items():
            click.echo(f"  • {mood_name:15} - {description}")
        click.echo()
        return
    
    # Validate required arguments
    if not mood:
        click.echo("❌ Error: --mood is required (or use --list-moods to see options)")
        return
    
    if not duration:
        click.echo("❌ Error: --duration is required (in seconds)")
        return
    
    # Generate video
    try:
        mix_info = ""
        if rhythm_volume is not None:
            mix_info += f" | drums: {rhythm_volume:.0%}"
        if drone_volume is not None:
            mix_info += f" | drone: {drone_volume:.0%}"

        click.echo(f"\n🚀 Starting generation: {mood} ({duration}s){mix_info}\n")

        result = orchestrator.generate(
            mood=mood,
            duration=duration,
            output_dir=output,
            rhythm_volume=rhythm_volume,
            drone_volume=drone_volume
        )
        
        click.echo(f"\n✨ Generation complete!\n")
        click.echo(f"📹 Video:     {result['video_path']}")
        click.echo(f"📄 Metadata:  {result['metadata_path']}")
        click.echo(f"🖼️  Thumbnail: {result['thumbnail_path']}\n")
        
    except ValueError as e:
        click.echo(f"❌ Error: {e}")
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}")
        raise


if __name__ == '__main__':
    main()

