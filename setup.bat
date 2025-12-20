@echo off
echo ===============================================
echo Vedantu Chat System - Setup
echo ===============================================
echo.

echo Checking if Python is installed...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ===============================================
echo Setup Complete!
echo ===============================================
echo.
echo To start the server, run:
echo   python app.py
echo.
echo Then open: http://localhost:5000
echo.
echo Demo Credentials:
echo   User ID: admin
echo   Password: password123
echo.
echo   User ID: agent
echo   Password: agent123
echo.
pause
