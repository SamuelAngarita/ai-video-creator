# config.py
# Samuel Angarita
# English: Central configuration module defining project paths and work directory
# Español: Módulo de configuración central que define rutas del proyecto y directorio de trabajo

from pathlib import Path

# Project root = the folder where THIS file lives
# Raíz del proyecto = la carpeta donde vive ESTE archivo
PROJECT_ROOT = Path(__file__).resolve().parent

# Centralized work folder under the Code directory
# Carpeta de trabajo centralizada bajo el directorio Code
workdir = PROJECT_ROOT / ".work"
# Create work directory if it doesn't exist
# Crear directorio de trabajo si no existe
workdir.mkdir(parents=True, exist_ok=True)  # create it once at import time