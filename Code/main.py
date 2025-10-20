# main.py
# Samuel Angarita
# English: Main pipeline orchestrator for AI video creation from images, prompts, and music
# Español: Orquestador principal del pipeline para creación de videos IA desde imágenes, prompts y música

import json
from config import PROJECT_ROOT, workdir
from read import download_image, download_song
from google_api import calling_veo
from prompt import get_prompt
from combine import ensure_ffmpeg_available, create_txt, combine_videos, add_music


# Main pipeline function that orchestrates the entire AI video creation process
# Función principal del pipeline que orquesta todo el proceso de creación de videos IA
def main():
    # Main pipeline function that orchestrates the entire video creation process
    # Función principal del pipeline que orquesta todo el proceso de creación de video
    # Read input.json FROM Code/.work instead of Code/
    # Leer input.json DESDE Code/.work en lugar de Code/
    with open(workdir / "input.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Download all images from URLs specified in input.json
    # Descargar todas las imágenes desde URLs especificadas en input.json
    for i, img in enumerate(data["images"]):
        download_image(img["url"], i+1)  # +1 so it starts at 1,...
        print(f"IMAGE NUMER {i+1} HAS BEEN DOWNLOADED!!!!!!!!!!!!!!!")

    # Download background music from URL
    # Descargar música de fondo desde URL
    download_song(data["music"]["url"])
    print("SONG DOWNLOADED!!!!!!!!!!!!!!!!!!!!!!!!111")

    # google_api.py calling main
    # Llamada principal de google_api.py
    # Start enumerate at 1 so index matches your filenames (downloaded_image1.jpg, AIvideo1.mp4, ...)
    # Comenzar enumeración en 1 para que el índice coincida con nombres de archivo (downloaded_image1.jpg, AIvideo1.mp4, ...)
    for y, tran in enumerate(data["images"], start=1):
        try:
            # Use workdir for image path, not a hard-coded ".work"
            # Usar workdir para ruta de imagen, no un ".work" codificado
            result = calling_veo(
                get_prompt(tran["transition"]),
                str(workdir / f"downloaded_image{y}.jpg"),
                y
            )
            print(f"[demo] success: {result}")
        except (TimeoutError, RuntimeError, SystemExit) as e:
            # Friendly, short messages only (no secrets, no long traces).
            # Mensajes amigables y cortos solamente (sin secretos, sin trazas largas).
            print(f"[demo] error: {e}")

    # Imagine AI videos have been downloaded as AIvideo1.mp4, AIvideo2.mp4, ...
    # Imaginar que los videos IA han sido descargados como AIvideo1.mp4, AIvideo2.mp4, ...

    print("=== Pipeline start ===")

    # Check if ffmpeg is available before proceeding
    # Verificar si ffmpeg está disponible antes de continuar
    ensure_ffmpeg_available()

    # Create concatenation list file for ffmpeg
    # Crear archivo de lista de concatenación para ffmpeg
    print("[info] Creating list file...")
    create_txt(len(data["images"]))  # example: builds mylist for N files AIvideo1/2/3.mp4

    # Concatenate all AI-generated videos into one merged video
    # Concatenar todos los videos generados por IA en un video fusionado
    print("[info] Combining videos...")
    combine_videos()

    # Add background music to the merged video
    # Agregar música de fondo al video fusionado
    print("[info] Adding music onto merged video...")
    add_music()

    print("=== Pipeline end ===")

if __name__ == "__main__":
    main()
