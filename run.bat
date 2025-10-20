@echo off
REM AI Video Creator - Run Script
REM Samuel Angarita

echo Starting AI Video Creator...
echo.

REM Set your API key
set GOOGLE_API_KEY=AIzaSyAN3wwudY6f480lldD2CRvRMA9OSZeWzkk

REM Run the Python script
python -u "Code\main.py"

echo.
echo Press any key to exit...
pause >nul
