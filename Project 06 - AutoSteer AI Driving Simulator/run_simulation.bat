@echo off
title AI Self-Driving Car Simulator (Project 06)
set BACKEND_PORT=4567

echo ===================================================
echo      AI SELF-DRIVING CAR SIMULATOR STARTUP
echo ===================================================

echo [1/4] Cleaning up previous sessions...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%BACKEND_PORT%') do taskkill /f /pid %%a >nul 2>&1
echo Done.

echo [2/4] Verifying Python Dependencies...
cd backend
pip install -r requirements.txt --quiet
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Dependency check failed. Please run: pip install -r backend/requirements.txt
    pause
    exit /b
)

echo [3/4] Starting Simulation Bridge (Port %BACKEND_PORT%)...
start "AI-CAR-BACKEND" /min cmd /c "python drive.py"
timeout /t 3 >nul

echo [4/4] Starting Dashboard (Vite)...
cd ../dashboard
start "AI-CAR-DASHBOARD" /min cmd /c "npm run dev -- --port 3000"

echo ===================================================
echo   SUCCESS: AI System is booting up!
echo   - Backend: http://localhost:%BACKEND_PORT%
echo   - Dashboard: http://localhost:3000
echo ===================================================
echo Windows will open in background. Check taskbar for cmd windows.
pause
