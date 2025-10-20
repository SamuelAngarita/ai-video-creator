# Creador de Video con IA

**Generación automatizada de videos MP4 a partir de imágenes fijas usando Google Veo AI y FFmpeg**

## Descripción general

AI Video Creator transforma imágenes estáticas en videos MP4 dinámicos usando Veo AI de Google para animaciones inteligentes y FFmpeg para procesamiento de video profesional.

## Características

* 🤖 **Animaciones con IA** usando la API de Google Veo (zoom, paneo, zoom-out)
* 🎬 **Procesamiento profesional de video** con normalización y concatenación mediante FFmpeg
* 🎵 **Integración de música de fondo** con mezcla de audio automática
* 🐳 **Listo para Docker** para un despliegue sencillo en cualquier plataforma
* 🔄 **Sistema de respaldo inteligente** con generación de video dummy cuando se alcanzan límites de la API
* 📁 **Entrada flexible** mediante configuración JSON
* 🌍 **Soporte bilingüe** (inglés/español) en comentarios del código

## Arquitectura de un vistazo

El sistema sigue una canalización robusta: descarga recursos → genera videos con IA → normaliza clips → concatena → añade música.

## Estructura de archivos

```
ai-video-creator/
├── Code/
│   ├── main.py              # Orquestador principal del pipeline
│   ├── config.py            # Configuración de rutas y preparación del directorio de trabajo
│   ├── read.py              # Descarga de recursos (imágenes, música) con validación
│   ├── google_api.py        # Integración con la API de Google Veo con fallback
│   ├── prompt.py            # Generación de prompts de animación para distintas transiciones
│   ├── combine.py           # Pipeline de video (normalizar, concatenar, mezclar)
│   └── .work/               # Directorio de trabajo para todos los artefactos
│       └── input.json       # Archivo de configuración (imágenes, música, transiciones)
├── Dockerfile               # Configuración del contenedor
├── docker-compose.yml       # Despliegue sencillo con Docker
├── requirements.txt         # Dependencias de Python
└── .dockerignore            # Exclusiones para la construcción de Docker
```

## Requisitos / Prerrequisitos

* **Python 3.9+** y pip
* **FFmpeg** (verifica con `ffmpeg -version`)
* **Acceso a la API de Google** (define la variable de entorno `GOOGLE_API_KEY`)
* **Docker** (opcional, para despliegue en contenedor)

## 🚀 Súper fácil paso a paso (para principiantes)

**Sigue estos pasos exactamente para poner a funcionar tu creador de videos con IA:**

### Paso 1: Descarga el proyecto

