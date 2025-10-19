# config.py
from pathlib import Path

# Project root = the folder where THIS file lives
PROJECT_ROOT = Path(__file__).resolve().parent

# Centralized work folder under the project root
workdir = PROJECT_ROOT / ".work"
workdir.mkdir(parents=True, exist_ok=True)  # create it once at import time

