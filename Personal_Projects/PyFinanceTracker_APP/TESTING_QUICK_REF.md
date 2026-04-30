# Backend Testing Quick Reference Card

## 🚀 Quick Start (30 seconds)

### Option 1: Python Direct Test (RECOMMENDED)
```bash
cd backend_v2
python test_stock_fetcher.py
```
**What you'll see**: Colored output showing which tests pass/fail ✅ ✗

---

## 🌐 API Endpoints (For cURL Testing)

All endpoints return JSON. You can test with browser, cURL, or Postman.

### 1️⃣ Health Check
```bash
curl http://localhost:5000/api/health
```
**Response**: `{"status":"ok"}`

### 2️⃣ Fetch Watchlist
```bash
curl http://localhost:5000/api/watchlist
```
**Response**: 
```json
{
  "watchlist": [
    {"symbol": "AAPL", "percentage_change": 2.5, "current_price": 175.50},
    {"symbol": "MSFT", "percentage_change": 1.85, "current_price": 425.30},
    {"symbol": "GOOGL", "percentage_change": 3.42, "current_price": 140.20}
  ],
  "ohlc_data": {"AAPL": [...], "MSFT": [...], "GOOGL": [...]},
  "fetched_at": "2026-04-29T14:30:45.123456",
  "is_demo_data": false
}
```

### 3️⃣ Fetch Top Stocks
```bash
curl http://localhost:5000/api/top-stocks
```
**Response**: Similar to watchlist, but with top 5 performing stocks

---

## 🔍 What to Check

### ✅ Data Present
```
Look for: "symbol": "AAPL", "percentage_change": 2.5
Should NOT see: empty arrays [], null values, error messages
```

### ✅ Live vs Demo Data
```
is_demo_data: false  → Live data from Yahoo Finance ✅
is_demo_data: true   → Demo data (fallback, still valid) ⚠️
```

### ✅ Response Time
```
< 10 seconds   → Excellent ✅✅
10-15 seconds  → Good ✅
15-20 seconds  → Acceptable ✅
> 20 seconds   → Problem ❌
```

### ✅ Stock Data Quality
```
Look for:
- symbol: uppercase (AAPL, MSFT, etc.)
- company_name: full name (Apple Inc., Microsoft Corporation)
- percentage_change: number (positive or negative)
- current_price: positive number (not zero or negative)
- previous_close: positive number (close to current_price)
- ohlc_data: array with 7 dates, each with open/high/low/close
```

---

## 🛠️ Testing Methods Comparison

| Method | Speed | Difficulty | Shows Details |
|--------|-------|-----------|---------------|
| **Python test** | Fast | Easy | YES ✅ |
| **cURL** | Fast | Easy | Partial |
| **Browser** | Slow | Easy | NO |
| **Python REPL** | Medium | Medium | YES ✅ |

---

## 🐛 Common Issues & Fixes

### ❌ No data returned
**Check**:
1. Backend running? `curl http://localhost:5000/api/health`
2. Internet connected? `curl https://finance.yahoo.com`
3. Check logs: Look for errors in backend console

### ❌ Response time > 20 seconds
**Check**:
1. Logs for "Approaching timeout" message
2. Internet speed/latency
3. Try during off-peak hours (avoid market hours)

### ❌ `is_demo_data: true` always
**Means**: Live data fetching is failing  
**Try**:
1. Check backend logs for errors
2. Restart backend
3. Check if Yahoo Finance is accessible

### ❌ `curl: (7) Failed to connect`
**Means**: Backend not running  
**Fix**:
```bash
cd backend_v2
python main.py
```

### ❌ Python import errors
**Means**: Virtual environment not active  
**Fix**:
```bash
# Windows
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

---

## 📊 Response Size Guide

### Typical Response Sizes
```
Watchlist:  10-15 KB (3 stocks with OHLC)
Top Stocks: 12-20 KB (5 stocks with OHLC)
Total:      < 50 KB
```

### Check in Browser DevTools
1. F12 → Network tab
2. Look for `/api/watchlist` request
3. Check "Size" column
4. Should be 10-20 KB range

---

## 🎯 Real-World Testing Scenario

### Step 1: Start Backend
```bash
cd backend_v2
python main.py
```
Wait for: `Application startup complete`

### Step 2: Run Python Test
```bash
# New terminal/PowerShell
cd backend_v2
python test_stock_fetcher.py
```
Look for: ✅ (green checkmarks)

### Step 3: Test via Browser
1. Open `http://localhost:3000`
2. F12 → Network tab
3. Look for `/api` requests
4. Click on each request
5. Check Response size (10-20 KB range)

### Step 4: Watch Backend Logs
While browser loads, backend logs should show:
```
Fetching watchlist with 3 symbols...
[1/3] Fetching AAPL...
[1/3] AAPL: 2.15% change
... (2 more symbols)
Fetching OHLC data...
Watchlist fetch complete in 12.45s.
```

---

## 📝 Testing Checklist

Copy & paste this checklist:

```
BACKEND TESTING CHECKLIST
========================

[ ] Backend running? (python main.py)
[ ] Python test passes? (python test_stock_fetcher.py)
[ ] Health check works? (curl http://localhost:5000/api/health)
[ ] Watchlist returns data? (< 15 seconds)
[ ] Top stocks returns data? (< 18 seconds)
[ ] Data contains symbols? (AAPL, MSFT, GOOGL, etc.)
[ ] Data contains prices? (numbers, not null/zero)
[ ] Data contains percentage changes? (number, +/-)
[ ] OHLC data present? (7 days of data)
[ ] No error messages? (Check JSON response)
[ ] is_demo_data is false? (means live data ✅)
```

---

## 🔗 Related Files

- **Test Script**: `backend_v2/test_stock_fetcher.py` (comprehensive)
- **Test Script**: `backend_v2/test_quick.sh` or `test_quick.bat` (quick)
- **Testing Guide**: `BACKEND_TESTING_GUIDE.md` (detailed)
- **Timeout Refactoring**: `TIMEOUT_REFACTORING.md` (technical details)

---

## 💡 Pro Tips

### Monitor Requests in Real-Time
```bash
# Watch backend logs while testing
# Terminal 1: Start backend
cd backend_v2
python main.py

# Terminal 2: Run test
python test_stock_fetcher.py

# See live request logging in Terminal 1
```

### Test Individual Stocks
```bash
# In Python REPL
python
>>> from app.services.stock_fetcher import StockFetcher
>>> StockFetcher.get_stock_performance("AAPL")
>>> exit()
```

### Check Cache Working
```bash
# Run test twice, second should be instant
python test_stock_fetcher.py
python test_stock_fetcher.py  # Should complete in < 1 second
```

### Export Full Response to File
```bash
curl http://localhost:5000/api/watchlist > response.json
# Then open response.json in editor to inspect
```

---

## 📞 When Something's Wrong

1. **Check backend logs** - most info there
2. **Check browser DevTools** - Network tab shows HTTP status
3. **Try Python test** - isolates the problem
4. **Check internet** - curl https://finance.yahoo.com

**Don't see expected results?** Check `BACKEND_TESTING_GUIDE.md` for detailed troubleshooting.
