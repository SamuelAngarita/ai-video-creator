# combine.py
# Samuel Angarita
# English: Video processing pipeline for concatenating, normalizing, and adding music to AI-generated clips
# Español: Pipeline de procesamiento de video para concatenar, normalizar y agregar música a clips generados por IA

import subprocess
from pathlib import Path
import shutil
import re
import os

# ------------------------------
# Robust paths & folders
# ------------------------------
# Import centralized work directory from config module
# Importar directorio de trabajo centralizado desde el módulo de configuración
from config import workdir as WORKDIR                                       #################################################################################
# Ensure work directory exists before proceeding
# Asegurar que el directorio de trabajo existe antes de continuar
WORKDIR.mkdir(parents=True, exist_ok=True)

# Default artifact paths/names
# Rutas y nombres de artefactos por defecto
MYLIST_TXT   = WORKDIR / "mylist.txt"
MERGED_OUT   = WORKDIR / "merged.mp4"
FINAL_OUT    = WORKDIR / "Final.mp4"
MUSIC_IN     = WORKDIR / "downloaded_music.mp4"  # matches read.download_song()

# Normalization settings & outputs
# Configuraciones de normalización y salidas
TARGET_W     = 1920                                                             #################################################################################
TARGET_H     = 1080                                                             #################################################################################
TARGET_FPS   = 30                                                               #################################################################################
TARGET_AR    = 48000  # audio sample rate                                       #################################################################################
TARGET_AC    = 2      # audio channels                                          #################################################################################
NORM_DIR     = WORKDIR / "normalized"                                           #################################################################################
MYLIST_NORM  = WORKDIR / "mylist_normalized.txt"                                #################################################################################

def _run(cmd: list[str]):
    """Run a command and raise with a short, friendly message on failure."""
    # Execute subprocess command with error handling
    # Ejecutar comando de subproceso con manejo de errores
    try:
        res = subprocess.run(cmd, check=True, capture_output=True, text=True)   #################################################################################
        return res
    except subprocess.CalledProcessError as e:
        # Extract last error line for user-friendly message
        # Extraer última línea de error para mensaje amigable al usuario
        err = (e.stderr or "").strip().splitlines()[-1:]                        #################################################################################
        hint = f" ({err[0]})" if err else ""
        raise RuntimeError(f"Command failed: {' '.join(cmd[:3])}...{hint}") from e  #################################################################################

def ensure_ffmpeg_available():
    # Check if ffmpeg and ffprobe are available on system PATH
    # Verificar si ffmpeg y ffprobe están disponibles en el PATH del sistema
    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg not found on PATH. Please install ffmpeg.")
    if shutil.which("ffprobe") is None:                                         #################################################################################
        raise SystemExit("ffprobe not found on PATH. Please install ffmpeg.")   #################################################################################
    print("[ok] ffmpeg/ffprobe are available")                                  #################################################################################

# ------------------------------
# Preflight with ffprobe (NEW)
# ------------------------------
def _ffprobe_csv(path: Path, stream: str, fields: list[str]) -> str:            #################################################################################
    """
    Return a CSV line of requested fields for the first matching stream.
    Empty string means the stream is missing (e.g., no audio).
    """
    # Query specific stream properties using ffprobe
    # Consultar propiedades específicas del stream usando ffprobe
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", stream,              # e.g., v:0 or a:0
        "-show_entries", f"stream={','.join(fields)}",
        "-of", "csv=p=0:s=|",
        str(path),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return (res.stdout or "").strip()

