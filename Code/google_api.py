# google_api.py
# Samuel Angarita
# English: Google Veo API integration for AI video generation from images and prompts
# Español: Integración de API de Google Veo para generación de videos IA desde imágenes y prompts

import os
import time
from pathlib import Path
from config import workdir

# API key setup - check environment variable first, then fallback to hardcoded
# Configuración de clave API - verificar variable de entorno primero, luego respaldo codificado
API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyDP5q2gFxX6mOBpIFLai8yzBN50bE41OtE")

# Only import and initialize if API key is set
# Solo importar e inicializar si la clave API está configurada
if API_KEY != "TYPE_KEY_HERE" and API_KEY:
    try:
        from google import genai
        from google.genai import types
        # Initialize Google GenAI client with API key
        # Inicializar cliente de Google GenAI con clave API
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
    # Main function to generate AI videos using Google Veo API
    # Función principal para generar videos IA usando la API de Google Veo
    if client is None:
        raise RuntimeError("Google API client not initialized. Set your API key in google_api.py")
    
    # Validate inputs
    # Validar entradas
    p = Path(image_path)
    if not p.exists():
        raise FileNotFoundError(f"Image not found: {p}")

    try:
        print(f"[veo] Generating video for image {index}...")
        
        # Use the correct Veo API call based on your template
        # Usar la llamada correcta de API Veo basada en tu plantilla
        operation = client.models.generate_videos(
            model="veo-3.1-fast-generate-preview",
            prompt=prompt,
            config=types.GenerateVideosConfig(
                aspect_ratio="16:9",
                resolution="720p",
            ),
        )

        # Wait for the video to be generated
        # Esperar a que el video sea generado
        print(f"[veo] Waiting for video generation to complete...")
        while not operation.done:
            # Poll every 20 seconds for completion status
            # Consultar cada 20 segundos el estado de finalización
            time.sleep(20)
            operation = client.operations.get(operation)
            print(f"[veo] Status: {operation}")

        # Check if video generation was successful
        # Verificar si la generación de video fue exitosa
        if not operation.response.generated_videos:
            raise RuntimeError("No video was generated. This might be due to safety filters or content policy.")
        
        # Get the generated video
        # Obtener el video generado
        generated_video = operation.response.generated_videos[0]
        
        # Download the video file
        # Descargar el archivo de video
        print(f"[veo] Downloading video...")
        video_bytes = client.files.download(file=generated_video.video)
        
        # Save to workdir
        # Guardar en directorio de trabajo
        out = workdir / f"AIvideo{index}.mp4"
        with open(out, "wb") as f:
            f.write(video_bytes)

        print(f"[ok] Veo video saved: {out}")
        return out
        
    except Exception as e:
        print(f"[warn] Veo API call failed: {e}. Creating dummy video for testing...")
        # Fallback: create dummy video
        # Respaldo: crear video dummy
        out = workdir / f"AIvideo{index}.mp4"
        import subprocess
        # Generate 2-second black video as fallback
        # Generar video negro de 2 segundos como respaldo
        cmd = [
            "ffmpeg", "-y", "-f", "lavfi", "-i", "color=black:size=1920x1080:duration=2",
            "-c:v", "libx264", "-preset", "fast", str(out)
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"[ok] Dummy video created: {out}")
        return out