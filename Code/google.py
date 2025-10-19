"""
import time
import os
from pathlib import Path
from google import genai
from google.genai import types

def calling_veo(prompt: str, image: str, index: int):
    # Set up API key (you'll need to get this from Google AI Studio)
    # Option 1: Set environment variable
    os.environ['GOOGLE_API_KEY'] = ''

    # Option 2: Set it directly when creating the client
    # client = genai.Client(api_key='your-api-key-here')

    # Initialize the client
    client = genai.Client()

    # Define paths
    input_image_path = image
    output_folder = ".work"
    output_filename = f"video{index}.mp4"  # <-- changed to use the provided index

    # Check if input image exists
    if not os.path.exists(input_image_path):
        print(f"Error: Input image {input_image_path} not found!")
        exit(1)

    print(f"Using input image: {input_image_path}")
    print("Generating drone-like zoom video with Google Veo API...")
    print("Note: You need to set up your Google API key first!")
    print("   1. Go to https://ai.google.dev/")
    print("   2. Get your API key")
    print("   3. Set it in this script or as GOOGLE_API_KEY environment variable")

    # Create the video generation operation with drone-like zoom effect
    try:
        operation = client.models.generate_videos(
            model="veo-3.1-fast-generate-preview",
            prompt=prompt,
            config=types.GenerateVideosConfig(
                negative_prompt="shaky camera, jerky movement, static shot, no movement, poor quality, blurry",
                aspect_ratio="16:9",  # Better for drone shots
                resolution="1080p",    # Higher quality for cinematic effect
            ),
        )

        print("Video generation started. This may take several minutes...")

        # Wait for the video generation to complete
        while not operation.done:
            time.sleep(30)  # Check every 30 seconds
            operation = client.operations.get(operation)
            print(f"Status: {operation.metadata}")

        print("Video generation completed!")

        # Download and save the generated video
        generated_video = operation.response.generated_videos[0]
        client.files.download(file=generated_video.video)

        # Ensure output directory exists
        os.makedirs(output_folder, exist_ok=True)

        # Save the video with the specified filename
        output_path = os.path.join(output_folder, output_filename)
        generated_video.video.save(output_path)

        print(f"Video successfully saved as: {output_path}")
        print(f"Full path: {os.path.abspath(output_path)}")

    except Exception as e:
        print(f"Error: {e}")
        print("\nSetup Instructions:")
        print("1. Go to https://ai.google.dev/")
        print("2. Sign in with your Google account")
        print("3. Create a new project or select existing one")
        print("4. Enable the Veo API")
        print("5. Generate an API key")
        print("6. Set the API key in this script by uncommenting and updating the genai.configure() line")
        print("   OR set it as an environment variable: GOOGLE_API_KEY=your-key-here")

        
"""















# veo_runner.py
# --------------------------------------------------------------------
# Google Veo video generation helper with safe error handling.
# Implements:
#  1) API key handling (fail fast, no env mutation in the function)
#  2) Input validation (image path exists, index non-negative, prompt non-empty)
#  3) Robust polling (20-minute timeout, exponential backoff, early error exit)
#  4) Defensive response checks (no assumptions about list fields)
#  5) Basic download/save checks
#  6) Raise exceptions with short messages; main() prints friendly output
#  7) Simple print-based logging (fine for small tools)
#  8) Retry wrapper for transient API failures
#  9) Don’t print secrets
# --------------------------------------------------------------------

import os
import time
from pathlib import Path

from google import genai
from google.genai import types


# ---- 1) API key handling (fail fast) ----------------------------------------
# Read the key once at import. If missing, exit with a clear message.
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise SystemExit("Missing GOOGLE_API_KEY. Set it in your environment before running.")

# Create the client explicitly with the API key (no env mutation inside functions).
client = genai.Client(api_key=API_KEY)


# ---- 2) Input validation -----------------------------------------------------
def _validate_inputs(prompt: str, image: str, index: int) -> None:
    """Fail early on bad inputs (clear, short messages)."""
    # Ensure input image exists (common user typo/path issue).
    img_path = Path(image)
    if not img_path.is_file():
        raise SystemExit(f"Input image not found: {img_path}")

    # Keep filenames reasonable: non-negative integer index.
    if not isinstance(index, int) or index < 0:
        raise SystemExit("Index must be a non-negative integer.")

    # Optional but recommended: prompt should not be empty/blank.
    if not isinstance(prompt, str) or not prompt.strip():
        raise SystemExit("Prompt must not be empty.")


# ---- 8) Transient error retry helper ----------------------------------------
def _retry(api_call, *, attempts: int = 3, backoff: float = 1.5):
    """
    Retry a callable a few times with exponential backoff.
    Keeps messages short; raises RuntimeError if all attempts fail.
    """
    last_err = None
    for i in range(1, attempts + 1):
        try:
            return api_call()
        except Exception as e:
            last_err = e
            if i < attempts:
                sleep_s = backoff ** i
                print(f"[veo] retry {i}/{attempts} after error: {e}; sleeping {sleep_s:.1f}s")
                time.sleep(sleep_s)
            else:
                raise RuntimeError(f"API call failed after {attempts} attempts: {e}") from e


