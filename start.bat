@echo off
echo ========================================
echo College Event Management System
echo ========================================
echo.

:: Check if virtual environment exists, if not create it
echo [1/3] Checking Python environment...
if not exist "backend\venv\" (
    echo Creating virtual environment...
    cd backend
    py -m venv venv
    cd ..
    echo Virtual environment created!
) else (
    echo Virtual environment exists!
)
echo.

:: Activate virtual environment and install dependencies
echo [2/3] Installing/Updating dependencies...
cd backend
call venv\Scripts\activate.bat
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install dependencies.
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

:: Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Creating .env from .env.example...
    copy ..\\.env.example .env >nul
    echo .env file created. Please configure SUPABASE_URL before running.
    echo.
)

:: Start the Flask application
echo [3/3] Starting Flask application...
echo.
echo ========================================
echo  Server starting on http://localhost:5000
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

py app.py

:: If server stops, deactivate virtual environment
deactivate
cd ..
echo.
echo Server stopped.
pause
