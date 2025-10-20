# main.py
import json
from config import PROJECT_ROOT, workdir 
from read import download_image, download_song
from google_api import calling_veo
from prompt import get_prompt
from combine import ensure_ffmpeg_available, create_txt, combine_videos, add_music

def main():
    # Read input.json FROM Code/.work instead of Code/
    with open(workdir / "input.json", "r", encoding="utf-8") as f:          #################################################################################
        data = json.load(f)

    for i, img in enumerate(data["images"]):
        download_image(img["url"], i+1)  # +1 so it starts at 1,...
        print(f"IMAGE NUMER {i+1} HAS BEEN DOWNLOADED!!!!!!!!!!!!!!!")

    download_song(data["music"]["url"])
    print("SONG DOWNLOADED!!!!!!!!!!!!!!!!!!!!!!!!111")

    # google_api.py calling main
    # Start enumerate at 1 so index matches your filenames (downloaded_image1.jpg, AIvideo1.mp4, ...)
    for y, tran in enumerate(data["images"], start=1):                       #################################################################################
        try:
            # Use workdir for image path, not a hard-coded ".work"
            result = calling_veo(                                            #################################################################################
                get_prompt(tran["transition"]),
                str(workdir / f"downloaded_image{y}.jpg"),                   #################################################################################
                y
            )
            print(f"[demo] success: {result}")
        except (TimeoutError, RuntimeError, SystemExit) as e:
            # Friendly, short messages only (no secrets, no long traces).
            print(f"[demo] error: {e}")

    # Imagine AI videos have been downloaded as AIvideo1.mp4, AIvideo2.mp4, ...

    print("=== Pipeline start ===")

    ensure_ffmpeg_available()

    print("[info] Creating list file...")
    create_txt(len(data["images"]))  # example: builds mylist for N files AIvideo1/2/3.mp4

    print("[info] Combining videos...")
    combine_videos()

    print("[info] Adding music onto merged video...")
    add_music()

    print("=== Pipeline end ===")

if __name__ == "__main__":
    main()


