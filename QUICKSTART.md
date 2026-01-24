# Living Ambient Engine - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Setup

Run the automated setup script:

```bash
./scripts/setup.sh
```

This will:
- Check for Python 3.9+
- Verify FFmpeg is installed
- Create a virtual environment
- Install all dependencies
- Create necessary directories

**OR** do it manually:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

### Step 2: Generate Your First Video

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Generate a 1-minute deep focus video
python run_job.py --mood deep_focus --duration 60
```

### Step 3: Check Your Output

Your video will be in the `output/` directory:
- `deep_focus_60s_TIMESTAMP.mp4` - The video
- `deep_focus_60s_TIMESTAMP.json` - Metadata
- `deep_focus_60s_TIMESTAMP.png` - Thumbnail

## 🎨 Try Different Moods

```bash
# List all available moods
python run_job.py --list-moods

# Generate different moods
python run_job.py --mood sleep --duration 300      # 5-min sleep video
python run_job.py --mood chill --duration 180      # 3-min chill video
python run_job.py --mood study --duration 600      # 10-min study video
python run_job.py --mood energize --duration 120   # 2-min energize video
```

## 🧪 Test All Moods

Run the test script to generate a short video for each mood:

```bash
./scripts/test_generation.sh
```

This creates 10-second test videos in `./test_output/`

## ⚙️ Customize

Edit `config/moods.yaml` to:
- Modify existing moods
- Create new mood presets
- Adjust colors, patterns, frequencies

Edit `config/defaults.yaml` to:
- Change video resolution
- Adjust FPS
- Modify output settings

## 🎬 Production Videos

For YouTube-ready content:

```bash
# 10-minute 1080p video
python run_job.py --mood deep_focus --duration 600

# 1-hour sleep video
python run_job.py --mood sleep --duration 3600

# Custom output location
python run_job.py --mood chill --duration 1800 --output ~/Videos/ambient
```

## 🐛 Troubleshooting

**FFmpeg not found:**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg
```

**Import errors:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Video generation fails:**
- Check that you have enough disk space
- Ensure FFmpeg is properly installed: `ffmpeg -version`
- Check logs for specific errors

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [SECURITY.md](SECURITY.md) for secrets management
- Explore the code in `audio/`, `visuals/`, and `render/` modules
- Create custom mood presets in `config/moods.yaml`

## 🎯 Example Workflow

```bash
# 1. Activate environment
source venv/bin/activate

# 2. Generate a test video
python run_job.py --mood deep_focus --duration 30

# 3. Review the output
open output/deep_focus_30s_*.mp4  # macOS
# or
vlc output/deep_focus_30s_*.mp4   # Linux

# 4. Generate production video
python run_job.py --mood deep_focus --duration 600

# 5. Upload to YouTube (manual for now, automated in Milestone 2)
```

Happy generating! 🎨🎵✨

