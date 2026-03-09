@echo off
echo Stopping College Event Management System...
echo.

:: Find and kill Python processes running on port 5000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
    echo Stopping process with PID: %%a
    taskkill /PID %%a /F >nul 2>&1
)

echo.
echo Server stopped.
pause
