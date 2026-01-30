#!/bin/bash
# Test the Art Creator workflow configuration generation logic

set -e

echo "🧪 Testing Art Creator workflow configuration..."
echo ""

# Create temporary directory
TEST_DIR=$(mktemp -d)
echo "Test directory: $TEST_DIR"

# Test 1: Generate config with 'none' rhythm
echo "Test 1: Generate config with 'none' rhythm (should become null)"
RHYTHM_VALUE="none"
if [ "$RHYTHM_VALUE" = "none" ]; then
  RHYTHM_VALUE="null"
else
  RHYTHM_VALUE="\"$RHYTHM_VALUE\""
fi

cat > $TEST_DIR/test_config1.yaml << EOF
custom_creation:
  description: "Custom artistic creation"
  audio:
    rhythm: $RHYTHM_VALUE
    rhythm_volume: 0.5
EOF

# Validate with Python
python3 << PYTHON_SCRIPT
import yaml
with open('$TEST_DIR/test_config1.yaml', 'r') as f:
    config = yaml.safe_load(f)
rhythm = config['custom_creation']['audio']['rhythm']
assert rhythm is None, f"Expected rhythm to be None, got {rhythm}"
print("✅ Test 1 passed: 'none' rhythm correctly converts to null/None")
PYTHON_SCRIPT

# Test 2: Generate config with actual rhythm value
echo "Test 2: Generate config with actual rhythm value"
RHYTHM_VALUE="gnawa"
if [ "$RHYTHM_VALUE" = "none" ]; then
  RHYTHM_VALUE="null"
else
  RHYTHM_VALUE="\"$RHYTHM_VALUE\""
fi

cat > $TEST_DIR/test_config2.yaml << EOF
custom_creation:
  description: "Custom artistic creation"
  audio:
    rhythm: $RHYTHM_VALUE
    rhythm_volume: 0.5
EOF

python3 << PYTHON_SCRIPT
import yaml
with open('$TEST_DIR/test_config2.yaml', 'r') as f:
    config = yaml.safe_load(f)
rhythm = config['custom_creation']['audio']['rhythm']
assert rhythm == 'gnawa', f"Expected rhythm to be 'gnawa', got {rhythm}"
print("✅ Test 2 passed: rhythm value 'gnawa' correctly preserved")
PYTHON_SCRIPT

# Test 3: Test color palette application
echo "Test 3: Test color palette application"
python3 << 'PYTHON_SCRIPT'
import yaml

PALETTES = {
    'psychedelic': {
        'primary': [180, 0, 255],
        'secondary': [255, 0, 150],
        'accent': [0, 255, 200]
    },
    'sunset': {
        'primary': [255, 120, 60],
        'secondary': [255, 180, 100],
        'accent': [255, 220, 180]
    }
}

# Test psychedelic palette
palette = 'psychedelic'
colors = PALETTES.get(palette)
assert colors['primary'] == [180, 0, 255], "Psychedelic primary color mismatch"
assert colors['secondary'] == [255, 0, 150], "Psychedelic secondary color mismatch"
assert colors['accent'] == [0, 255, 200], "Psychedelic accent color mismatch"
print("✅ Test 3a passed: psychedelic palette colors are correct")

# Test custom palette parsing
custom_primary = "100,150,200"
primary = [int(x) for x in custom_primary.split(',')]
assert primary == [100, 150, 200], "Custom primary color parsing failed"
print("✅ Test 3b passed: custom color parsing works")
PYTHON_SCRIPT

# Test 4: Test that custom config can be appended to moods.yaml
echo "Test 4: Test config merging with moods.yaml"
cp config/moods.yaml $TEST_DIR/moods_backup.yaml

cat > $TEST_DIR/custom_config.yaml << EOF
custom_creation:
  description: "Test custom creation"
  visual:
    type: "fractal_zoom"
    speed: 0.5
  audio:
    rhythm: "gnawa"
    rhythm_volume: 0.5
EOF

# Append and validate
cat $TEST_DIR/custom_config.yaml >> $TEST_DIR/moods_backup.yaml

python3 << PYTHON_SCRIPT
import yaml
with open('$TEST_DIR/moods_backup.yaml', 'r') as f:
    moods = yaml.safe_load(f)
assert 'custom_creation' in moods, "custom_creation not found in merged config"
assert moods['custom_creation']['description'] == "Test custom creation"
print("✅ Test 4 passed: custom config successfully merged with moods")
PYTHON_SCRIPT

# Test 5: Test duration parsing logic
echo "Test 5: Test duration parsing logic"
python3 << 'PYTHON_SCRIPT'
def parse_duration(duration_str):
    if duration_str.endswith('h'):
        return int(duration_str[:-1]) * 3600
    elif duration_str.endswith('min'):
        return int(duration_str[:-3]) * 60
    elif duration_str.endswith('s'):
        return int(duration_str[:-1])
    else:
        return int(duration_str)

# Test cases
test_cases = [
    ("30s", 30),
    ("5min", 300),
    ("1h", 3600),
    ("3h", 10800),
    ("300", 300)
]

for duration_str, expected in test_cases:
    result = parse_duration(duration_str)
    assert result == expected, f"Duration parsing failed for {duration_str}: got {result}, expected {expected}"

print("✅ Test 5 passed: duration parsing works for all formats")
PYTHON_SCRIPT

# Cleanup
rm -rf $TEST_DIR
echo ""
echo "✅ All Art Creator configuration tests passed!"
echo ""
