#!/bin/bash
# Quick test script to generate a short video for each mood

set -e

echo "🧪 Testing Living Ambient Engine with all moods..."
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Test duration (short for quick testing)
DURATION=10

# Test each mood
for mood in deep_focus sleep chill study energize; do
    echo "Testing mood: $mood"
    python run_job.py --mood $mood --duration $DURATION --output ./test_output
    echo ""
done

echo "✅ All tests complete! Check ./test_output directory for results."

