"""
Main orchestrator for the Living Ambient Engine.
Coordinates audio generation, visual generation, and rendering.
"""

import yaml
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
import tempfile
import shutil

from audio import AudioGenerator
from visuals import VisualGenerator
from render import Renderer


class Orchestrator:
    """Orchestrate the complete video generation pipeline."""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.moods = self._load_moods()
        self.defaults = self._load_defaults()
        
    def _load_moods(self) -> Dict:
        """Load mood configurations."""
        moods_path = self.config_dir / "moods.yaml"
        with open(moods_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _load_defaults(self) -> Dict:
        """Load default configurations."""
        defaults_path = self.config_dir / "defaults.yaml"
        with open(defaults_path, 'r') as f:
            return yaml.safe_load(f)
    
    def generate(self, mood: str, duration: int, output_dir: Optional[str] = None,
                 rhythm_volume: Optional[float] = None, drone_volume: Optional[float] = None) -> Dict:
        """
        Generate a complete ambient video.

        Args:
            mood: Mood preset name (e.g., 'deep_focus', 'sleep')
            duration: Duration in seconds
            output_dir: Output directory (optional, uses config default if not provided)
            rhythm_volume: Override for tribal drum volume (0.0-1.0)
            drone_volume: Override for drone/ambient layer volume (0.0-1.0)

        Returns:
            Dictionary with paths to generated files and metadata
        """
        # Validate mood
        if mood not in self.moods:
            raise ValueError(f"Unknown mood: {mood}. Available: {list(self.moods.keys())}")
        
        mood_config = self.moods[mood]
        
        # Setup output paths
        if output_dir is None:
            output_dir = self.defaults['output']['directory']
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_base = f"{mood}_{duration}s_{timestamp}"
        
        # Create temp directory for intermediate files
        temp_dir = Path(tempfile.mkdtemp(prefix="ambient_engine_"))
        
        try:
            print(f"🎨 Generating hypnotic visuals for '{mood}'...")
            visual_path = temp_dir / "visual.mp4"
            visual_gen = VisualGenerator(
                mood_config['visual'],
                width=self.defaults['video']['resolution']['width'],
                height=self.defaults['video']['resolution']['height'],
                fps=self.defaults['video']['fps']
            )
            visual_gen.generate(duration, str(visual_path))
            
            print(f"🎵 Generating ambient audio for '{mood}'...")
            audio_path = temp_dir / "audio.wav"
            audio_gen = AudioGenerator(
                mood_config['audio'],
                sample_rate=self.defaults['audio']['sample_rate'],
                channels=self.defaults['audio']['channels'],
                rhythm_volume_override=rhythm_volume,
                drone_volume_override=drone_volume
            )
            audio_gen.generate(duration, str(audio_path))
            
            print(f"🎬 Rendering final video...")
            final_path = output_path / f"{filename_base}.mp4"

            # Generate title from template
            rhythm_name = mood_config.get('audio', {}).get('rhythm', 'Ambient')
            rhythm_name = rhythm_name.replace('_', ' ').title()
            rhythm_origin = mood_config.get('rhythm_origin', '')
            duration_str = self._format_duration(duration)

            title_template = mood_config.get('title_template', '{mood} | {rhythm_name} | {duration_str}')
            video_title = title_template.format(
                mood=mood.replace('_', ' ').title(),
                rhythm_name=rhythm_name,
                duration_str=duration_str
            )

            # Prepare metadata
            metadata = {
                'mood': mood,
                'duration': duration,
                'duration_str': duration_str,
                'description': mood_config.get('description', ''),
                'video_title': video_title,
                'rhythm': mood_config.get('audio', {}).get('rhythm', 'ambient'),
                'rhythm_name': rhythm_name,
                'rhythm_origin': rhythm_origin,
                'generated_at': timestamp,
                'visual_config': mood_config['visual'],
                'audio_config': mood_config['audio']
            }
            
            renderer = Renderer(self.defaults)
            renderer.render(str(visual_path), str(audio_path), str(final_path), metadata)
            
            print(f"✅ Complete! Video saved to: {final_path}")
            
            return {
                'video_path': str(final_path),
                'metadata_path': str(final_path.with_suffix('.json')),
                'thumbnail_path': str(final_path.with_suffix('.png')),
                'metadata': metadata
            }
            
        finally:
            # Cleanup temp directory
            if self.defaults['render'].get('cleanup_temp', True):
                shutil.rmtree(temp_dir, ignore_errors=True)
    
    def _format_duration(self, seconds: int) -> str:
        """Format duration for display in title."""
        if seconds < 60:
            return f"{seconds} Seconds"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes} Min" if minutes == 1 else f"{minutes} Mins"
        else:
            hours = seconds // 3600
            return f"{hours} Hour" if hours == 1 else f"{hours} Hours"

    def list_moods(self) -> Dict[str, str]:
        """List available moods with descriptions."""
        return {
            mood: config.get('description', 'No description')
            for mood, config in self.moods.items()
        }

