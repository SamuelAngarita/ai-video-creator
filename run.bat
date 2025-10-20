@echo off
REM AI Video Creator - Run Script
REM Samuel Angarita

echo Starting AI Video Creator...
echo.

REM Set your API key
REM IMPORTANT: Replace 'your_google_api_key_here' with your actual API key
set GOOGLE_API_KEY=your_google_api_key_here

REM Run the Python script
python -u "Code\main.py"

echo.
echo Press any key to exit...
pause >nul
