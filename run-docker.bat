@echo off
REM AI Video Creator - Docker Run Script
REM Samuel Angarita

echo Starting AI Video Creator with Docker...
echo.

REM Set your API key
REM IMPORTANT: Replace 'your_google_api_key_here' with your actual API key
set GOOGLE_API_KEY=your_google_api_key_here

REM Stop any running containers
docker-compose down

REM Run with Docker
docker-compose up

echo.
echo Press any key to exit...
pause >nul
