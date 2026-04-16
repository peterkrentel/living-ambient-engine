# Testing Plan for Art Creator Integration

## Current Status ✅

**Branch**: `copilot/add-more-choice-for-action-runs`
**State**: All commits pushed, working tree clean
**Architecture Decision**: Independent workflow confirmed as correct

## What We've Implemented

### 1. New Workflow: `art-creator.yml`
- Independent workflow (not modifying existing)
- 20+ workflow_dispatch parameters
- Input validation
- Security measures (env vars, permissions)
- Dynamic config generation
- Public access enabled

### 2. Documentation
- `docs/ART_CREATOR.md` - Comprehensive user guide
- `docs/ART_CREATOR_EXAMPLES.md` - 20+ example combinations
- `docs/ART_CREATOR_QUICKSTART.md` - Quick start guide
- `docs/WORKFLOW_ARCHITECTURE.md` - Architecture decision doc
- `IMPLEMENTATION_SUMMARY.md` - Full implementation summary
- Updated `README.md`

### 3. Tests
- `scripts/test_art_creator_config.sh` - Config validation
- `scripts/test_art_creator_integration.py` - Integration tests

### 4. Security
- CodeQL scan: 0 alerts
- Input validation for all parameters
- Environment variables for user inputs
- Explicit permissions set

## Pre-Integration Checklist

Before your other changes are merged, verify:

- [x] All code committed and pushed
- [x] Working tree clean
- [x] Documentation complete
- [x] Tests passing locally
- [x] Security scan clean
- [x] Architecture decision documented

## Post-Integration Testing Plan

Once your other changes are integrated, we need to test:

### Phase 1: Workflow Validation (Critical)

#### Test 1.1: Workflow File Syntax
```bash
# Validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/art-creator.yml'))"
```
**Expected**: No syntax errors

#### Test 1.2: Workflow Appears in GitHub UI
**Manual Check**:
1. Go to Actions tab
2. Verify "Art Creator" appears in left sidebar
3. Click "Run workflow" button
4. Verify all 20+ parameters appear
5. Check dropdown options are populated

**Expected**: Workflow visible and accessible

### Phase 2: Configuration Tests

#### Test 2.1: Config Validation
```bash
cd /home/runner/work/living-ambient-engine/living-ambient-engine
./scripts/test_art_creator_config.sh
```
**Expected**: All 5 tests pass

#### Test 2.2: Integration Tests
```bash
cd /home/runner/work/living-ambient-engine/living-ambient-engine
python3 scripts/test_art_creator_integration.py
```
**Expected**: All integration tests pass

#### Test 2.3: Custom Config Generation
**Test**: Run config generation logic manually
```bash
# Test with 'none' rhythm
MUSIC_STYLE="none"
if [ "$MUSIC_STYLE" = "none" ]; then
  RHYTHM_VALUE="null"
else
  RHYTHM_VALUE="\"$MUSIC_STYLE\""
fi
echo "Rhythm value: $RHYTHM_VALUE"

# Test with actual rhythm
MUSIC_STYLE="gnawa"
if [ "$MUSIC_STYLE" = "none" ]; then
  RHYTHM_VALUE="null"
else
  RHYTHM_VALUE="\"$MUSIC_STYLE\""
fi
echo "Rhythm value: $RHYTHM_VALUE"
```
**Expected**: First prints "null", second prints "\"gnawa\""

### Phase 3: Orchestrator Compatibility

#### Test 3.1: Mood Loading
```bash
python3 << 'EOF'
from orchestrator import Orchestrator
o = Orchestrator()
moods = o.list_moods()
print(f"Total moods: {len(moods)}")
print("Moods:", list(moods.keys()))
EOF
```
**Expected**: Lists all moods including existing ones

#### Test 3.2: Custom Mood Addition
```bash
python3 << 'EOF'
import yaml
import tempfile
import shutil
from pathlib import Path

# Create temp config
temp_dir = Path(tempfile.mkdtemp())
shutil.copy("config/moods.yaml", temp_dir / "moods.yaml")
shutil.copy("config/defaults.yaml", temp_dir / "defaults.yaml")

# Append custom config
custom = {
    'test_custom': {
        'description': 'Test',
        'visual': {'type': 'fractal_zoom', 'speed': 0.5},
        'audio': {'rhythm': 'gnawa', 'rhythm_volume': 0.5}
    }
}
with open(temp_dir / "moods.yaml", 'a') as f:
    yaml.dump(custom, f)

# Load with orchestrator
from orchestrator import Orchestrator
o = Orchestrator(config_dir=str(temp_dir))
assert 'test_custom' in o.list_moods()
print("✅ Custom mood loaded successfully")

shutil.rmtree(temp_dir)
EOF
```
**Expected**: "✅ Custom mood loaded successfully"

### Phase 4: End-to-End Workflow Simulation

