"""
Contract tests for Config Validation.

Verifies the validation schemas enforce guardrails defined in:
    docs/spec/GUARDRAILS.md
"""

import pytest

# Import validator - may need jsonschema
try:
    from config.validator import (
        validate_audio_config,
        validate_visual_config,
        validate_journey_config,
        validate_workflow_inputs,
        clamp_to_guardrails,
        HAS_JSONSCHEMA
    )
except ImportError:
    HAS_JSONSCHEMA = False

pytestmark = pytest.mark.skipif(not HAS_JSONSCHEMA, reason="jsonschema not installed")


class TestAudioConfigValidation:
    """Test audio config validation against guardrails."""
    
    def test_valid_config(self):
        """Valid config should pass."""
        config = {'tempo': 60, 'rhythm_volume': 0.5}
        valid, errors = validate_audio_config(config)
        assert valid, f"Should be valid: {errors}"
    
    def test_tempo_required(self):
        """Tempo is required."""
        config = {'rhythm_volume': 0.5}
        valid, errors = validate_audio_config(config)
        assert not valid
        assert any('tempo' in e.lower() for e in errors)
    
    def test_tempo_min_boundary(self):
        """Tempo must be >= 20."""
        config = {'tempo': 19}
        valid, errors = validate_audio_config(config)
        assert not valid
    
    def test_tempo_max_boundary(self):
        """Tempo must be <= 200."""
        config = {'tempo': 201}
        valid, errors = validate_audio_config(config)
        assert not valid
    
    def test_rhythm_volume_range(self):
        """Rhythm volume must be 0.0-1.0."""
        config = {'tempo': 60, 'rhythm_volume': 1.5}
        valid, errors = validate_audio_config(config)
        assert not valid


class TestVisualConfigValidation:
    """Test visual config validation against guardrails."""
    
    @pytest.fixture
    def valid_config(self):
        return {
            'colors': {
                'primary': [100, 100, 100],
                'secondary': [50, 50, 50],
                'accent': [200, 200, 200]
            }
        }
    
    def test_valid_config(self, valid_config):
        """Valid config should pass."""
        valid, errors = validate_visual_config(valid_config)
        assert valid, f"Should be valid: {errors}"
    
    def test_colors_required(self):
        """Colors is required."""
        config = {'speed': 0.5}
        valid, errors = validate_visual_config(config)
        assert not valid
        assert any('colors' in e.lower() for e in errors)
    
    def test_speed_min_boundary(self, valid_config):
        """Speed must be >= 0.01."""
        valid_config['speed'] = 0.001
        valid, errors = validate_visual_config(valid_config)
        assert not valid
    
    def test_speed_max_boundary(self, valid_config):
        """Speed must be <= 1.5."""
        valid_config['speed'] = 2.0
        valid, errors = validate_visual_config(valid_config)
        assert not valid
    
    def test_complexity_range(self, valid_config):
        """Complexity must be 0.1-1.0."""
        valid_config['complexity'] = 0.05
        valid, errors = validate_visual_config(valid_config)
        assert not valid


class TestJourneyConfigValidation:
    """Test journey config validation."""
    
    def test_valid_journey(self):
        """Valid journey preset should pass."""
        config = {'journey': 'awakening', 'journey_intensity': 'moderate'}
        valid, errors = validate_journey_config(config)
        assert valid, f"Should be valid: {errors}"
    
    def test_invalid_journey(self):
        """Invalid journey preset should fail."""
        config = {'journey': 'nonexistent'}
        valid, errors = validate_journey_config(config)
        assert not valid
    
    def test_invalid_intensity(self):
        """Invalid intensity should fail."""
        config = {'journey': 'steady', 'journey_intensity': 'extreme'}
        valid, errors = validate_journey_config(config)
        assert not valid


class TestClampToGuardrails:
    """Test clamping function applies guardrails."""
    
    def test_clamp_tempo_high(self):
        """Tempo over 200 should be clamped."""
        config = {'tempo': 300}
        clamped = clamp_to_guardrails(config, 'audio_config')
        assert clamped['tempo'] == 200
    
    def test_clamp_tempo_low(self):
        """Tempo under 20 should be clamped."""
        config = {'tempo': 10}
        clamped = clamp_to_guardrails(config, 'audio_config')
        assert clamped['tempo'] == 20
    
    def test_clamp_speed_high(self):
        """Speed over 1.5 should be clamped."""
        config = {'speed': 3.0}
        clamped = clamp_to_guardrails(config, 'visual_config')
        assert clamped['speed'] == 1.5
    
    def test_clamp_preserves_valid(self):
        """Valid values should not be changed."""
        config = {'tempo': 100}
        clamped = clamp_to_guardrails(config, 'audio_config')
        assert clamped['tempo'] == 100
    
    def test_clamp_preserves_type(self):
        """Clamping should preserve int/float type."""
        config = {'tempo': 300}  # int
        clamped = clamp_to_guardrails(config, 'audio_config')
        assert isinstance(clamped['tempo'], int)

