# read.py
import time
from io import BytesIO
from pathlib import Path
import requests
from PIL import Image

from config import workdir                                                   #################################################################################

USER_AGENT = "ai-video-creator/1.0"

def _http_get(url: str, timeout=30) -> bytes:
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    resp.raise_for_status()
    return resp.content

def download_image(url: str, index: int) -> Path:
    """Download an image and verify it. Saved as downloaded_image{index}.jpg in workdir."""
    data = _http_get(url, timeout=60)
    img = Image.open(BytesIO(data))
    img = img.convert("RGB")  # ensure jpg-compatible
    out = workdir / f"downloaded_image{index}.jpg"                             #################################################################################
    img.save(out, format="JPEG", quality=92)
    print(f"[ok] image saved: {out}")
    return out

def download_song(url: str) -> Path:
    """Download music/video file to workdir as downloaded_music.mp4 (streamed)."""
    out = workdir / "downloaded_music.mp4"                                    #################################################################################
    with requests.get(url, stream=True, headers={"User-Agent": USER_AGENT}, timeout=60) as r:
        r.raise_for_status()
        with open(out, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 256):
                if chunk:
                    f.write(chunk)
    print(f"[ok] music saved: {out}")
    return out
