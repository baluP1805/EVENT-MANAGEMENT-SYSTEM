@echo off
echo ========================================
echo College EMS - Installation Script
echo ========================================
echo.

:: Check Python installation
echo [1/3] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo Python is installed!
echo.

:: Create virtual environment
echo [2/3] Creating virtual environment...
cd backend
if exist "venv\" (
    echo Virtual environment already exists. Skipping...
) else (
    python -m venv venv
    echo Virtual environment created!
)
echo.

:: Install dependencies
echo [3/3] Installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip setuptools wheel
rem Try to install binary wheels first (faster, avoids building native deps)
python -m pip install --only-binary=:all: -r ..\requirements.txt || (
    echo "Binary wheel install failed, falling back to source builds"
    python -m pip install -r ..\requirements.txt
)
echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure MongoDB is installed and running
echo 2. Copy .env.example to .env and configure it
echo 3. Run start.bat to start the application
echo.
deactivate
cd ..
pause
