# Quick Setup & Testing Guide

## Getting Started in 5 Minutes

### Prerequisites
- Python 3.8+ ([Download](https://www.python.org/))
- Node.js 16+ ([Download](https://nodejs.org/))
- A terminal (Command Prompt, PowerShell, or bash)

### Setup Steps

#### 1. Backend Setup
```bash
cd backend_v2
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. Frontend Setup
```bash
cd frontend_v2
npm install
```

### Running the Application

#### Option A: Quick Start Script
From `PyFinanceTracker_APP` directory:
```bash
# Windows
start.bat

# macOS/Linux
chmod +x start.sh
./start.sh
```

#### Option B: Manual (Two Terminals)

**Terminal 1 - Backend:**
```bash
cd backend_v2
# Activate venv if not already
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend_v2
npm start
```

### Access the App
- **UI**: http://localhost:3000
- **API Docs**: http://localhost:5000/docs

---

## Testing Checklist

### ✅ Backend Testing

#### 1. Health Check
```bash
curl http://localhost:5000/api/health
```
**Expected**: `{"status":"ok","message":"Stock API is running"}`

#### 2. Top Stocks
```bash
curl "http://localhost:5000/api/top-stocks?limit=50&delay=0.7"
```
**Expected**: JSON with top_stocks array and ohlc_data

#### 3. Watchlist
```bash
curl "http://localhost:5000/api/watchlist?delay=0.5"
```
**Expected**: JSON with watchlist array and ohlc_data

#### 4. Individual Stock
```bash
curl "http://localhost:5000/api/stock/AAPL?period=7d"
```
**Expected**: JSON with OHLC data for AAPL

#### 5. Check Logs
Look for in backend terminal:
- `Stock Dashboard Backend v2.0 running on http://localhost:5000`
- `Uvicorn running on 0.0.0.0:5000`

### ✅ Frontend Testing

#### 1. Page Loads
- Open http://localhost:3000
- Should see "Stock Dashboard" header
- Should see dark theme UI

#### 2. Sidebar Loads
- Verify "Top 5 Performers" tab is visible
- Verify "Watchlist" tab is visible
- Verify "Refresh" buttons exist

#### 3. Data Loads
- Wait 10-20 seconds for data to fetch
- Check if stocks appear in sidebar
- Look for green/red percentage changes

#### 4. Chart Displays
- Click on a stock in the sidebar
- Chart should appear on the right
- Should show "Closing Price Trend" and "OHLC Data"

#### 5. Tab Switching
- Click "Watchlist" tab
- Stocks should change
- Chart should update

#### 6. Refresh Function
- Click refresh button
- Stocks should reload
- Chart should update

### ✅ API Documentation

1. Visit http://localhost:5000/docs
2. Should see Swagger UI
3. Click each endpoint to view:
   - Request parameters
   - Response schema
   - Example values

### ✅ Console Checks

#### Frontend Console (F12)
No red errors should appear. May see:
- Yellow warnings are OK
- Network requests to `/api/top-stocks`, `/api/watchlist`, `/api/stock/SYMBOL`

#### Backend Console
Should show:
```
INFO:     Started server process
INFO:     Uvicorn running on 0.0.0.0:5000
INFO:     Application startup complete
```

---

## Testing Scenarios

### Scenario 1: Full Data Load Flow
1. Start both services
2. Open http://localhost:3000
3. Wait for stocks to load (10-20 seconds)
4. Verify 5 stocks appear
5. Click a stock
6. Verify chart loads with 7 days of data

### Scenario 2: Tab Switching
1. Start on "Top 5 Performers"
2. Note the stocks shown
3. Switch to "Watchlist"
4. Verify different stocks
5. Switch back to "Top 5"
6. Should be same as step 2

### Scenario 3: Refresh Data
1. Note current stock prices
2. Click refresh button
3. Wait for data (10-20 seconds)
4. Prices may change (depends on market)
5. Timestamps should update

### Scenario 4: API Direct Call
1. Open new terminal
2. Run: `curl "http://localhost:5000/api/top-stocks?limit=20&delay=0.5"`
3. Verify JSON response with top_stocks array
4. Each stock should have: symbol, company_name, percentage_change, current_price

---

## Common Issues & Solutions

### Issue: "Failed to fetch"
**Cause**: Backend not running or wrong URL
**Solution**:
1. Check backend is running: `http://localhost:5000`
2. Check .env file: `REACT_APP_API_URL=http://localhost:5000/api`

### Issue: No stocks appearing
**Cause**: Slow API or timeout
**Solution**:
1. Wait longer (can take 30+ seconds on first load)
2. Check backend logs for errors
3. Try smaller limit: `?limit=20&delay=0.5`

### Issue: "Module not found"
**Cause**: Missing dependencies
**Solution**:
```bash
# Backend
cd backend_v2 && pip install -r requirements.txt

# Frontend
cd frontend_v2 && npm install
```

### Issue: Port already in use
**Solution**:
```bash
# Change port in backend .env
PORT=5001

# Change frontend port (Windows)
set PORT=3001 && npm start

# Change frontend port (Mac/Linux)
PORT=3001 npm start
```

---

## Performance Metrics

### Expected Load Times
- **First load**: 15-30 seconds (API calls to yfinance)
- **Refresh**: 10-20 seconds
- **Chart render**: <1 second
- **UI interactions**: <100ms

### Network Calls
- Initial load makes ~6 API calls
- Each stock fetch: ~100-200ms
- Delays between calls are intentional (rate limiting)

---

## Architecture Validation

### ✅ Verify Unified Python Stack
```bash
# All backend code is Python
ls backend_v2/app/**/*.py
```

### ✅ Verify SPA Setup
- No page reloads when switching tabs
- No proxy configuration needed
- Direct API calls from frontend

### ✅ Verify Type Safety
Check `backend_v2/app/models/stock.py` for Pydantic models

### ✅ Verify Modular Structure
```
backend_v2/app/
├── models/       # Data models
├── services/     # Business logic
├── routes/       # API endpoints
└── utils/        # Utilities
```

---

## Next Steps

1. **Local Testing**: Complete all tests above
2. **API Testing**: Try different parameters
3. **UI Customization**: Modify colors in CSS files
4. **Add Features**: Extend API or frontend
5. **Deploy**: Ready for production deployment

---

## Support

**For debugging**:
1. Open browser DevTools (F12)
2. Check Network tab for API calls
3. Check Console for JavaScript errors
4. Check backend terminal for Python errors

**API Issues**:
1. Check http://localhost:5000/docs for endpoint details
2. Verify parameters match documentation
3. Try with curl to test without frontend

**Not Working?**
1. Verify all prerequisites installed
2. Delete venv and node_modules, reinstall
3. Restart both services
4. Try with fresh terminal windows
