#!/bin/bash
# setup.sh
# Samuel Angarita
# English: Interactive setup script for AI Video Creator - helps you configure your Google API key
# Español: Script de configuración interactivo para Creador de Videos IA - te ayuda a configurar tu clave API de Google
# 
# How to use/ Cómo usar:
# 1. Make executable: chmod +x setup.sh
# 2. Run: ./setup.sh
# 3. Enter your Google API key when prompted
# 4. Run your app: python Code/main.py or docker-compose up --build

echo "AI Video Creator Setup/ Configuración de Creador de Videos IA"
echo "=============================================================="

# Check if API key is already set
if [ -n "$GOOGLE_API_KEY" ]; then
    echo "API key already set/ Clave API ya configurada"
    echo "Current key/ Clave actual: ${GOOGLE_API_KEY:0:10}..."
else
    echo "Please enter your Google API key/ Por favor ingrese su clave API de Google:"
    read -p "GOOGLE_API_KEY: " api_key
    
    if [ -n "$api_key" ]; then
        export GOOGLE_API_KEY="$api_key"
        echo "API key set for this session/ Clave API configurada para esta sesión"
        echo "To make it permanent, add this to your ~/.bashrc or ~/.zshrc:"
        echo "export GOOGLE_API_KEY=\"$api_key\""
    else
        echo "No API key provided. Google AI features will be disabled/ No se proporcionó clave API. Las funciones de Google AI estarán deshabilitadas"
    fi
fi

echo ""
echo "Setup complete! You can now run:/ ¡Configuración completada! Ahora puede ejecutar:"
echo "  Local: python Code/main.py"
echo "  Docker: docker-compose up --build"