def _needs_normalize(files: list[Path]) -> bool:                                #################################################################################
    """
    Decide if we must normalize BEFORE concat:
      - any file missing audio
      - any mismatch in v: codec/size/pix_fmt/SAR/fps
      - any mismatch in a: codec/sample_rate/channels
    """
    # Check if video files need normalization before concatenation
    # Verificar si los archivos de video necesitan normalización antes de la concatenación
    if not files:
        return True

    # Define video and audio properties to check for consistency
    # Definir propiedades de video y audio para verificar consistencia
    v_fields = ["codec_name", "width", "height", "pix_fmt", "sample_aspect_ratio", "avg_frame_rate"]  #################################################################################
    a_fields = ["codec_name", "sample_rate", "channels"]                                              #################################################################################

    # Get reference properties from first file
    # Obtener propiedades de referencia del primer archivo
    v_sig0 = _ffprobe_csv(files[0], "v:0", v_fields)                                                  #################################################################################
    a_sig0 = _ffprobe_csv(files[0], "a:0", a_fields)                                                  #################################################################################

    # If first clip has no audio, we will normalize to inject silent audio
    # Si el primer clip no tiene audio, normalizaremos para inyectar audio silencioso
    if not a_sig0:
        return True

    # Compare all files against reference properties
    # Comparar todos los archivos contra las propiedades de referencia
    for f in files[1:]:
        v_sig = _ffprobe_csv(f, "v:0", v_fields)
        a_sig = _ffprobe_csv(f, "a:0", a_fields)
        # any missing audio OR any difference in signatures -> normalize
        # cualquier audio faltante O cualquier diferencia en firmas -> normalizar
        if (not a_sig) or (v_sig != v_sig0) or (a_sig != a_sig0):                                     #################################################################################
            return True
    return False

# ------------------------------
# Helpers
# ------------------------------
def _parse_mylist(list_path: Path) -> list[Path]:                               #################################################################################
    # Parse ffmpeg concat list file to extract video file paths
    # Analizar archivo de lista de concatenación de ffmpeg para extraer rutas de archivos de video
    files = []
    if not list_path.exists():
        return files
    for line in list_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Match ffmpeg concat format: file 'path/to/video.mp4'
        # Coincidir formato de concatenación de ffmpeg: file 'ruta/al/video.mp4'
        m = re.match(r"file\s+'(.+)'", line)
        if m:
            files.append(Path(m.group(1)))
    return files

def _find_input_clips() -> list[Path]:
    # Scan work directory for AI-generated video files
    # Escanear directorio de trabajo para archivos de video generados por IA
    clips = []
    for p in WORKDIR.glob("AIvideo*.mp4"):
        # Extract numeric index from filename for proper ordering
        # Extraer índice numérico del nombre de archivo para ordenamiento correcto
        m = re.search(r"AIvideo(\d+)\.mp4$", p.name)
        if m:
            clips.append((int(m.group(1)), p))
    clips.sort(key=lambda t: t[0])
    return [p for _, p in clips]

def _write_list_for(files, list_path: Path):
    # Create ffmpeg concat list file with proper escaping
    # Crear archivo de lista de concatenación de ffmpeg con escape apropiado
    lines = []
    for f in files:
        if not f.exists():
            raise FileNotFoundError(f"Missing clip: {f}")
        # Escape single quotes for ffmpeg concat demuxer
        # Escapar comillas simples para el demuxer de concatenación de ffmpeg
        s = str(f).replace("'", r"'\''")
        lines.append(f"file '{s}'")
    list_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[ok] wrote list: {list_path}")

def _has_audio(src: Path) -> bool:                                              #################################################################################
    # Check if video file contains audio stream
    # Verificar si el archivo de video contiene stream de audio
    return bool(_ffprobe_csv(src, "a:0", ["codec_name"]))                        #################################################################################

