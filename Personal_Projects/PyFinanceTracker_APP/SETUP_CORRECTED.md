# Stock Dashboard - Corrected Setup Guide

## ❌ Problem Resolved
**Error**: `npm ERR! ENOENT: no such file or directory, open 'backend_v2/package.json'`

**Root Cause**: The old startup scripts (`start.bat` and `start.sh`) were configured for a Node.js backend, but the actual working backend is **`backend_v2`** — a Python/FastAPI application that doesn't need npm.

## ✅ Solution Implemented

### Architecture Overview
```
PyFinanceTracker_APP/
├── backend_v2/              ← Python FastAPI backend (ACTIVE)
│   ├── main.py             ← Entry point (runs on port 5000)
│   ├── requirements.txt     ← Python dependencies
│   └── app/
│       ├── main.py
│       ├── routes/
│       ├── services/
│       └── models/
├── frontend_v2/            ← React frontend (ACTIVE)
│   ├── package.json        ← Node.js dependencies
│   ├── src/
│   └── public/
├── start.bat              ← Updated startup script (Windows)
└── start.sh               ← Updated startup script (Linux/Mac)
```

### What Changed
1. **Updated `start.bat`** (Windows)
   - Now starts Python backend: `python main.py` instead of `npm start`
   - Creates Python virtual environment if needed
   - Uses `frontend_v2` instead of `frontend`
   - Installs Python dependencies from `requirements.txt`

2. **Updated `start.sh`** (Linux/macOS)
   - Same logic as Windows batch file
   - Uses `python3 -m venv` and `source venv/bin/activate`
   - Updated paths to `frontend_v2` and `backend_v2`

## 🚀 Quick Start

### Windows
```bash
cd PyFinanceTracker_APP
start.bat
```

This will:
1. Install frontend dependencies (if needed)
2. Create Python virtual environment (if needed)
3. Install Python dependencies
4. Start Python backend on **port 5000**
5. Start React frontend on **port 3000**

### Linux/macOS
```bash
cd PyFinanceTracker_APP
chmod +x start.sh
./start.sh
```

## 🔍 Verification

### Backend Running?
```
GET http://localhost:5000/api/health
GET http://localhost:5000/api/watchlist
```

### Frontend Running?
```
GET http://localhost:3000
```

Frontend automatically proxies `/api/*` requests to `http://localhost:5000/api/*`

## 📋 Technology Stack

### Backend (`backend_v2`)
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Data Source**: yfinance
- **Language**: Python 3.x
- **Port**: 5000

### Frontend (`frontend_v2`)
- **Framework**: React 18
- **Build Tool**: Create React App
- **Charting**: Recharts
- **Language**: JavaScript
- **Port**: 3000
- **Proxy**: Routes `/api` to backend

## ⚠️ Troubleshooting

### "Python not found"
- Ensure Python 3.x is installed: `python --version`
- On macOS/Linux, use `python3` instead

### "npm not found"
- Ensure Node.js is installed: `npm --version`
- Required only for frontend (v17+)

### "Port 5000/3000 already in use"
- Windows: `netstat -ano | findstr :5000`
- Linux/Mac: `lsof -i :5000`
- Kill the process or change `PORT` environment variable

### Import errors in Python
```bash
cd backend_v2
source venv/bin/activate  # On Windows: venv\Scripts\activate.bat
pip install -r requirements.txt
```

## 🔧 Manual Startup (if scripts don't work)

### Backend (Python)
```bash
cd backend_v2
python -m venv venv

# Windows
venv\Scripts\activate.bat
pip install -r requirements.txt
python main.py

# Linux/macOS
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Frontend (React)
```bash
cd frontend_v2
npm install
npm start
```

## 📝 Environment Variables

### Backend (`backend_v2/.env`)
```
HOST=0.0.0.0
PORT=5000
DEBUG=False
```

## ✨ Summary
- ✅ Removed reference to old Node.js backend
- ✅ Updated startup scripts to use Python backend
- ✅ Both scripts now use `frontend_v2` and `backend_v2`
- ✅ Proper virtual environment setup
- ✅ Clear port assignments (Backend: 5000, Frontend: 3000)
