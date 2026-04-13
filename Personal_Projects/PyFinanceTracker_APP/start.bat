@echo off
REM Start Stock Dashboard

echo.
echo ========================================
echo   Stock Dashboard - Starting Servers
echo ========================================
echo.

REM Check if node_modules exist in both directories
if not exist "frontend\node_modules" (
    echo Installing frontend dependencies...
    cd frontend
    call npm install
    cd ..
)

if not exist "backend\node_modules" (
    echo Installing backend dependencies...
    cd backend
    call npm install
    cd ..
)

REM Start backend in a new window
echo Starting backend server (port 5000)...
start "Stock Dashboard Backend" cmd /k "cd backend && npm start"
timeout /t 3 /nobreak

REM Start frontend in a new window
echo Starting frontend server (port 3000)...
start "Stock Dashboard Frontend" cmd /k "cd frontend && call npm start"

echo.
echo ========================================
echo Servers are starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo ========================================
echo.
