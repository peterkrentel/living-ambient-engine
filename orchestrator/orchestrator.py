"""
Main orchestrator for the Living Ambient Engine.
Coordinates audio generation, visual generation, and rendering.
"""

import yaml
import random
import numpy as np
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
        """Load mood configurations from ``config/moods.yaml`` (single source of truth)."""
        moods_path = self.config_dir / "moods.yaml"
        with open(moods_path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    
    def _load_defaults(self) -> Dict:
        """Load default configurations."""
        defaults_path = self.config_dir / "defaults.yaml"
        with open(defaults_path, 'r') as f:
            return yaml.safe_load(f)

    def _apply_variation(self, config: Dict, variation_config: Dict = None) -> Dict:
        """
        Apply random variation to config values based on variation ranges.

        For each key in config, if there's a corresponding key_variation in variation_config,
        apply random variation within that range.

        Example:
            config = {'speed': 0.5, 'complexity': 0.8}
            variation_config = {'speed_variation': 0.2, 'complexity_variation': 0.1}
            Result: speed could be 0.3-0.7, complexity could be 0.7-0.9
        """
        import copy
        result = copy.deepcopy(config)

        if variation_config is None:
            variation_config = config

        # Keys that should never be negative
        non_negative_keys = {'frequency', 'amplitude', 'speed', 'complexity', 'drop_rate',
                            'crackle_rate', 'wave_period', 'tempo', 'carrier', 'beat',
                            'base_frequency', 'binaural_beat', 'pulse_frequency', 'bird_rate'}

        def apply_to_dict(d, var_d):
            for key, value in list(d.items()):
                if isinstance(value, dict):
                    apply_to_dict(value, var_d.get(key, {}) if isinstance(var_d.get(key), dict) else {})
                elif isinstance(value, (int, float)) and not isinstance(value, bool):
                    var_key = f"{key}_variation"
                    if var_key in var_d:
                        var_range = var_d[var_key]
                        if isinstance(var_range, (int, float)):
                            # Apply +/- variation
                            new_val = value + random.uniform(-var_range, var_range)
                            # Ensure non-negative for certain keys
                            if key in non_negative_keys:
                                new_val = max(0.001, new_val)  # Small positive minimum
                            d[key] = new_val
                            # Keep same type
                            if isinstance(value, int):
                                d[key] = int(round(d[key]))
                elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], (int, float)):
                    # Handle color lists like [r, g, b]
                    var_key = f"{key}_variation"
                    if var_key in var_d:
                        var_range = var_d[var_key]
                        if isinstance(var_range, list) and len(var_range) == len(value):
                            d[key] = [
                                int(max(0, min(255, v + random.uniform(-vr, vr))))
                                for v, vr in zip(value, var_range)
                            ]
                        elif isinstance(var_range, (int, float)):
                            d[key] = [
                                int(max(0, min(255, v + random.uniform(-var_range, var_range))))
                                for v in value
                            ]

        apply_to_dict(result, variation_config)
        return result
    
    def generate(self, mood: str, duration: int, output_dir: Optional[str] = None,
                 rhythm_volume: Optional[float] = None, drone_volume: Optional[float] = None,
                 seed: Optional[int] = None) -> Dict:
        """
        Generate a complete ambient video.

        Args:
            mood: Mood preset name (e.g., 'deep_focus', 'sleep')
            duration: Duration in seconds
            output_dir: Output directory (optional, uses config default if not provided)
            rhythm_volume: Override for tribal drum volume (0.0-1.0)
            drone_volume: Override for drone/ambient layer volume (0.0-1.0)
            seed: Random seed for reproducible generation (auto-generated if not provided)

        Returns:
            Dictionary with paths to generated files and metadata
        """
        # Validate mood
        if mood not in self.moods:
            raise ValueError(f"Unknown mood: {mood}. Available: {list(self.moods.keys())}")

        # Setup seed for reproducibility
        if seed is None:
            seed = random.randint(0, 2**31 - 1)

        # Set seeds for all random sources
        random.seed(seed)
        np.random.seed(seed)

        print(f"🎲 Using seed: {seed} (save this to reproduce this exact video)")

        mood_config = self.moods[mood]

        # Apply random variation to visual and audio configs
        visual_config = self._apply_variation(mood_config['visual'])
        audio_config = self._apply_variation(mood_config['audio'])

        print(f"🎛️  Applied random variations (deterministic with seed)")

        # Setup output paths
        if output_dir is None:
            output_dir = self.defaults['output']['directory']
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate filename (include seed for reproducibility)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_base = f"{mood}_{duration}s_seed{seed}_{timestamp}"
        
        # Create temp directory for intermediate files
        temp_dir = Path(tempfile.mkdtemp(prefix="ambient_engine_"))

        # Extract journey parameters (for synchronized audio-visual dynamics)
        journey = mood_config.get('journey', 'steady')
        journey_intensity = mood_config.get('journey_intensity', 'moderate')

        try:
            print(f"🎨 Generating hypnotic visuals for '{mood}' (journey: {journey})...")
            visual_path = temp_dir / "visual.mp4"
            visual_gen = VisualGenerator(
                visual_config,  # Use varied config
                width=self.defaults['video']['resolution']['width'],
                height=self.defaults['video']['resolution']['height'],
                fps=self.defaults['video']['fps'],
                journey=journey,
                journey_intensity=journey_intensity
            )
            visual_gen.generate(duration, str(visual_path))

            print(f"🎵 Generating ambient audio for '{mood}' (journey: {journey})...")
            audio_path = temp_dir / "audio.wav"
            audio_gen = AudioGenerator(
                audio_config,  # Use varied config
                sample_rate=self.defaults['audio']['sample_rate'],
                channels=self.defaults['audio']['channels'],
                rhythm_volume_override=rhythm_volume,
                drone_volume_override=drone_volume,
                journey=journey,
                journey_intensity=journey_intensity
            )
            audio_gen.generate(duration, str(audio_path))
            
            print(f"🎬 Rendering final video...")
            final_path = output_path / f"{filename_base}.mp4"

            # Generate title from template
            rhythm_name = mood_config.get('audio', {}).get('rhythm', None)
            if rhythm_name is None:
                rhythm_name = 'Ambient'
            else:
                rhythm_name = rhythm_name.replace('_', ' ').title()
            rhythm_origin = mood_config.get('rhythm_origin', '')
            duration_str = self._format_duration(duration)

            title_template = mood_config.get('title_template', '{mood} | {rhythm_name} | {duration_str}')
            video_title = title_template.format(
                mood=mood.replace('_', ' ').title(),
                rhythm_name=rhythm_name,
                duration_str=duration_str
            )

            # Prepare metadata (include varied configs for exact reproduction)
            metadata = {
                'mood': mood,
                'duration': duration,
                'duration_str': duration_str,
                'seed': seed,  # For reproducibility
                'description': mood_config.get('description', ''),
                'description_template': mood_config.get('description_template', ''),  # SEO description
                'tags': mood_config.get('tags', []),  # SEO tags
                'video_title': video_title,
                'rhythm': audio_config.get('rhythm', 'ambient'),
                'rhythm_name': rhythm_name,
                'rhythm_origin': rhythm_origin,
                'generated_at': timestamp,
                'visual_config': visual_config,  # The actual varied config used
                'audio_config': audio_config,    # The actual varied config used
                'base_visual_config': mood_config['visual'],  # Original for reference
                'base_audio_config': mood_config['audio']     # Original for reference
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

    def _strip_melody_layers(self, audio_config: Dict) -> Dict:
        """Remove melody/musical layers from audio config for pure ambience version.

        Keeps: rain, fire, ocean, forest, wind, pink_noise, white_noise, binaural, pad (low volume)
        Removes: melody, arpeggio, progression, polyrhythm, call_response, sine (high freq)
        """
        import copy
        config = copy.deepcopy(audio_config)

        # Layer types to keep for pure ambience
        ambience_layers = {'rain', 'fire', 'ocean', 'forest', 'wind', 'pink_noise', 'white_noise', 'binaural'}

        if 'layers' in config:
            filtered_layers = []
            for layer in config['layers']:
                layer_type = layer.get('type', '')

                # Keep ambience layers
                if layer_type in ambience_layers:
                    filtered_layers.append(layer)
                # Keep pad but reduce volume for subtle warmth
                elif layer_type == 'pad':
                    layer_copy = copy.deepcopy(layer)
                    layer_copy['amplitude'] = layer_copy.get('amplitude', 0.1) * 0.5
                    filtered_layers.append(layer_copy)
                # Skip melody, arpeggio, progression, etc.

            config['layers'] = filtered_layers

        # Remove rhythm for pure ambience (unless it's heartbeat which is ambient)
        rhythm = config.get('rhythm')
        if rhythm and rhythm != 'heartbeat':
            config['rhythm'] = None
            config['rhythm_volume'] = 0

        return config

    def generate_dual(self, mood: str, duration: int, output_dir: Optional[str] = None,
                      seed: Optional[int] = None) -> Dict:
        """
        Generate BOTH ambience-only and melody versions from the same mood.

        Shares the same visuals between both versions for efficiency.

        Args:
            mood: Mood preset name
            duration: Duration in seconds
            output_dir: Output directory
            seed: Random seed for reproducibility

        Returns:
            Dictionary with paths to both generated videos and metadata
        """
        # Validate mood
        if mood not in self.moods:
            raise ValueError(f"Unknown mood: {mood}. Available: {list(self.moods.keys())}")

        # Setup seed for reproducibility
        if seed is None:
            seed = random.randint(0, 2**31 - 1)

        # Set seeds for all random sources
        random.seed(seed)
        np.random.seed(seed)

        print(f"🎲 Using seed: {seed} (save this to reproduce these exact videos)")
        print(f"🎬 Generating DUAL output: Ambience + Melody versions")

        mood_config = self.moods[mood]

        # Apply random variation to visual and audio configs
        visual_config = self._apply_variation(mood_config['visual'])
        audio_config_full = self._apply_variation(mood_config['audio'])

        # Create ambience-only version of audio config
        audio_config_ambience = self._strip_melody_layers(audio_config_full)

        print(f"🎛️  Applied random variations (deterministic with seed)")

        # Setup output paths
        if output_dir is None:
            output_dir = self.defaults['output']['directory']

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Generate filename base
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_base = f"{mood}_{duration}s_seed{seed}_{timestamp}"

        # Create temp directory for intermediate files
        temp_dir = Path(tempfile.mkdtemp(prefix="ambient_engine_dual_"))

        try:
            # Generate visuals ONCE (shared between both versions)
            print(f"🎨 Generating hypnotic visuals for '{mood}' (shared)...")
            visual_path = temp_dir / "visual.mp4"
            visual_gen = VisualGenerator(
                visual_config,
                width=self.defaults['video']['resolution']['width'],
                height=self.defaults['video']['resolution']['height'],
                fps=self.defaults['video']['fps']
            )
            visual_gen.generate(duration, str(visual_path))

            results = {'ambience': None, 'melody': None}

            # Generate AMBIENCE version
            print(f"\n🌧️  Generating AMBIENCE audio (no melody)...")
            audio_path_ambience = temp_dir / "audio_ambience.wav"
            audio_gen_ambience = AudioGenerator(
                audio_config_ambience,
                sample_rate=self.defaults['audio']['sample_rate'],
                channels=self.defaults['audio']['channels']
            )
            audio_gen_ambience.generate(duration, str(audio_path_ambience))

            print(f"🎬 Rendering AMBIENCE video...")
            final_path_ambience = output_path / f"{filename_base}_AMBIENCE.mp4"

            duration_str = self._format_duration(duration)
            metadata_ambience = self._create_metadata(
                mood, duration, duration_str, seed, timestamp,
                mood_config, visual_config, audio_config_ambience,
                suffix="Pure Ambience"
            )

            renderer = Renderer(self.defaults)
            renderer.render(str(visual_path), str(audio_path_ambience), str(final_path_ambience), metadata_ambience)

            results['ambience'] = {
                'video_path': str(final_path_ambience),
                'metadata_path': str(final_path_ambience.with_suffix('.json')),
                'thumbnail_path': str(final_path_ambience.with_suffix('.png')),
                'metadata': metadata_ambience
            }
            print(f"✅ Ambience version saved: {final_path_ambience}")

            # Generate MELODY version
            print(f"\n🎵 Generating MELODY audio (full musical)...")
            audio_path_melody = temp_dir / "audio_melody.wav"
            audio_gen_melody = AudioGenerator(
                audio_config_full,
                sample_rate=self.defaults['audio']['sample_rate'],
                channels=self.defaults['audio']['channels']
            )
            audio_gen_melody.generate(duration, str(audio_path_melody))

            print(f"🎬 Rendering MELODY video...")
            final_path_melody = output_path / f"{filename_base}_MELODY.mp4"

            metadata_melody = self._create_metadata(
                mood, duration, duration_str, seed, timestamp,
                mood_config, visual_config, audio_config_full,
                suffix="With Music"
            )

            renderer.render(str(visual_path), str(audio_path_melody), str(final_path_melody), metadata_melody)

            results['melody'] = {
                'video_path': str(final_path_melody),
                'metadata_path': str(final_path_melody.with_suffix('.json')),
                'thumbnail_path': str(final_path_melody.with_suffix('.png')),
                'metadata': metadata_melody
            }
            print(f"✅ Melody version saved: {final_path_melody}")

            print(f"\n🎉 DUAL generation complete!")
            print(f"   📁 Ambience: {final_path_ambience}")
            print(f"   📁 Melody:   {final_path_melody}")

            return results

        finally:
            # Cleanup temp directory
            if self.defaults['render'].get('cleanup_temp', True):
                shutil.rmtree(temp_dir, ignore_errors=True)

    def _create_metadata(self, mood: str, duration: int, duration_str: str, seed: int,
                         timestamp: str, mood_config: Dict, visual_config: Dict,
                         audio_config: Dict, suffix: str = "") -> Dict:
        """Create metadata dictionary for a video."""
        rhythm_name = audio_config.get('rhythm', None)
        if rhythm_name is None:
            rhythm_name = 'Ambient'
        else:
            rhythm_name = rhythm_name.replace('_', ' ').title()
        rhythm_origin = mood_config.get('rhythm_origin', '')

        title_template = mood_config.get('title_template', '{mood} | {rhythm_name} | {duration_str}')
        video_title = title_template.format(
            mood=mood.replace('_', ' ').title(),
            rhythm_name=rhythm_name,
            duration_str=duration_str
        )

        if suffix:
            video_title = f"{video_title} [{suffix}]"

        return {
            'mood': mood,
            'duration': duration,
            'duration_str': duration_str,
            'seed': seed,
            'description': mood_config.get('description', ''),
            'description_template': mood_config.get('description_template', ''),  # SEO description
            'tags': mood_config.get('tags', []),  # SEO tags
            'video_title': video_title,
            'rhythm': audio_config.get('rhythm', 'ambient'),
            'rhythm_name': rhythm_name,
            'rhythm_origin': rhythm_origin,
            'generated_at': timestamp,
            'version': suffix.lower().replace(' ', '_') if suffix else 'standard',
            'visual_config': visual_config,
            'audio_config': audio_config,
            'base_visual_config': mood_config['visual'],
            'base_audio_config': mood_config['audio']
        }

    def list_moods(self) -> Dict[str, str]:
        """List available moods with descriptions."""
        return {
            mood: config.get('description', 'No description')
            for mood, config in self.moods.items()
        }