# ------------------------------
# Public API
# ------------------------------
def create_txt(num: int):
    """
    Build concat list for ffmpeg demuxer:
    file 'AIvideo1.mp4'
    file 'AIvideo2.mp4'
    ...
    """
    # Create concatenation list file for ffmpeg
    # Crear archivo de lista de concatenación para ffmpeg
    if num <= 0:
        raise ValueError("Number of clips must be > 0")

    files = _find_input_clips()
    if len(files) != num:
        print(f"[warn] Found {len(files)} AI videos but expected {num}. Using existing videos only.")
        if not files:
            print("[error] No AI videos found. Creating dummy videos for testing...")
            # Create dummy videos for testing
            # Crear videos dummy para pruebas
            for i in range(1, num + 1):
                dummy_file = WORKDIR / f"AIvideo{i}.mp4"
                if not dummy_file.exists():
                    import subprocess
                    # Generate 2-second black video as placeholder
                    # Generar video negro de 2 segundos como marcador de posición
                    cmd = [
                        "ffmpeg", "-y", "-f", "lavfi", 
                        "-i", f"color=black:size=1920x1080:duration=2",
                        "-c:v", "libx264", "-preset", "fast", 
                        str(dummy_file)
                    ]
                    subprocess.run(cmd, check=True, capture_output=True)
                    print(f"[ok] Created dummy video: {dummy_file}")
            files = _find_input_clips()
    _write_list_for(files, MYLIST_TXT)

def _normalize_clips(src_files: list[Path]) -> list[Path]:
    """
    Normalize each clip to consistent canvas (WxH), CFR fps, SAR=1:1, yuv420p,
    and audio (AAC, 48kHz, stereo). Inject silent audio if the source has none.
    """
    # Normalize video clips to consistent format for reliable concatenation
    # Normalizar clips de video a formato consistente para concatenación confiable
    if not src_files:
        raise FileNotFoundError("No clips to normalize.")

    NORM_DIR.mkdir(parents=True, exist_ok=True)
    norm_files = []

    for i, src in enumerate(src_files, start=1):
        dst = NORM_DIR / f"clip{i:03d}.mp4"

        # Build video filter for scaling, padding, and format conversion
        # Construir filtro de video para escalado, relleno y conversión de formato
        vf = (
            f"scale={TARGET_W}:{TARGET_H}:force_original_aspect_ratio=decrease,"
            f"pad={TARGET_W}:{TARGET_H}:(ow-iw)/2:(oh-ih)/2:color=black,"
            f"setsar=1,fps={TARGET_FPS},format=yuv420p"
        )                                                                        #################################################################################

        if _has_audio(src):                                                      #################################################################################
            # Process video with existing audio
            # Procesar video con audio existente
            cmd = [
                "ffmpeg",
                "-y",
                "-hide_banner", "-loglevel", "error",
                "-i", str(src),
                "-vf", vf,
                "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-c:a", "aac", "-ar", str(TARGET_AR), "-ac", str(TARGET_AC),
                "-movflags", "+faststart",
                str(dst),
            ]
        else:
            # Inject silent audio for videos without audio
            # Inyectar audio silencioso para videos sin audio
            cmd = [
                "ffmpeg",
                "-y",
                "-hide_banner", "-loglevel", "error",
                "-i", str(src),
                "-f", "lavfi", "-i", f"anullsrc=r={TARGET_AR}:cl=stereo",       #################################################################################
                "-vf", vf,
                "-map", "0:v:0", "-map", "1:a:0",                                #################################################################################
                "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-c:a", "aac", "-ar", str(TARGET_AR), "-ac", str(TARGET_AC),
                "-shortest",
                "-movflags", "+faststart",
                str(dst),
            ]

        _run(cmd)
        norm_files.append(dst)
        print(f"[ok] normalized -> {dst}")

    _write_list_for(norm_files, MYLIST_NORM)
    return norm_files

