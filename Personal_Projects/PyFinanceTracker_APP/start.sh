#!/bin/bash

# Start Stock Dashboard

echo ""
echo "========================================"
echo "  Stock Dashboard - Starting Servers"
echo "========================================"
echo ""

# Check and install frontend dependencies
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Check and install backend dependencies
if [ ! -d "backend/node_modules" ]; then
    echo "Installing backend dependencies..."
    cd backend
    npm install
    cd ..
fi

# Start backend in background
echo "Starting backend server (port 5000)..."
cd backend
npm start &
BACKEND_PID=$!
cd ..

sleep 2

# Start frontend
echo "Starting frontend server (port 3000)..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "Servers are starting..."
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo "========================================"
echo ""

# Wait for both processes
wait
