# Getting Started with Living Ambient Engine

## What Can You Do With This?

The Living Ambient Engine is a powerful tool for creating hypnotic ambient videos for YouTube monetization. Here's what you can accomplish:

### 🎬 **Create Professional Ambient Videos**
Generate high-quality videos combining:
- **Mesmerizing fractals** (Mandelbrot/Julia sets with color cycling)
- **Tribal drum patterns** (8 authentic rhythms from around the world)
- **Brainwave entrainment** (Binaural beats for focus, sleep, meditation)
- **Healing frequencies** (Solfeggio tones like 432Hz, 528Hz)

### 💰 **Monetize on YouTube**
- Create content for popular niches: meditation, focus music, sleep sounds
- Automate video production with CI/CD
- Generate hours of content per run (batch + Actions)
- SEO-optimized titles and descriptions

### 🤖 **Automate Everything**
- Batch generate multiple videos at once
- Run on GitHub Actions (free!) — manual or scheduled (personal `content-factory` cron is off in YAML until you enable it)
- Optional daily schedule when you uncomment cron in `.github/workflows/content-factory.yml`

---

## Installation

### Prerequisites
- Python 3.9 or higher
- FFmpeg (for video rendering)
- Git

### Setup Steps

```bash
# 1. Clone the repository
git clone https://github.com/peterkrentel/living-ambient-engine.git
cd living-ambient-engine

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify installation
python run_job.py --help
```

### Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

---

## Your First Video

Let's create your first ambient video! This will generate a 60-second "deep focus" video:

```bash
python run_job.py --mood deep_focus --duration 60
```

**What happens:**
1. Generates fractal visuals with 40Hz gamma brainwave patterns
2. Creates tribal drum audio with 432Hz solfeggio frequency
3. Renders final video to `output/` directory
4. Creates thumbnail and metadata

**Output files:**
- `output/video_<timestamp>.mp4` - Your final video
- `output/thumbnail_<timestamp>.png` - YouTube thumbnail
- `output/metadata_<timestamp>.json` - Video metadata

---

## Examples Gallery

### Example 1: Sleep Aid Video (10 minutes)
Perfect for bedtime meditation and deep sleep:

```bash
python run_job.py --mood sleep --duration 600
```

**Features:**
- 2Hz Delta waves (deep sleep state)
- 528Hz healing frequency
- Gentle heartbeat rhythm
- Slow-moving visuals

---

### Example 2: Study Focus Session (2 hours)
Great for concentration and productivity:

```bash
python run_job.py --mood study --duration 7200
```

**Features:**
- 12Hz Alpha waves (focused relaxation)
- 432Hz natural tuning
- Taiko drum pattern
- Energizing color palette

---

### Example 3: Meditation Journey (30 minutes)
For deep meditation and spiritual practice:

```bash
python run_job.py --mood ceremony --duration 1800
```

**Features:**
- 7Hz Theta waves (meditation state)
- 528Hz "miracle tone"
- Candomblé ceremonial rhythm
- Sacred geometry visuals

---

### Example 4: Morning Energy Boost (15 minutes)
Start your day with high energy:

```bash
python run_job.py --mood energize --duration 900
```

**Features:**
- 25Hz Beta waves (alertness)
- 741Hz awakening frequency
- Kuku tribal rhythm
- Vibrant colors

---

### Example 5: Trance State (1 hour)
Deep theta meditation and creativity:

```bash
python run_job.py --mood trance --duration 3600
```

**Features:**
- 6Hz Theta waves (creative flow)
- 528Hz healing tone
- Gnawa hypnotic rhythm
- Psychedelic visuals

---

## Batch Generation

Generate multiple videos at once for different moods and durations:

```bash
# Generate all moods with 1-hour and 2-hour versions
python batch_generate.py --moods all --durations 1h,2h

# Generate specific moods
python batch_generate.py --moods sleep,study,trance --durations 30m,1h

# Custom output directory
python batch_generate.py --moods all --durations 1h --output ./my_videos
```

**Time formats:**
- `30s` = 30 seconds
- `5m` = 5 minutes
- `1h` = 1 hour
- `2h30m` = 2 hours 30 minutes

---

## Understanding Moods

Each mood preset is scientifically designed for specific mental states:

### 🧠 Deep Focus
- **Best for:** Work, coding, studying
- **Brainwave:** 40Hz Gamma (peak concentration)
- **Frequency:** 432Hz (natural tuning)
- **Rhythm:** Taiko (steady, grounding)

### 😴 Sleep
- **Best for:** Falling asleep, insomnia
- **Brainwave:** 2Hz Delta (deep sleep)
- **Frequency:** 528Hz (healing)
- **Rhythm:** Heartbeat (calming)

