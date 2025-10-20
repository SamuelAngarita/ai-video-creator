@echo off
REM setup.bat
REM Samuel Angarita
REM English: Interactive setup script for AI Video Creator (Windows) - helps you configure your Google API key
REM Español: Script de configuración interactivo para Creador de Videos IA (Windows) - te ayuda a configurar tu clave API de Google
REM 
REM How to use/ Cómo usar:
REM 1. Double-click setup.bat or run: setup.bat
REM 2. Enter your Google API key when prompted
REM 3. Run your app: python Code/main.py or docker-compose up --build

echo AI Video Creator Setup/ Configuración de Creador de Videos IA
echo ==============================================================

REM Check if API key is already set
if defined GOOGLE_API_KEY (
    echo API key already set/ Clave API ya configurada
    echo Current key/ Clave actual: %GOOGLE_API_KEY:~0,10%...
) else (
    echo Please enter your Google API key/ Por favor ingrese su clave API de Google:
    set /p api_key="GOOGLE_API_KEY: "
    
    if not "%api_key%"=="" (
        set GOOGLE_API_KEY=%api_key%
        echo API key set for this session/ Clave API configurada para esta sesión
        echo To make it permanent, add this to your system environment variables:
        echo GOOGLE_API_KEY=%api_key%
    ) else (
        echo No API key provided. Google AI features will be disabled/ No se proporcionó clave API. Las funciones de Google AI estarán deshabilitadas
    )
)

echo.
echo Setup complete! You can now run:/ ¡Configuración completada! Ahora puede ejecutar:
echo   Local: python Code/main.py
echo   Docker: docker-compose up --build
pause
