"""
Configuration validator using JSON Schema.

Validates configs against schemas defined in config/schemas/.
See docs/spec/GUARDRAILS.md for parameter limits.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Try to import jsonschema, but allow graceful fallback
try:
    import jsonschema
    from jsonschema import Draft202012Validator, ValidationError
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False
    ValidationError = Exception

SCHEMA_DIR = Path(__file__).parent / "schemas"


def load_schema(schema_name: str) -> Dict[str, Any]:
    """Load a JSON schema by name."""
    schema_path = SCHEMA_DIR / f"{schema_name}.json"
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    
    with open(schema_path) as f:
        return json.load(f)


def validate_config(config: Dict[str, Any], schema_name: str) -> Tuple[bool, List[str]]:
    """
    Validate a config dict against a named schema.
    
    Args:
        config: Configuration dictionary to validate
        schema_name: Name of schema (without .json extension)
    
    Returns:
        Tuple of (is_valid, list of error messages)
    """
    if not HAS_JSONSCHEMA:
        # Graceful fallback - skip validation if jsonschema not installed
        return True, ["Warning: jsonschema not installed, validation skipped"]
    
    try:
        schema = load_schema(schema_name)
    except FileNotFoundError as e:
        return False, [str(e)]
    
    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(config))
    
    if not errors:
        return True, []
    
    error_messages = []
    for error in errors:
        path = ".".join(str(p) for p in error.absolute_path) if error.absolute_path else "root"
        error_messages.append(f"{path}: {error.message}")
    
    return False, error_messages


def validate_audio_config(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate audio generator configuration."""
    return validate_config(config, "audio_config")


def validate_visual_config(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate visual generator configuration."""
    return validate_config(config, "visual_config")


def validate_journey_config(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate journey configuration."""
    return validate_config(config, "journey_config")


def validate_workflow_inputs(inputs: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate workflow inputs."""
    return validate_config(inputs, "workflow_inputs")


def clamp_to_guardrails(config: Dict[str, Any], schema_name: str) -> Dict[str, Any]:
    """
    Clamp config values to guardrail limits defined in schema.
    
    This applies Level 1 enforcement (silent clamping) for numeric values.
    """
    try:
        schema = load_schema(schema_name)
    except FileNotFoundError:
        return config
    
    result = config.copy()
    properties = schema.get("properties", {})
    
    for key, value in result.items():
        if key not in properties:
            continue
        
        prop_schema = properties[key]
        
        # Clamp numeric values
        if isinstance(value, (int, float)):
            if "minimum" in prop_schema:
                value = max(value, prop_schema["minimum"])
            if "maximum" in prop_schema:
                value = min(value, prop_schema["maximum"])
            result[key] = type(config[key])(value)  # Preserve int/float type
    
    return result


if __name__ == "__main__":
    # Quick test
    test_audio = {"tempo": 60, "rhythm_volume": 0.5}
    valid, errors = validate_audio_config(test_audio)
    print(f"Audio config valid: {valid}")
    if errors:
        print(f"  Errors: {errors}")
    
    test_visual = {
        "colors": {"primary": [100, 100, 100], "secondary": [50, 50, 50], "accent": [200, 200, 200]},
        "speed": 0.5
    }
    valid, errors = validate_visual_config(test_visual)
    print(f"Visual config valid: {valid}")
    if errors:
        print(f"  Errors: {errors}")
    
    # Test clamping
    over_limit = {"tempo": 300, "rhythm_volume": 1.5}
    clamped = clamp_to_guardrails(over_limit, "audio_config")
    print(f"Clamped: {clamped}")  # Should show tempo=200, rhythm_volume=1.0

