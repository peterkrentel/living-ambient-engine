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

    def __init__(self, config: Dict, sample_rate: int = 44100, channels: int = 2,
                 rhythm_volume_override: float = None, drone_volume_override: float = None):
        self.config = config
        self.sample_rate = sample_rate
        self.channels = channels
        # Allow CLI overrides for mixing
        self.rhythm_volume_override = rhythm_volume_override
        self.drone_volume_override = drone_volume_override

    def generate(self, duration: int, output_path: str) -> str:
        """Generate audio file."""
        num_samples = duration * self.sample_rate
        audio = np.zeros((num_samples, self.channels))

        # Generate tribal rhythm layer
        rhythm_type = self.config.get('rhythm', 'bamboula')
        rhythm_volume = self.rhythm_volume_override if self.rhythm_volume_override is not None else self.config.get('rhythm_volume', 0.4)
        if rhythm_type and rhythm_type in TRIBAL_PATTERNS:
            rhythm_audio = self._generate_tribal_rhythm(rhythm_type, num_samples)
            audio += rhythm_audio * rhythm_volume

        # Drone volume multiplier (applies to sine/binaural layers)
        drone_mult = self.drone_volume_override if self.drone_volume_override is not None else 1.0

        # Generate each tonal layer and mix
        layers = self.config.get('layers', [])
        for layer in layers:
            layer_audio = self._generate_layer(layer, num_samples)
            audio += layer_audio * drone_mult

        # Normalize to prevent clipping
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = audio / max_val * 0.85  # Leave headroom

        # Apply fade in/out
        audio = self._apply_fade(audio, fade_duration=2.0)

        # Save as WAV
        sf.write(output_path, audio, self.sample_rate)
        return output_path

    def _generate_tribal_rhythm(self, rhythm_type: str, num_samples: int) -> np.ndarray:
        """Generate tribal drum pattern."""
        pattern = TRIBAL_PATTERNS[rhythm_type]
        bpm = pattern['bpm']

        # Calculate timing
        beat_duration = 60.0 / bpm  # seconds per beat
        sixteenth_duration = beat_duration / 4  # 16th note duration
        sixteenth_samples = int(sixteenth_duration * self.sample_rate)

        audio = np.zeros((num_samples, self.channels))

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
        else:
            return np.zeros((num_samples, self.channels))
    
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
        """Generate pink noise (1/f noise) - more natural than white noise."""
        # Generate white noise
        white = np.random.randn(num_samples)
        
        # Apply pink noise filter (simple approximation)
        # Use multiple poles for better approximation
        b0, b1, b2, b3, b4, b5, b6 = 0, 0, 0, 0, 0, 0, 0
        pink = np.zeros(num_samples)
        
        for i in range(num_samples):
            white_val = white[i]
            b0 = 0.99886 * b0 + white_val * 0.0555179
            b1 = 0.99332 * b1 + white_val * 0.0750759
            b2 = 0.96900 * b2 + white_val * 0.1538520
            b3 = 0.86650 * b3 + white_val * 0.3104856
            b4 = 0.55000 * b4 + white_val * 0.5329522
            b5 = -0.7616 * b5 - white_val * 0.0168980
            pink[i] = b0 + b1 + b2 + b3 + b4 + b5 + b6 + white_val * 0.5362
            b6 = white_val * 0.115926
        
        # Normalize
        pink = pink / np.max(np.abs(pink)) * amplitude
        
        # Stereo
        audio = np.column_stack([pink, pink])
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

