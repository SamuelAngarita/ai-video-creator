# google_api.py
import os
import time
from pathlib import Path
from config import workdir

# Simple API key setup - replace "TYPE_KEY_HERE" with your actual API key
API_KEY = "TYPE_KEY_HERE"  # Replace this with your actual Google API key

# Only import and initialize if API key is set
if API_KEY != "TYPE_KEY_HERE" and API_KEY:
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=API_KEY)
        print("[veo] API key loaded: yes")
    except ImportError:
        print("[veo] Google AI libraries not installed. Install with: pip install google-genai")
        client = None
else:
    print("[veo] API key not set - Google AI features disabled")
    client = None

def calling_veo(prompt: str, image_path: str, index: int) -> Path:
    """
    Generate AI video using Google Veo API.
    Returns the path to the generated video file.
    """
    if client is None:
        raise RuntimeError("Google API client not initialized. Set your API key in google_api.py")
    
    # Validate inputs
    p = Path(image_path)
    if not p.exists():
        raise FileNotFoundError(f"Image not found: {p}")

    try:
        print(f"[veo] Generating video for image {index}...")
        
        # Use the correct Veo API call based on your template
        operation = client.models.generate_videos(
            model="veo-3.1-fast-generate-preview",
            prompt=prompt,
            config=types.GenerateVideosConfig(
                aspect_ratio="16:9",
                resolution="720p",
            ),
        )

        # Wait for the video to be generated
        print(f"[veo] Waiting for video generation to complete...")
        while not operation.done:
            time.sleep(20)
            operation = client.operations.get(operation)
            print(f"[veo] Status: {operation}")

        # Check if video generation was successful
        if not operation.response.generated_videos:
            raise RuntimeError("No video was generated. This might be due to safety filters or content policy.")
        
        # Get the generated video
        generated_video = operation.response.generated_videos[0]
        
        # Download the video file
        print(f"[veo] Downloading video...")
        video_bytes = client.files.download(file=generated_video.video)
        
        # Save to workdir
        out = workdir / f"AIvideo{index}.mp4"
        with open(out, "wb") as f:
            f.write(video_bytes)

        print(f"[ok] Veo video saved: {out}")
        return out
        
    except Exception as e:
        print(f"[warn] Veo API call failed: {e}. Creating dummy video for testing...")
        # Fallback: create dummy video
        out = workdir / f"AIvideo{index}.mp4"
        import subprocess
        cmd = [
            "ffmpeg", "-y", "-f", "lavfi", "-i", "color=black:size=1920x1080:duration=2",
            "-c:v", "libx264", "-preset", "fast", str(out)
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"[ok] Dummy video created: {out}")
        return out
