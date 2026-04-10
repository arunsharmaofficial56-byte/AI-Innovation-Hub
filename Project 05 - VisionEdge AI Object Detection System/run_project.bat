@echo off
echo ===================================================
echo   AI Object Detection System - Startup Script
echo ===================================================

echo [1/4] Checking Python dependencies...
cd backend
pip install -r requirements.txt

echo [2/4] Checking Frontend dependencies...
cd ../frontend
call npm install

echo [3/4] Starting Backend Server (Flask)...
cd ../backend
start cmd /k "python app.py"

echo [4/4] Starting Frontend Server (Vite)...
cd ../frontend
start cmd /k "npm run dev"

echo ===================================================
echo   System is starting! 
echo   - Backend: http://localhost:5000
echo   - Frontend: http://localhost:3000
echo ===================================================
pause
