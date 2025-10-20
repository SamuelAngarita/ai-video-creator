# AI Video Creator

**Automated MP4 video generation from still images using Google Veo AI and FFmpeg**

## Overview

AI Video Creator transforms static images into dynamic MP4 videos using Google's Veo AI for intelligent animations and FFmpeg for professional video processing.

## Features

- 🤖 **AI-powered animations** using Google Veo API (zoom, pan, zoom-out effects)
- 🎬 **Professional video processing** with FFmpeg normalization and concatenation
- 🎵 **Background music integration** with automatic audio mixing
- 🐳 **Docker-ready** for easy deployment on any platform
- 🔄 **Smart fallback system** with dummy video generation when API limits are reached
- 📁 **Flexible input** via JSON configuration
- 🌍 **Bilingual support** (English/Spanish) in code comments

## Architecture at a Glance

The system follows a robust pipeline: downloads assets → generates AI videos → normalizes clips → concatenates → adds music.
## File Structure

```
ai-video-creator/
├── Code/
│   ├── main.py              # Main pipeline orchestrator
│   ├── config.py            # Path configuration and work directory setup
│   ├── read.py              # Asset download (images, music) with validation
│   ├── google_api.py        # Google Veo API integration with fallback
│   ├── prompt.py            # Animation prompt generation for different transitions
│   ├── combine.py           # Video processing pipeline (normalize, concat, mix)
│   └── .work/               # Working directory for all artifacts
│       └── input.json       # Configuration file (images, music, transitions)
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Easy Docker deployment
├── requirements.txt         # Python dependencies
└── .dockerignore           # Docker build exclusions
```

## Requirements / Prerequisites

- **Python 3.9+** and pip
- **FFmpeg** (verify with `ffmpeg -version`)
- **Google API access** (set `GOOGLE_API_KEY` environment variable)
- **Docker** (optional, for containerized deployment)

## 🚀 Super Easy Step-by-Step (For Beginners)

**Follow these steps exactly to get your AI video creator running:**

### Step 1: Download the Project
1. Go to: https://github.com/SamuelAngarita/ai-video-creator
2. Click the green **"Code"** button
3. Click **"Download ZIP"**
4. Extract the ZIP file to your desktop

### Step 2: Install Docker
1. Go to: https://www.docker.com/products/docker-desktop
2. Download Docker Desktop for your computer
3. Install it and restart your computer
4. Open Docker Desktop and wait for it to start

### Step 3: Get Your Google API Key
1. Go to: https://aistudio.google.com/app/apikey
2. Click **"Create API Key"**
3. Copy the key (starts with "AIza...")
4. Keep this key safe - you'll need it in Step 5

### Step 4: Set Up Your API Key
**On Windows:**
1. Double-click `setup.bat` in the project folder
2. Paste your API key when asked
3. Press Enter

**On Mac/Linux:**
1. Right-click in the project folder → "Open Terminal"
2. Type: `chmod +x setup.sh` and press Enter
3. Type: `./setup.sh` and press Enter
4. Paste your API key when asked

### Step 5: Edit Your Video Settings
1. Open the file `Code/.work/input.json` in any text editor
2. Replace the image URLs with your own image URLs
3. Replace the music URL with your own music URL
4. Save the file

### Step 6: Run the App
1. Open Terminal/Command Prompt in the project folder
2. Type: `docker-compose up --build`
3. Wait for it to finish (takes a few minutes first time)
4. Your video will be saved as `Code/.work/Final.mp4`

**That's it! You now have an AI-generated video! 🎉**

---

## Installation (Advanced Users)

```bash
# Clone the repository
git clone https://github.com/SamuelAngarita/ai-video-creator.git
cd ai-video-creator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

### API Key Setup (Required)

**Option 1: Use Setup Script (Recommended)**
```bash
# Linux/Mac
chmod +x setup.sh
./setup.sh

# Windows
setup.bat
```

**Option 2: Manual Setup**
```bash
# Linux/Mac
export GOOGLE_API_KEY=your_google_api_key_here

