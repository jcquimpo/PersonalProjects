# Frontend-Backend Connection Troubleshooting Guide

## 🔴 Current Error: "API Disconnected" + "Request timeout after 60000ms"

**Issue**: Frontend shows "API Disconnected" badge and times out waiting for watchlist data.

---

## 🚀 Quick Fix (Try This First!)

### Step 1: Verify Backend is Running
```powershell
# In a terminal, go to backend directory
cd PyFinanceTracker_APP/backend_v2

# Start the backend
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
```

### Step 2: Test Backend Health
In a **separate terminal**, test the health endpoint:
```powershell
curl http://localhost:5000/api/health
```

Expected response:
```json
{"status": "ok", "message": "Stock Dashboard API is running"}
```

### Step 3: Verify Frontend Can Reach Backend
Check the browser console (F12 → Console tab) for messages like:
- `[REQUEST] http://localhost:3000/api/health` ✅ Good
- `[HEALTH CHECK] {status: "ok", ...}` ✅ Good
- `[HEALTH CHECK FAILED]` ❌ Problem

### Step 4: Use Quick Endpoint
Try the faster endpoint first:
```powershell
curl http://localhost:5000/api/quick-watchlist
```

This should respond in 3-5 seconds instead of 30+.

### Step 5: Update Frontend to Use Quick Endpoint

Edit [frontend_v2/src/hooks/useStockData.js](frontend_v2/src/hooks/useStockData.js):
```javascript
const loadWatchlist = async (delay = 0.5) => {
  setLoadingWatchlist(true);
  setError(null);
  try {
    // Try quick endpoint first
    const data = await api.fetchWatchlist(delay);  // Change to quick-watchlist
    setWatchlist(data.watchlist || []);
    setOhlcDataWatchlist(data.ohlc_data || {});
  } catch (err) {
    setError(err.message);
    console.error('Failed to load watchlist:', err);
  } finally {
    setLoadingWatchlist(false);
  }
};
```

---

## 🔍 Detailed Troubleshooting

### Issue: "API Disconnected" Badge (Red)

**Cause**: Health check endpoint is failing.

**Debug Steps**:

1. **Check backend is actually running**
   ```powershell
   # Check if port 5000 is listening
   netstat -ano | findstr :5000
   ```

2. **Check health endpoint directly**
   ```powershell
   curl -v http://localhost:5000/api/health
   ```

3. **Check browser console**
   - Open DevTools (F12)
   - Go to Console tab
   - Look for `[HEALTH CHECK]` messages
   - If you see `[HEALTH CHECK FAILED]`, note the error message

4. **Check proxy is working**
   - In Console, try:
     ```javascript
     fetch('/api/health').then(r => r.json()).then(console.log)
     ```
   - This tests if proxy middleware is working

### Issue: "Request timeout after 60000ms" (Old Behavior)

**Old Timeout**: Was 60 seconds (too long)
**New Timeout**: 20 seconds (better)
**Best Practice**: Use quick endpoints (3-5 seconds)

**Solution**: 
- Frontend timeout reduced from 60s → 20s
- Add exponential backoff retry
- Use `/quick-watchlist` endpoint instead of `/watchlist`

### Issue: Backend Very Slow (Taking 30+ seconds)

**Causes**:
1. **yfinance API is slow** - Normal during market hours
2. **Too many symbols being fetched** - Default was 30, now 15
3. **Rate limiting** - Yahoo Finance throttling requests
4. **Network latency** - Check internet connection

**Solutions**:

**Option 1: Use Quick Endpoints**
```bash
# Returns in 3-5 seconds (no OHLC data)
curl http://localhost:5000/api/quick-watchlist

# Load OHLC separately later
curl "http://localhost:5000/api/stock/AAPL?period=7d"
```

**Option 2: Reduce Symbol Limit**
```bash
curl "http://localhost:5000/api/top-stocks?limit=5&delay=0.5"
```

**Option 3: Increase Delays Between Requests**
```bash
curl "http://localhost:5000/api/top-stocks?limit=20&delay=1.5"
```

---

## 🧪 Connection Testing Checklist

### ✅ Backend Health
- [ ] `python main.py` starts without errors
- [ ] `curl http://localhost:5000/api/health` returns 200 OK
- [ ] Backend console shows no errors

### ✅ Proxy Configuration
- [ ] `npm start` in frontend_v2 runs without errors
- [ ] Frontend loads at http://localhost:3000
- [ ] Browser opens without CORS errors

### ✅ API Connectivity
- [ ] `curl http://localhost:5000/api/quick-watchlist` returns data
- [ ] Frontend console shows `[HEALTH CHECK]` messages
- [ ] API status badge shows green ✅

### ✅ Data Fetching
- [ ] `/quick-watchlist` endpoint returns in < 10 seconds
- [ ] `/watchlist` endpoint returns in < 30 seconds
- [ ] Charts display properly when data loads

---

## 📊 Full Connection Flow

### When Everything Works:

```
User Loads App (localhost:3000)
         ↓
React App Mounts
         ↓
Health Check (5s timeout)
  GET /api/health
         ↓
setupProxy.js Routes to localhost:5000
         ↓
Backend /api/health Responds
         ↓
Load Watchlist & Top Stocks in Parallel
  - GET /api/quick-watchlist (5s)
  - GET /api/top-stocks (10s)
         ↓
Both Complete → Display Data ✅
```

