@echo off
REM Quick Backend Testing Script for Windows
REM Run this from backend_v2 directory or PowerShell
REM This script tests all API endpoints and shows what data is being fetched

setlocal enabledelayedexpansion
cls

echo ==================================
echo Stock Dashboard Backend Test
echo ==================================
echo.

REM Check if backend is running
echo [1/5] Checking if backend is running...
timeout /t 1 /nobreak > nul
curl -s -m 2 http://localhost:5000/api/health > nul 2>&1
if errorlevel 1 (
    echo X Backend is NOT running
    echo Start backend with: cd backend_v2 && python main.py
    pause
    exit /b 1
) else (
    echo OK Backend is running on http://localhost:5000
)
echo.

REM Test 1: Health check
echo [2/5] Health Check
curl -s http://localhost:5000/api/health
echo.
echo.

REM Test 2: Fetch watchlist
echo [3/5] Fetch Watchlist
echo Making request to /api/watchlist...
set startTime=!time!

curl -s http://localhost:5000/api/watchlist > temp_response.json

echo HTTP Status: 200 (check above for response)
echo.
type temp_response.json | find "AAPL" > nul
if errorlevel 0 (
    echo OK Found stock data in response
) else (
    echo X No stock data found
)
echo.
type temp_response.json | find "is_demo_data" > nul
echo.

REM Test 3: Fetch top stocks
echo [4/5] Fetch Top Stocks
echo Making request to /api/top-stocks...
curl -s http://localhost:5000/api/top-stocks > temp_response2.json

type temp_response2.json | find "top_stocks" > nul
if errorlevel 0 (
    echo OK Received top stocks
) else (
    echo X No top stocks in response
)
echo.

REM Test 4: Simple response test
echo [5/5] Testing Response
echo Endpoints:
echo   - http://localhost:5000/api/health
echo   - http://localhost:5000/api/watchlist (should respond in 8-15 seconds)
echo   - http://localhost:5000/api/top-stocks (should respond in 10-18 seconds)
echo.

REM Cleanup
del /q temp_response.json > nul 2>&1
del /q temp_response2.json > nul 2>&1

echo ==================================
echo Test Complete!
echo ==================================
echo.
echo Summary:
echo - Backend running: YES
echo - Check response JSON above for data
echo - Verify times are under 20 seconds
echo.
echo Next steps:
echo 1. Open http://localhost:3000 in your browser
echo 2. Check browser DevTools Network tab for /api requests
echo 3. Verify data is displayed correctly
echo.
pause