### 😌 Chill
- **Best for:** Relaxation, unwinding
- **Brainwave:** 10Hz Alpha (calm alertness)
- **Frequency:** 639Hz (connection)
- **Rhythm:** Gamelan (flowing)

### 📚 Study
- **Best for:** Learning, reading
- **Brainwave:** 12Hz Alpha (focus)
- **Frequency:** 432Hz
- **Rhythm:** Taiko

### 🌀 Trance
- **Best for:** Meditation, creativity
- **Brainwave:** 6Hz Theta (trance state)
- **Frequency:** 528Hz
- **Rhythm:** Gnawa (hypnotic)

### ⚡ Energize
- **Best for:** Morning routine, exercise
- **Brainwave:** 25Hz Beta (alertness)
- **Frequency:** 741Hz (awakening)
- **Rhythm:** Kuku (energetic)

### 🔮 Ceremony
- **Best for:** Spiritual practice
- **Brainwave:** 7Hz Theta (meditation)
- **Frequency:** 528Hz
- **Rhythm:** Candomblé (sacred)

### ⚔️ Warrior
- **Best for:** Motivation, confidence
- **Brainwave:** 20Hz Beta (active)
- **Frequency:** 741Hz
- **Rhythm:** Burundi (powerful)

---

## Advanced Usage

### Custom Output Directory
```bash
python run_job.py --mood trance --duration 300 --output ./custom_folder
```

### Verbose Logging
```bash
python run_job.py --mood sleep --duration 600 --verbose
```

### Dry Run (Test Without Rendering)
```bash
python run_job.py --mood deep_focus --duration 60 --dry-run
```

---

## YouTube Upload

### One-Time Setup

1. **Create Google Cloud Project:**
   - Go to [console.cloud.google.com](https://console.cloud.google.com)
   - Create a new project
   - Enable "YouTube Data API v3"

2. **Get OAuth2 Credentials:**
   - Create OAuth2 credentials (Desktop app)
   - Download `client_secrets.json`
   - Place in project root

3. **Authenticate:**
   ```bash
   python youtube_upload.py --auth
   ```
   This opens a browser for authentication and saves the token.

### Upload Videos

```bash
# Upload a single video
python youtube_upload.py --file output/video_123456.mp4

# Upload entire batch
python youtube_upload.py --batch ./batch_output

# Custom title and description
python youtube_upload.py --file video.mp4 --title "Custom Title" --description "My description"
```

See [docs/youtube-auth.md](youtube-auth.md) for detailed setup instructions.

---

## Automation with GitHub Actions

Run the content factory automatically on GitHub's infrastructure (free!):

### Setup
1. Fork this repository
2. Add `YOUTUBE_TOKEN_B64` to GitHub Secrets
3. Enable GitHub Actions

### Scheduled Generation
The personal **Content Factory** workflow can run on a **daily 2 AM UTC** cron, but in the **current repo** that cron is **commented out** (manual runs only until you re-enable it). See `.github/workflows/content-factory.yml`. Brand and other workflows may use their own triggers — see [`docs/spec/workflows.md`](spec/workflows.md).

### Manual Trigger
1. Go to "Actions" tab
2. Select "Content Factory"
3. Click "Run workflow"
4. Choose mood and duration

---

## Tips & Best Practices

### 🎯 **For YouTube Success**
- Start with 1-hour videos (most popular length)
- Use varied moods (see `config/moods.yaml`; README highlights eight examples)
- Upload consistently (**schedule** when cron is on, or **manual** Actions runs)
- Let videos run ads after 8 minutes

### 🚀 **Optimization**
- Batch generate overnight
- Use 720p for smaller files
- Test 30-second videos first
- Monitor render times

### 💡 **Creative Ideas**
- Combine moods for playlists
- Create themed series (sleep challenge, study week)
- Seasonal content (holiday meditation)
- Respond to trending keywords

---

## What's Next?

1. **Create your first video** - Try the examples above
2. **Experiment with moods** - Find what resonates
3. **Batch generate** - Create a library
4. **Set up YouTube** - Start monetizing
5. **Automate** - Let GitHub Actions handle it

---

## Need Help?

- **Documentation:** [docs/](../docs)
- **Issues:** [GitHub Issues](https://github.com/peterkrentel/living-ambient-engine/issues)
- **Architecture:** [docs/architecture.md](architecture.md)
- **YouTube Setup:** [docs/youtube-auth.md](youtube-auth.md)

**Happy Creating! 🎨🎵🧘**