def combine_videos():
    """
    Strategy:
      PRE-FLIGHT with ffprobe. If any mismatch → normalize path.
      Otherwise:
        1) Fast concat (demuxer, copy)
      If fast concat fails:
        2) Normalize then concat (copy)
      If that fails:
        3) Concat filter (re-encode once) over normalized clips
    """
    # Main video concatenation function with multiple fallback strategies
    # Función principal de concatenación de video con múltiples estrategias de respaldo
    # Build/validate list
    # Construir/validar lista
    if MYLIST_TXT.exists():
        files = _parse_mylist(MYLIST_TXT)                                       #################################################################################
    else:
        files = _find_input_clips()
        if files:
            _write_list_for(files, MYLIST_TXT)

    if not files:
        raise FileNotFoundError("No input clips found. Run the Veo step first.")

    # --- PRE-FLIGHT: skip fast path if streams differ ---
    # --- PRE-VUELO: omitir ruta rápida si los streams difieren ---
    if _needs_normalize(files):                                                  #################################################################################
        print("[info] Stream parameters differ (or audio missing). Normalizing first...") #################################################################################
        norm_files = _normalize_clips(files)                                     #################################################################################
        # Try fast concatenation after normalization
        # Intentar concatenación rápida después de normalización
        cmd_norm_copy = [
            "ffmpeg",
            "-y",
            "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0",
            "-i", str(MYLIST_NORM),
            "-c", "copy",
            str(MERGED_OUT),
        ]
        try:
            _run(cmd_norm_copy)
            print(f"[ok] concatenated normalized -> {MERGED_OUT}")
            return
        except RuntimeError:
            print("[warn] concat after normalization failed; using concat FILTER ...")
            # Fall through to concat filter on normalized clips
            # Continuar con filtro de concatenación en clips normalizados
            files = norm_files                                                  #################################################################################
    else:
        # --- 1) Fast path: concat demuxer (no re-encode) ---
        # --- 1) Ruta rápida: demuxer de concatenación (sin re-codificación) ---
        cmd_fast = [
            "ffmpeg",
            "-y",
            "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0",
            "-i", str(MYLIST_TXT),
            "-c", "copy",
            str(MERGED_OUT),
        ]
        try:
            _run(cmd_fast)
            print(f"[ok] concatenated -> {MERGED_OUT}")
            return
        except RuntimeError:
            print("[warn] fast concat failed; normalizing clips then retrying ...")
            files = _normalize_clips(files)                                      #################################################################################

    # --- 3) Last resort: concat filter (re-encode once) ---
    # --- 3) Último recurso: filtro de concatenación (re-codificar una vez) ---
    inputs = []
    for p in files:
        inputs += ["-i", str(p)]
    n = len(files)
    if n == 0:
        raise FileNotFoundError("No clips to concat.")

    # For normalized files we know 1v/1a per input
    # Para archivos normalizados sabemos 1v/1a por entrada
    filter_graph = "".join(f"[{i}:v:0][{i}:a:0]" for i in range(n)) + f"concat=n={n}:v=1:a=1[outv][outa]" #################################################################################

    cmd_concat_filter = [
        "ffmpeg",
        "-y",
        "-hide_banner", "-loglevel", "error",
        *inputs,
        "-filter_complex", filter_graph,
        "-map", "[outv]", "-map", "[outa]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-ar", str(TARGET_AR), "-ac", str(TARGET_AC),
        "-movflags", "+faststart",
        str(MERGED_OUT),
    ]
    _run(cmd_concat_filter)
    print(f"[ok] concatenated (concat filter) -> {MERGED_OUT}")

def add_music():
    """
    Replace audio on merged video using the downloaded music.
    If MUSIC_IN is missing, we just copy merged -> Final.mp4.
    """
    # Add background music to the concatenated video
    # Agregar música de fondo al video concatenado
    if not MERGED_OUT.exists():
        raise FileNotFoundError("merged.mp4 not found. Run combine_videos() first.")

    if not MUSIC_IN.exists():
        print("[warn] no downloaded music found; copying merged -> Final.mp4")
        WORKDIR.mkdir(parents=True, exist_ok=True)
        # Copy video without music if no music file available
        # Copiar video sin música si no hay archivo de música disponible
        FINAL_OUT.write_bytes(MERGED_OUT.read_bytes())
        print(f"[ok] Final written: {FINAL_OUT}")
        return

    # Replace video audio with music track
    # Reemplazar audio del video con pista de música
    cmd = [
        "ffmpeg",
        "-y",
        "-hide_banner", "-loglevel", "error",
        "-i", str(MERGED_OUT),
        "-i", str(MUSIC_IN),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        str(FINAL_OUT),
    ]
    _run(cmd)
    print(f"[ok] music added -> {FINAL_OUT}")