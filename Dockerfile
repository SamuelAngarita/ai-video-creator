# Use the official Python image as the base (updated to Python 3.12)
FROM python:3.12-slim

# Set environment variables for better Python performance
# Establecer variables de entorno para mejor rendimiento de Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies including FFmpeg and other utilities
# Instalar dependencias del sistema incluyendo FFmpeg y otras utilidades
RUN apt-get update && \
    apt-get install -y \
        ffmpeg \
        wget \
        curl \
        git \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/* \
        && apt-get autoremove -y

# Create app user for security
# Crear usuario de aplicación para seguridad
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set the working directory inside the container
# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copy requirements first for better Docker layer caching
# Copiar requirements primero para mejor caché de capas de Docker
COPY requirements.txt .

# Install Python dependencies with optimizations
# Instalar dependencias de Python con optimizaciones
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy your project files into the container
# Copiar archivos del proyecto al contenedor
COPY Code/ /app/Code/
COPY Images/ /app/Images/
COPY Music/ /app/Music/
COPY input.json /app/input.json
COPY README.md /app/README.md

# Create necessary directories and set permissions
# Crear directorios necesarios y establecer permisos
RUN mkdir -p /app/Code/.work /app/Code/.work/normalized && \
    chown -R appuser:appuser /app

# Switch to non-root user for security
# Cambiar a usuario no-root por seguridad
USER appuser

# Set the default command to run your main Python script
# Establecer comando por defecto para ejecutar tu script principal de Python
CMD ["python", "Code/main.py"]