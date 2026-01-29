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
            with open(self.catalog_path, 'r') as f:
                return json.load(f)
        else:
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
        
        with open(self.catalog_path, 'w') as f:
            json.dump(self.catalog, f, indent=2, default=str)
    
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
        """Generate a unique catalog ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        count = len(self.catalog["videos"]) + 1
        return f"video_{count:04d}_{timestamp}"
    
    def _is_duplicate(self, entry: Dict) -> bool:
        """Check if video already exists in catalog."""
        youtube_id = entry["youtube_id"]
        
        # Check by YouTube ID
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
        results = self.catalog["videos"]
        
        if mood:
            results = [v for v in results if v["mood"] == mood]
        
        if rhythm:
            results = [v for v in results if v["rhythm"] == rhythm]
        
        if min_duration is not None:
            results = [v for v in results if v["duration"] >= min_duration]
        
        if max_duration is not None:
            results = [v for v in results if v["duration"] <= max_duration]
        
        if version:
            results = [v for v in results if v["version"] == version]
        
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
            mood = video["mood"]
            if mood not in videos_by_mood:
                videos_by_mood[mood] = []
            videos_by_mood[mood].append(video)
        
        for mood in sorted(videos_by_mood.keys()):
            md_lines.extend([
                f"### {mood.replace('_', ' ').title()}",
                ""
            ])
            
            for video in videos_by_mood[mood]:
                version_tag = f" `{video['version']}`" if video['version'] != 'standard' else ""
                md_lines.extend([
                    f"#### {video['title']}{version_tag}",
                    "",
                    f"🔗 **Watch:** [{video['youtube_url']}]({video['youtube_url']})",
                    "",
                    f"- **Duration:** {video['duration_str']}",
                    f"- **Rhythm:** {video['rhythm_name']}",
                    f"- **Uploaded:** {video['uploaded_at'][:10]}",
                    f"- **Seed:** `{video['seed']}`",
                    f"- **Catalog ID:** `{video['catalog_id']}`",
                    ""
                ])
        
        # Write to file
        with open(output_path, 'w') as f:
            f.write('\n'.join(md_lines))
        
        return output_path
