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
from library import ContentLibrary


def generate_description(metadata: dict) -> str:
    """Generate SEO-optimized YouTube description based on mood type."""
    mood = metadata.get('mood', 'ambient')
    rhythm = metadata.get('rhythm_name', '')
    origin = metadata.get('rhythm_origin', '')
    duration = metadata.get('duration_str', '')
    title = metadata.get('video_title', 'Ambient Music')

    # Nature/ambient moods (no rhythm, pure ambience)
    nature_moods = ['rain_sleep', 'ocean_waves', 'fireplace', 'forest_morning']

    # Music moods with binaural beats
    music_moods = ['deep_focus', 'sleep', 'trance', 'ceremony', 'warrior', 'energize',
                   'study', 'chill', 'lofi_study', 'piano_relax']

    if mood in nature_moods:
        # Nature sounds description
        mood_descriptions = {
            'rain_sleep': "🌧️ Gentle rain sounds to help you relax, sleep, and unwind. The natural rhythm of rainfall creates the perfect ambient backdrop for rest and relaxation.",
            'ocean_waves': "🌊 Peaceful ocean waves washing onto the shore. Let the rhythmic sound of the sea carry away your stress and help you find deep relaxation.",
            'fireplace': "🔥 Cozy crackling fireplace sounds for ultimate relaxation. The warm, comforting ambience of a real fire to help you feel at home.",
            'forest_morning': "🌲 Immerse yourself in a peaceful forest morning with gentle birdsong and rustling leaves. Nature's own meditation soundtrack."
        }
        mood_desc = mood_descriptions.get(mood, "Natural ambient sounds for relaxation.")

        perfect_for = """Perfect for:
• Sleeping and relaxation
• Stress relief and unwinding
• Meditation and mindfulness
• Reading and quiet time
• Creating a cozy atmosphere
• Blocking out distractions"""

        hashtags = f"#{mood.replace('_', '')} #NatureSounds #Sleep #Relaxation #ASMR #WhiteNoise #AmbientSounds"

        return f"""🎵 {title}

{mood_desc}

{perfect_for}

⏱️ Duration: {duration}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔔 Subscribe for daily ambient content
👍 Like if this helps you relax

{hashtags}
"""

    else:
        # Music/beats description
        rhythm_info = f"\n🥁 Rhythm: {rhythm}" if rhythm and rhythm != 'Ambient' else ""
        origin_info = f"\n{origin}" if origin else ""

        perfect_for = """Perfect for:
• Deep focus and concentration
• Meditation and relaxation
• Sleep and rest
• Study sessions
• Yoga and mindfulness"""

        brainwave_info = """
🧠 Brainwave Entrainment:
This track uses scientifically-designed binaural beats and Solfeggio frequencies to help guide your mind into optimal states."""

        hashtags = f"#AmbientMusic #BinauralBeats #Focus #Meditation #StudyMusic #SleepMusic #{mood.replace('_', '')}"

        return f"""🎵 {title}
{origin_info}
{perfect_for}
{brainwave_info}

⏱️ Duration: {duration}{rhythm_info}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔔 Subscribe for daily ambient content
👍 Like if this helps you focus

{hashtags}
"""


