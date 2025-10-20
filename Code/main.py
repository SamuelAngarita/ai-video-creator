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
        print(f"Downloading image {i+1}/ Descargando imagen {i+1}")

    # Download background music from URL
    # Descargar música de fondo desde URL
    download_song(data["music"]["url"])
    print("Downloading music/ Descargando música")

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
            print(f"Video generated successfully/ Video generado exitosamente: {result}")
        except (TimeoutError, RuntimeError, SystemExit) as e:
            # Friendly, short messages only (no secrets, no long traces).
            # Mensajes amigables y cortos solamente (sin secretos, sin trazas largas).
            print(f"Video generation failed/ Fallo en generación de video: {e}")

    # Imagine AI videos have been downloaded as AIvideo1.mp4, AIvideo2.mp4, ...
    # Imaginar que los videos IA han sido descargados como AIvideo1.mp4, AIvideo2.mp4, ...

    print("Starting video processing/ Iniciando procesamiento de video")

    # Check if ffmpeg is available before proceeding
    # Verificar si ffmpeg está disponible antes de continuar
    ensure_ffmpeg_available()

    # Create concatenation list file for ffmpeg
    # Crear archivo de lista de concatenación para ffmpeg
    print("Creating video list/ Creando lista de videos")
    create_txt(len(data["images"]))  # example: builds mylist for N files AIvideo1/2/3.mp4

    # Concatenate all AI-generated videos into one merged video
    # Concatenar todos los videos generados por IA en un video fusionado
    print("Combining videos/ Combinando videos")
    combine_videos()

    # Add background music to the merged video (if enabled)
    # Agregar música de fondo al video fusionado (si está habilitado)
    if data["music"]["enabled"]:
        print("Adding background music/ Añadiendo música de fondo")
        add_music()
    else:
        print("Music disabled - finalizing video/ Música deshabilitada - finalizando video")
        # Rename merged.mp4 to Final.mp4 when music is disabled
        # Renombrar merged.mp4 a Final.mp4 cuando la música está deshabilitada
        import shutil
        from pathlib import Path
        merged_path = workdir / "merged.mp4"
        final_path = workdir / "Final.mp4"
        if merged_path.exists():
            shutil.move(str(merged_path), str(final_path))
            print(f"Final video saved/ Video final guardado: {final_path}")

    print("Video processing complete/ Procesamiento de video completado")

if __name__ == "__main__":
    main()
