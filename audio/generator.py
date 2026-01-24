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
        """Generate a simple, hypnotic melody using a scale."""
        root = config.get('root', 220)  # A3
        scale = config.get('scale', 'pentatonic_minor')
        tempo = config.get('tempo', 60)  # BPM

        intervals = self._get_scale_intervals(scale)

        # Calculate note duration
        beat_samples = int(self.sample_rate * 60 / tempo)
        note_samples = beat_samples * 2  # Half notes for slow, hypnotic feel

        audio = np.zeros((num_samples, self.channels))

        # Generate melody notes
        current_sample = 0
        note_index = 0
        direction = 1

        while current_sample < num_samples:
            # Get frequency for current note
            semitones = intervals[note_index % len(intervals)]
            octave = note_index // len(intervals)
            freq = root * (2 ** (semitones / 12)) * (2 ** octave)

            # Keep in reasonable range
            while freq > root * 4:
                freq /= 2
            while freq < root / 2:
                freq *= 2

            # Generate note with envelope
            note_len = min(note_samples, num_samples - current_sample)
            t = np.arange(note_len) / self.sample_rate

            # Soft synth tone with harmonics
            wave = np.sin(2 * np.pi * freq * t)
            wave += np.sin(2 * np.pi * freq * 2 * t) * 0.3  # Octave
            wave += np.sin(2 * np.pi * freq * 1.5 * t) * 0.15  # Fifth

            # ADSR envelope
            attack = int(note_len * 0.1)
            decay = int(note_len * 0.1)
            release = int(note_len * 0.3)
            sustain_level = 0.7

            envelope = np.ones(note_len)
            envelope[:attack] = np.linspace(0, 1, attack)
            envelope[attack:attack+decay] = np.linspace(1, sustain_level, decay)
            envelope[-release:] = np.linspace(sustain_level, 0, release)

            wave = wave * envelope * amplitude

            # Stereo with slight pan variation
            pan = 0.5 + 0.2 * np.sin(note_index * 0.5)
            left = wave * (1 - pan)
            right = wave * pan

            audio[current_sample:current_sample+note_len, 0] += left
            audio[current_sample:current_sample+note_len, 1] += right

            current_sample += note_samples

            # Move through scale (up and down pattern)
            note_index += direction
            if note_index >= len(intervals) * 2 - 1:
                direction = -1
            elif note_index <= 0:
                direction = 1

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

        audio = np.zeros((num_samples, self.channels))
        current_sample = 0
        note_index = 0

        while current_sample < num_samples:
            # Cycle through chord tones
            semitones = intervals[note_index % len(intervals)]
            octave = (note_index // len(intervals)) % 2  # Alternate octaves
            freq = root * (2 ** (semitones / 12)) * (2 ** octave)

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
        wave = np.zeros(num_samples)

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
        """Generate realistic rain sounds using filtered noise + droplet impacts."""
        audio = np.zeros((num_samples, self.channels))

        # Base: pink noise filtered to sound like rain
        pink = self._generate_pink_noise(num_samples, amplitude * 0.6)[:, 0]

        # Apply bandpass-like filtering for rain characteristics
        # Rain is mostly mid-high frequency (1kHz - 8kHz)
        # Simple approach: high-pass filter the pink noise
        filtered = np.zeros(num_samples)
        alpha = 0.95  # High-pass coefficient
        for i in range(1, num_samples):
            filtered[i] = alpha * (filtered[i-1] + pink[i] - pink[i-1])

        # Add rain intensity variation (waves of heavy/light rain)
        t = np.arange(num_samples) / self.sample_rate
        rain_intensity = 0.7 + 0.3 * np.sin(2 * np.pi * 0.02 * t)  # ~50 sec cycle
        filtered = filtered * rain_intensity

        # Add individual droplet impacts for realism
        drop_rate = config.get('drop_rate', 50)  # drops per second
        num_drops = int(num_samples / self.sample_rate * drop_rate)

        for _ in range(num_drops):
            # Random position
            pos = np.random.randint(0, num_samples - 500)
            # Droplet sound: short burst of filtered noise
            drop_len = np.random.randint(200, 500)
            drop_freq = np.random.uniform(2000, 6000)
            drop_t = np.arange(drop_len) / self.sample_rate
            drop = np.sin(2 * np.pi * drop_freq * drop_t) * np.exp(-drop_t * 40)
            drop *= np.random.uniform(0.3, 1.0) * amplitude * 0.3

            # Add slight stereo variation
            pan = np.random.uniform(0.3, 0.7)
            end_pos = min(pos + drop_len, num_samples)
            actual_len = end_pos - pos
            audio[pos:end_pos, 0] += drop[:actual_len] * (1 - pan)
            audio[pos:end_pos, 1] += drop[:actual_len] * pan

        # Mix in the base rain
        audio[:, 0] += filtered
        audio[:, 1] += filtered

        return audio

    def _generate_fire(self, config: Dict, num_samples: int, amplitude: float) -> np.ndarray:
        """Generate crackling fire sounds."""
        audio = np.zeros((num_samples, self.channels))

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
        roar = np.zeros(num_samples)
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
        """Generate ocean waves sounds."""
        audio = np.zeros((num_samples, self.channels))
        t = np.arange(num_samples) / self.sample_rate

        # Wave cycle period (seconds between waves)
        wave_period = config.get('wave_period', 8)

        # Create wave envelope: slow rise and fall
        wave_phase = (t / wave_period) % 1.0
        # Wave envelope: builds up slowly, crashes, then recedes
        wave_env = np.sin(wave_phase * np.pi) ** 2

        # Base: filtered pink noise for the ocean body
        pink = self._generate_pink_noise(num_samples, 1.0)[:, 0]
        ocean = pink * wave_env * amplitude * 0.5

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
        audio = np.zeros((num_samples, self.channels))
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

