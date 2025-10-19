# main.py
import json
from config import PROJECT_ROOT, workdir 
from read import download_image, download_song

def main():
    with open(PROJECT_ROOT / "input.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for i, img in enumerate(data["images"]):
        download_image(img["url"], i)

    download_song(data["music"]["url"])

if __name__ == "__main__":
    main()


    
