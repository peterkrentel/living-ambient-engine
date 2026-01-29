#!/usr/bin/env python3
"""
Content Library CLI - Query and View Generated Content
Browse the catalog of generated videos with YouTube links.
"""

import click
import json
from pathlib import Path
from library import ContentLibrary


@click.group()
def cli():
    """Content Library - Browse your generated video catalog."""
    pass


@cli.command()
@click.option('--catalog-path', help='Path to catalog file (default: content_catalog.json)')
def stats(catalog_path: str):
    """Show catalog statistics."""
    library = ContentLibrary(catalog_path=catalog_path)
    stats = library.get_stats()
    
    click.echo("\n📊 Content Library Statistics\n")
    click.echo(f"Total Videos: {stats['total_videos']}")
    click.echo(f"Total Duration: {stats['total_duration_hours']} hours")
    
    if stats['total_videos'] > 0:
        click.echo(f"Average Duration: {stats['average_duration_minutes']} minutes")
        click.echo("\nVideos by Mood:")
        for mood, count in sorted(stats['moods'].items()):
            click.echo(f"  • {mood.replace('_', ' ').title()}: {count}")
    click.echo()


@cli.command()
@click.option('--catalog-path', help='Path to catalog file (default: content_catalog.json)')
@click.option('--mood', '-m', help='Filter by mood')
@click.option('--rhythm', '-r', help='Filter by rhythm')
@click.option('--min-duration', type=int, help='Minimum duration in seconds')
@click.option('--max-duration', type=int, help='Maximum duration in seconds')
@click.option('--version', '-v', help='Filter by version (e.g., pure_ambience, with_music)')
@click.option('--json-output', '-j', is_flag=True, help='Output as JSON')
def search(catalog_path: str, mood: str, rhythm: str, min_duration: int, max_duration: int, version: str, json_output: bool):
    """Search for videos in the catalog."""
    library = ContentLibrary(catalog_path=catalog_path)
    
    results = library.search(
        mood=mood,
        rhythm=rhythm,
        min_duration=min_duration,
        max_duration=max_duration,
        version=version
    )
    
    if json_output:
        click.echo(json.dumps(results, indent=2, default=str))
        return
    
    click.echo(f"\n🔍 Found {len(results)} videos\n")
    
    for video in results:
        version_tag = f" [{video['version']}]" if video['version'] != 'standard' else ""
        click.echo(f"📹 {video['title']}{version_tag}")
        click.echo(f"   🔗 {video['youtube_url']}")
        click.echo(f"   ⏱️  {video['duration_str']} | 🎨 {video['mood']} | 🥁 {video['rhythm_name']}")
        click.echo(f"   📅 {video['uploaded_at'][:10]} | 🎲 Seed: {video['seed']}")
        click.echo()


@cli.command()
@click.option('--catalog-path', help='Path to catalog file (default: content_catalog.json)')
@click.option('--output', '-o', default='CONTENT_LIBRARY.md', help='Output markdown file')
def export(catalog_path: str, output: str):
    """Export catalog as markdown."""
    library = ContentLibrary(catalog_path=catalog_path)
    md_path = library.export_markdown(output_path=output)
    click.echo(f"✅ Exported catalog to: {md_path}")


@cli.command()
@click.option('--catalog-path', help='Path to catalog file (default: content_catalog.json)')
@click.option('--mood', '-m', help='Filter by mood')
def list(catalog_path: str, mood: str):
    """List all videos or videos by mood."""
    library = ContentLibrary(catalog_path=catalog_path)
    
    if mood:
        videos = library.get_by_mood(mood)
        click.echo(f"\n📚 Videos with mood '{mood}': {len(videos)}\n")
    else:
        videos = library.get_all_videos()
        click.echo(f"\n📚 All Videos: {len(videos)}\n")
    
    for video in videos:
        version_tag = f" [{video['version']}]" if video['version'] != 'standard' else ""
        click.echo(f"• {video['title']}{version_tag}")
        click.echo(f"  🔗 {video['youtube_url']}")
        click.echo(f"  ⏱️  {video['duration_str']} | 🎲 Seed: {video['seed']}")
        click.echo()


@cli.command()
@click.option('--catalog-path', help='Path to catalog file (default: content_catalog.json)')
@click.argument('youtube_id')
def get(catalog_path: str, youtube_id: str):
    """Get details for a specific video by YouTube ID."""
    library = ContentLibrary(catalog_path=catalog_path)
    
    # Find video by YouTube ID
    video = None
    for v in library.get_all_videos():
        if v['youtube_id'] == youtube_id:
            video = v
            break
    
    if not video:
        click.echo(f"❌ Video not found: {youtube_id}")
        return
    
    click.echo(f"\n📹 {video['title']}")
    click.echo(f"\n🔗 YouTube: {video['youtube_url']}")
    click.echo(f"📋 Catalog ID: {video['catalog_id']}")
    click.echo(f"🎨 Mood: {video['mood']}")
    click.echo(f"⏱️  Duration: {video['duration_str']} ({video['duration']} seconds)")
    click.echo(f"🥁 Rhythm: {video['rhythm_name']}")
    click.echo(f"📦 Version: {video['version']}")
    click.echo(f"🎲 Seed: {video['seed']}")
    click.echo(f"📅 Generated: {video['generated_at'][:10]}")
    click.echo(f"📤 Uploaded: {video['uploaded_at'][:10]}")
    click.echo()


if __name__ == '__main__':
    cli()