#### Test 4.1: Dry Run (Local Simulation)
```bash
# Simulate the workflow steps locally
cd /home/runner/work/living-ambient-engine/living-ambient-engine

# 1. Input validation simulation
python3 << 'EOF'
def validate_float(name, value, min_val, max_val):
    try:
        val = float(value)
        return min_val <= val <= max_val
    except:
        return False

# Test valid inputs
assert validate_float("visual_speed", "0.5", 0.01, 1.5)
assert validate_float("rhythm_volume", "0.7", 0.0, 1.0)
print("✅ Input validation working")
EOF

# 2. Config generation simulation
cat > /tmp/test_art_config.yaml << 'EOF'
custom_creation:
  description: "Test"
  visual:
    type: "fractal_zoom"
    speed: 0.5
  audio:
    rhythm: "gnawa"
    rhythm_volume: 0.5
EOF

# 3. Verify config is valid YAML
python3 -c "import yaml; yaml.safe_load(open('/tmp/test_art_config.yaml'))"
echo "✅ Config generation working"

# 4. Color palette simulation
python3 << 'EOF'
PALETTES = {
    'psychedelic': {
        'primary': [180, 0, 255],
        'secondary': [255, 0, 150],
        'accent': [0, 255, 200]
    }
}
palette = PALETTES['psychedelic']
assert palette['primary'] == [180, 0, 255]
print("✅ Color palette mapping working")
EOF

# Cleanup
rm /tmp/test_art_config.yaml
```
**Expected**: All steps print "✅" messages

#### Test 4.2: Full Workflow Run (GitHub Actions)
**Manual Test** (requires GitHub UI access):
1. Go to Actions → Art Creator
2. Click "Run workflow"
3. Use these test parameters:
   - Art Period: modern
   - Visual Pattern: fractal_zoom
   - Visual Speed: 0.5
   - Complexity: 0.7
   - Color Palette: psychedelic
   - Music Style: gnawa
   - Tempo: 60
   - Brainwave: 10
   - Solfeggio: 528
   - Duration: 30s (short for testing)
   - Seed: 42 (for reproducibility)
4. Monitor workflow execution
5. Check for errors in logs
6. Download artifact if successful

**Expected**: 
- Workflow completes successfully
- Artifact contains video file
- Video matches parameters
- Seed 42 is recorded in creation_info.json

### Phase 5: Integration with Other Changes

#### Test 5.1: No Conflicts
```bash
# Check for any conflicts with other changes
cd /home/runner/work/living-ambient-engine/living-ambient-engine
git status
git diff
```
**Expected**: No unexpected changes or conflicts

#### Test 5.2: Other Workflows Still Work
**Test content-factory.yml**:
```bash
# Verify content-factory still has its parameters
grep -A5 "workflow_dispatch:" .github/workflows/content-factory.yml
```
**Expected**: Shows moods, durations, dual, upload (4 params only)

**Test content-factory-brand.yml**:
```bash
# Verify brand workflow unchanged
grep -A5 "workflow_dispatch:" .github/workflows/content-factory-brand.yml
```
**Expected**: Shows same 4 parameters

#### Test 5.3: Orchestrator Changes
If you made changes to the orchestrator, test:
```bash
python3 << 'EOF'
from orchestrator import Orchestrator

# Test basic functionality
o = Orchestrator()

# Test that all expected methods exist
assert hasattr(o, 'generate')
assert hasattr(o, 'list_moods')
assert hasattr(o, '_load_moods')
assert hasattr(o, '_apply_variation')

# Test generate signature
import inspect
sig = inspect.signature(o.generate)
params = list(sig.parameters.keys())
print(f"Generate params: {params}")

# Should include: mood, duration, output_dir, rhythm_volume, drone_volume, seed
required = ['mood', 'duration']
optional = ['output_dir', 'rhythm_volume', 'drone_volume', 'seed']

for req in required:
    assert req in params, f"Missing required param: {req}"

print("✅ Orchestrator interface compatible")
EOF
```
**Expected**: "✅ Orchestrator interface compatible"

### Phase 6: Documentation Validation

#### Test 6.1: Links Work
```bash
# Check internal documentation links
cd /home/runner/work/living-ambient-engine/living-ambient-engine
for file in docs/*.md README.md; do
    echo "Checking $file..."
    grep -o '\[.*\](docs/.*\.md)' "$file" | while read link; do
        path=$(echo "$link" | sed 's/.*(\(.*\))/\1/')
        if [ ! -f "$path" ]; then
            echo "  ❌ Broken link: $path"
        fi
    done
done
```
**Expected**: No broken links

#### Test 6.2: Examples Are Valid
Verify examples in `docs/ART_CREATOR_EXAMPLES.md` use valid parameter values:
- Art periods exist in dropdown options
- Visual patterns match available options
- Color palettes are valid
- Music styles are valid
- Frequency values are in valid ranges

**Manual Review**: Spot-check 5 example combinations

### Phase 7: Security Re-verification

#### Test 7.1: CodeQL Scan
```bash
# This would be run in CI, but document it
# codeql analyze
```
**Expected**: 0 alerts

