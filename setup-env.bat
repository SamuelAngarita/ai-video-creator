@echo off
REM setup-env.bat
REM Samuel Angarita
REM English: Create .env file for Docker environment variables
REM Español: Crear archivo .env para variables de entorno de Docker

echo AI Video Creator - Environment Setup
echo ===================================
echo.

REM Check if .env already exists
if exist .env (
    echo .env file already exists!
    echo Current content:
    type .env
    echo.
    set /p overwrite="Do you want to overwrite it? (y/n): "
    if /i not "%overwrite%"=="y" (
        echo Setup cancelled.
        pause
        exit /b
    )
)

echo Please enter your Google API key:
set /p api_key="GOOGLE_API_KEY: "

if "%api_key%"=="" (
    echo No API key provided. Creating .env with placeholder.
    echo GOOGLE_API_KEY=your_google_api_key_here > .env
    echo TZ=UTC >> .env
) else (
    echo GOOGLE_API_KEY=%api_key% > .env
    echo TZ=UTC >> .env
    echo .env file created successfully!
)

echo.
echo You can now run: docker-compose up --build
pause
