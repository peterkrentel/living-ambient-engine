#!/usr/bin/env python3
"""
YouTube Upload CLI - Content Factory
Upload generated videos to YouTube with metadata.
"""

import click
import json
import os
from pathlib import Path

from youtube.uploader import YouTubeUploader, GOOGLE_API_AVAILABLE


def generate_description(metadata: dict) -> str:
    """Generate SEO-optimized YouTube description."""
    mood = metadata.get('mood', 'ambient')
    rhythm = metadata.get('rhythm_name', 'Tribal')
    origin = metadata.get('rhythm_origin', '')
    duration = metadata.get('duration_str', '')
    
    return f"""🎵 {metadata.get('video_title', 'Ambient Music')}

{origin}

Perfect for:
• Deep focus and concentration
• Meditation and relaxation
• Sleep and rest
• Study sessions
• Yoga and mindfulness

🧠 Brainwave Entrainment:
This track uses scientifically-designed binaural beats and Solfeggio frequencies to help guide your mind into optimal states.

⏱️ Duration: {duration}
🥁 Rhythm: {rhythm}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔔 Subscribe for daily ambient content
👍 Like if this helps you focus

#AmbientMusic #BinauralBeats #Focus #Meditation #StudyMusic #SleepMusic #TribalBeats #{mood.replace('_', '')}
"""


def get_tags(metadata: dict) -> list:
    """Generate YouTube tags for SEO."""
    base_tags = [
        "ambient music", "binaural beats", "focus music", "study music",
        "meditation music", "relaxation", "concentration", "sleep music",
        "tribal drums", "healing frequencies", "432 hz", "528 hz",
        "theta waves", "alpha waves", "deep focus", "work music"
    ]
    
    mood = metadata.get('mood', '')
    rhythm = metadata.get('rhythm_name', '')
    
    if mood:
        base_tags.append(mood.replace('_', ' '))
    if rhythm:
        base_tags.append(f"{rhythm} rhythm")
        base_tags.append(f"{rhythm} drums")
    
    return base_tags[:30]  # YouTube limit


@click.command()
@click.option('--video', '-v', help='Path to video file')
@click.option('--metadata', '-m', help='Path to metadata JSON (auto-detected if not provided)')
@click.option('--privacy', '-p', default='public', type=click.Choice(['public', 'private', 'unlisted']))
@click.option('--auth', is_flag=True, help='Just authenticate (for first-time setup)')
@click.option('--batch', '-b', help='Upload all videos from manifest.json in directory')
def main(video: str, metadata: str, privacy: str, auth: bool, batch: str):
    """
    Upload videos to YouTube.
    
    First time setup:
        1. Get client_secrets.json from Google Cloud Console
        2. Run: python youtube_upload.py --auth
        
    Upload single video:
        python youtube_upload.py -v output/video.mp4
        
    Upload batch from manifest:
        python youtube_upload.py --batch ./batch_output
    """
    if not GOOGLE_API_AVAILABLE:
        click.echo("❌ Google API libraries not installed. Run:")
        click.echo("   pip install google-auth-oauthlib google-api-python-client")
        return
    
    uploader = YouTubeUploader()
    
    if auth:
        click.echo("🔐 Authenticating with YouTube...")
        uploader.authenticate()
        click.echo("✅ Authentication successful! Token saved.")
        return

    # Require video or batch if not just authenticating
    if not video and not batch:
        click.echo("❌ Either --video or --batch is required (or use --auth for setup)")
        return

    if batch:
        # Batch upload from manifest
        manifest_path = Path(batch) / "manifest.json"
        if not manifest_path.exists():
            click.echo(f"❌ Manifest not found: {manifest_path}")
            return
        
        with open(manifest_path) as f:
            manifest = json.load(f)
        
        videos = manifest.get('videos', [])
        click.echo(f"📦 Found {len(videos)} videos to upload")
        
        for i, v in enumerate(videos, 1):
            result = v.get('result', {})
            video_path = result.get('video_path')
            meta = result
            
            if not video_path or not os.path.exists(video_path):
                click.echo(f"  [{i}] ⏭️  Skipping (file not found)")
                continue
            
            click.echo(f"  [{i}/{len(videos)}] Uploading {Path(video_path).name}...")
            upload_single(uploader, video_path, meta, privacy)
        return
    
    # Single video upload
    if not video or not os.path.exists(video):
        click.echo(f"❌ Video not found: {video}")
        return
    
    # Auto-detect metadata
    if not metadata:
        metadata = video.replace('.mp4', '.json')
    
    meta = {}
    if os.path.exists(metadata):
        with open(metadata) as f:
            meta = json.load(f)
    
    upload_single(uploader, video, meta, privacy)


def upload_single(uploader: YouTubeUploader, video_path: str, meta: dict, privacy: str):
    """Upload a single video."""
    title = meta.get('video_title', Path(video_path).stem)
    description = generate_description(meta)
    tags = get_tags(meta)
    thumbnail = video_path.replace('.mp4', '.png')
    
    result = uploader.upload(
        video_path=video_path,
        title=title,
        description=description,
        tags=tags,
        privacy=privacy,
        thumbnail_path=thumbnail if os.path.exists(thumbnail) else None
    )
    
    click.echo(f"  ✅ Uploaded: {result['url']}")


if __name__ == "__main__":
    main()