# Windows
set GOOGLE_API_KEY=your_google_api_key_here
```

**Option 3: Docker with Environment Variable**
```bash
docker run -e GOOGLE_API_KEY=your_key_here ai-video-creator
```

### Other Environment Variables (Optional)
```bash
FFMPEG_PATH=/usr/local/bin/ffmpeg  # If not in PATH
OUTPUT_DIR=Code/.work              # Working directory
```

### Input Configuration
Edit `Code/.work/input.json`:
```json
{
    "music": {
        "enabled": true,
        "url": "https://example.com/your-music.mp4"
    },
    "images": [
        {
            "url": "https://example.com/image1.jpg",
            "transition": "zoom_in"
        },
        {
            "url": "https://example.com/image2.jpg", 
            "transition": "pan"
        }
    ]
}
```

**Available transitions:** `zoom_in`, `zoom_out`, `pan`

## How to Run (Local)

### Quick Start (Windows)
```bash
# Just double-click the batch file!
run.bat
```

### Manual Commands
```bash
# 1. Set up your API key first
export GOOGLE_API_KEY=your_key_here  # Linux/Mac
# OR
set GOOGLE_API_KEY=your_key_here     # Windows

# 2. Run the application
python Code/main.py
```

**Output:** `Code/.work/Final.mp4` - your generated video!

## How to Run in Docker

### Quick Start (Recommended)
```bash
# 1. Set your API key
export GOOGLE_API_KEY=your_key_here  # Linux/Mac
set GOOGLE_API_KEY=your_key_here     # Windows

# 2. Build and run with docker-compose
docker-compose up --build

# Your video will appear in Code/.work/Final.mp4
```

### Manual Docker Commands
```bash
# Build the image
docker build -t ai-video-creator .

# Run with volume mounting (to access output files)
docker run --rm -it \
  -v "$PWD/Code/.work:/app/Code/.work" \
  -e GOOGLE_API_KEY=your_key_here \
  ai-video-creator
```

### Using Your Own Input File
```bash
# Method 1: Edit the existing file
nano Code/.work/input.json

# Method 2: Mount your custom input
docker run --rm -it \
  -v "$PWD/my-custom-input.json:/app/Code/.work/input.json" \
  -v "$PWD/Code/.work:/app/Code/.work" \
  -e GOOGLE_API_KEY=your_key_here \
  ai-video-creator
```

### Docker Compose with Custom Input
```yaml
# In docker-compose.yml, add:
volumes:
  - ./Code/.work:/app/Code/.work
  - ./my-input.json:/app/Code/.work/input.json:ro  # Optional custom input
```

## Tools & Services

### FFmpeg
- **Purpose:** Video normalization, concatenation, and audio mixing
- **Usage:** Automatically detected in PATH
- **Fallback:** Creates dummy videos when AI generation fails

### Google GenAI/Veo
- **Purpose:** AI video generation from static images
- **Credentials:** Set via `GOOGLE_API_KEY` environment variable
- **Rate Limits:** Automatically falls back to dummy videos when quota exceeded
- **Models:** Uses `veo-3.1-fast-generate-preview`

## Pipelines / Workflows

1. **Asset Download** → Downloads images and music from URLs
2. **AI Generation** → Creates animated videos using Google Veo API
3. **Normalization** → Ensures consistent video properties (1920x1080, 30fps, yuv420p)
4. **Concatenation** → Combines all video clips into single merged video
5. **Music Mixing** → Adds background music to final video

**Logs:** All output goes to console with `[info]`, `[ok]`, `[warn]` prefixes.

## Troubleshooting

### FFmpeg Issues
```bash
# Check if FFmpeg is installed
ffmpeg -version

# Install FFmpeg (Ubuntu/Debian)
sudo apt update && sudo apt install ffmpeg

# Install FFmpeg (macOS)
brew install ffmpeg
```

### Google API Issues
```bash
# Check API key
echo $GOOGLE_API_KEY

# Test API access
python -c "from google import genai; print('API key valid')"
```

### Docker Issues
```bash
# Check Docker is running
docker --version

# Rebuild if code changes
docker-compose up --build --force-recreate

# Check container logs
docker logs ai-video-creator
```

### Video Processing Issues
- **Concat failures:** System automatically falls back to re-encoding
- **Missing audio:** Silent audio is automatically injected
- **Format mismatches:** All clips are normalized before concatenation

## Known Issues / Bugs

- **API Quota Limits:** Google Veo has rate limits; system creates dummy videos as fallback
- **Large File Downloads:** Music files are streamed to handle large sizes efficiently
- **Windows Paths:** Use forward slashes in JSON URLs for cross-platform compatibility
- **Memory Usage:** Large video files may require sufficient RAM during processing

## Acknowledgments / Credits

- **Google Veo API** for AI video generation capabilities
- **FFmpeg** for robust video processing and concatenation
- **Python community** for excellent libraries (requests, Pillow, pathlib)

---

**Maintainer:** Samuel Angarita  
**Repository:** https://github.com/SamuelAngarita/ai-video-creator  
**License:** MIT

For issues and contributions, please open an issue on GitHub.