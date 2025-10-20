# read.py
# Samuel Angarita
# English: Asset download module for images and music files with validation and error handling
# Español: Módulo de descarga de assets para archivos de imágenes y música con validación y manejo de errores

from io import BytesIO
from pathlib import Path
import requests
from PIL import Image

from config import workdir                                                   

# User agent string for HTTP requests to identify our application
# Cadena de agente de usuario para solicitudes HTTP para identificar nuestra aplicación
USER_AGENT = "ai-video-creator/1.0"

# Helper function to perform HTTP GET requests with error handling and custom user agent
# Función auxiliar para realizar solicitudes HTTP GET con manejo de errores y agente de usuario personalizado
def _http_get(url: str, timeout=30) -> bytes:
    # Generic HTTP GET function with error handling and user agent
    # Función genérica HTTP GET con manejo de errores y agente de usuario
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    resp.raise_for_status()
    return resp.content

# Downloads and validates an image from URL, converts to JPEG format and saves to work directory
# Descarga y valida una imagen desde URL, convierte a formato JPEG y guarda en directorio de trabajo
def download_image(url: str, index: int) -> Path:
    """Download an image and verify it. Saved as downloaded_image{index}.jpg in workdir."""
    # Download and validate image from URL, convert to JPEG format
    # Descargar y validar imagen desde URL, convertir a formato JPEG
    data = _http_get(url, timeout=60)
    img = Image.open(BytesIO(data))
    # Ensure image is RGB for JPEG compatibility
    # Asegurar que la imagen sea RGB para compatibilidad JPEG
    img = img.convert("RGB")  # ensure jpg-compatible
    out = workdir / f"downloaded_image{index}.jpg"                            
    # Save with high quality JPEG compression
    # Guardar con compresión JPEG de alta calidad
    img.save(out, format="JPEG", quality=92)
    print(f"[ok] image saved: {out}")
    return out

# Downloads music or video file from URL using streaming for large files and saves to work directory
# Descarga archivo de música o video desde URL usando streaming para archivos grandes y guarda en directorio de trabajo
def download_song(url: str) -> Path:
    """Download music/video file to workdir as downloaded_music.mp4 (streamed)."""
    # Download music/video file using streaming for large files
    # Descargar archivo de música/video usando streaming para archivos grandes
    out = workdir / "downloaded_music.mp4"                                   
    with requests.get(url, stream=True, headers={"User-Agent": USER_AGENT}, timeout=60) as r:
        r.raise_for_status()
        # Stream download in chunks to handle large files efficiently
        # Descarga por streaming en fragmentos para manejar archivos grandes eficientemente
        with open(out, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 256):
                if chunk:
                    f.write(chunk)
    print(f"[ok] music saved: {out}")
    return out