### When API Disconnected (What's Happening Now):

```
User Loads App
         ↓
Health Check Request
  GET /api/health
         ↓
setupProxy.js Tries to Route
  → Cannot reach localhost:5000
         ↓
Request Times Out (5s)
         ↓
Health Status = "error"
         ↓
Badge Shows "API Disconnected" ❌
```

---

## 🛠️ Configuration Files to Check

### [frontend_v2/src/setupProxy.js](frontend_v2/src/setupProxy.js)
Should route `/api` to `http://localhost:5000`:
```javascript
target: 'http://localhost:5000',
changeOrigin: true,
```

### [frontend_v2/.env.local](frontend_v2/.env.local)
Should have:
```
REACT_APP_API_URL=/api
```

### [backend_v2/.env](backend_v2/.env)
Should have:
```
HOST=0.0.0.0
PORT=5000
DEBUG=False
```

### [backend_v2/app/main.py](backend_v2/app/main.py)
Should have CORS enabled:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📝 API Endpoints Reference

### Status Endpoints (Fast)
- `GET /api/health` - Health check (5s timeout)
- `GET /api/diagnostic` - Full diagnostic tests

### Quick Data Endpoints (3-5 seconds)
- `GET /api/quick-watchlist?delay=0.2` - Watchlist without OHLC
- `GET /api/quick-top-stocks?limit=10&delay=0.3` - Top stocks without OHLC

### Full Data Endpoints (10-30 seconds)
- `GET /api/watchlist?delay=0.5` - Watchlist with OHLC data
- `GET /api/top-stocks?limit=50&delay=0.7` - Top stocks with OHLC data

### Individual Stock Endpoints
- `GET /api/stock/AAPL?period=7d` - Single stock OHLC data
- `GET /api/stock/AAPL?period=1mo` - Monthly data

### Cache Management
- `POST /api/reset-cache` - Clear failed symbols cache

---

## 🐛 Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| "API Disconnected" | Backend not running | Run `python main.py` |
| "Request timeout" | Backend too slow | Use `/quick-watchlist` |
| CORS error | Proxy not working | Check setupProxy.js |
| Empty data arrays | yfinance failing | Check `/api/diagnostic` |
| "Cannot GET /api/health" | Backend crashed | Check backend logs |
| Proxy error in console | http-proxy-middleware missing | Run `npm install` |

---

## 🆘 Step-by-Step Debug Process

### If "API Disconnected":

1. **Backend Check**
   ```powershell
   # Stop any running backend
   # Terminal: Press Ctrl+C
   
   # Start fresh
   cd backend_v2
   python main.py
   ```

2. **Port Check**
   ```powershell
   netstat -ano | findstr :5000
   # If port in use, kill process or use different port
   ```

3. **Direct Connection Test**
   ```powershell
   curl http://localhost:5000/api/health
   ```

4. **Frontend Check**
   - Open http://localhost:3000
   - Press F12 (DevTools)
   - Go to Console tab
   - Look for network errors

5. **Proxy Check**
   ```javascript
   // In browser console:
   fetch('/api/health').then(r => r.json()).then(console.log)
   ```

6. **Restart Everything**
   ```powershell
   # Stop frontend (Ctrl+C)
   # Stop backend (Ctrl+C)
   # Clear cache
   cd backend_v2 && npm install
   cd ../../frontend_v2 && npm install
   # Restart both
   ```

### If Timeout:

1. **Check Backend Logs**
   - Look for error messages
   - Check if yfinance is responding

2. **Try Quick Endpoint**
   ```powershell
   curl http://localhost:5000/api/quick-watchlist
   ```

3. **Reduce Timeout**
   - Already done: reduced from 60s → 20s
   - Can further reduce to 15s if needed

4. **Check Network**
   ```powershell
   ping yahoo.com
   # If fails, internet issue
   ```

---

## ✨ Changes Made to Fix This

### Frontend Changes
- ✅ Reduced timeout from 60s → 20s
- ✅ Added exponential backoff retry (500ms, 1s, 2s)
- ✅ Added periodic health checks (every 30s)
- ✅ Added console logging for debugging
- ✅ Shorter health check timeout (5s)

### Backend Changes
- ✅ Reduced default symbols from 30 → 15
- ✅ Added `/quick-watchlist` endpoint
- ✅ Added `/quick-top-stocks` endpoint
- ✅ Enhanced DEBUG logging throughout
- ✅ Added `/diagnostic` endpoint

### Configuration Changes
- ✅ CORS enabled properly
- ✅ Proxy middleware configured
- ✅ Environment files created

---

## 📞 Quick Commands Reference

```bash
# Check backend health
curl http://localhost:5000/api/health

# Get quick watchlist (3-5s)
curl http://localhost:5000/api/quick-watchlist

# Get full watchlist (10-30s)
curl http://localhost:5000/api/watchlist

# Run diagnostics
curl http://localhost:5000/api/diagnostic

# Clear cache
curl -X POST http://localhost:5000/api/reset-cache

# Get one stock
curl "http://localhost:5000/api/stock/AAPL?period=7d"
```

---

## 📌 Remember

- **Backend must be running** on port 5000
- **Frontend runs** on port 3000
- **Proxy** connects them automatically
- **Use quick endpoints** for faster responses
- **Check browser console** (F12) for detailed errors
- **Check backend terminal** for server-side errors

🎉 Once connected, you'll see green API badge and data loading!

