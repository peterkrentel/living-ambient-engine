"""
Contract tests for Visual Generator.

Verifies pre-conditions, post-conditions, and invariants defined in:
    docs/spec/contracts/orchestrator-visual.md
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path

import pytest

from visuals.generator import VisualGenerator


class TestVisualContractPreConditions:
    """Test pre-conditions are enforced."""
    
    @pytest.fixture
    def valid_config(self):
        return {
            'colors': {
                'primary': [100, 100, 100],
                'secondary': [50, 50, 50],
                'accent': [200, 200, 200]
            },
            'speed': 0.5,
            'complexity': 0.7
        }
    
    def test_config_must_be_dict(self):
        """Pre: config must be a dict."""
        with pytest.raises((TypeError, AttributeError)):
            VisualGenerator("not a dict")
    
    def test_colors_required(self, valid_config):
        """Pre: colors key must exist in config."""
        del valid_config['colors']
        with pytest.raises(KeyError):
            VisualGenerator(valid_config)
    
    def test_duration_must_be_positive(self, valid_config):
        """Pre: duration must be > 0."""
        gen = VisualGenerator(valid_config, width=320, height=240, fps=15)
        with pytest.raises((ValueError, AssertionError)):
            with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
                gen.generate(-1, f.name)
    
    def test_output_dir_must_exist(self, valid_config):
        """Pre: output path directory must exist."""
        gen = VisualGenerator(valid_config, width=320, height=240, fps=15)
        with pytest.raises((IOError, OSError, FileNotFoundError)):
            gen.generate(5, '/nonexistent/dir/test.mp4')
    
    def test_invalid_journey_fallback(self, valid_config):
        """Pre: invalid journey falls back to 'steady'."""
        gen = VisualGenerator(valid_config, journey='nonexistent_journey')
        # Should not raise, should fall back
        assert gen is not None


class TestVisualContractPostConditions:
    """Test post-conditions are met after successful generation."""
    
    @pytest.fixture
    def valid_config(self):
        return {
            'colors': {
                'primary': [100, 100, 100],
                'secondary': [50, 50, 50],
                'accent': [200, 200, 200]
            },
            'speed': 0.5,
            'complexity': 0.7,
            'pattern': 'slow_waves'  # Fast pattern for tests
        }
    
    @pytest.fixture
    def generator(self, valid_config):
        return VisualGenerator(valid_config, width=320, height=240, fps=15)
    
    def test_file_exists_after_generate(self, generator):
        """Post: output file must exist."""
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
            output_path = f.name
        
        try:
            generator.generate(2, output_path)
            assert Path(output_path).exists()
        finally:
            if Path(output_path).exists():
                os.unlink(output_path)
    
    def test_file_non_empty(self, generator):
        """Post: output file must be non-empty."""
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
            output_path = f.name
        
        try:
            generator.generate(2, output_path)
            assert Path(output_path).stat().st_size > 0
        finally:
            if Path(output_path).exists():
                os.unlink(output_path)
    
    @pytest.mark.skipif(
        subprocess.run(['which', 'ffprobe'], capture_output=True).returncode != 0,
        reason="ffprobe not installed"
    )
    def test_duration_matches(self, generator):
        """Post: duration matches requested ±0.5 seconds."""
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
            output_path = f.name
        
        try:
            requested_duration = 3
            generator.generate(requested_duration, output_path)
            
            result = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                 '-of', 'json', output_path],
                capture_output=True, text=True
            )
            info = json.loads(result.stdout)
            actual_duration = float(info['format']['duration'])
            
            assert abs(actual_duration - requested_duration) < 0.5
        finally:
            if Path(output_path).exists():
                os.unlink(output_path)
    
    @pytest.mark.skipif(
        subprocess.run(['which', 'ffprobe'], capture_output=True).returncode != 0,
        reason="ffprobe not installed"
    )
    def test_resolution_correct(self, valid_config):
        """Post: resolution matches specified."""
        width, height = 320, 240
        gen = VisualGenerator(valid_config, width=width, height=height, fps=15)
        
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
            output_path = f.name
        
        try:
            gen.generate(2, output_path)
            
            result = subprocess.run(
                ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                 '-show_entries', 'stream=width,height', '-of', 'json', output_path],
                capture_output=True, text=True
            )
            info = json.loads(result.stdout)
            stream = info['streams'][0]
            
            assert stream['width'] == width
            assert stream['height'] == height
        finally:
            if Path(output_path).exists():
                os.unlink(output_path)

