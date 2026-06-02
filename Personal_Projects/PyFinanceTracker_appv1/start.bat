@echo off
REM Start Stock Dashboard with Python Backend

echo.
echo ========================================
echo   Stock Dashboard - Starting Servers
echo ========================================
echo.

REM Check if node_modules exist in frontend
if not exist "frontend_v2\node_modules" (
    echo Installing frontend dependencies...
    cd frontend_v2
    call npm install
    cd ..
)

REM Check if Python environment is set up
if not exist "backend_v2\venv" (
    echo Setting up Python virtual environment...
    cd backend_v2
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    cd ..
) else (
    echo Python environment already exists
)

REM Start Python backend in a new window
echo Starting Python backend server (port 5000)...
start "Stock Dashboard Backend" cmd /k "cd backend_v2 && venv\Scripts\activate.bat && python main.py"
timeout /t 3 /nobreak

REM Start frontend in a new window
echo Starting frontend server (port 3000)...
start "Stock Dashboard Frontend" cmd /k "cd frontend_v2 && call npm start"

echo.
echo ========================================
echo Servers are starting...
echo Backend (Python): http://localhost:5000
echo Frontend (React): http://localhost:3000
echo ========================================
echo.
