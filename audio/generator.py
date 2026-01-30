"""
Ambient audio generator with tribal rhythms, binaural beats and procedural synthesis.
Creates psychoacoustic soundscapes designed for focus, relaxation, and trance states.
Features authentic tribal rhythm patterns from world traditions.
"""

import numpy as np
import soundfile as sf
from typing import Dict, List, Tuple
import math


# Tribal rhythm patterns (in 16th notes, 1 = hit, 0 = rest)
TRIBAL_PATTERNS = {
    # Bamboula - New Orleans/Caribbean - driving hypnotic groove
    'bamboula': {
        'bpm': 110,
        'low':   [1,0,0,1, 0,0,1,0, 0,1,0,0, 1,0,0,0],  # Bass drum
        'mid':   [0,0,1,0, 0,1,0,0, 1,0,0,1, 0,0,1,0],  # Mid tom
        'high':  [1,0,1,0, 1,0,1,0, 1,0,1,0, 1,0,1,0],  # Shaker/hi-hat
    },
    # Kuku - West African (Guinea) - celebratory, energizing
    'kuku': {
        'bpm': 130,
        'low':   [1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0],  # Dundun
        'mid':   [0,0,1,0, 0,1,0,1, 0,0,1,0, 0,1,0,0],  # Sangban
        'high':  [1,0,1,1, 0,1,1,0, 1,0,1,1, 0,1,0,1],  # Djembe slaps
    },
    # Gnawa - Moroccan trance music - deep spiritual
    'gnawa': {
        'bpm': 70,
        'low':   [1,0,0,0, 0,0,1,0, 0,0,0,0, 1,0,0,0],  # Guembri bass
        'mid':   [0,0,0,1, 0,0,0,0, 0,1,0,0, 0,0,1,0],  # Krakebs
        'high':  [1,1,0,1, 1,0,1,1, 0,1,1,0, 1,1,0,1],  # Krakebs pattern
    },
    # Burundi - East African - intense building waves
    'burundi': {
        'bpm': 120,
        'low':   [1,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0],  # Ingoma bass
        'mid':   [0,0,1,0, 1,0,1,0, 0,0,1,0, 1,0,1,0],  # Ingoma accent
        'high':  [1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1],  # Constant pulse
    },
    # Taiko - Japanese ceremonial - powerful meditative
    'taiko': {
        'bpm': 75,
        'low':   [1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],  # Big taiko
        'mid':   [0,0,0,0, 1,0,0,0, 0,0,1,0, 0,0,0,0],  # Chu-daiko
        'high':  [0,0,1,0, 0,0,1,0, 0,0,1,0, 0,0,1,0],  # Shime-daiko
    },
    # Gamelan - Indonesian - ethereal layered
    'gamelan': {
        'bpm': 85,
        'low':   [1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],  # Gong
        'mid':   [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0],  # Kenong
        'high':  [1,0,1,0, 0,1,0,1, 1,0,1,0, 0,1,0,0],  # Saron
    },
    # Candomble - Brazilian/African - polyrhythmic ceremony
    'candomble': {
        'bpm': 105,
        'low':   [1,0,0,1, 0,0,1,0, 0,1,0,0, 0,0,1,0],  # Rum
        'mid':   [0,1,0,0, 1,0,0,1, 0,0,1,0, 1,0,0,0],  # Rumpi
        'high':  [1,0,1,0, 1,1,0,1, 0,1,0,1, 1,0,1,1],  # Le
    },
    # Heartbeat - Universal - primal sync
    'heartbeat': {
        'bpm': 65,
        'low':   [1,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0],  # Lub-dub
        'mid':   [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],  # Silent
        'high':  [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],  # Silent
    },
}