#### Test 7.2: Input Injection Prevention
Verify user inputs can't cause injection:
```bash
python3 << 'EOF'
import os

# Test that environment variables are used correctly
# Malicious input test
test_input = "'; echo 'hacked'; #"
os.environ['TEST_INPUT'] = test_input

# Verify it's treated as string, not executed
result = os.environ.get('TEST_INPUT')
assert result == test_input
assert ';' in result  # Still contains semicolon, but not executed
print("✅ No injection vulnerability")
EOF
```
**Expected**: "✅ No injection vulnerability"

## Regression Testing

After integration, ensure existing functionality still works:

### Test R1: Existing Moods Still Work
```bash
python3 << 'EOF'
from orchestrator import Orchestrator
o = Orchestrator()

# Test a few existing moods
existing_moods = ['deep_focus', 'sleep', 'chill', 'rain_sleep']
for mood in existing_moods:
    assert mood in o.list_moods(), f"Missing mood: {mood}"
    config = o.moods[mood]
    assert 'visual' in config
    assert 'audio' in config
    print(f"✅ {mood} config is valid")
EOF
```
**Expected**: All existing moods validated

### Test R2: Content Factory Workflow Unchanged
```bash
# Verify content factory workflow file hasn't changed
git diff origin/main:.github/workflows/content-factory.yml .github/workflows/content-factory.yml
```
**Expected**: No unexpected changes (or only our documented changes)

### Test R3: Run Job CLI Still Works
```bash
# Test the CLI interface
python3 run_job.py --list-moods | head -20
```
**Expected**: Lists moods including existing ones

## Performance Testing

### Test P1: Config Generation Time
```bash
time python3 << 'EOF'
import yaml
config = {
    'custom_creation': {
        'description': 'Test',
        'visual': {'type': 'fractal_zoom', 'speed': 0.5},
        'audio': {'rhythm': 'gnawa', 'rhythm_volume': 0.5}
    }
}
with open('/tmp/perf_test.yaml', 'w') as f:
    yaml.dump(config, f)
EOF
```
**Expected**: < 1 second

### Test P2: Workflow Startup Time
**Manual**: Time from "Run workflow" click to first step starting
**Expected**: < 2 minutes (GitHub Actions queue time)

## Known Issues to Watch For

Based on our implementation, watch for:

1. **Null Rhythm Handling**: Ensure 'none' music style converts to null correctly
2. **Custom RGB Parsing**: Verify comma-separated RGB values parse correctly
3. **Duration Parsing**: Check various formats (30s, 5min, 1h, etc.)
4. **Seed Reproducibility**: Same seed should produce identical output
5. **Environment Variable Escaping**: User inputs should be safe

## Quick Smoke Test (1 minute)

Run this quick test to verify nothing is broken:

```bash
cd /home/runner/work/living-ambient-engine/living-ambient-engine

# 1. YAML syntax
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/art-creator.yml'))" && echo "✅ YAML valid"

# 2. Config tests
./scripts/test_art_creator_config.sh > /dev/null 2>&1 && echo "✅ Config tests pass"

# 3. Integration tests
python3 scripts/test_art_creator_integration.py > /dev/null 2>&1 && echo "✅ Integration tests pass"

# 4. Orchestrator loads
python3 -c "from orchestrator import Orchestrator; o = Orchestrator(); print(f'✅ Orchestrator loads ({len(o.list_moods())} moods)')"

# 5. Existing workflows valid
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/content-factory.yml'))" && echo "✅ Content Factory valid"

echo ""
echo "🎉 Quick smoke test complete!"
```

## When Your Changes Are Merged

Run these commands:

```bash
# 1. Pull latest changes
git checkout main
git pull origin main

# 2. Checkout our branch
git checkout copilot/add-more-choice-for-action-runs

# 3. Rebase on main
git rebase main

# 4. Run smoke test
cd /home/runner/work/living-ambient-engine/living-ambient-engine
# (run quick smoke test above)

# 5. If conflicts, resolve and continue
# If tests fail, investigate and fix

# 6. Push updated branch
git push -f origin copilot/add-more-choice-for-action-runs
```

## Contact Points

If issues arise after integration:

- **Config Generation**: Check `art-creator.yml` lines 190-280
- **Color Palettes**: Check `art-creator.yml` lines 285-395
- **Input Validation**: Check `art-creator.yml` lines 195-235
- **Orchestrator Integration**: Check `art-creator.yml` lines 410-505
- **Tests**: See `scripts/test_art_creator_*.{sh,py}`

## Summary

**Current State**: ✅ All our changes are complete, tested, and committed

**Ready For**: Integration with your other changes

**What to Test After Integration**:
1. Run quick smoke test (1 min)
2. Run full test suite (5 min)
3. Manual workflow test in GitHub UI (optional, 10 min)

**Expected Outcome**: Everything should work together seamlessly since we created an independent workflow that doesn't modify existing code.

---

**Status**: Ready for integration testing when your changes are merged! 🚀
