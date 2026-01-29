#!/usr/bin/env python3
"""
Example: Using the Content Library API

Demonstrates how to programmatically interact with the content catalog.
"""

from library import ContentLibrary
import json


def example_basic_usage():
    """Basic content library operations."""
    print("=" * 60)
    print("BASIC USAGE")
    print("=" * 60)
    
    # Initialize library (uses content_catalog.json by default)
    library = ContentLibrary()
    
    # Get statistics
    stats = library.get_stats()
    print(f"\n📊 Total Videos: {stats['total_videos']}")
    print(f"📊 Total Duration: {stats['total_duration_hours']} hours")
    
    if stats['total_videos'] > 0:
        print(f"📊 Average Duration: {stats['average_duration_minutes']} minutes")
        print("\n📊 Videos by Mood:")
        for mood, count in sorted(stats['moods'].items()):
            print(f"   • {mood.replace('_', ' ').title()}: {count}")


def example_search():
    """Search and filter videos."""
    print("\n" + "=" * 60)
    print("SEARCH EXAMPLES")
    print("=" * 60)
    
    library = ContentLibrary()
    
    # Search by mood
    focus_videos = library.search(mood='deep_focus')
    print(f"\n🔍 Deep Focus videos: {len(focus_videos)}")
    
    # Search by duration (1+ hours)
    long_videos = library.search(min_duration=3600)
    print(f"🔍 Videos 1+ hours: {len(long_videos)}")
    
    # Search by version
    ambience_only = library.search(version='pure_ambience')
    print(f"🔍 Pure ambience versions: {len(ambience_only)}")
    
    # Combined search
    long_focus = library.search(mood='deep_focus', min_duration=3600)
    print(f"🔍 Deep focus 1+ hours: {len(long_focus)}")


def example_display_videos():
    """Display video information."""
    print("\n" + "=" * 60)
    print("DISPLAY VIDEOS")
    print("=" * 60)
    
    library = ContentLibrary()
    videos = library.get_all_videos()
    
    if not videos:
        print("\n📭 No videos in catalog yet.")
        print("Run the Content Factory workflow to generate and upload videos.")
        return
    
    print(f"\n📚 Showing {min(5, len(videos))} most recent videos:\n")
    
    for video in videos[-5:]:  # Show last 5
        version_tag = f" [{video['version']}]" if video['version'] != 'standard' else ""
        print(f"📹 {video['title']}{version_tag}")
        print(f"   🔗 {video['youtube_url']}")
        print(f"   ⏱️  {video['duration_str']} | 🎨 {video['mood']} | 🥁 {video['rhythm_name']}")
        print(f"   🎲 Seed: {video['seed']} | 📅 {video['uploaded_at'][:10]}")
        print()


def example_add_video():
    """Example of adding a video to the catalog (normally done by youtube_upload.py)."""
    print("\n" + "=" * 60)
    print("ADD VIDEO EXAMPLE")
    print("=" * 60)
    
    print("\n⚠️  Note: Videos are normally added automatically by youtube_upload.py")
    print("This is just an example of the API.\n")
    
    # This would typically be called by youtube_upload.py after successful upload
    # library = ContentLibrary()
    # entry = library.add_video(
    #     youtube_id='ABC123XYZ',
    #     youtube_url='https://youtube.com/watch?v=ABC123XYZ',
    #     title='Deep Focus | Taiko | 3 Hours',
    #     metadata={
    #         'mood': 'deep_focus',
    #         'duration': 10800,
    #         'duration_str': '3 Hours',
    #         'seed': 987654321,
    #         'rhythm': 'taiko',
    #         'rhythm_name': 'Taiko',
    #         'version': 'standard'
    #     }
    # )
    # print(f"✅ Added video: {entry['catalog_id']}")


def example_export():
    """Export catalog as markdown."""
    print("\n" + "=" * 60)
    print("EXPORT EXAMPLE")
    print("=" * 60)
    
    library = ContentLibrary()
    
    if library.get_stats()['total_videos'] == 0:
        print("\n📭 No videos to export yet.")
        return
    
    # Export to markdown
    md_path = library.export_markdown('example_export.md')
    print(f"\n✅ Exported catalog to: {md_path}")
    print("📄 This file contains a human-readable list of all videos.")


def example_by_mood():
    """Get videos grouped by mood."""
    print("\n" + "=" * 60)
    print("VIDEOS BY MOOD")
    print("=" * 60)
    
    library = ContentLibrary()
    
    # Get unique moods
    moods = library.get_stats().get('moods', {})
    
    if not moods:
        print("\n📭 No videos yet.")
        return
    
    print("\n📚 Videos grouped by mood:\n")
    
    for mood in sorted(moods.keys()):
        videos = library.get_by_mood(mood)
        print(f"{mood.replace('_', ' ').title()}: {len(videos)} videos")
        for video in videos[:2]:  # Show first 2
            print(f"  • {video['title']} ({video['duration_str']})")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("CONTENT LIBRARY EXAMPLES")
    print("=" * 60)
    
    example_basic_usage()
    example_search()
    example_display_videos()
    example_by_mood()
    example_add_video()
    example_export()
    
    print("\n" + "=" * 60)
    print("EXAMPLES COMPLETE")
    print("=" * 60)
    print("\nFor more information:")
    print("  • Documentation: docs/CONTENT_LIBRARY.md")
    print("  • CLI help: python library_cli.py --help")
    print("  • API: from library import ContentLibrary")
    print()


if __name__ == '__main__':
    main()