1. Ve a: [https://github.com/SamuelAngarita/ai-video-creator](https://github.com/SamuelAngarita/ai-video-creator)
2. Haz clic en el botón verde **"Code"**
3. Haz clic en **"Download ZIP"**
4. Extrae el archivo ZIP en tu escritorio

### Paso 2: Instala Docker

1. Ve a: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Descarga Docker Desktop para tu computadora
3. Instálalo y reinicia tu computadora
4. Abre Docker Desktop y espera a que inicie

### Paso 3: Obtén tu clave de API de Google

1. Ve a: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Haz clic en **"Create API Key"**
3. Copia la clave (empieza con "AIza...")
4. Guarda esta clave de forma segura: la necesitarás en el Paso 5

### Paso 4: Configura tu clave de API

**En Windows:**

1. Haz doble clic en `setup.bat` dentro de la carpeta del proyecto
2. Pega tu clave de API cuando se te solicite
3. Presiona Enter

**En Mac/Linux:**

1. Clic derecho en la carpeta del proyecto → "Open Terminal"
2. Escribe: `chmod +x setup.sh` y presiona Enter
3. Escribe: `./setup.sh` y presiona Enter
4. Pega tu clave de API cuando se te solicite

**⚠️ NOTA IMPORTANTE DE SEGURIDAD:**
- Nunca pongas tu clave de API real en los archivos `run.bat` o `run-docker.bat`
- Estos archivos contienen texto placeholder `your_google_api_key_here` - reemplázalo con tu clave real
- Tu clave de API solo debe configurarse como variable de entorno o a través de los scripts de configuración

### Paso 5: Edita la configuración de tu video

1. Abre el archivo `Code/.work/input.json` con cualquier editor de texto
2. Reemplaza las URLs de imágenes por tus propias URLs
3. Reemplaza la URL de la música por tu propia URL
4. Guarda el archivo

### Paso 6: Ejecuta la aplicación

**Opción A: Usando Docker (Recomendado)**
1. Abre la terminal/Command Prompt en la carpeta del proyecto
2. Escribe: `docker-compose up --build`
3. Espera a que termine (la primera vez puede tardar unos minutos)
4. Tu video se guardará como `Code/.work/Final.mp4`

**Opción B: Usando archivos batch (Windows)**
1. Edita `run.bat` y reemplaza `your_google_api_key_here` con tu clave de API real
2. Haz doble clic en `run.bat` para ejecutar localmente
3. Tu video se guardará como `Code/.work/Final.mp4`

**Opción C: Usando archivo batch de Docker (Windows)**
1. Edita `run-docker.bat` y reemplaza `your_google_api_key_here` con tu clave de API real
2. Haz doble clic en `run-docker.bat` para ejecutar con Docker
3. Tu video se guardará como `Code/.work/Final.mp4`

**¡Eso es todo! ¡Ya tienes un video generado con IA! 🎉**

---

## Instalación (usuarios avanzados)

```bash
# Clona el repositorio
git clone https://github.com/SamuelAngarita/ai-video-creator.git
cd ai-video-creator

# Crea un entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instala las dependencias
pip install -r requirements.txt
```

## Configuración

### Configuración de la clave API (obligatoria)

**Opción 1: Usar el script de configuración (recomendado)**

```bash
# Linux/Mac
chmod +x setup.sh
./setup.sh

# Windows
setup.bat
```

**Opción 2: Configuración manual**

```bash
# Linux/Mac
export GOOGLE_API_KEY=your_google_api_key_here

# Windows
set GOOGLE_API_KEY=your_google_api_key_here
```

**Opción 3: Docker con variable de entorno**

```bash
docker run -e GOOGLE_API_KEY=your_key_here ai-video-creator
```

### Otras variables de entorno (opcional)

```bash
FFMPEG_PATH=/usr/local/bin/ffmpeg  # Si no está en PATH
OUTPUT_DIR=Code/.work              # Directorio de trabajo
```

### Configuración de entrada

Edita `Code/.work/input.json`:

```json
{
    "music": {
        "enabled": true,
        "url": "https://example.com/your-music.mp4"
    },
    "images": [
        {
            "url": "https://example.com/image1.jpg",
            "transition": "zoom_in"
        },
        {
            "url": "https://example.com/image2.jpg", 
            "transition": "pan"
        }
    ]
}
```

**Transiciones disponibles:** `zoom_in`, `zoom_out`, `pan`

## Cómo ejecutar (local)

### Inicio rápido (Windows)
```bash
# 1. Primero, edita run.bat y reemplaza 'your_google_api_key_here' con tu clave de API real
# 2. ¡Luego haz doble clic en el archivo batch!
run.bat

# O para Docker:
run-docker.bat
```

### Comandos manuales
```bash
# 1. Configura primero tu clave API
export GOOGLE_API_KEY=your_key_here  # Linux/Mac
# O
set GOOGLE_API_KEY=your_key_here     # Windows

# 2. Ejecuta la aplicación
python Code/main.py
```

**Salida:** `Code/.work/Final.mp4` - ¡tu video generado!

## Cómo ejecutar en Docker

### Inicio rápido (recomendado)

```bash
# 1. Define tu clave API
export GOOGLE_API_KEY=your_key_here  # Linux/Mac
set GOOGLE_API_KEY=your_key_here     # Windows

# 2. Construye y ejecuta con docker-compose
docker-compose up --build

# Tu video aparecerá en Code/.work/Final.mp4
```

### Comandos manuales de Docker

```bash
# Construye la imagen
docker build -t ai-video-creator .

# Ejecuta con montaje de volumen (para acceder a los archivos de salida)
docker run --rm \
  -v "$PWD/Code/.work:/app/Code/.work" \
  -e GOOGLE_API_KEY=your_key_here \
  ai-video-creator
```

### Usar tu propio archivo de entrada

```bash
# Método 1: Edita el archivo existente
nano Code/.work/input.json

# Método 2: Monta tu entrada personalizada
docker run --rm \
  -v "$PWD/my-custom-input.json:/app/Code/.work/input.json" \
  -v "$PWD/Code/.work:/app/Code/.work" \
  -e GOOGLE_API_KEY=your_key_here \
  ai-video-creator
```

### Docker Compose con entrada personalizada

```yaml
# En docker-compose.yml, añade:
volumes:
  - ./Code/.work:/app/Code/.work
  - ./my-input.json:/app/Code/.work/input.json:ro  # Entrada personalizada opcional
```

## Herramientas y servicios

### FFmpeg

* **Propósito:** Normalización de video, concatenación y mezcla de audio
* **Uso:** Detectado automáticamente en PATH
* **Alternativa:** Crea videos dummy cuando falla la generación con IA

### Google GenAI/Veo

* **Propósito:** Generación de video con IA a partir de imágenes estáticas
* **Credenciales:** Se establecen mediante la variable de entorno `GOOGLE_API_KEY`
* **Límites de tasa:** Cambia automáticamente a videos dummy cuando se excede la cuota
* **Modelos:** Usa `veo-3.1-fast-generate-preview`

## Pipelines / Flujos de trabajo

1. **Descarga de recursos** → Descarga imágenes y música desde URLs
2. **Generación con IA** → Crea videos animados usando la API de Google Veo
3. **Normalización** → Asegura propiedades consistentes (1920x1080, 30fps, yuv420p)
4. **Concatenación** → Combina todos los clips en un único video
5. **Mezcla de música** → Añade música de fondo al video final

**Registros:** Todo el output va a la consola con prefijos `[info]`, `[ok]`, `[warn]`.

## Solución de problemas

### Problemas con FFmpeg

```bash
# Verifica si FFmpeg está instalado
ffmpeg -version

# Instalar FFmpeg (Ubuntu/Debian)
sudo apt update y sudo apt install ffmpeg

# Instalar FFmpeg (macOS)
brew install ffmpeg
```

### Problemas con la API de Google

```bash
# Verifica la clave API
echo $GOOGLE_API_KEY

# Prueba el acceso a la API
python -c "from google import genai; print('API key valid')"
```

### Problemas con Docker

```bash
# Verifica que Docker esté en ejecución
docker --version

# Reconstruye si cambia el código
docker-compose up --build --force-recreate

# Revisa los logs del contenedor
docker logs ai-video-creator
```

### Problemas de procesamiento de video

* **Fallos en concatenación:** El sistema cambia automáticamente a re-codificación
* **Audio faltante:** Se inyecta audio silencioso automáticamente
* **Incompatibilidades de formato:** Todos los clips se normalizan antes de concatenar

## Problemas conocidos / Errores

* **Límites de cuota de la API:** Google Veo tiene límites; el sistema crea videos dummy como respaldo
* **Descargas de archivos grandes:** Los archivos de música se transmiten para manejar grandes tamaños eficientemente
* **Rutas en Windows:** Usa barras diagonales (forward slashes) en URLs del JSON para compatibilidad multiplataforma
* **Uso de memoria:** Los archivos de video grandes pueden requerir RAM suficiente durante el proceso

## Agradecimientos / Créditos

* **API de Google Veo** por sus capacidades de generación de video con IA
* **FFmpeg** por su sólido procesamiento y concatenación de video
* **Comunidad de Python** por excelentes librerías (requests, Pillow, pathlib)

---

**Mantenedor:** Samuel Angarita
**Repositorio:** [https://github.com/SamuelAngarita/ai-video-creator](https://github.com/SamuelAngarita/ai-video-creator)
**Licencia:** MIT

Para incidencias y contribuciones, por favor abre un *issue* en GitHub.