class AudioGenerator:
    """Generate ambient audio with tribal rhythms, binaural beats and layered synthesis."""

    # Phase system: evolves audio every 3-7 minutes to prevent repetition
    # settle → drift → deepen → resolve (cycles for long content)
    PHASES = ['settle', 'drift', 'deepen', 'resolve']

    # Phase characteristics (relative modifiers)
    PHASE_MODS = {
        'settle': {
            'chord_shift': 0,      # Root key
            'noise_brightness': 0.8,  # Softer noise
            'tempo_factor': 0.95,  # Slightly slower
            'volume_mult': 0.85,   # Quieter start
        },
        'drift': {
            'chord_shift': 5,      # Up a 4th
            'noise_brightness': 1.0,  # Normal
            'tempo_factor': 1.0,   # Normal tempo
            'volume_mult': 0.95,
        },
        'deepen': {
            'chord_shift': 7,      # Up a 5th
            'noise_brightness': 0.7,  # Darker noise
            'tempo_factor': 0.9,   # Slower
            'volume_mult': 1.0,    # Full volume
        },
        'resolve': {
            'chord_shift': 0,      # Back to root
            'noise_brightness': 0.9,  # Gentle
            'tempo_factor': 0.92,  # Calming down
            'volume_mult': 0.9,
        },
    }

    def __init__(self, config: Dict, sample_rate: int = 44100, channels: int = 2,
                 rhythm_volume_override: float = None, drone_volume_override: float = None):
        self.config = config
        self.sample_rate = sample_rate
        self.channels = channels
        # Allow CLI overrides for mixing
        self.rhythm_volume_override = rhythm_volume_override
        self.drone_volume_override = drone_volume_override
        # Phase tracking
        self.current_phase_idx = 0
        self.phase_duration_range = (180, 420)  # 3-7 minutes in seconds

    def _get_phase_boundaries(self, duration: int) -> List[Tuple[int, str, Dict]]:
        """Calculate phase boundaries for the entire duration.

        Returns list of (start_sample, phase_name, phase_mods) tuples.
        """
        boundaries = []
        current_time = 0
        phase_idx = 0

        while current_time < duration:
            phase_name = self.PHASES[phase_idx % len(self.PHASES)]
            phase_mods = self.PHASE_MODS[phase_name].copy()

            # Random phase duration between 3-7 minutes
            min_dur, max_dur = self.phase_duration_range
            phase_len = np.random.randint(min_dur, max_dur + 1)

            # Don't exceed total duration
            if current_time + phase_len > duration:
                phase_len = duration - current_time

            start_sample = int(current_time * self.sample_rate)
            boundaries.append((start_sample, phase_name, phase_mods, phase_len))

            current_time += phase_len
            phase_idx += 1

        return boundaries

    def generate(self, duration: int, output_path: str) -> str:
        """Generate audio file with evolving phases."""
        num_samples = duration * self.sample_rate
        audio = np.zeros((num_samples, self.channels), dtype=np.float32)

        # Calculate phase boundaries for this duration
        phase_boundaries = self._get_phase_boundaries(duration)

        # Log phase plan for debugging
        if len(phase_boundaries) > 1:
            print(f"    📊 Audio phases ({len(phase_boundaries)} total):")
            for start_sample, phase_name, mods, phase_len in phase_boundaries:
                start_min = start_sample / self.sample_rate / 60
                print(f"       {start_min:.1f}min: {phase_name} ({phase_len//60}m{phase_len%60}s)")

        # Generate tribal rhythm layer (with phase-based tempo variation)
        rhythm_type = self.config.get('rhythm', 'bamboula')
        rhythm_volume = self.rhythm_volume_override if self.rhythm_volume_override is not None else self.config.get('rhythm_volume', 0.4)
        if rhythm_type and rhythm_type in TRIBAL_PATTERNS:
            rhythm_audio = self._generate_tribal_rhythm_phased(
                rhythm_type, num_samples, phase_boundaries
            )
            audio += rhythm_audio * rhythm_volume

        # Drone volume multiplier (applies to sine/binaural layers)
        drone_mult = self.drone_volume_override if self.drone_volume_override is not None else 1.0

        # Generate each tonal layer with phase modulation
        layers = self.config.get('layers', [])
        for layer in layers:
            layer_audio = self._generate_layer_phased(
                layer, num_samples, phase_boundaries
            )
            audio += layer_audio * drone_mult

        # Apply phase-based volume envelope for smooth evolution
        volume_envelope = self._create_phase_volume_envelope(
            num_samples, phase_boundaries
        )
        audio = audio * volume_envelope[:, np.newaxis]

        # Normalize to prevent clipping
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = audio / max_val * 0.85  # Leave headroom

        # Apply fade in/out
        audio = self._apply_fade(audio, fade_duration=2.0)

        # Save as WAV
        sf.write(output_path, audio, self.sample_rate)
        return output_path

    def _create_phase_volume_envelope(self, num_samples: int,
                                       phase_boundaries: List) -> np.ndarray:
        """Create smooth volume envelope based on phases."""
        envelope = np.ones(num_samples)

        for i, (start_sample, phase_name, mods, phase_len) in enumerate(phase_boundaries):
            end_sample = start_sample + int(phase_len * self.sample_rate)
            end_sample = min(end_sample, num_samples)

            phase_samples = end_sample - start_sample
            target_volume = mods['volume_mult']

            # Smooth transition (crossfade over 5 seconds)
            crossfade_samples = min(int(5 * self.sample_rate), phase_samples // 4)

            # Ramp up at start of phase
            if crossfade_samples > 0:
                ramp = np.linspace(envelope[start_sample], target_volume, crossfade_samples)
                ramp_end = min(start_sample + crossfade_samples, num_samples)
                envelope[start_sample:ramp_end] = ramp[:ramp_end - start_sample]

            # Sustain at target volume
            sustain_start = start_sample + crossfade_samples
            envelope[sustain_start:end_sample] = target_volume

        return envelope

    def _generate_tribal_rhythm_phased(self, rhythm_type: str, num_samples: int,
                                        phase_boundaries: List) -> np.ndarray:
        """Generate tribal rhythm with phase-based tempo variation."""
        # For now, generate base rhythm and apply phase modulation
        # Future: could vary tempo per phase
        return self._generate_tribal_rhythm(rhythm_type, num_samples)

    def _generate_layer_phased(self, layer_config: Dict, num_samples: int,
                                phase_boundaries: List) -> np.ndarray:
        """Generate a layer with phase-based modifications."""
        layer_type = layer_config.get('type', 'sine')

        # For frequency-based layers, apply chord shifts per phase
        if layer_type in ['sine', 'binaural', 'pad', 'melody', 'arpeggio']:
            return self._generate_layer_with_chord_shifts(
                layer_config, num_samples, phase_boundaries
            )

        # For noise-based layers, apply brightness variation
        elif layer_type in ['pink_noise', 'rain', 'ocean']:
            return self._generate_layer_with_brightness(
                layer_config, num_samples, phase_boundaries
            )

        # Other layers: generate normally
        else:
            return self._generate_layer(layer_config, num_samples)

    def _generate_layer_with_chord_shifts(self, layer_config: Dict,
                                           num_samples: int,
                                           phase_boundaries: List) -> np.ndarray:
        """Generate tonal layer with phase-based chord/key shifts."""
        audio = np.zeros((num_samples, self.channels), dtype=np.float32)

        for i, (start_sample, phase_name, mods, phase_len) in enumerate(phase_boundaries):
            end_sample = start_sample + int(phase_len * self.sample_rate)
            end_sample = min(end_sample, num_samples)
            segment_samples = end_sample - start_sample

            if segment_samples <= 0:
                continue

            # Create modified config with chord shift
            modified_config = layer_config.copy()
            chord_shift = mods.get('chord_shift', 0)

            # Apply frequency shift for harmonic movement
            if 'frequency' in modified_config:
                base_freq = modified_config['frequency']
                # Shift by semitones
                modified_config['frequency'] = base_freq * (2.0 ** (chord_shift / 12.0))

            if 'carrier' in modified_config:  # Binaural
                base_carrier = modified_config['carrier']
                modified_config['carrier'] = base_carrier * (2.0 ** (chord_shift / 12.0))

            if 'root' in modified_config:  # Melody/arpeggio
                base_root = modified_config['root']
                modified_config['root'] = base_root * (2.0 ** (chord_shift / 12.0))

            # Generate segment
            segment = self._generate_layer(modified_config, segment_samples)

            # Crossfade between phases (prevent clicks)
            crossfade = min(int(2 * self.sample_rate), segment_samples // 4)
            if crossfade > 0 and i > 0:
                fade_in = np.linspace(0, 1, crossfade)
                segment[:crossfade] = segment[:crossfade] * fade_in[:, np.newaxis]
            if crossfade > 0 and i < len(phase_boundaries) - 1:
                fade_out = np.linspace(1, 0, crossfade)
                segment[-crossfade:] = segment[-crossfade:] * fade_out[:, np.newaxis]

            audio[start_sample:end_sample] += segment

        return audio

    def _generate_layer_with_brightness(self, layer_config: Dict,
                                         num_samples: int,
                                         phase_boundaries: List) -> np.ndarray:
        """Generate noise-based layer with phase-based brightness variation."""
        # Generate base layer
        audio = self._generate_layer(layer_config, num_samples)

        # Apply brightness modulation via simple lowpass approximation
        # (multiply high frequencies less when brightness < 1)
        for start_sample, phase_name, mods, phase_len in phase_boundaries:
            end_sample = start_sample + int(phase_len * self.sample_rate)
            end_sample = min(end_sample, num_samples)

            brightness = mods.get('noise_brightness', 1.0)

            # Simple brightness: reduce amplitude slightly for darker phases
            # (A full filter would be more complex)
            if brightness < 1.0:
                audio[start_sample:end_sample] *= brightness

        return audio

    def _generate_tribal_rhythm(self, rhythm_type: str, num_samples: int) -> np.ndarray:
        """Generate tribal drum pattern."""
        pattern = TRIBAL_PATTERNS[rhythm_type]
        bpm = pattern['bpm']

        # Calculate timing
        beat_duration = 60.0 / bpm  # seconds per beat
        sixteenth_duration = beat_duration / 4  # 16th note duration
        sixteenth_samples = int(sixteenth_duration * self.sample_rate)

        audio = np.zeros((num_samples, self.channels), dtype=np.float32)

        # Generate drum sounds
        low_drum = self._synth_drum(80, 0.3, 'low')    # Deep bass drum
        mid_drum = self._synth_drum(150, 0.15, 'mid')  # Mid tom
        high_drum = self._synth_drum(300, 0.08, 'high') # High percussion

        # Place hits according to pattern
        pattern_length = len(pattern['low'])
        current_sample = 0

        while current_sample < num_samples:
            for i in range(pattern_length):
                if current_sample >= num_samples:
                    break

                # Add slight humanization (timing variation)
                humanize = int((np.random.rand() - 0.5) * sixteenth_samples * 0.05)
                hit_pos = current_sample + humanize
                hit_pos = max(0, min(hit_pos, num_samples - 1))

                # Add drums based on pattern
                if pattern['low'][i]:
                    self._add_sound(audio, low_drum, hit_pos, 0.7 + np.random.rand() * 0.3)
                if pattern['mid'][i]:
                    self._add_sound(audio, mid_drum, hit_pos, 0.5 + np.random.rand() * 0.3)
                if pattern['high'][i]:
                    self._add_sound(audio, high_drum, hit_pos, 0.3 + np.random.rand() * 0.2)

                current_sample += sixteenth_samples

        return audio

    def _synth_drum(self, freq: float, decay: float, drum_type: str) -> np.ndarray:
        """Synthesize a drum sound."""
        duration = decay * 2
        num_samples = int(duration * self.sample_rate)
        t = np.arange(num_samples) / self.sample_rate

        if drum_type == 'low':
            # Deep bass drum - pitch drop + sine
            pitch_env = np.exp(-t * 30)  # Rapid pitch drop
            freq_sweep = freq * (1 + pitch_env * 2)
            phase = np.cumsum(freq_sweep / self.sample_rate) * 2 * np.pi
            wave = np.sin(phase)
            # Add some noise for attack
            noise = np.random.randn(num_samples) * np.exp(-t * 50) * 0.3
            wave = wave + noise

        elif drum_type == 'mid':
            # Mid tom - pitched membrane
            pitch_env = np.exp(-t * 20)
            freq_sweep = freq * (1 + pitch_env * 1.5)
            phase = np.cumsum(freq_sweep / self.sample_rate) * 2 * np.pi
            wave = np.sin(phase) * 0.7 + np.sin(phase * 2.3) * 0.3

        else:  # high
            # High percussion - mostly noise with pitched element
            noise = np.random.randn(num_samples)
            tone = np.sin(2 * np.pi * freq * t)
            wave = noise * 0.6 + tone * 0.4

        # Apply envelope
        envelope = np.exp(-t / decay)
        wave = wave * envelope

        # Stereo
        return np.column_stack([wave, wave])

    def _add_sound(self, audio: np.ndarray, sound: np.ndarray, position: int, velocity: float):
        """Add a sound to the audio buffer at a specific position."""
        end_pos = min(position + len(sound), len(audio))
        sound_length = end_pos - position
        if sound_length > 0:
            audio[position:end_pos] += sound[:sound_length] * velocity
    
    def _generate_layer(self, layer_config: Dict, num_samples: int) -> np.ndarray:
        """Generate a single audio layer."""
        layer_type = layer_config.get('type', 'sine')
        amplitude = layer_config.get('amplitude', 0.3)

        if layer_type == 'sine':
            return self._generate_sine(layer_config, num_samples, amplitude)
        elif layer_type == 'binaural':
            return self._generate_binaural(layer_config, num_samples, amplitude)
        elif layer_type == 'pink_noise':
            return self._generate_pink_noise(num_samples, amplitude)
        elif layer_type == 'white_noise':
            return self._generate_white_noise(num_samples, amplitude)
        elif layer_type == 'melody':
            return self._generate_melody(layer_config, num_samples, amplitude)
        elif layer_type == 'arpeggio':
            return self._generate_arpeggio(layer_config, num_samples, amplitude)
        elif layer_type == 'pad':
            return self._generate_pad(layer_config, num_samples, amplitude)
        elif layer_type == 'rain':
            return self._generate_rain(layer_config, num_samples, amplitude)
        elif layer_type == 'fire':
            return self._generate_fire(layer_config, num_samples, amplitude)
        elif layer_type == 'ocean':
            return self._generate_ocean(layer_config, num_samples, amplitude)
        elif layer_type == 'forest':
            return self._generate_forest(layer_config, num_samples, amplitude)
        elif layer_type == 'wind':
            return self._generate_wind(layer_config, num_samples, amplitude)
        elif layer_type == 'progression':
            return self._generate_progression(layer_config, num_samples, amplitude)
        elif layer_type == 'polyrhythm':
            return self._generate_polyrhythm(layer_config, num_samples, amplitude)
        elif layer_type == 'call_response':
            return self._generate_call_response(layer_config, num_samples, amplitude)
        else:
            return np.zeros((num_samples, self.channels), dtype=np.float32)
    
    def _generate_sine(self, config: Dict, num_samples: int, amplitude: float) -> np.ndarray:
        """Generate warm pad tone with harmonics (not harsh pure sine)."""
        frequency = config.get('frequency', 432)
        warmth = config.get('warmth', 0.7)  # 0 = pure sine, 1 = rich harmonics
        t = np.arange(num_samples) / self.sample_rate

        # Base sine wave
        wave = np.sin(2 * np.pi * frequency * t)

        # Add harmonics for warmth (like a filtered pad)
        if warmth > 0:
            # Octave below (sub)
            wave += np.sin(2 * np.pi * (frequency / 2) * t) * 0.3 * warmth
            # Fifth above
            wave += np.sin(2 * np.pi * (frequency * 1.5) * t) * 0.15 * warmth
            # Octave above (gentle)
            wave += np.sin(2 * np.pi * (frequency * 2) * t) * 0.08 * warmth

        # Slow amplitude modulation for movement (breathing effect)
        mod_freq = 0.1  # Very slow modulation
        modulation = 0.85 + 0.15 * np.sin(2 * np.pi * mod_freq * t)
        wave = wave * modulation

        # Apply soft envelope to remove harshness
        wave = wave * amplitude

        # Add subtle reverb/space
        wave = self._add_reverb(wave, decay=0.3, mix=0.4)

        # Stereo with slight widening
        left = wave
        right = np.roll(wave, int(self.sample_rate * 0.01))  # 10ms delay for width

        audio = np.column_stack([left, right])
        return audio

    def _generate_binaural(self, config: Dict, num_samples: int, amplitude: float) -> np.ndarray:
        """Generate smooth binaural beat for brainwave entrainment."""
        carrier = config.get('carrier', 200)  # Base frequency
        beat = config.get('beat', 10)         # Beat frequency (difference)

        t = np.arange(num_samples) / self.sample_rate

        # Use lower carrier frequency for less piercing sound
        # Optimal range is 100-400 Hz for binaural effectiveness

        # Add warmth - not pure sine, slight harmonics
        warmth = 0.2

        # Left ear: carrier frequency with subtle harmonics
        left = np.sin(2 * np.pi * carrier * t)
        left += np.sin(2 * np.pi * (carrier / 2) * t) * 0.2 * warmth  # Sub octave

        # Right ear: carrier + beat frequency
        right = np.sin(2 * np.pi * (carrier + beat) * t)
        right += np.sin(2 * np.pi * ((carrier + beat) / 2) * t) * 0.2 * warmth

        # Gentle amplitude envelope - fade the binaural in/out slowly
        # This makes it less fatiguing on the ears
        cycle_length = self.sample_rate * 10  # 10 second cycle
        envelope = 0.7 + 0.3 * np.sin(2 * np.pi * t / 10)

        left = left * amplitude * envelope
        right = right * amplitude * envelope

        audio = np.column_stack([left, right])
        return audio

    def _add_reverb(self, signal: np.ndarray, decay: float = 0.3, mix: float = 0.3) -> np.ndarray:
        """Add simple reverb effect for space and depth."""
        # Simple comb filter reverb
        delay_samples = int(self.sample_rate * 0.03)  # 30ms delay
        reverb = np.zeros_like(signal)

        # Multiple delay taps for richer reverb
        delays = [
            (int(self.sample_rate * 0.023), 0.6),   # 23ms
            (int(self.sample_rate * 0.037), 0.5),   # 37ms
            (int(self.sample_rate * 0.053), 0.4),   # 53ms
            (int(self.sample_rate * 0.079), 0.3),   # 79ms
        ]

        for delay, level in delays:
            if delay < len(signal):
                delayed = np.zeros_like(signal)
                delayed[delay:] = signal[:-delay] * level * decay
                reverb += delayed

        # Mix dry and wet
        return signal * (1 - mix) + reverb * mix
    
    def _generate_pink_noise(self, num_samples: int, amplitude: float) -> np.ndarray:
        """Generate pink noise (1/f noise) using fast Voss-McCartney algorithm."""
        # Voss-McCartney algorithm - vectorized for speed
        rows = 16  # Number of random sources
        cols = num_samples

        # Generate random values for each row
        array = np.random.randn(rows, cols)

        # Each row gets updated at different rates (powers of 2)
        # Row 0: every sample, Row 1: every 2 samples, Row 2: every 4 samples, etc.
        for i in range(rows):
            step = 2 ** i
            if step < cols:
                # Hold values constant between updates
                indices = np.arange(0, cols, step)
                held_values = array[i, indices]
                array[i] = np.repeat(held_values, step)[:cols]

        # Sum all rows
        pink = np.sum(array, axis=0)

        # Normalize
        max_val = np.max(np.abs(pink))
        if max_val > 0:
            pink = pink / max_val * amplitude

        # Stereo with slight variation for width
        right = np.roll(pink, int(self.sample_rate * 0.02))  # 20ms delay
        audio = np.column_stack([pink, right])
        return audio
    
    def _generate_white_noise(self, num_samples: int, amplitude: float) -> np.ndarray:
        """Generate white noise."""
        noise = np.random.randn(num_samples, self.channels) * amplitude
        return noise
    
    def _apply_fade(self, audio: np.ndarray, fade_duration: float = 2.0) -> np.ndarray:
        """Apply fade in and fade out to prevent clicks."""
        fade_samples = int(fade_duration * self.sample_rate)

        # Fade in
        fade_in = np.linspace(0, 1, fade_samples)
        audio[:fade_samples] *= fade_in[:, np.newaxis]

        # Fade out
        fade_out = np.linspace(1, 0, fade_samples)
        audio[-fade_samples:] *= fade_out[:, np.newaxis]

        return audio

    def _get_scale_intervals(self, scale_name: str) -> List[int]:
        """Get semitone intervals for a scale."""
        scales = {
            'pentatonic_major': [0, 2, 4, 7, 9],           # Happy, universal
            'pentatonic_minor': [0, 3, 5, 7, 10],          # Melancholic, soulful
            'phrygian': [0, 1, 4, 5, 7, 8, 10],            # Dark, exotic, Spanish
            'lydian': [0, 2, 4, 6, 7, 9, 11],              # Dreamy, ethereal
            'dorian': [0, 2, 3, 5, 7, 9, 10],              # Jazzy, sophisticated
            'mixolydian': [0, 2, 4, 5, 7, 9, 10],          # Bluesy, relaxed
            'harmonic_minor': [0, 2, 3, 5, 7, 8, 11],      # Dramatic, Middle Eastern
            'whole_tone': [0, 2, 4, 6, 8, 10],             # Dreamy, floating
        }
        return scales.get(scale_name, scales['pentatonic_major'])

    def _generate_melody(self, config: Dict, num_samples: int, amplitude: float) -> np.ndarray:
        """Generate evolving, hypnotic melody with tempo variation and phrase development."""
        root = config.get('root', 220)  # A3
        scale = config.get('scale', 'pentatonic_minor')
        base_tempo = config.get('tempo', 60)  # BPM
        evolve = config.get('evolve', True)  # Enable melodic evolution

        intervals = self._get_scale_intervals(scale)
        audio = np.zeros((num_samples, self.channels), dtype=np.float32)
        duration = num_samples / self.sample_rate

        # Melodic phrases - patterns of scale degrees (more musical than just up/down)
        phrases = [
            [0, 2, 4, 2],           # Simple rise and fall
            [0, 4, 2, 4, 0],        # Arch shape
            [4, 2, 0, 2],           # Descending start
            [0, 1, 2, 4, 2, 1],     # Stepwise with leap
            [0, 4, 3, 4, 2, 0],     # Call and response feel
            [2, 4, 2, 0, 1, 0],     # Complex phrase
        ]

        current_sample = 0
        phrase_index = 0
        note_in_phrase = 0
        octave_offset = 0

        # Tempo variation parameters
        tempo_variation_cycle = 120  # seconds for full tempo cycle
        tempo_variation_amount = 0.15  # +/- 15% tempo variation

        while current_sample < num_samples:
            # Current time for modulation
            current_time = current_sample / self.sample_rate

            # Tempo variation (accelerando/ritardando)
            tempo_mod = 1.0 + tempo_variation_amount * np.sin(2 * np.pi * current_time / tempo_variation_cycle)
            current_tempo = base_tempo * tempo_mod

            # Calculate note duration with tempo variation
            beat_samples = int(self.sample_rate * 60 / current_tempo)

            # Vary note lengths within phrase (rhythmic interest)
            rhythm_patterns = [2, 2, 1, 1, 2, 1, 1, 2]  # In beat units
            rhythm_index = note_in_phrase % len(rhythm_patterns)
            note_samples = beat_samples * rhythm_patterns[rhythm_index]

            # Get current phrase
            current_phrase = phrases[phrase_index % len(phrases)]
            scale_degree = current_phrase[note_in_phrase % len(current_phrase)]

            # Get frequency from scale
            semitones = intervals[scale_degree % len(intervals)]
            freq = root * (2.0 ** (semitones / 12.0)) * (2.0 ** float(octave_offset))

            # Keep in reasonable range
            while freq > root * 4:
                freq /= 2
            while freq < root / 2:
                freq *= 2

            # Generate note
            note_len = min(note_samples, num_samples - current_sample)
            if note_len <= 0:
                break

            t = np.arange(note_len) / self.sample_rate

            # Evolving timbre - harmonics change over time
            timbre_evolution = 0.5 + 0.5 * np.sin(2 * np.pi * current_time / 180)  # 3 min cycle

            wave = np.sin(2 * np.pi * freq * t)
            wave += np.sin(2 * np.pi * freq * 2 * t) * 0.25 * timbre_evolution
            wave += np.sin(2 * np.pi * freq * 1.5 * t) * 0.15 * (1 - timbre_evolution * 0.5)
            wave += np.sin(2 * np.pi * freq * 3 * t) * 0.08 * timbre_evolution

            # Dynamic ADSR based on note length and position
            attack = int(note_len * np.random.uniform(0.08, 0.15))
            decay = int(note_len * 0.1)
            release = int(note_len * np.random.uniform(0.25, 0.4))
            sustain_level = np.random.uniform(0.6, 0.8)

            envelope = np.ones(note_len)
            if attack > 0:
                envelope[:attack] = np.linspace(0, 1, attack)
            if decay > 0 and attack + decay < note_len:
                envelope[attack:attack+decay] = np.linspace(1, sustain_level, decay)
            if release > 0:
                envelope[-release:] = np.linspace(sustain_level, 0, release)

            # Velocity variation (dynamics)
            velocity = 0.7 + 0.3 * np.sin(note_in_phrase * 0.8 + phrase_index * 0.3)
            wave = wave * envelope * amplitude * velocity

            # Stereo movement
            pan = 0.5 + 0.25 * np.sin(current_time * 0.1 + note_in_phrase * 0.3)
            left = wave * (1 - pan)
            right = wave * pan

            audio[current_sample:current_sample+note_len, 0] += left
            audio[current_sample:current_sample+note_len, 1] += right

            current_sample += note_samples
            note_in_phrase += 1

            # Move to next phrase
            if note_in_phrase >= len(current_phrase):
                note_in_phrase = 0
                phrase_index += 1

                # Occasionally shift octave for evolution
                if evolve and np.random.random() < 0.2:
                    octave_offset = np.random.choice([-1, 0, 0, 1])  # Bias toward root octave

        # Add reverb for space
        audio[:, 0] = self._add_reverb(audio[:, 0], decay=0.4, mix=0.5)
        audio[:, 1] = self._add_reverb(audio[:, 1], decay=0.4, mix=0.5)

        return audio

    def _generate_arpeggio(self, config: Dict, num_samples: int, amplitude: float) -> np.ndarray:
        """Generate hypnotic arpeggio pattern."""
        root = config.get('root', 110)  # A2
        chord = config.get('chord', 'minor7')
        tempo = config.get('tempo', 120)  # BPM

        # Chord intervals in semitones
        chords = {
            'major': [0, 4, 7],
            'minor': [0, 3, 7],
            'major7': [0, 4, 7, 11],
            'minor7': [0, 3, 7, 10],
            'sus4': [0, 5, 7],
            'add9': [0, 4, 7, 14],
        }
        intervals = chords.get(chord, chords['minor7'])

        # Note duration (16th notes for flowing arpeggio)
        note_samples = int(self.sample_rate * 60 / tempo / 4)

        audio = np.zeros((num_samples, self.channels), dtype=np.float32)
        current_sample = 0
        note_index = 0

        while current_sample < num_samples:
            # Cycle through chord tones
            semitones = intervals[note_index % len(intervals)]
            octave = (note_index // len(intervals)) % 2  # Alternate octaves
            freq = root * (2.0 ** (semitones / 12.0)) * (2.0 ** float(octave))

            # Generate note
            note_len = min(note_samples, num_samples - current_sample)
            t = np.arange(note_len) / self.sample_rate

            # Soft pluck sound
            wave = np.sin(2 * np.pi * freq * t)
            wave += np.sin(2 * np.pi * freq * 2 * t) * 0.2

            # Quick attack, longer decay
            envelope = np.exp(-t * 8)  # Exponential decay
            wave = wave * envelope * amplitude

            # Stereo spread
            pan = 0.3 + 0.4 * (note_index % len(intervals)) / len(intervals)
            audio[current_sample:current_sample+note_len, 0] += wave * (1 - pan)
            audio[current_sample:current_sample+note_len, 1] += wave * pan

            current_sample += note_samples
            note_index += 1

        # Add delay for rhythmic interest
        delay_samples = int(self.sample_rate * 60 / tempo * 0.75)  # Dotted eighth
        if delay_samples < num_samples:
            delayed = np.zeros_like(audio)
            delayed[delay_samples:] = audio[:-delay_samples] * 0.4
            audio += delayed

        return audio

    def _generate_pad(self, config: Dict, num_samples: int, amplitude: float) -> np.ndarray:
        """Generate warm, evolving pad sound."""
        frequency = config.get('frequency', 110)  # A2

        t = np.arange(num_samples) / self.sample_rate

        # Rich pad with multiple detuned oscillators
        wave = np.zeros(num_samples, dtype=np.float32)

        # Main oscillators (slightly detuned for richness)
        detune = [0.98, 0.99, 1.0, 1.01, 1.02]
        for d in detune:
            wave += np.sin(2 * np.pi * frequency * d * t) * 0.2

        # Sub bass
        wave += np.sin(2 * np.pi * frequency * 0.5 * t) * 0.3

        # Fifth above
        wave += np.sin(2 * np.pi * frequency * 1.5 * t) * 0.1

        # Slow filter sweep (simulated with amplitude modulation of harmonics)
        lfo = 0.5 + 0.5 * np.sin(2 * np.pi * 0.05 * t)  # Very slow LFO
        wave = wave * (0.7 + 0.3 * lfo)

        # Slow amplitude modulation (breathing)
        breath = 0.8 + 0.2 * np.sin(2 * np.pi * 0.08 * t)
        wave = wave * breath * amplitude

        # Stereo widening
        left = wave
        right = np.roll(wave, int(self.sample_rate * 0.015))  # 15ms delay

        audio = np.column_stack([left, right])

        # Heavy reverb for pad
        audio[:, 0] = self._add_reverb(audio[:, 0], decay=0.5, mix=0.6)
        audio[:, 1] = self._add_reverb(audio[:, 1], decay=0.5, mix=0.6)

        return audio

    def _generate_rain(self, config: Dict, num_samples: int, amplitude: float) -> np.ndarray:
        """Generate realistic rain sounds using filtered noise + droplet impacts + thunder.

        Based on top-performing YouTube ambient formula:
        ambient(t) = A(t) * N_pink(t) + sum(thunder_events)

        Uses very slow modulation (0.0005-0.002 Hz) for natural wave patterns.
        """
        audio = np.zeros((num_samples, self.channels), dtype=np.float32)
        t = np.arange(num_samples) / self.sample_rate
        duration = num_samples / self.sample_rate

        # Base: pink noise for rain texture (proven best for rain ambience)
        pink = self._generate_pink_noise(num_samples, amplitude * 0.6)[:, 0]

        # Very slow amplitude modulation - key to hypnotic quality
        # Primary wave: ~33 minute cycle (0.0005 Hz) - barely perceptible
        # Secondary wave: ~5 minute cycle (0.003 Hz) - subtle variation
        # Tertiary wave: ~1 minute cycle (0.015 Hz) - gentle breathing
        mod_freq_1 = config.get('mod_freq_slow', 0.0005)  # ~33 min cycle
        mod_freq_2 = config.get('mod_freq_med', 0.003)    # ~5.5 min cycle
        mod_freq_3 = config.get('mod_freq_fast', 0.015)   # ~67 sec cycle

        rain_intensity = 0.7 + 0.15 * np.sin(2 * np.pi * mod_freq_1 * t)  # Very slow
        rain_intensity *= 0.9 + 0.1 * np.sin(2 * np.pi * mod_freq_2 * t)  # Medium
        rain_intensity *= 0.95 + 0.05 * np.sin(2 * np.pi * mod_freq_3 * t)  # Fast subtle
        filtered = pink * rain_intensity

        # Add individual droplet impacts for realism
        drop_rate = config.get('drop_rate', 50)  # drops per second
        num_drops = int(duration * drop_rate)

        for _ in range(num_drops):
            pos = np.random.randint(0, max(1, num_samples - 500))
            drop_len = np.random.randint(200, 500)
            drop_freq = np.random.uniform(2000, 6000)
            drop_t = np.arange(drop_len) / self.sample_rate
            drop = np.sin(2 * np.pi * drop_freq * drop_t) * np.exp(-drop_t * 40)
            drop *= np.random.uniform(0.3, 1.0) * amplitude * 0.3

            pan = np.random.uniform(0.3, 0.7)
            end_pos = min(pos + drop_len, num_samples)
            actual_len = end_pos - pos
            audio[pos:end_pos, 0] += drop[:actual_len] * (1 - pan)
            audio[pos:end_pos, 1] += drop[:actual_len] * pan

        # Mix in the base rain
        audio[:, 0] += filtered
        audio[:, 1] += filtered

        # Add thunder (brown noise bursts) - configurable
        thunder_rate = config.get('thunder_rate', 0.5)  # thunders per minute
        if thunder_rate > 0 and duration > 30:  # Only add thunder for longer tracks
            num_thunders = max(1, int(duration / 60 * thunder_rate))

            # Generate base brown noise (cumulative sum of white noise)
            brown_base = np.cumsum(np.random.randn(num_samples))
            brown_base = brown_base / np.max(np.abs(brown_base))

            for _ in range(num_thunders):
                # Thunder position (not too close to start/end)
                pos = np.random.randint(int(self.sample_rate * 5), max(int(self.sample_rate * 6), num_samples - int(self.sample_rate * 10)))

                # Thunder duration: 3-8 seconds
                thunder_len = int(np.random.uniform(3, 8) * self.sample_rate)
                thunder_len = min(thunder_len, num_samples - pos)

                # Thunder envelope: slow build, peak, long decay
                thunder_t = np.arange(thunder_len) / self.sample_rate
                attack_time = np.random.uniform(0.5, 1.5)
                decay_time = thunder_len / self.sample_rate - attack_time

                env = np.zeros(thunder_len, dtype=np.float32)
                attack_samples = int(attack_time * self.sample_rate)
                env[:attack_samples] = np.linspace(0, 1, attack_samples)
                env[attack_samples:] = np.exp(-np.arange(thunder_len - attack_samples) / (decay_time * self.sample_rate) * 3)

                # Thunder sound: low-frequency rumble
                thunder = brown_base[pos:pos + thunder_len] * env * amplitude * np.random.uniform(0.3, 0.6)

                # Add some crackle at the peak
                crackle_pos = attack_samples
                crackle_len = min(int(0.3 * self.sample_rate), thunder_len - crackle_pos)
                if crackle_len > 0:
                    crackle = np.random.randn(crackle_len) * np.exp(-np.arange(crackle_len) / self.sample_rate * 20)
                    thunder[crackle_pos:crackle_pos + crackle_len] += crackle * amplitude * 0.2

                # Stereo with slight delay for distance effect
                audio[pos:pos + thunder_len, 0] += thunder
                delay = int(np.random.uniform(0.05, 0.15) * self.sample_rate)  # 50-150ms delay
                delayed_pos = min(pos + delay, num_samples - thunder_len)
                if delayed_pos + thunder_len <= num_samples:
                    audio[delayed_pos:delayed_pos + thunder_len, 1] += thunder * 0.9

        return audio

    def _generate_fire(self, config: Dict, num_samples: int, amplitude: float) -> np.ndarray:
        """Generate crackling fire sounds."""
        audio = np.zeros((num_samples, self.channels), dtype=np.float32)

        # Base: low rumble (the fire's breath)
        t = np.arange(num_samples) / self.sample_rate
        rumble_freq = 80
        rumble = np.sin(2 * np.pi * rumble_freq * t) * amplitude * 0.2

        # Add slow modulation for breathing fire effect
        breath = 0.5 + 0.5 * np.sin(2 * np.pi * 0.1 * t)
        rumble *= breath

        # Low frequency filtered noise for the roar
        white = np.random.randn(num_samples)
        # Simple low-pass filter
        roar = np.zeros(num_samples, dtype=np.float32)
        alpha = 0.05  # Low-pass coefficient (cuts high freqs)
        for i in range(1, num_samples):
            roar[i] = alpha * white[i] + (1 - alpha) * roar[i-1]
        roar *= amplitude * 0.4 * breath

        audio[:, 0] = rumble + roar
        audio[:, 1] = rumble + roar

        # Add crackles and pops
        crackle_rate = config.get('crackle_rate', 8)  # crackles per second
        num_crackles = int(num_samples / self.sample_rate * crackle_rate)

        for _ in range(num_crackles):
            pos = np.random.randint(0, num_samples - 2000)

            # Crackle: burst of noise with fast decay
            crackle_len = np.random.randint(500, 2000)
            crackle_t = np.arange(crackle_len) / self.sample_rate

            # Mix of noise and high-frequency pop
            noise = np.random.randn(crackle_len)
            pop_freq = np.random.uniform(1500, 4000)
            pop = np.sin(2 * np.pi * pop_freq * crackle_t)
            crackle = (noise * 0.7 + pop * 0.3) * np.exp(-crackle_t * 30)
            crackle *= np.random.uniform(0.5, 1.0) * amplitude * 0.5

            # Stereo placement
            pan = np.random.uniform(0.3, 0.7)
            end_pos = min(pos + crackle_len, num_samples)
            actual_len = end_pos - pos
            audio[pos:end_pos, 0] += crackle[:actual_len] * (1 - pan)
            audio[pos:end_pos, 1] += crackle[:actual_len] * pan

        return audio

    def _generate_ocean(self, config: Dict, num_samples: int, amplitude: float) -> np.ndarray:
        """Generate ocean waves sounds.

        Formula: ocean(t) = A(t) * N_pink(t)
        Uses higher modulation depth (0.5-0.7) and very slow frequency (~0.0003 Hz).
        """
        audio = np.zeros((num_samples, self.channels), dtype=np.float32)
        t = np.arange(num_samples) / self.sample_rate

        # Wave cycle period (seconds between waves)
        wave_period = config.get('wave_period', 8)

        # Create wave envelope: slow rise and fall
        wave_phase = (t / wave_period) % 1.0
        # Wave envelope: builds up slowly, crashes, then recedes
        wave_env = np.sin(wave_phase * np.pi) ** 2

        # Very slow overall intensity modulation (tide-like, ~55 min cycle)
        tide_mod = 0.5 + 0.5 * np.sin(2 * np.pi * 0.0003 * t)  # Per Copilot formula

        # Base: filtered pink noise for the ocean body
        pink = self._generate_pink_noise(num_samples, 1.0)[:, 0]
        ocean = pink * wave_env * tide_mod * amplitude * 0.5

        # Add white noise for the foam/crash
        white = np.random.randn(num_samples) * amplitude * 0.3
        # Foam is loudest at wave peak
        foam_env = np.where(wave_phase > 0.4, np.sin((wave_phase - 0.4) / 0.3 * np.pi), 0)
        foam_env = np.clip(foam_env, 0, 1) ** 2
        foam = white * foam_env

        # Low frequency rumble for power
        rumble_freq = 40
        rumble = np.sin(2 * np.pi * rumble_freq * t) * wave_env * amplitude * 0.15

        # Combine
        combined = ocean + foam + rumble

        # Stereo with slight variation
        audio[:, 0] = combined
        audio[:, 1] = np.roll(combined, int(self.sample_rate * 0.05))  # 50ms delay

        return audio

    def _generate_forest(self, config: Dict, num_samples: int, amplitude: float) -> np.ndarray:
        """Generate forest ambience with birds and wind."""
        audio = np.zeros((num_samples, self.channels), dtype=np.float32)
        t = np.arange(num_samples) / self.sample_rate

        # Base: gentle wind (very soft pink noise with slow modulation)
        pink = self._generate_pink_noise(num_samples, amplitude * 0.15)[:, 0]
        wind_mod = 0.5 + 0.5 * np.sin(2 * np.pi * 0.03 * t)  # ~33 sec cycle
        wind = pink * wind_mod

        audio[:, 0] = wind
        audio[:, 1] = wind

        # Add bird chirps
        bird_rate = config.get('bird_rate', 3)  # birds per minute average
        num_birds = int(num_samples / self.sample_rate / 60 * bird_rate * 10)  # ~10 chirps per bird

        for _ in range(num_birds):
            pos = np.random.randint(0, num_samples - 10000)

            # Bird chirp: frequency-modulated sine
            chirp_len = np.random.randint(1000, 4000)
            chirp_t = np.arange(chirp_len) / self.sample_rate

            # Random bird characteristics
            base_freq = np.random.uniform(2000, 5000)
            freq_mod = np.random.uniform(500, 1500)
            mod_rate = np.random.uniform(10, 30)

            # Frequency modulation for realistic chirp
            freq = base_freq + freq_mod * np.sin(2 * np.pi * mod_rate * chirp_t)
            phase = np.cumsum(freq / self.sample_rate) * 2 * np.pi
            chirp = np.sin(phase)

            # Envelope: quick attack, sustain, quick decay
            env = np.ones(chirp_len)
            attack = int(chirp_len * 0.1)
            decay = int(chirp_len * 0.3)
            env[:attack] = np.linspace(0, 1, attack)
            env[-decay:] = np.linspace(1, 0, decay)

            chirp *= env * np.random.uniform(0.3, 0.8) * amplitude * 0.4

            # Stereo placement (birds in different positions)
            pan = np.random.uniform(0.1, 0.9)
            end_pos = min(pos + chirp_len, num_samples)
            actual_len = end_pos - pos
            audio[pos:end_pos, 0] += chirp[:actual_len] * (1 - pan)
            audio[pos:end_pos, 1] += chirp[:actual_len] * pan

        return audio

    def _generate_wind(self, config: Dict, num_samples: int, amplitude: float) -> np.ndarray:
        """Generate wind ambience using white noise with very slow modulation.

        Formula: wind(t) = A(t) * N_white(t)
        Uses modulation frequency 0.0002-0.002 Hz for natural gusting patterns.
        """
        audio = np.zeros((num_samples, self.channels), dtype=np.float32)
        t = np.arange(num_samples) / self.sample_rate

        # Base: white noise (characteristic of wind/air movement)
        white = self._generate_white_noise(num_samples, 1.0)[:, 0]

        # Very slow modulation for natural gusting (per Copilot formula)
        # Primary: ~83 min cycle (0.0002 Hz) - barely perceptible overall intensity
        # Secondary: ~8 min cycle (0.002 Hz) - slow gusts
        # Tertiary: ~2 min cycle (0.008 Hz) - individual gusts
        mod_freq_1 = config.get('mod_freq_slow', 0.0002)
        mod_freq_2 = config.get('mod_freq_med', 0.002)
        mod_freq_3 = config.get('mod_freq_fast', 0.008)

        wind_intensity = 0.6 + 0.2 * np.sin(2 * np.pi * mod_freq_1 * t)
        wind_intensity *= 0.8 + 0.2 * np.sin(2 * np.pi * mod_freq_2 * t)
        wind_intensity *= 0.85 + 0.15 * np.sin(2 * np.pi * mod_freq_3 * t)

        # Apply modulation
        wind = white * wind_intensity * amplitude

        # Low-pass filter effect (wind is mostly low frequency)
        # Simulate by adding more low-frequency content
        low_rumble = np.sin(2 * np.pi * 50 * t) * wind_intensity * amplitude * 0.1
        wind += low_rumble

        # Stereo with slight variation for spaciousness
        audio[:, 0] = wind
        audio[:, 1] = np.roll(wind, int(self.sample_rate * 0.03))  # 30ms delay

        # Optional: add occasional gusts (stronger wind events)
        gust_rate = config.get('gust_rate', 0.5)  # gusts per minute
        duration = num_samples / self.sample_rate
        if gust_rate > 0 and duration > 30:
            num_gusts = max(1, int(duration / 60 * gust_rate))

            for _ in range(num_gusts):
                gust_pos = np.random.randint(int(self.sample_rate * 5),
                                             max(int(self.sample_rate * 6), num_samples - int(self.sample_rate * 10)))
                gust_len = int(np.random.uniform(2, 5) * self.sample_rate)
                gust_len = min(gust_len, num_samples - gust_pos)

                # Gust envelope: gradual build, peak, gradual fade
                gust_t = np.arange(gust_len) / self.sample_rate
                gust_env = np.sin(np.pi * gust_t / (gust_len / self.sample_rate)) ** 2

                # Gust sound: extra white noise
                gust_sound = np.random.randn(gust_len) * gust_env * amplitude * 0.3

                audio[gust_pos:gust_pos + gust_len, 0] += gust_sound
                audio[gust_pos:gust_pos + gust_len, 1] += gust_sound * 0.9

        return audio

    def _generate_progression(self, config: Dict, num_samples: int, amplitude: float) -> np.ndarray:
        """Generate harmonic chord progression that evolves over time."""
        root = config.get('root', 110)  # A2
        progression_type = config.get('progression', 'ambient')
        chord_duration = config.get('chord_duration', 16)  # Beats per chord
        tempo = config.get('tempo', 60)

        # Chord progressions (intervals in semitones from root)
        progressions = {
            'ambient': [
                [0, 7, 12, 16],      # Root maj add9
                [5, 9, 12, 17],      # IV maj7
                [7, 11, 14, 19],     # V add9
                [0, 4, 7, 12],       # I maj
            ],
            'dreamy': [
                [0, 4, 7, 11],       # I maj7
                [9, 12, 16, 21],     # vi maj7
                [5, 9, 12, 16],      # IV maj7
                [7, 11, 14, 17],     # V maj7
            ],
            'dark': [
                [0, 3, 7, 10],       # i min7
                [5, 8, 12, 15],      # iv min7
                [3, 7, 10, 14],      # bIII maj7
                [7, 10, 14, 17],     # v min7
            ],
            'ethereal': [
                [0, 7, 12, 19],      # Open fifth + octaves
                [5, 12, 17, 24],     # IV open
                [7, 14, 19, 26],     # V open
                [0, 7, 14, 21],      # I open high
            ],
        }

        chords = progressions.get(progression_type, progressions['ambient'])

        beat_samples = int(self.sample_rate * 60 / tempo)
        chord_samples = beat_samples * chord_duration

        audio = np.zeros((num_samples, self.channels), dtype=np.float32)
        current_sample = 0
        chord_index = 0

        while current_sample < num_samples:
            chord = chords[chord_index % len(chords)]

            chunk_len = min(chord_samples, num_samples - current_sample)
            if chunk_len <= 0:
                break

            t = np.arange(chunk_len) / self.sample_rate
            chunk = np.zeros(chunk_len, dtype=np.float32)

            for semitones in chord:
                freq = root * (2 ** (semitones / 12))

                # Detuned oscillators for richness
                for detune in [-0.02, -0.01, 0, 0.01, 0.02]:
                    chunk += np.sin(2 * np.pi * freq * (1 + detune * 0.01) * t) * 0.15

            # Slow amplitude envelope for pad-like feel
            env = np.ones(chunk_len)
            fade_len = min(int(chord_samples * 0.1), chunk_len // 2)
            if fade_len > 0:
                env[:fade_len] = np.linspace(0.5, 1, fade_len)
                env[-fade_len:] = np.linspace(1, 0.5, fade_len)

            # LFO for movement
            lfo = 0.8 + 0.2 * np.sin(2 * np.pi * 0.1 * t)

            chunk = chunk * env * lfo * amplitude

            # Stereo spread
            audio[current_sample:current_sample + chunk_len, 0] += chunk
            audio[current_sample:current_sample + chunk_len, 1] += np.roll(chunk, int(self.sample_rate * 0.02))

            current_sample += chord_samples
            chord_index += 1

        # Add heavy reverb
        audio[:, 0] = self._add_reverb(audio[:, 0], decay=0.6, mix=0.7)
        audio[:, 1] = self._add_reverb(audio[:, 1], decay=0.6, mix=0.7)

        return audio

    def _generate_polyrhythm(self, config: Dict, num_samples: int, amplitude: float) -> np.ndarray:
        """Generate polyrhythmic patterns with different time signatures layered."""
        root = config.get('root', 110)
        tempo = config.get('tempo', 80)
        patterns = config.get('patterns', [3, 4])  # e.g., 3 against 4

        audio = np.zeros((num_samples, self.channels), dtype=np.float32)
        beat_samples = int(self.sample_rate * 60 / tempo)

        # Cycle length = LCM of patterns * beat_samples
        cycle_beats = np.lcm.reduce(patterns)
        cycle_samples = cycle_beats * beat_samples

        for layer_idx, pattern in enumerate(patterns):
            # Each pattern divides the cycle differently
            layer_beat_samples = cycle_samples // pattern

            # Different pitch for each layer
            layer_root = root * (2 ** (layer_idx * 7 / 12))  # Stack fifths

            current_sample = 0
            beat_in_pattern = 0

            while current_sample < num_samples:
                # Generate note
                note_len = min(layer_beat_samples, num_samples - current_sample)
                if note_len <= 0:
                    break

                t = np.arange(note_len) / self.sample_rate

                # Accent first beat of each pattern cycle
                accent = 1.2 if beat_in_pattern == 0 else 0.8

                # Soft mallet-like tone
                freq = layer_root
                wave = np.sin(2 * np.pi * freq * t)
                wave += np.sin(2 * np.pi * freq * 2 * t) * 0.3

                # Quick attack, medium decay
                env = np.exp(-t * 4) * accent
                wave = wave * env * amplitude * 0.5

                # Pan each layer differently
                pan = 0.3 + 0.4 * (layer_idx / max(1, len(patterns) - 1))

                audio[current_sample:current_sample + note_len, 0] += wave * (1 - pan)
                audio[current_sample:current_sample + note_len, 1] += wave * pan

                current_sample += layer_beat_samples
                beat_in_pattern = (beat_in_pattern + 1) % pattern

        return audio

    def _generate_call_response(self, config: Dict, num_samples: int, amplitude: float) -> np.ndarray:
        """Generate call-and-response melodic patterns between two voices."""
        root = config.get('root', 220)
        scale = config.get('scale', 'pentatonic_minor')
        tempo = config.get('tempo', 70)

        intervals = self._get_scale_intervals(scale)
        audio = np.zeros((num_samples, self.channels), dtype=np.float32)

        beat_samples = int(self.sample_rate * 60 / tempo)
        phrase_beats = 4  # 4 beats per phrase
        phrase_samples = beat_samples * phrase_beats

        # Call phrases (lower voice, left-panned)
        call_phrases = [
            [(0, 2), (2, 1), (4, 1)],           # Simple ascending
            [(4, 2), (2, 1), (0, 1)],           # Simple descending
            [(0, 1), (2, 1), (4, 1), (2, 1)],   # Up and back
            [(0, 2), (4, 2)],                   # Leap
        ]

        # Response phrases (higher voice, right-panned)
        response_phrases = [
            [(4, 1), (5, 1), (4, 1), (2, 1)],   # Ornamental response
            [(2, 1), (0, 1), (-1, 2)],          # Descending answer
            [(4, 2), (5, 1), (4, 1)],           # Echo with variation
            [(7, 1), (5, 1), (4, 1), (2, 1)],   # Higher answer
        ]

        current_sample = 0
        phrase_index = 0
        is_call = True  # Alternate between call and response

        while current_sample < num_samples:
            phrases = call_phrases if is_call else response_phrases
            phrase = phrases[phrase_index % len(phrases)]

            # Voice characteristics
            voice_root = root if is_call else root * 2  # Response an octave higher
            pan = 0.25 if is_call else 0.75  # Left for call, right for response

            phrase_pos = 0
            for scale_deg, duration in phrase:
                if current_sample + phrase_pos >= num_samples:
                    break

                note_samples = beat_samples * duration
                note_len = min(note_samples, num_samples - current_sample - phrase_pos)
                if note_len <= 0:
                    break

                # Get frequency
                actual_deg = scale_deg % len(intervals)
                octave = scale_deg // len(intervals)
                semitones = intervals[actual_deg]
                freq = voice_root * (2.0 ** (semitones / 12.0)) * (2.0 ** float(octave))

                t = np.arange(note_len) / self.sample_rate

                # Different timbres for call vs response
                if is_call:
                    # Warmer, fuller sound for call
                    wave = np.sin(2 * np.pi * freq * t)
                    wave += np.sin(2 * np.pi * freq * 0.5 * t) * 0.3  # Sub
                    wave += np.sin(2 * np.pi * freq * 2 * t) * 0.2
                else:
                    # Brighter, lighter sound for response
                    wave = np.sin(2 * np.pi * freq * t)
                    wave += np.sin(2 * np.pi * freq * 2 * t) * 0.35
                    wave += np.sin(2 * np.pi * freq * 3 * t) * 0.15

                # ADSR envelope
                attack = int(note_len * 0.1)
                release = int(note_len * 0.3)
                envelope = np.ones(note_len)
                if attack > 0:
                    envelope[:attack] = np.linspace(0, 1, attack)
                if release > 0:
                    envelope[-release:] = np.linspace(1, 0, release)

                wave = wave * envelope * amplitude * 0.7

                pos = current_sample + phrase_pos
                end_pos = pos + note_len
                audio[pos:end_pos, 0] += wave * (1 - pan)
                audio[pos:end_pos, 1] += wave * pan

                phrase_pos += note_samples

            current_sample += phrase_samples

            # Alternate call/response
            if not is_call:
                phrase_index += 1  # Move to next phrase pair after response
            is_call = not is_call

        # Add reverb
        audio[:, 0] = self._add_reverb(audio[:, 0], decay=0.5, mix=0.5)
        audio[:, 1] = self._add_reverb(audio[:, 1], decay=0.5, mix=0.5)

        return audio