# ---- 3) Robust operation polling (20 min timeout) ---------------------------
def _wait_for_operation(_client, operation, *, max_minutes: int = 20):
    """
    Poll the operation with exponential backoff, up to max_minutes.
    If the SDK exposes an error on the operation, stop early.
    """
    print("[veo] polling operation...")
    deadline = time.time() + max_minutes * 60
    delay = 5.0         # start at 5 seconds
    max_delay = 60.0    # cap delay at 60 seconds

    while not getattr(operation, "done", False):
        if time.time() > deadline:
            raise TimeoutError(f"Timed out after {max_minutes} minutes.")

        # If metadata exists, log it (often contains progress/state).
        meta = getattr(operation, "metadata", None)
        if meta:
            print(f"[veo] status: {meta}")

        time.sleep(delay)
        # Backoff up to max_delay
        delay = min(delay * 1.5, max_delay)

        # Refresh operation (SDK-specific pattern)
        operation = _client.operations.get(operation)

        # If the SDK exposes an error field/status, bail out early.
        if getattr(operation, "error", None):
            raise RuntimeError(f"Operation failed: {operation.error}")

    return operation


# ---- 4) Defensive response checks -------------------------------------------
def _extract_video_object(operation):
    """
    Carefully pull out the first generated video, checking each step.
    Avoids IndexError/AttributeError when responses are empty or partial.
    """
    resp = getattr(operation, "response", None)
    if not resp:
        raise RuntimeError("No response payload returned.")

    videos = getattr(resp, "generated_videos", None)
    if not videos or len(videos) == 0:
        raise RuntimeError("No generated videos in the response.")

    video_obj = videos[0]
    if not getattr(video_obj, "video", None):
        raise RuntimeError("Generated video object has no 'video' payload.")

    return video_obj


# ---- 5) Download + save with basic checks -----------------------------------
def _download_and_save_video(_client, video_obj, out_dir: Path, filename: str) -> Path:
    """
    Download and save the video. Keeps messages short; raises RuntimeError on failure.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / filename

    try:
        print("[veo] downloading result...")
        # Depending on SDK behavior: download may populate internal cache/temp.
        _client.files.download(file=video_obj.video)

        # If the SDK exposes a .save() helper on the object, use it:
        video_obj.video.save(str(out_path))

        print(f"[veo] saved: {out_path.resolve()}")
        return out_path
    except Exception as e:
        raise RuntimeError(f"Download/save failed: {e}") from e


# ---- Public function (your original entry point) -----------------------------
def calling_veo(prompt: str, image: str, index: int):
    """
    Generate a video using Google Veo (simple, commented version).
    Raises RuntimeError/TimeoutError/SystemExit with short messages on failure.
    """
    # Validate inputs first (clear errors before hitting the API).
    print("[veo] validating inputs...")
    _validate_inputs(prompt, image, index)

    # Fixed output folder and name (kept from your original logic).
    output_folder = Path(".work")
    output_filename = f"video{index}.mp4"

    print(f"[veo] using input image: {image}")
    print("[veo] starting video generation... (this can take a while)")

    # Create the operation (wrapped in a retry to smooth transient failures).
    operation = _retry(lambda: client.models.generate_videos(
        model="veo-3.1-fast-generate-preview",
        prompt=prompt,
        config=types.GenerateVideosConfig(
            negative_prompt="shaky camera, jerky movement, static shot, no movement, poor quality, blurry",
            aspect_ratio="16:9",  # similar to your original choices
            resolution="1080p",
        ),
    ))

    # Poll until done (20-minute cap, exponential backoff; early error on failure).
    operation = _wait_for_operation(client, operation, max_minutes=20)

    # Carefully extract the first generated video object.
    generated_video = _extract_video_object(operation)

    # Download and save to disk (basic checks).
    out_path = _download_and_save_video(client, generated_video, output_folder, output_filename)

    # Return the final saved path (useful to the caller).
    return out_path


# ---- 6 & 7) Simple demo main with friendly messages -------------------------
if __name__ == "__main__":
    # NOTE: Replace these with real values when testing.
    sample_prompt = "A smooth drone-like zoom over a coastal city at sunset, cinematic."
    sample_image = "input.jpg"  # must exist on disk
    sample_index = 0

    print("[demo] starting...")
    try:
        result = calling_veo(sample_prompt, sample_image, sample_index)
        print(f"[demo] success: {result}")
    except (TimeoutError, RuntimeError, SystemExit) as e:
        # Friendly, short messages only (no secrets, no long traces).
        print(f"[demo] error: {e}")


