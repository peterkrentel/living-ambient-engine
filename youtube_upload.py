#!/usr/bin/env python3
"""
YouTube Upload CLI - Generative Ambient Art Engine
Upload generated videos to YouTube with metadata.
"""

import click
import json
import sys
import os
from datetime import datetime
from pathlib import Path

from youtube.uploader import YouTubeUploader, GOOGLE_API_AVAILABLE, QuotaExceededError
from library import ContentLibrary

from agent.log_generation import record_generation_upload


def _duration_label_to_seconds(label) -> int:
    """Parse batch manifest duration labels (e.g. 5min, 1h) to seconds."""
    if label is None:
        return 300
    if isinstance(label, (int, float)):
        return max(1, int(label))
    s = str(label).lower().strip()
    try:
        if s.endswith("min"):
            return int(float(s.replace("min", "").strip()) * 60)
        if s.endswith("h"):
            return int(float(s.replace("h", "").strip()) * 3600)
        if s.endswith("s"):
            return int(float(s.replace("s", "").strip()))
    except ValueError:
        pass
    return 300


def _workflow_name() -> str:
    return os.environ.get("GITHUB_WORKFLOW") or "youtube-upload-cli"


def generate_description(metadata: dict) -> str:
    """Generate YouTube description with 3-line format: Intent, Guarantee, Use case.

    If metadata contains 'description_template', uses that (with variable substitution).
    Otherwise falls back to hardcoded mood-specific descriptions.
    """
    # Check for custom description_template from moods.yaml (SEO-optimized)
    description_template = metadata.get('description_template', '')
    if description_template:
        # Format template with available metadata variables
        try:
            return description_template.format(
                mood=metadata.get('mood', 'ambient'),
                duration_str=metadata.get('duration_str', ''),
                rhythm_name=metadata.get('rhythm_name', ''),
                rhythm_origin=metadata.get('rhythm_origin', ''),
                video_title=metadata.get('video_title', ''),
            )
        except KeyError:
            # If template has unknown variables, return as-is
            return description_template

    # Fallback to hardcoded descriptions for backward compatibility
    mood = metadata.get('mood', 'ambient')
    rhythm = metadata.get('rhythm_name', '')
    origin = metadata.get('rhythm_origin', '')
    duration = metadata.get('duration_str', '')
    title = metadata.get('video_title', 'Ambient Music')

    # Nature/ambient moods (no rhythm, pure ambience)
    nature_moods = ['rain_sleep', 'ocean_waves', 'fireplace', 'forest_morning']

    if mood in nature_moods:
        # Nature sounds - 3-line format
        intent_lines = {
            'rain_sleep': "🌧️ Created to help you fall asleep naturally with gentle, ever-changing rain.",
            'ocean_waves': "🌊 Created to carry your mind away on endless, evolving ocean tides.",
            'fireplace': "🔥 Created to wrap you in the warm comfort of a crackling fire.",
            'forest_morning': "🌲 Created to transport you to a peaceful forest clearing at dawn."
        }
        use_case_lines = {
            'rain_sleep': "Best for: falling asleep, deep rest, blocking out the world.",
            'ocean_waves': "Best for: meditation, sleep, letting go of stress.",
            'fireplace': "Best for: cozy evenings, reading, unwinding after a long day.",
            'forest_morning': "Best for: morning meditation, calm focus, nature immersion."
        }

        intent = intent_lines.get(mood, "Created to help you relax and unwind.")
        guarantee = "✨ This soundscape evolves continuously and never loops."
        use_case = use_case_lines.get(mood, "Best for: relaxation, sleep, meditation.")

        hashtags = f"#{mood.replace('_', '')} #NatureSounds #Sleep #Relaxation #AmbientSounds"

        return f"""{intent}
{guarantee}
{use_case}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏱️ Duration: {duration}

🔔 Subscribe for weekly long-form ambient
👍 Like if this helps you rest

{hashtags}
"""

    else:
        # Music/beats - 3-line format
        intent_lines = {
            'deep_focus': "🎯 Created to quiet an overactive mind and unlock deep concentration.",
            'sleep': "😴 Created to guide you gently into restful, restorative sleep.",
            'chill': "✨ Created to help you decompress and find your calm.",
            'study': "📚 Created to keep you focused without pulling your attention.",
            'energize': "⚡ Created to build energy and momentum when you need a boost.",
            'trance': "🌀 Created to take you on an inward journey of hypnotic depth.",
            'ceremony': "🕯️ Created to hold space for ritual, intention, and presence.",
            'warrior': "💪 Created to fuel your inner fire and strengthen your resolve.",
            'lofi_study': "🎧 Created to keep you in the zone with chill, drifting beats.",
            'piano_relax': "🎹 Created to melt away tension with soft, evolving piano."
        }
        use_case_lines = {
            'deep_focus': "Best for: deep work, coding, writing, any task requiring flow.",
            'sleep': "Best for: insomnia, restless nights, transitioning to sleep.",
            'chill': "Best for: unwinding, gentle background, stress relief.",
            'study': "Best for: studying, reading, learning, quiet focus.",
            'energize': "Best for: workouts, morning energy, breaking through resistance.",
            'trance': "Best for: meditation, altered states, inner exploration.",
            'ceremony': "Best for: rituals, intention setting, sacred space.",
            'warrior': "Best for: training, motivation, building intensity.",
            'lofi_study': "Best for: homework, casual study, creative sessions.",
            'piano_relax': "Best for: stress relief, gentle background, winding down."
        }

        intent = intent_lines.get(mood, "Created to support focus and relaxation.")
        guarantee = "✨ This soundscape evolves through phases and never repeats."
        use_case = use_case_lines.get(mood, "Best for: focus, meditation, relaxation.")

        rhythm_info = f"\n🥁 Rhythm: {rhythm}" if rhythm and rhythm != 'Ambient' else ""
        origin_info = f"\n🌍 {origin}" if origin else ""

        hashtags = f"#AmbientMusic #BinauralBeats #Focus #Meditation #{mood.replace('_', '')}"

        return f"""{intent}
{guarantee}
{use_case}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏱️ Duration: {duration}{rhythm_info}{origin_info}

🧠 Uses binaural beats & Solfeggio frequencies for brainwave entrainment.

🔔 Subscribe for weekly long-form ambient
👍 Like if this helps you focus

{hashtags}
"""


