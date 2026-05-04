# Frontend-Backend Communication Analysis (v2)

## Overview
The frontend (React) and backend (FastAPI) v2 folders have a well-structured setup for API communication. Here's the detailed analysis:

---

## ✅ What's Working Correctly

### Backend Setup
- **FastAPI Framework**: Properly configured with Uvicorn server
- **CORS Enabled**: `allow_origins=["*"]` configured in `CORSMiddleware`
- **API Routes**: Three well-defined endpoints:
  - `GET /api/top-stocks` - Returns top performing stocks with OHLC data
  - `GET /api/watchlist` - Returns watchlist stocks with OHLC data
  - `GET /api/stock/{symbol}` - Returns detailed OHLC data for specific stock
  - `GET /api/health` - Health check endpoint
- **Response Models**: Pydantic models properly defined:
  - `TopStocksResponse` - Contains `top_stocks` and `ohlc_data`
  - `WatchlistResponse` - Contains `watchlist` and `ohlc_data`
  - `StockDetail` - Contains symbol, company_name, and data array

### Frontend Setup
- **API Service Layer**: Centralized API calls in `src/services/api.js`
- **Data Fetching Hook**: Custom `useStockData` hook for state management
- **Component Structure**: Proper React component hierarchy
- **Data Flow**: Correct prop passing from App → StockList/StockChart

### API Communication Flow
```
Frontend (http://localhost:3000)
    ↓
API Service (api.js uses fetch)
    ↓
API_BASE_URL: http://localhost:5000/api
    ↓
Backend (http://localhost:5000)
    ↓
FastAPI Routes
    ↓
Stock Data Response (JSON)
```

---

## ⚠️ Issues & Missing Configuration

### 1. **Missing setupProxy.js for Development**
**Status**: ❌ File doesn't exist  
**Impact**: During development, frontend runs on `localhost:3000` but tries to reach backend on `localhost:5000`, which requires CORS handling

**Current Setup**:
- Frontend uses absolute URLs: `http://localhost:5000/api`
- CORS is enabled on backend, so it should work

**Recommendation**: Create `setupProxy.js` for cleaner development experience

---

### 2. **Missing Environment Variable Documentation**
**Status**: ⚠️ Incomplete configuration  
**Issue**: Frontend has `process.env.REACT_APP_API_URL` but no `.env.local` file provided

**Current Behavior**:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
```

**Missing**: 
- No `.env.local` or `.env` file in frontend_v2
- No documentation on production URL setup
- Unclear how to override API endpoint

---

### 3. **No Backend .env File**
**Status**: ⚠️ Incomplete configuration  
**Issue**: Backend uses `python-dotenv` but no `.env` file provided

**Current Defaults** (from main.py):
```python
host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", 5000))
debug = os.getenv("DEBUG", "False").lower() == "true"
```

**Missing**: No way to configure these without creating `.env`

---

### 4. **Response Data Structure Mismatch Risk**
**Status**: ✓ Looks correct but verify

The frontend expects:
```javascript
data.top_stocks  // Array of StockPerformance
data.ohlc_data   // Object with symbol keys -> Array of OHLC
```

Backend provides:
```python
{
    "top_stocks": [...],
    "ohlc_data": {...},
    "fetched_at": "ISO datetime"
}
```

✅ **This matches correctly**

---

### 5. **Error Handling in Frontend**
**Status**: ✓ Partially implemented

**Good**:
- API service has try/catch blocks
- useStockData hook catches errors
- Error state displayed in App.jsx

**Could Improve**:
- No retry logic for failed API calls
- No timeout handling
- No distinction between network errors vs API errors

---

### 6. **Loading States**
**Status**: ✓ Properly implemented

Frontend handles:
- `loadingTop` and `loadingWatchlist` states
- Loading spinners in StockList
- Disabled refresh button during loading

---

## 📋 Data Flow Verification

### Request Chain: Top Stocks
```
1. App.jsx mounts → useStockData hook runs → loadTopStocks() called
2. api.js: fetchTopStocks(limit=50, delay=0.7)
3. Frontend: GET http://localhost:5000/api/top-stocks?limit=50&delay=0.7
4. Backend: StockFetcher.fetch_top_stocks(limit=50, delay=0.7)
5. Response: TopStocksResponse model returned as JSON
6. Frontend: Sets topStocks and ohlcDataTop state
7. Render: StockList displays stocks, StockChart displays OHLC data
```

✅ **This flow is correct**

---

### Request Chain: Watchlist
```
1. App.jsx mounts → useStockData hook runs → loadWatchlist() called
2. api.js: fetchWatchlist(delay=0.5)
3. Frontend: GET http://localhost:5000/api/watchlist?delay=0.5
4. Backend: StockFetcher.fetch_watchlist(delay=0.5)
5. Response: WatchlistResponse model returned as JSON
6. Frontend: Sets watchlist and ohlcDataWatchlist state
7. Render: StockList displays stocks, StockChart displays OHLC data
```

✅ **This flow is correct**

---

## 🚀 Setup & Startup Instructions

### Backend Setup
```bash
cd backend_v2
pip install -r requirements.txt
python main.py
```
Runs on: http://localhost:5000

### Frontend Setup
```bash
cd frontend_v2
npm install
npm start
```
Runs on: http://localhost:3000

### Both Running Together
Once both are running:
1. Frontend accessible at: http://localhost:3000
2. Backend API at: http://localhost:5000/api
3. API docs at: http://localhost:5000/docs (Swagger UI)

---

## 🔧 Recommended Improvements

### Priority 1: Environment Configuration
1. Create `backend_v2/.env`:
```env
HOST=0.0.0.0
PORT=5000
DEBUG=False
```

2. Create `frontend_v2/.env.local`:
```env
REACT_APP_API_URL=http://localhost:5000/api
```

3. Create `frontend_v2/.env.production`:
```env
REACT_APP_API_URL=https://your-production-api.com/api
```

### Priority 2: Development Proxy Setup
Create `frontend_v2/src/setupProxy.js`:
```javascript
const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:5000',
      changeOrigin: true,
      pathRewrite: {
        '^/api': '/api',
      },
    })
  );
};
```

Then update `api.js`:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';
```

### Priority 3: Add Timeout & Retry Logic
Update `frontend_v2/src/services/api.js` to include timeouts:
```javascript
const DEFAULT_TIMEOUT = 30000; // 30 seconds

const fetchWithTimeout = (url, timeout = DEFAULT_TIMEOUT) => {
  return Promise.race([
    fetch(url),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error('API request timeout')), timeout)
    ),
  ]);
};
```

---

## ✨ Current Status Summary

| Component | Status | Issues |
|-----------|--------|--------|
| Backend API Endpoints | ✅ Working | None |
| Frontend Data Fetching | ✅ Working | Missing proxy setup |
| CORS Configuration | ✅ Enabled | Too permissive for production |
| Environment Variables | ⚠️ Partial | Missing .env files |
| Error Handling | ⚠️ Basic | No retry/timeout logic |
| Loading States | ✅ Good | None |
| Data Models | ✅ Correct | None |
| Component Structure | ✅ Good | None |

---

## 🎯 Next Steps

1. ✅ **Verify both servers are running** on correct ports
2. ✅ **Test API endpoints** using `http://localhost:5000/docs`
3. ⚠️ **Create environment files** (.env for backend, .env.local for frontend)
4. ⚠️ **Set up dev proxy** for cleaner development
5. ⚠️ **Add error handling** and retry logic
6. ⚠️ **Test in production** with actual API URLs

