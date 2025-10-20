@echo off
REM AI Video Creator - Docker Run Script
REM Samuel Angarita

echo Starting AI Video Creator with Docker...
echo.

REM Set your API key
set GOOGLE_API_KEY=AIzaSyAN3wwudY6f480lldD2CRvRMA9OSZeWzkk

REM Stop any running containers
docker-compose down

REM Run with Docker
docker-compose up

echo.
echo Press any key to exit...
pause >nul
