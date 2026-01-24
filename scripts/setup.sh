#!/bin/bash
# Setup script for Living Ambient Engine

set -e

echo "🚀 Setting up Living Ambient Engine..."

# Check Python version
echo "Checking Python version..."
python3 --version

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null
then
    echo "❌ FFmpeg is not installed!"
    echo "Please install FFmpeg:"
    echo "  macOS:        brew install ffmpeg"
    echo "  Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "  Windows:      Download from https://ffmpeg.org/download.html"
    exit 1
fi

echo "✅ FFmpeg found: $(ffmpeg -version | head -n 1)"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create output directories
echo "Creating output directories..."
mkdir -p output
mkdir -p artifacts
mkdir -p temp

# Copy .env.example to .env if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To generate your first video, run:"
echo "  python run_job.py --mood deep_focus --duration 60"
echo ""

