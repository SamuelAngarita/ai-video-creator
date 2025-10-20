# Use the official Python image as the base
FROM python:3.9-slim

# Install system dependencies including FFmpeg
# Instalar dependencias del sistema incluyendo FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copy the requirements file and install Python dependencies
# Copiar archivo de requirements e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your project files into the container
# Copiar archivos del proyecto al contenedor
COPY Code/ /app/Code/

# Create the work directory for temporary files
# Crear directorio de trabajo para archivos temporales
RUN mkdir -p /app/Code/.work

# Copy input.json from Code/.work directory
# Copiar input.json desde directorio Code/.work
COPY Code/.work/input.json /app/Code/.work/input.json

# Set the default command to run your main Python script
# Establecer comando por defecto para ejecutar tu script principal de Python
CMD ["python", "Code/main.py"]