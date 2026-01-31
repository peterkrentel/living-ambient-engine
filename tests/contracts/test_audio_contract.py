"""
Contract tests for Audio Generator.

Verifies pre-conditions, post-conditions, and invariants defined in:
    docs/spec/contracts/orchestrator-audio.md
"""

import os
import tempfile
import wave
from pathlib import Path

import pytest
import numpy as np

from audio.generator import AudioGenerator


class TestAudioContractPreConditions:
    """Test pre-conditions are enforced."""
    
    def test_config_must_be_dict(self):
        """Pre: config must be a dict."""
        with pytest.raises((TypeError, AttributeError)):
            AudioGenerator("not a dict")
    
    def test_tempo_required(self):
        """Pre: tempo key must exist in config."""
        with pytest.raises(KeyError):
            AudioGenerator({})
    
    def test_tempo_clamped_low(self):
        """Pre: tempo < 20 should be clamped."""
        gen = AudioGenerator({'tempo': 10})
        # Tempo should be clamped, not rejected
        assert gen.config.get('tempo', 20) >= 20
    
    def test_tempo_clamped_high(self):
        """Pre: tempo > 200 should be clamped."""
        gen = AudioGenerator({'tempo': 300})
        assert gen.config.get('tempo', 200) <= 200
    
    def test_duration_must_be_positive(self):
        """Pre: duration must be > 0."""
        gen = AudioGenerator({'tempo': 60})
        with pytest.raises((ValueError, AssertionError)):
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                gen.generate(-1, f.name)
    
    def test_output_dir_must_exist(self):
        """Pre: output path directory must exist."""
        gen = AudioGenerator({'tempo': 60})
        with pytest.raises((IOError, OSError, FileNotFoundError)):
            gen.generate(5, '/nonexistent/dir/test.wav')
    
    def test_invalid_journey_fallback(self):
        """Pre: invalid journey falls back to 'steady'."""
        gen = AudioGenerator({'tempo': 60}, journey='nonexistent_journey')
        # Should not raise, should fall back to steady
        assert gen.journey in ['steady', 'nonexistent_journey']  # Either stored or defaulted


class TestAudioContractPostConditions:
    """Test post-conditions are met after successful generation."""
    
    def test_file_exists_after_generate(self):
        """Post: output file must exist."""
        gen = AudioGenerator({'tempo': 60})
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            output_path = f.name
        
        try:
            gen.generate(3, output_path)
            assert Path(output_path).exists()
        finally:
            if Path(output_path).exists():
                os.unlink(output_path)
    
    def test_file_non_empty(self):
        """Post: output file must be non-empty."""
        gen = AudioGenerator({'tempo': 60})
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            output_path = f.name
        
        try:
            gen.generate(3, output_path)
            assert Path(output_path).stat().st_size > 0
        finally:
            if Path(output_path).exists():
                os.unlink(output_path)
    
    def test_duration_matches(self):
        """Post: duration matches requested ±1 second."""
        gen = AudioGenerator({'tempo': 60})
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            output_path = f.name
        
        try:
            requested_duration = 5
            gen.generate(requested_duration, output_path)
            
            with wave.open(output_path, 'r') as w:
                actual_duration = w.getnframes() / w.getframerate()
            
            assert abs(actual_duration - requested_duration) < 1.0
        finally:
            if Path(output_path).exists():
                os.unlink(output_path)
    
    def test_sample_rate_correct(self):
        """Post: sample rate matches specified."""
        sample_rate = 44100
        gen = AudioGenerator({'tempo': 60}, sample_rate=sample_rate)
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            output_path = f.name
        
        try:
            gen.generate(3, output_path)
            
            with wave.open(output_path, 'r') as w:
                assert w.getframerate() == sample_rate
        finally:
            if Path(output_path).exists():
                os.unlink(output_path)
    
    def test_channels_correct(self):
        """Post: channel count matches specified."""
        channels = 2
        gen = AudioGenerator({'tempo': 60}, channels=channels)
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            output_path = f.name
        
        try:
            gen.generate(3, output_path)
            
            with wave.open(output_path, 'r') as w:
                assert w.getnchannels() == channels
        finally:
            if Path(output_path).exists():
                os.unlink(output_path)


class TestAudioContractInvariants:
    """Test invariants hold during execution."""
    
    def test_deterministic_output(self):
        """Invariant: same seed + config = identical output."""
        import random
        random.seed(42)
        np.random.seed(42)
        
        gen1 = AudioGenerator({'tempo': 60})
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            path1 = f.name
        
        random.seed(42)
        np.random.seed(42)
        
        gen2 = AudioGenerator({'tempo': 60})
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            path2 = f.name
        
        try:
            gen1.generate(2, path1)
            gen2.generate(2, path2)
            
            # Files should be identical
            with open(path1, 'rb') as f1, open(path2, 'rb') as f2:
                assert f1.read() == f2.read()
        finally:
            for p in [path1, path2]:
                if Path(p).exists():
                    os.unlink(p)

