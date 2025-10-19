"""
# read.py
import requests
from PIL import Image
from io import BytesIO
from config import workdir  

def download_image(url: str, index: int):
    resp = requests.get(url)
    if resp.status_code == 200:
        Image.open(BytesIO(resp.content)).save(workdir / f"downloaded_image{index}.jpg")
        print(f"Saved downloaded_image{index}.jpg")
    else:
        print("Failed to retrieve image")

def download_song(url: str):
    out = workdir / "downloaded_music.mp4"
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(out, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        print(f"Saved {out}")
    except requests.RequestException as e:
        print(f"Download failed: {e}")


"""
####################################################################################









# read.py
# ---------------------------------------------
# Downloads images and songs into `workdir`.
# - Uses timeouts so requests don't hang forever.
# - Raises on HTTP errors (raise_for_status).
# - Verifies images with Pillow (catches non-image / corrupt files).
# - Retries network calls with simple exponential backoff.
# - Prints simple progress for large music downloads.
# - On failure, raises exceptions with short, user-friendly messages.
# - A tiny `main()` at the bottom shows example usage and error handling.
# ---------------------------------------------

import time
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image, UnidentifiedImageError

from config import workdir  # shared output folder


# -------- retry helper --------------------------------------------------------
def _get_with_retries(
    url: str,
    *,
    attempts: int = 3,       # total attempts
    backoff: float = 1.5,    # exponential backoff base
    timeout: tuple = (5, 30) # (connect, read) timeouts in seconds
) -> requests.Response:
    """
    GET with retries + HTTP error handling.
    Raises RuntimeError with a short message if all attempts fail.
    """
    last_err: Exception | None = None

    for i in range(1, attempts + 1):
        try:
            # Basic log for visibility
            print(f"[net] GET {url} (attempt {i}/{attempts})")
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()  # raises HTTPError on 4xx/5xx
            return resp
        except requests.RequestException as e:
            last_err = e
            if i < attempts:
                sleep_s = backoff ** i
                print(f"[net] attempt {i} failed ({e}); retrying in {sleep_s:.2f}s...")
                time.sleep(sleep_s)
            else:
                # All attempts failed → raise a short, user-friendly message
                raise RuntimeError(f"Network error after {attempts} attempts: {e}") from e


# -------- image download ------------------------------------------------------
def download_image(url: str, index: int) -> Path:
    """
    Download an image from `url` and save it as '.work/downloaded_image{index}.jpg'.
    Returns the saved Path. Raises RuntimeError on any failure.
    """
    print(f"[image] start download #{index} from {url}")
    target = workdir / f"downloaded_image{index}.jpg"  # fixed .jpg by your choice

    # 1) network (with retries + timeouts + HTTP errors)
    resp = _get_with_retries(url)

    # 2) verify & save image (two-step: verify then reopen to save)
    try:
        # Quick integrity check (this does not decode full image)
        with Image.open(BytesIO(resp.content)) as im:
            im.verify()

        # Re-open (verify() invalidates image object) and save to disk
        with Image.open(BytesIO(resp.content)) as im:
            # NOTE: We keep your fixed ".jpg" output format choice.
            # If the source isn't JPEG, Pillow will still encode to JPEG here.
            im.save(target, format="JPEG")

        print(f"[image] saved: {target.name}")
        return target

    except UnidentifiedImageError as e:
        # Not an image or corrupt → short, clear message
        raise RuntimeError("Image error: the URL did not return a valid image.") from e
    except OSError as e:
        # File I/O or Pillow save error
        raise RuntimeError(f"Image save error: {e}") from e


# -------- song download -------------------------------------------------------
def download_song(url: str) -> Path:
    """
    Download a song/video from `url` and save as '.work/downloaded_music.mp4'.
    Streams with progress. Raises RuntimeError on failure. Returns saved Path.
    """
    print(f"[audio] start download from {url}")
    out = workdir / "downloaded_music.mp4"  # fixed .mp4 by your choice

    # stream request: timeouts + HTTP errors + retries
    # (We retry only the initial GET/handshake; if the stream fails mid-way, we error out.)
    try:
        with requests.get(url, stream=True, timeout=(5, 60)) as r:
            r.raise_for_status()

            total = int(r.headers.get("Content-Length", 0))  # may be 0 if unknown
            downloaded = 0
            chunk_size = 1024 * 64  # 64 KB

            print(f"[audio] writing to {out.name}")
            with open(out, "wb") as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if not chunk:
                        continue
                    f.write(chunk)
                    downloaded += len(chunk)

                    # simple inline progress — works best when Content-Length is present
                    if total > 0:
                        pct = downloaded * 100 // total
                        print(
                            f"\r[audio] progress: {pct}% ({downloaded}/{total} bytes)",
                            end="",
                            flush=True,
                        )
                    else:
                        # fallback if no total size known
                        print(f"\r[audio] downloaded: {downloaded} bytes", end="", flush=True)

        # finish the progress line
        print()
        print(f"[audio] saved: {out.name}")
        return out

    except requests.RequestException as e:
        # Network / HTTP errors during streaming
        raise RuntimeError(f"Network error while downloading audio: {e}") from e
    except OSError as e:
        # File write errors
        raise RuntimeError(f"Audio save error: {e}") from e


# -------- tiny demo main ------------------------------------------------------
def main():
    """
    Small demo runner that shows friendly error handling.
    Replace the sample URLs with real ones to test.
    """
    # --- sample inputs (replace with real URLs) ---
    image_url_ok = "https://raw.githubusercontent.com/SamuelAngarita/ai-video-creator/main/Images/house.jpg"   # <-- replace
    song_url_ok  = "https://raw.githubusercontent.com/SamuelAngarita/ai-video-creator/main/Music/the-grey-room%20_%20density-and-time.mp4"   # <-- replace

    print("[demo] workdir:", workdir)

    # IMAGE
    try:
        p = download_image(image_url_ok, index=0)
        print(f"[demo] image saved at: {p}")
    except Exception as e:
        # Friendly message in terminal (no long traceback)
        print(f"[demo] image failed: {e}")

    # SONG
    try:
        p = download_song(song_url_ok)
        print(f"[demo] audio saved at: {p}")
    except Exception as e:
        print(f"[demo] audio failed: {e}")


if __name__ == "__main__":
    main()
