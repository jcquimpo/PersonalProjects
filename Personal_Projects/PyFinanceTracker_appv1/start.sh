#!/bin/bash

# Start Stock Dashboard with Python Backend

echo ""
echo "========================================"
echo "  Stock Dashboard - Starting Servers"
echo "========================================"
echo ""

# Check and install frontend dependencies
if [ ! -d "frontend_v2/node_modules" ]; then
    echo "Installing frontend dependencies..."
    cd frontend_v2
    npm install
    cd ..
fi

# Check and setup Python environment
if [ ! -d "backend_v2/venv" ]; then
    echo "Setting up Python virtual environment..."
    cd backend_v2
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
else
    echo "Python environment already exists"
fi

# Start backend in background
echo "Starting Python backend server (port 5000)..."
cd backend_v2
source venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

sleep 2

# Start frontend
echo "Starting frontend server (port 3000)..."
cd frontend_v2
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "Servers are starting..."
echo "Backend (Python): http://localhost:5000"
echo "Frontend (React): http://localhost:3000"
echo "========================================"
echo ""
echo "PIDs: Backend=$BACKEND_PID, Frontend=$FRONTEND_PID"
echo "To stop: kill $BACKEND_PID $FRONTEND_PID"

# Wait for both processes
wait
