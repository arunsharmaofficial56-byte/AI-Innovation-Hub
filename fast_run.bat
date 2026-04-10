@echo off
echo [1/3] Starting Backend...
start cmd /k "cd backend && python drive.py"
timeout /t 5

echo [2/3] Starting Dashboard...
start cmd /k "cd dashboard && npm run dev -- --port 3000"
timeout /t 10

echo [3/3] Starting Demo Client...
start cmd /k "cd backend && python demo_client.py"

echo All systems starting! Check the dashboard at http://localhost:3000
pause