def get_tags(metadata: dict) -> list:
    """Generate YouTube tags for SEO based on mood type.

    If metadata contains 'tags' array from moods.yaml, uses those.
    Otherwise falls back to hardcoded mood-specific tags.
    """
    # Check for custom tags from moods.yaml (SEO-optimized)
    custom_tags = metadata.get('tags', [])
    if custom_tags:
        return custom_tags[:30]  # YouTube limit: 30 tags

    # Fallback to hardcoded tags for backward compatibility
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

        # Count already uploaded (idempotency check)
        already_uploaded = sum(1 for v in videos if v.get('video_id'))
        pending = len(videos) - already_uploaded

        click.echo(f"📦 Found {len(videos)} videos in manifest")
        if already_uploaded > 0:
            click.echo(f"   ✅ {already_uploaded} already uploaded, {pending} pending")

        # Initialize content library if catalog updates enabled
        library = None
        if update_catalog:
            library = ContentLibrary(catalog_path=catalog_path)
            click.echo(f"📚 Content catalog: {library.catalog_path}")

        def save_manifest():
            """Save manifest to disk (for crash recovery)."""
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)

        uploaded_count = 0
        skipped_count = 0
        for i, v in enumerate(videos, 1):
            # IDEMPOTENCY: Skip already uploaded videos
            if v.get('video_id'):
                click.echo(f"  [{i}] ⏭️  Already uploaded: {v.get('video_id')}")
                skipped_count += 1
                continue

            # Support both old format (result.video_path) and new slim format (video_path)
            video_path = v.get('video_path') or v.get('result', {}).get('video_path')

            # Build metadata from slim or old format
            if 'title' in v:
                # New slim format - use fields directly
                meta = {
                    'video_title': v.get('title'),
                    'mood': v.get('mood'),
                    'duration': v.get('duration'),
                    'description': v.get('description', ''),
                    'tags': v.get('tags', []),
                }
            else:
                # Old format - use nested result/metadata
                result = v.get('result', {})
                meta = result.get('metadata', result)

            if not video_path or not os.path.exists(video_path):
                click.echo(f"  [{i}] ⏭️  Skipping (file not found: {video_path})")
                continue

            click.echo(f"  [{i}/{len(videos)}] Uploading {Path(video_path).name}...")

            try:
                upload_result = upload_single(uploader, video_path, meta, privacy)

                # Update manifest with video_id (idempotency)
                v['video_id'] = upload_result['video_id']
                v['upload_status'] = 'uploaded'
                v['uploaded_at'] = datetime.now().isoformat()
                v['youtube_url'] = upload_result['url']

                # Save manifest after each upload (crash recovery)
                save_manifest()

                # Add to content library
                if library and upload_result:
                    library.add_video(
                        youtube_id=upload_result['video_id'],
                        youtube_url=upload_result['url'],
                        title=upload_result['title'],
                        metadata=meta
                    )
                    uploaded_count += 1

                if upload_result:
                    try:
                        record_generation_upload(
                            video_id=upload_result['video_id'],
                            workflow=_workflow_name(),
                            generation_id=v.get('generation_id'),
                            mood=meta.get('mood') or v.get('mood'),
                            duration_seconds=_duration_label_to_seconds(
                                meta.get('duration') or v.get('duration')
                            ),
                            seed=v.get('seed'),
                            variant=v.get('variant'),
                            params={
                                k: v.get(k)
                                for k in ('seed', 'variant')
                                if v.get(k) is not None
                            },
                            metadata={
                                'title': upload_result.get('title'),
                                **{k: meta[k] for k in ('video_title', 'description', 'tags') if k in meta},
                            },
                            generated_at=v.get('created_at'),
                        )
                    except Exception as e:
                        click.echo(f"  ⚠️  Could not write generations.json: {e}", err=True)

            except QuotaExceededError as e:
                click.echo(f"\n⚠️  {e}", err=True)
                click.echo("   Saving progress and exiting. Re-run after quota resets.", err=True)
                save_manifest()  # Save progress so we can resume
                sys.exit(2)  # Special exit code for quota exceeded

            except Exception as e:
                click.echo(f"  ❌ Upload failed: {e}")
                v['upload_status'] = 'failed'
                v['upload_error'] = str(e)
                save_manifest()  # Save error state
                continue

        # Final manifest save
        save_manifest()

        # Calculate failed count
        failed_count = len(videos) - uploaded_count - skipped_count - already_uploaded

        # Summary
        click.echo(f"\n{'='*60}")
        click.echo(f"✨ BATCH UPLOAD COMPLETE")
        click.echo(f"   Uploaded: {uploaded_count}")
        click.echo(f"   Skipped (already uploaded): {skipped_count}")
        click.echo(f"   Failed: {failed_count}")

        # Export markdown summary if catalog was updated
        if library and uploaded_count > 0:
            try:
                md_path = library.export_markdown()
                click.echo(f"\n📄 Content library updated: {library.catalog_path}")
                click.echo(f"📄 Markdown export: {md_path}")
            except Exception as e:
                click.echo(f"\n⚠️  Warning: Could not export markdown: {e}")

        # Exit with error code if any uploads failed
        if failed_count > 0:
            sys.exit(1)

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

    if upload_result:
        try:
            slim_meta = {
                k: meta[k]
                for k in meta
                if k
                not in (
                    'description',
                    'description_template',
                )
            }
            record_generation_upload(
                video_id=upload_result['video_id'],
                workflow=_workflow_name(),
                generation_id=None,
                mood=meta.get('mood'),
                duration_seconds=_duration_label_to_seconds(meta.get('duration')),
                params={k: slim_meta[k] for k in slim_meta if k not in ('video_title', 'mood', 'tags')},
                metadata={
                    'title': upload_result.get('title'),
                    **{k: meta[k] for k in ('video_title', 'description', 'tags') if k in meta},
                },
            )
        except Exception as e:
            click.echo(f"⚠️  Could not write generations.json: {e}", err=True)

    # Save upload result to file (for workflow integration)
    if upload_result:
        result_path = video.replace('.mp4', '_upload_result.json')
        # Also save to directory's youtube_upload.json for backward compat
        dir_result_path = os.path.join(os.path.dirname(video), 'youtube_upload.json')
        with open(result_path, 'w') as f:
            json.dump(upload_result, f, indent=2)
        with open(dir_result_path, 'w') as f:
            json.dump(upload_result, f, indent=2)
        click.echo(f"📁 Upload result saved: {result_path}")

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

