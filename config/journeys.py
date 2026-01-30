"""
Journey presets for synchronized audio-visual dynamics.

Each journey defines how tempo, speed, and complexity evolve over time,
creating cohesive experiences where audio and visuals move together.
"""

import math
from typing import Dict, Callable, Tuple


def _linear(start: float, end: float) -> Callable[[float], float]:
    """Linear interpolation from start to end."""
    return lambda t: start + (end - start) * t


def _sine_wave(center: float, amplitude: float, cycles: float = 1.0) -> Callable[[float], float]:
    """Oscillating sine wave around center value."""
    return lambda t: center + amplitude * math.sin(t * cycles * 2 * math.pi)


def _arc(start: float, peak: float, end: float) -> Callable[[float], float]:
    """Arc shape: start -> peak at midpoint -> end."""
    def curve(t: float) -> float:
        if t < 0.5:
            # Rising to peak
            return start + (peak - start) * (t * 2)
        else:
            # Falling from peak
            return peak + (end - peak) * ((t - 0.5) * 2)
    return curve


def _exponential_rise(start: float, end: float, steepness: float = 3.0) -> Callable[[float], float]:
    """Exponential rise - slow start, fast finish."""
    return lambda t: start + (end - start) * (1 - math.exp(-steepness * t)) / (1 - math.exp(-steepness))


def _exponential_fall(start: float, end: float, steepness: float = 3.0) -> Callable[[float], float]:
    """Exponential fall - fast start, slow finish."""
    return lambda t: start + (end - start) * (math.exp(-steepness * (1 - t)) - math.exp(-steepness)) / (1 - math.exp(-steepness))


# Journey presets
# Each returns: (tempo_curve, speed_curve, complexity_curve)
# All curves are functions that take t (0.0 to 1.0) and return the value

JOURNEY_PRESETS: Dict[str, Dict] = {
    'steady': {
        'name': 'Steady State',
        'description': 'Constant tempo and visuals - traditional ambient',
        'tempo': lambda base: (lambda t: base),
        'speed': lambda base: (lambda t: base),
        'complexity': lambda base: (lambda t: base),
    },
    
    'awakening': {
        'name': 'Awakening',
        'description': 'Gradual rise from stillness to energy - morning meditation',
        'tempo': lambda base: _linear(base * 0.6, base * 1.3),
        'speed': lambda base: _linear(base * 0.4, base * 1.2),
        'complexity': lambda base: _linear(base * 0.5, base * 1.0),
    },
    
    'deep_dive': {
        'name': 'Deep Dive',
        'description': 'Descending into calm - sleep preparation',
        'tempo': lambda base: _linear(base * 1.2, base * 0.5),
        'speed': lambda base: _linear(base * 1.0, base * 0.3),
        'complexity': lambda base: _linear(base * 0.8, base * 0.4),
    },
    
    'breathing': {
        'name': 'Breathing',
        'description': 'Rhythmic oscillation - guided breathing sync',
        'tempo': lambda base: _sine_wave(base, base * 0.25, cycles=8),
        'speed': lambda base: _sine_wave(base, base * 0.3, cycles=8),
        'complexity': lambda base: _sine_wave(base, base * 0.15, cycles=4),
    },
    
    'crescendo': {
        'name': 'Crescendo',
        'description': 'Build to peak then release - emotional journey',
        'tempo': lambda base: _arc(base * 0.7, base * 1.4, base * 0.8),
        'speed': lambda base: _arc(base * 0.5, base * 1.3, base * 0.6),
        'complexity': lambda base: _arc(base * 0.6, base * 1.0, base * 0.5),
    },
    
    'trance': {
        'name': 'Trance Induction',
        'description': 'Slow build with hypnotic repetition',
        'tempo': lambda base: _exponential_rise(base * 0.8, base * 1.1),
        'speed': lambda base: _sine_wave(base, base * 0.1, cycles=16),
        'complexity': lambda base: _exponential_rise(base * 0.6, base * 0.9),
    },
    
    'waves': {
        'name': 'Ocean Waves',
        'description': 'Long slow swells like ocean waves',
        'tempo': lambda base: _sine_wave(base, base * 0.2, cycles=3),
        'speed': lambda base: _sine_wave(base, base * 0.25, cycles=3),
        'complexity': lambda base: _sine_wave(base, base * 0.1, cycles=1.5),
    },
}


def get_journey(name: str) -> Dict:
    """Get a journey preset by name."""
    return JOURNEY_PRESETS.get(name, JOURNEY_PRESETS['steady'])


def get_journey_names() -> list:
    """Get list of available journey names."""
    return list(JOURNEY_PRESETS.keys())


def sample_journey(journey_name: str, t: float, base_tempo: float, 
                   base_speed: float, base_complexity: float) -> Tuple[float, float, float]:
    """
    Sample journey curves at time t (0.0 to 1.0).
    
    Returns: (tempo, speed, complexity) at that point in the journey.
    """
    journey = get_journey(journey_name)
    
    tempo = journey['tempo'](base_tempo)(t)
    speed = journey['speed'](base_speed)(t)
    complexity = journey['complexity'](base_complexity)(t)
    
    # Clamp to reasonable ranges
    tempo = max(20, min(200, tempo))
    speed = max(0.05, min(1.5, speed))
    complexity = max(0.1, min(1.0, complexity))
    
    return tempo, speed, complexity

