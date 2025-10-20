#prompt.py
def get_prompt(transition:str)-> str:

    if transition == "zoom_in":
        return "Animate this still image with a smooth camera zoom-in from 100% to 130% over 4 seconds at 24 fps. Keep the main subject centered; use ease-in-out timing and subtle motion blur. Preserve original color and detail; do not add or remove elements or text. Maintain aspect ratio; scale and crop minimally to 1920x1080 to avoid black bars. Export clean MP4 (H.264), no audio."
    elif transition == "zoom_out":
        return "Animate this still image with a smooth camera zoom-out from 120% to 100% over 4 seconds at 24 fps. Keep the main subject centered; use ease-in-out timing and subtle motion blur. Preserve original color and detail; do not add or remove elements or text. Maintain aspect ratio; scale and crop minimally to 1920x1080 to avoid black bars. Export clean MP4 (H.264), no audio."
    elif transition == "pan":
        return "Animate this still image with a smooth left-to-right pan moving ~12% of the frame width over 4 seconds at 24 fps. Keep the main subject centered; use ease-in-out timing and subtle motion blur. Preserve original color and detail; do not add or remove elements or text. Maintain aspect ratio; scale and crop minimally to 1920x1080 to avoid black bars. Export clean MP4 (H.264), no audio."
    else:
        # Terminates the program with a non-zero exit code and prints the message
        raise SystemExit(f"Error: unknown command '{transition}'. Allowed: zoom_in, zoom_out, pan")
    


# -------- tiny demo main ------------------------------------------------------
def main():
    
    print(get_prompt("zoom_in"))


if __name__ == "__main__":
    main()

    


    
