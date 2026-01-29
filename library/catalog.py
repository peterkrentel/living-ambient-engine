"""
Content Library Catalog
Maintains a persistent catalog of all generated videos with YouTube links and metadata.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class ContentLibrary:
    """Manage the content catalog with YouTube links and metadata."""
    
    DEFAULT_CATALOG_PATH = "content_catalog.json"
    
    def __init__(self, catalog_path: str = None):
        """
        Initialize the content library.
        
        Args:
            catalog_path: Path to catalog JSON file (default: content_catalog.json in project root)
        """
        if catalog_path is None:
            catalog_path = self.DEFAULT_CATALOG_PATH
        self.catalog_path = Path(catalog_path)
        self.catalog = self._load_catalog()
    
    def _load_catalog(self) -> Dict:
        """Load existing catalog or create new one."""
        if self.catalog_path.exists():
            try:
                with open(self.catalog_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                # Backup corrupted file and create new catalog
                backup_path = self.catalog_path.with_suffix('.json.backup')
                try:
                    self.catalog_path.rename(backup_path)
                    print(f"⚠️  Warning: Corrupted catalog backed up to {backup_path}")
                except Exception:
                    pass
                # Return new catalog
        return {
            "catalog_version": "1.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "total_videos": 0,
            "videos": []
        }
    
    def _save_catalog(self):
        """Save catalog to disk."""
        self.catalog["last_updated"] = datetime.now().isoformat()
        self.catalog["total_videos"] = len(self.catalog["videos"])
        
        try:
            with open(self.catalog_path, 'w') as f:
                json.dump(self.catalog, f, indent=2, default=str)
        except (IOError, OSError) as e:
            print(f"❌ Error saving catalog: {e}")
            raise
    
    def add_video(
        self,
        youtube_id: str,
        youtube_url: str,
        title: str,
        metadata: Dict,
        upload_date: str = None
    ) -> Dict:
        """
        Add a video to the catalog.
        
        Args:
            youtube_id: YouTube video ID
            youtube_url: Full YouTube URL
            title: Video title
            metadata: Video metadata (mood, duration, seed, etc.)
            upload_date: Upload date (ISO format, defaults to now)
            
        Returns:
            The catalog entry created
        """
        if upload_date is None:
            upload_date = datetime.now().isoformat()
        
        # Create catalog entry
        entry = {
            "catalog_id": self._generate_catalog_id(),
            "youtube_id": youtube_id,
            "youtube_url": youtube_url,
            "title": title,
            "mood": metadata.get("mood", "unknown"),
            "duration": metadata.get("duration", 0),
            "duration_str": metadata.get("duration_str", ""),
            "seed": metadata.get("seed", None),
            "version": metadata.get("version", "standard"),
            "rhythm": metadata.get("rhythm", "ambient"),
            "rhythm_name": metadata.get("rhythm_name", ""),
            "uploaded_at": upload_date,
            "generated_at": metadata.get("generated_at", upload_date),
            "metadata": metadata
        }
        
        # Check for duplicates (same seed and mood)
        if not self._is_duplicate(entry):
            self.catalog["videos"].append(entry)
            self._save_catalog()
        
        return entry
    
    def _generate_catalog_id(self) -> str:
        """Generate a unique catalog ID with random component."""
        import uuid
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        count = len(self.catalog["videos"]) + 1
        # Add short random suffix to prevent collisions in parallel operations
        random_suffix = str(uuid.uuid4())[:8]
        return f"video_{count:04d}_{timestamp}_{random_suffix}"
    
    def _is_duplicate(self, entry: Dict) -> bool:
        """Check if video already exists in catalog by YouTube ID."""
        youtube_id = entry["youtube_id"]
        
        # Check by YouTube ID (primary uniqueness constraint)
        for video in self.catalog["videos"]:
            if video["youtube_id"] == youtube_id:
                return True
        
        return False
    
    def get_all_videos(self) -> List[Dict]:
        """Get all videos in the catalog."""
        return self.catalog["videos"]
    
    def get_by_mood(self, mood: str) -> List[Dict]:
        """Get all videos for a specific mood."""
        return [v for v in self.catalog["videos"] if v["mood"] == mood]
    
    def get_by_duration(self, min_seconds: int = None, max_seconds: int = None) -> List[Dict]:
        """Get videos filtered by duration."""
        videos = self.catalog["videos"]
        
        if min_seconds is not None:
            videos = [v for v in videos if v["duration"] >= min_seconds]
        
        if max_seconds is not None:
            videos = [v for v in videos if v["duration"] <= max_seconds]
        
        return videos
    
    def search(
        self,
        mood: str = None,
        rhythm: str = None,
        min_duration: int = None,
        max_duration: int = None,
        version: str = None
    ) -> List[Dict]:
        """
        Search catalog with filters.
        
        Args:
            mood: Filter by mood preset
            rhythm: Filter by rhythm type
            min_duration: Minimum duration in seconds
            max_duration: Maximum duration in seconds
            version: Filter by version (e.g., 'pure_ambience', 'with_music')
            
        Returns:
            List of matching videos
        """
        # Single-pass filtering for efficiency
        results = []
        for video in self.catalog["videos"]:
            # Apply all filters in one pass
            if mood and video.get("mood") != mood:
                continue
            if rhythm and video.get("rhythm") != rhythm:
                continue
            if min_duration is not None and video.get("duration", 0) < min_duration:
                continue
            if max_duration is not None and video.get("duration", 0) > max_duration:
                continue
            if version and video.get("version") != version:
                continue
            
            results.append(video)
        
        return results
    
    def get_stats(self) -> Dict:
        """Get catalog statistics."""
        if not self.catalog["videos"]:
            return {
                "total_videos": 0,
                "moods": {},
                "total_duration_hours": 0
            }
        
        moods = {}
        total_duration = 0
        
        for video in self.catalog["videos"]:
            mood = video["mood"]
            moods[mood] = moods.get(mood, 0) + 1
            total_duration += video["duration"]
        
        return {
            "total_videos": len(self.catalog["videos"]),
            "moods": moods,
            "total_duration_hours": round(total_duration / 3600, 2),
            "average_duration_minutes": round(total_duration / len(self.catalog["videos"]) / 60, 2)
        }
    
    def export_markdown(self, output_path: str = "CONTENT_LIBRARY.md"):
        """Export catalog as a markdown file for easy viewing."""
        stats = self.get_stats()
        
        md_lines = [
            "# Content Library",
            "",
            f"*Last updated: {self.catalog['last_updated']}*",
            "",
            "## Statistics",
            "",
            f"- **Total Videos:** {stats['total_videos']}",
            f"- **Total Duration:** {stats['total_duration_hours']} hours",
        ]
        
        if stats['total_videos'] > 0:
            md_lines.append(f"- **Average Duration:** {stats['average_duration_minutes']} minutes")
        
        md_lines.extend([
            "",
            "### Videos by Mood",
            ""
        ])
        
        for mood, count in sorted(stats['moods'].items()):
            md_lines.append(f"- **{mood.replace('_', ' ').title()}:** {count} videos")
        
        md_lines.extend([
            "",
            "## Videos",
            ""
        ])
        
        # Group videos by mood
        videos_by_mood = {}
        for video in self.catalog["videos"]:
            mood = video.get("mood", "unknown")
            if mood not in videos_by_mood:
                videos_by_mood[mood] = []
            videos_by_mood[mood].append(video)
        
        for mood in sorted(videos_by_mood.keys()):
            md_lines.extend([
                f"### {mood.replace('_', ' ').title()}",
                ""
            ])
            
            for video in videos_by_mood[mood]:
                version = video.get('version', 'standard')
                version_tag = f" `{version}`" if version != 'standard' else ""
                
                # Safe field access with defaults
                title = video.get('title', 'Unknown')
                youtube_url = video.get('youtube_url', '#')
                duration_str = video.get('duration_str', 'Unknown')
                rhythm_name = video.get('rhythm_name', 'Unknown')
                uploaded_at = video.get('uploaded_at', '')[:10] if video.get('uploaded_at') else 'Unknown'
                seed = video.get('seed', 'Unknown')
                catalog_id = video.get('catalog_id', 'Unknown')
                
                md_lines.extend([
                    f"#### {title}{version_tag}",
                    "",
                    f"🔗 **Watch:** [{youtube_url}]({youtube_url})",
                    "",
                    f"- **Duration:** {duration_str}",
                    f"- **Rhythm:** {rhythm_name}",
                    f"- **Uploaded:** {uploaded_at}",
                    f"- **Seed:** `{seed}`",
                    f"- **Catalog ID:** `{catalog_id}`",
                    ""
                ])
        
        # Write to file with error handling
        try:
            with open(output_path, 'w') as f:
                f.write('\n'.join(md_lines))
        except (IOError, OSError) as e:
            print(f"❌ Error exporting markdown: {e}")
            raise
        
        return output_path
