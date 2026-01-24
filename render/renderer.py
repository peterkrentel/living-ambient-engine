"""
FFmpeg-based renderer to combine audio and video into final MP4.
"""

import ffmpeg
import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
from PIL import Image
import cv2


class Renderer:
    """Render final video from audio and visual components."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.video_config = config.get('video', {})
        self.audio_config = config.get('audio', {})
        self.output_config = config.get('output', {})
        
    def render(self, visual_path: str, audio_path: str, output_path: str, 
               metadata: Optional[Dict] = None) -> str:
        """Combine visual and audio into final MP4."""
        
        # Ensure output directory exists
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # FFmpeg rendering
        try:
            video_stream = ffmpeg.input(visual_path)
            audio_stream = ffmpeg.input(audio_path)
            
            # Combine streams
            stream = ffmpeg.output(
                video_stream,
                audio_stream,
                output_path,
                vcodec=self.video_config.get('codec', 'libx264'),
                acodec=self.audio_config.get('codec', 'aac'),
                video_bitrate=self.video_config.get('bitrate', '5000k'),
                audio_bitrate=self.audio_config.get('bitrate', '192k'),
                preset=self.video_config.get('preset', 'medium'),
                crf=self.video_config.get('crf', 23),
                **{'c:a': 'aac', 'strict': 'experimental'}
            )
            
            # Run FFmpeg
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
            
        except ffmpeg.Error as e:
            print(f"FFmpeg error: {e.stderr.decode() if e.stderr else str(e)}")
            raise
        
        # Save metadata if requested
        if metadata and self.output_config.get('save_metadata', True):
            self._save_metadata(output_path, metadata)
        
        # Generate thumbnail if requested
        if self.output_config.get('save_thumbnail', True):
            self._generate_thumbnail(output_path)
        
        return output_path
    
    def _save_metadata(self, video_path: str, metadata: Dict):
        """Save metadata JSON alongside video."""
        metadata_path = Path(video_path).with_suffix('.json')
        
        # Add render timestamp
        metadata['rendered_at'] = datetime.now().isoformat()
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, indent=2, fp=f)
    
    def _generate_thumbnail(self, video_path: str):
        """Generate thumbnail from video."""
        thumbnail_path = Path(video_path).with_suffix('.png')
        thumbnail_time = self.output_config.get('thumbnail_time', 30)
        
        try:
            # Open video
            cap = cv2.VideoCapture(video_path)
            
            # Get FPS and calculate frame number
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_number = int(thumbnail_time * fps)
            
            # Set position
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            
            # Read frame
            ret, frame = cap.read()
            if ret:
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                img.save(thumbnail_path)
            
            cap.release()
            
        except Exception as e:
            print(f"Warning: Could not generate thumbnail: {e}")

