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
    try:
        library = ContentLibrary(catalog_path=catalog_path)
    except Exception as e:
        click.echo(f"❌ Error loading catalog: {e}")
        return
    
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
    try:
        library = ContentLibrary(catalog_path=catalog_path)
    except Exception as e:
        click.echo(f"❌ Error loading catalog: {e}")
        return
    
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
        version = video.get('version', 'standard')
        version_tag = f" [{version}]" if version != 'standard' else ""
        
        title = video.get('title', 'Unknown')
        youtube_url = video.get('youtube_url', '#')
        duration_str = video.get('duration_str', 'Unknown')
        mood = video.get('mood', 'unknown')
        rhythm_name = video.get('rhythm_name', 'Unknown')
        uploaded_at = video.get('uploaded_at', '')[:10] if video.get('uploaded_at') else 'Unknown'
        seed = video.get('seed', 'Unknown')
        
        click.echo(f"📹 {title}{version_tag}")
        click.echo(f"   🔗 {youtube_url}")
        click.echo(f"   ⏱️  {duration_str} | 🎨 {mood} | 🥁 {rhythm_name}")
        click.echo(f"   📅 {uploaded_at} | 🎲 Seed: {seed}")
        click.echo()


@cli.command()
@click.option('--catalog-path', help='Path to catalog file (default: content_catalog.json)')
@click.option('--output', '-o', default='CONTENT_LIBRARY.md', help='Output markdown file')
def export(catalog_path: str, output: str):
    """Export catalog as markdown."""
    try:
        library = ContentLibrary(catalog_path=catalog_path)
        md_path = library.export_markdown(output_path=output)
        click.echo(f"✅ Exported catalog to: {md_path}")
    except Exception as e:
        click.echo(f"❌ Error exporting catalog: {e}")


@cli.command()
@click.option('--catalog-path', help='Path to catalog file (default: content_catalog.json)')
@click.option('--mood', '-m', help='Filter by mood')
def list(catalog_path: str, mood: str):
    """List all videos or videos by mood."""
    try:
        library = ContentLibrary(catalog_path=catalog_path)
    except Exception as e:
        click.echo(f"❌ Error loading catalog: {e}")
        return
    
    if mood:
        videos = library.get_by_mood(mood)
        click.echo(f"\n📚 Videos with mood '{mood}': {len(videos)}\n")
    else:
        videos = library.get_all_videos()
        click.echo(f"\n📚 All Videos: {len(videos)}\n")
    
    for video in videos:
        version = video.get('version', 'standard')
        version_tag = f" [{version}]" if version != 'standard' else ""
        
        title = video.get('title', 'Unknown')
        youtube_url = video.get('youtube_url', '#')
        duration_str = video.get('duration_str', 'Unknown')
        seed = video.get('seed', 'Unknown')
        
        click.echo(f"• {title}{version_tag}")
        click.echo(f"  🔗 {youtube_url}")
        click.echo(f"  ⏱️  {duration_str} | 🎲 Seed: {seed}")
        click.echo()


@cli.command()
@click.option('--catalog-path', help='Path to catalog file (default: content_catalog.json)')
@click.argument('youtube_id')
def get(catalog_path: str, youtube_id: str):
    """Get details for a specific video by YouTube ID."""
    try:
        library = ContentLibrary(catalog_path=catalog_path)
    except Exception as e:
        click.echo(f"❌ Error loading catalog: {e}")
        return
    
    # Find video by YouTube ID
    video = None
    for v in library.get_all_videos():
        if v.get('youtube_id') == youtube_id:
            video = v
            break
    
    if not video:
        click.echo(f"❌ Video not found: {youtube_id}")
        return
    
    title = video.get('title', 'Unknown')
    youtube_url = video.get('youtube_url', '#')
    catalog_id = video.get('catalog_id', 'Unknown')
    mood = video.get('mood', 'unknown')
    duration_str = video.get('duration_str', 'Unknown')
    duration = video.get('duration', 0)
    rhythm_name = video.get('rhythm_name', 'Unknown')
    version = video.get('version', 'standard')
    seed = video.get('seed', 'Unknown')
    generated_at = video.get('generated_at', '')[:10] if video.get('generated_at') else 'Unknown'
    uploaded_at = video.get('uploaded_at', '')[:10] if video.get('uploaded_at') else 'Unknown'
    
    click.echo(f"\n📹 {title}")
    click.echo(f"\n🔗 YouTube: {youtube_url}")
    click.echo(f"📋 Catalog ID: {catalog_id}")
    click.echo(f"🎨 Mood: {mood}")
    click.echo(f"⏱️  Duration: {duration_str} ({duration} seconds)")
    click.echo(f"🥁 Rhythm: {rhythm_name}")
    click.echo(f"📦 Version: {version}")
    click.echo(f"🎲 Seed: {seed}")
    click.echo(f"📅 Generated: {generated_at}")
    click.echo(f"📤 Uploaded: {uploaded_at}")
    click.echo()


if __name__ == '__main__':
    cli()