def get_tags(metadata: dict) -> list:
    """Generate YouTube tags for SEO based on mood type."""
    mood = metadata.get('mood', '')
    rhythm = metadata.get('rhythm_name', '')

    # Nature sound moods
    nature_moods = ['rain_sleep', 'fireplace', 'ocean_waves', 'forest_morning']

    # Lofi/chill moods
    chill_moods = ['lofi_study', 'piano_relax']

    if mood in nature_moods:
        # Nature-specific tags (no binaural/rhythm mentions)
        mood_tags = {
            'rain_sleep': ["rain sounds", "rain for sleep", "rain sounds for sleeping", "rain asmr", "rain noise", "thunderstorm sounds", "rain on window"],
            'fireplace': ["fireplace sounds", "crackling fire", "fire asmr", "cozy fireplace", "fireplace ambience", "fire sounds for sleep"],
            'ocean_waves': ["ocean sounds", "ocean waves", "beach sounds", "sea sounds", "waves for sleep", "ocean asmr", "beach waves"],
            'forest_morning': ["forest sounds", "nature sounds", "bird sounds", "forest ambience", "morning birds", "nature asmr"],
        }
        base_tags = mood_tags.get(mood, ["ambient sounds", "nature sounds"])
        base_tags.extend(["relaxation", "sleep sounds", "white noise", "asmr", "ambient", "stress relief", "meditation sounds"])

    elif mood in chill_moods:
        # Lofi/chill tags
        base_tags = [
            "lofi", "lofi beats", "chill beats", "study music", "lofi hip hop",
            "relaxing music", "background music", "chill music", "beats to study to",
            "lofi chill", "homework music", "work music"
        ]

    else:
        # Music with rhythm/binaural tags
        base_tags = [
            "ambient music", "binaural beats", "focus music", "study music",
            "meditation music", "relaxation", "concentration", "sleep music",
            "healing frequencies", "432 hz", "528 hz",
            "theta waves", "alpha waves", "deep focus", "work music"
        ]
        if rhythm and rhythm != 'Ambient':
            base_tags.append(f"{rhythm} rhythm")
            base_tags.append(f"{rhythm} drums")

    # Add mood-specific tag
    if mood:
        base_tags.append(mood.replace('_', ' '))

    return base_tags[:30]  # YouTube limit


@click.command()
@click.option('--video', '-v', help='Path to video file')
@click.option('--metadata', '-m', help='Path to metadata JSON (auto-detected if not provided)')
@click.option('--privacy', '-p', default='public', type=click.Choice(['public', 'private', 'unlisted']))
@click.option('--auth', is_flag=True, help='Just authenticate (for first-time setup)')
@click.option('--batch', '-b', help='Upload all videos from manifest.json in directory')
@click.option('--update-catalog/--no-update-catalog', default=True, help='Update content catalog with YouTube links')
@click.option('--catalog-path', help='Path to catalog file (default: content_catalog.json)')
def main(video: str, metadata: str, privacy: str, auth: bool, batch: str, update_catalog: bool, catalog_path: str):
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
        
        # Initialize content library if catalog updates enabled
        library = None
        if update_catalog:
            library = ContentLibrary(catalog_path=catalog_path)
            click.echo(f"📚 Content catalog: {library.catalog_path}")
        
        uploaded_count = 0
        for i, v in enumerate(videos, 1):
            result = v.get('result', {})
            video_path = result.get('video_path')
            meta = result.get('metadata', result)  # Use nested metadata if available
            
            if not video_path or not os.path.exists(video_path):
                click.echo(f"  [{i}] ⏭️  Skipping (file not found)")
                continue
            
            click.echo(f"  [{i}/{len(videos)}] Uploading {Path(video_path).name}...")
            
            try:
                upload_result = upload_single(uploader, video_path, meta, privacy)
                
                # Add to content library
                if library and upload_result:
                    library.add_video(
                        youtube_id=upload_result['video_id'],
                        youtube_url=upload_result['url'],
                        title=upload_result['title'],
                        metadata=meta
                    )
                    uploaded_count += 1
            except Exception as e:
                click.echo(f"  ❌ Upload failed: {e}")
                continue
        
        # Export markdown summary if catalog was updated
        if library and uploaded_count > 0:
            try:
                md_path = library.export_markdown()
                click.echo(f"\n📄 Content library updated: {library.catalog_path}")
                click.echo(f"📄 Markdown export: {md_path}")
            except Exception as e:
                click.echo(f"\n⚠️  Warning: Could not export markdown: {e}")
        
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
    
    upload_result = upload_single(uploader, video, meta, privacy)
    
    # Add to content library
    if update_catalog and upload_result:
        try:
            library = ContentLibrary(catalog_path=catalog_path)
            library.add_video(
                youtube_id=upload_result['video_id'],
                youtube_url=upload_result['url'],
                title=upload_result['title'],
                metadata=meta
            )
            md_path = library.export_markdown()
            click.echo(f"\n📚 Added to content library: {library.catalog_path}")
            click.echo(f"📄 Markdown export: {md_path}")
        except Exception as e:
            click.echo(f"\n⚠️  Warning: Could not update catalog: {e}")


def upload_single(uploader: YouTubeUploader, video_path: str, meta: dict, privacy: str) -> dict:
    """Upload a single video and return the result."""
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
    return result


if __name__ == "__main__":
    main()

