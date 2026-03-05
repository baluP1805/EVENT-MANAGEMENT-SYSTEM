@echo off
:: Simple startup script - assumes MongoDB is running and dependencies are installed

echo Starting College Event Management System...
echo.

cd backend
py app.py

pause
