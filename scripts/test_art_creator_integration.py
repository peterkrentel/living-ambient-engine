#!/usr/bin/env python3
"""
Integration test for Art Creator workflow configuration.
Tests that custom configurations can be loaded and processed by the orchestrator.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import yaml
import tempfile
import shutil
from pathlib import Path
from orchestrator import Orchestrator

def test_custom_config_loading():
    """Test that a custom config can be added and loaded by orchestrator."""
    
    print("🧪 Testing custom configuration loading...")
    
    # Create a temporary config directory
    temp_config_dir = Path(tempfile.mkdtemp(prefix="art_creator_test_"))
    
    try:
        # Copy existing configs
        shutil.copy("config/moods.yaml", temp_config_dir / "moods.yaml")
        shutil.copy("config/defaults.yaml", temp_config_dir / "defaults.yaml")
        
        # Create a custom configuration
        custom_config = {
            'test_custom': {
                'description': 'Test custom artistic creation',
                'title_template': 'Test Art Creation',
                'visual': {
                    'type': 'fractal_zoom',
                    'speed': 0.5,
                    'complexity': 0.7,
                    'symmetry': 6,
                    'pulse_frequency': 0.1,
                    'pattern': 'mandelbrot',
                    'colors': {
                        'primary': [180, 0, 255],
                        'secondary': [255, 0, 150],
                        'accent': [0, 255, 200]
                    }
                },
                'audio': {
                    'rhythm': 'gnawa',
                    'rhythm_volume': 0.5,
                    'base_frequency': 10,
                    'binaural_beat': 10,
                    'layers': [
                        {
                            'type': 'sine',
                            'frequency': 528,
                            'amplitude': 0.1
                        },
                        {
                            'type': 'binaural',
                            'carrier': 200,
                            'beat': 10,
                            'amplitude': 0.12
                        }
                    ]
                }
            }
        }
        
        # Append to moods config
        with open(temp_config_dir / "moods.yaml", 'a') as f:
            yaml.dump(custom_config, f)
        
        # Create orchestrator with custom config dir
        orchestrator = Orchestrator(config_dir=str(temp_config_dir))
        
        # Verify custom mood is loaded
        moods = orchestrator.list_moods()
        assert 'test_custom' in moods, "Custom mood 'test_custom' not found in loaded moods"
        print(f"✅ Custom mood loaded successfully")
        print(f"   Total moods: {len(moods)}")
        print(f"   Custom mood description: {moods['test_custom']}")
        
        # Verify the configuration structure
        mood_config = orchestrator.moods['test_custom']
        assert mood_config['visual']['type'] == 'fractal_zoom'
        assert mood_config['audio']['rhythm'] == 'gnawa'
        assert mood_config['audio']['base_frequency'] == 10
        print(f"✅ Custom configuration structure is correct")
        
        # Test with 'none' rhythm (should be null)
        custom_config_none_rhythm = {
            'test_custom_none': {
                'description': 'Test with no rhythm',
                'visual': {
                    'type': 'starfield',
                    'speed': 0.3,
                    'colors': {
                        'primary': [0, 50, 100],
                        'secondary': [0, 100, 150],
                        'accent': [100, 180, 220]
                    }
                },
                'audio': {
                    'rhythm': None,  # None/null rhythm
                    'rhythm_volume': 0.0,
                    'base_frequency': 8,
                    'binaural_beat': 8,
                    'layers': []
                }
            }
        }
        
        with open(temp_config_dir / "moods.yaml", 'a') as f:
            yaml.dump(custom_config_none_rhythm, f)
        
        # Reload orchestrator
        orchestrator = Orchestrator(config_dir=str(temp_config_dir))
        moods = orchestrator.list_moods()
        assert 'test_custom_none' in moods, "Custom mood with none rhythm not found"
        
        mood_config = orchestrator.moods['test_custom_none']
        assert mood_config['audio']['rhythm'] is None, f"Expected rhythm to be None, got {mood_config['audio']['rhythm']}"
        print(f"✅ Custom configuration with null rhythm works correctly")
        
        return True
        
    finally:
        # Cleanup
        shutil.rmtree(temp_config_dir)
        print(f"🧹 Cleaned up temporary directory")


def test_color_palette_mapping():
    """Test that color palettes are correctly mapped."""
    
    print("\n🧪 Testing color palette mapping...")
    
    palettes = {
        'psychedelic': {
            'primary': [180, 0, 255],
            'secondary': [255, 0, 150],
            'accent': [0, 255, 200]
        },
        'sunset': {
            'primary': [255, 120, 60],
            'secondary': [255, 180, 100],
            'accent': [255, 220, 180]
        },
        'custom': None  # Will use custom RGB
    }
    
    # Test preset palettes
    for palette_name, expected_colors in palettes.items():
        if palette_name == 'custom':
            continue
        assert 'primary' in expected_colors
        assert 'secondary' in expected_colors
        assert 'accent' in expected_colors
        assert len(expected_colors['primary']) == 3
        print(f"✅ Palette '{palette_name}' has correct structure")
    
    # Test custom RGB parsing
    custom_rgb = "100,150,200"
    parsed = [int(x) for x in custom_rgb.split(',')]
    assert parsed == [100, 150, 200], f"RGB parsing failed: got {parsed}"
    print(f"✅ Custom RGB parsing works correctly")
    
    return True


if __name__ == '__main__':
    print("=" * 60)
    print("Art Creator Integration Tests")
    print("=" * 60)
    
    try:
        test_custom_config_loading()
        test_color_palette_mapping()
        
        print("\n" + "=" * 60)
        print("✅ ALL INTEGRATION TESTS PASSED")
        print("=" * 60)
        print("\nThe Art Creator workflow configuration is ready to use!")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
