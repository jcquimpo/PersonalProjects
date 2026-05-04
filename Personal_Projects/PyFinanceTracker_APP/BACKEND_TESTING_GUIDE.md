# Backend Testing Guide - Stock Fetcher

This guide shows you how to test the backend to verify it's making API calls and properly fetching data.

## Method 1: Direct Python Testing (Fastest)

### Run the Test Suite
```bash
# Navigate to backend_v2
cd backend_v2

# Make sure Python environment is active
# Windows
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate

# Run the test script
python test_stock_fetcher.py
```

### Expected Output
```
╔════════════════════════════════════════════════════════════════════╗
║ STOCK FETCHER SERVICE TEST SUITE                                  ║
║ Time: 2026-04-29 14:30:45                                         ║
╚════════════════════════════════════════════════════════════════════╝

======================================================================
TEST: Get Company Names
======================================================================
✓ AAPL → Apple Inc. (0.45s)
✓ MSFT → Microsoft Corporation (0.42s)
✓ GOOGL → Alphabet Inc. (0.48s)
ℹ UNKNOWN_SYMBOL → UNKNOWN_SYMBOL (0.15s)

======================================================================
TEST: Get Stock Performance
======================================================================
✓ AAPL
  Price: $175.50
  Change: +2.15%
  Time: 3.21s
✓ MSFT
  Price: $425.30
  Change: +1.85%
  Time: 2.98s
✓ GOOGL
  Price: $140.20
  Change: +3.42%
  Time: 3.15s
```

### What Each Test Does

| Test | Purpose | What to Look For |
|------|---------|-----------------|
| **Get Company Names** | Verify symbol→name mapping | Names resolve without errors |
| **Get Stock Performance** | Fetch current price & % change | Real prices, reasonable % changes |
| **Get OHLC Data** | Fetch 7 days of price history | Multiple dates with valid prices |
| **Fetch Watchlist (Full)** | Complete watchlist with OHLC | All 3 symbols with data |
| **Fetch Top Stocks (Full)** | Top performing stocks with OHLC | 5 stocks sorted by % change |
| **Cache Effectiveness** | Verify caching works | 2nd call is much faster |
| **Error Handling** | Test invalid symbols | Gracefully returns None |
| **Rate Limiting** | Test request throttling | Delays between requests |

---

## Method 2: HTTP Testing with cURL

### Test Individual Endpoints

#### 1. Get Top Stocks
```bash
curl -X GET "http://localhost:5000/api/top-stocks" \
  -H "accept: application/json" \
  -w "\nResponse time: %{time_total}s\n"
```

#### 2. Get Watchlist
```bash
curl -X GET "http://localhost:5000/api/watchlist" \
  -H "accept: application/json" \
  -w "\nResponse time: %{time_total}s\n"
```

#### 3. Health Check
```bash
curl -X GET "http://localhost:5000/api/health" \
  -H "accept: application/json"
```

### Expected Response (Successful)
```json
{
  "top_stocks": [
    {
      "symbol": "AAPL",
      "company_name": "Apple Inc.",
      "percentage_change": 2.5,
      "current_price": 175.50,
      "previous_close": 171.22
    },
    {
      "symbol": "MSFT",
      "company_name": "Microsoft Corporation",
      "percentage_change": 1.85,
      "current_price": 425.30,
      "previous_close": 417.55
    },
    ...
  ],
  "ohlc_data": {
    "AAPL": [
      {
        "date": "2026-04-23",
        "open": 172.50,
        "high": 176.80,
        "low": 172.20,
        "close": 175.50
      },
      ...
    ],
    "MSFT": [...],
    ...
  },
  "fetched_at": "2026-04-29T14:30:45.123456",
  "is_demo_data": false
}
```

### What to Check in Response

✅ **Data is present**: Not empty arrays or null values
✅ **Live vs Demo**: Check `is_demo_data` flag
✅ **Response time**: Should be < 20 seconds
✅ **Data types**: Prices are numbers, symbols are strings
✅ **Reasonable values**: Stock prices are positive, % changes are reasonable

---

## Method 3: Browser Testing with DevTools

### Test in Browser

1. **Start both backend and frontend**
   ```bash
   # Terminal 1: Backend
   cd backend_v2
   python main.py

   # Terminal 2: Frontend
   cd frontend_v2
   npm start
   ```

2. **Open Browser**
   - Navigate to `http://localhost:3000`

3. **Open DevTools** (F12)
   - Go to **Network** tab
   - Filter: `api`

4. **Watch Requests**
   - Refresh page
   - Should see:
     - `/api/watchlist` → Response code 200, < 20s
     - `/api/top-stocks` → Response code 200, < 20s
   
   Click each request:
   - **Headers**: Check request method (GET), URL, response status
   - **Response**: JSON with stock data
   - **Timing**: Breakdown of request phases

### Example Network Tab View
```
Name                    Method  Status  Type    Size      Time
/api/watchlist          GET     200     json    15.2 KB   8.45s
/api/top-stocks         GET     200     json    12.8 KB   12.15s
```

---

## Method 4: Backend Logging

### Enable Debug Logging

Edit `backend_v2/main.py`:
```python
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", 5000))
debug = os.getenv("DEBUG", "False").lower() == "true"

uvicorn.run(
    "app.main:app",
    host=host,
    port=port,
    reload=debug,
    log_level="debug"  # Changed from "info" to "debug"
)
```

### Watch Backend Logs While Making Requests

```
2026-04-29 14:30:45,123 - app.services.stock_fetcher - INFO - Fetching watchlist with 3 symbols...
2026-04-29 14:30:45,234 - app.services.stock_fetcher - DEBUG - Safe limit: 3 symbols (rate limiting: 2.0s between requests)
2026-04-29 14:30:45,345 - app.services.stock_fetcher - DEBUG - Using symbol list: ['AAPL', 'MSFT', 'GOOGL']
2026-04-29 14:30:45,456 - app.services.stock_fetcher - DEBUG - [1/3] Fetching AAPL...
2026-04-29 14:30:48,789 - app.services.stock_fetcher - DEBUG - [1/3] AAPL: 2.15% change
2026-04-29 14:30:49,123 - app.services.stock_fetcher - DEBUG - [2/3] Fetching MSFT...
2026-04-29 14:30:52,456 - app.services.stock_fetcher - DEBUG - [2/3] MSFT: 1.85% change
2026-04-29 14:30:53,789 - app.services.stock_fetcher - DEBUG - [3/3] Fetching GOOGL...
2026-04-29 14:30:56,234 - app.services.stock_fetcher - DEBUG - [3/3] GOOGL: 3.42% change
2026-04-29 14:30:56,345 - app.services.stock_fetcher - INFO - Found 3 valid stocks, fetching OHLC data...
2026-04-29 14:30:58,678 - app.services.stock_fetcher - DEBUG - [1/3] AAPL: OHLC fetched
2026-04-29 14:31:00,123 - app.services.stock_fetcher - DEBUG - [2/3] MSFT: OHLC fetched
2026-04-29 14:31:02,456 - app.services.stock_fetcher - DEBUG - [3/3] GOOGL: OHLC fetched
2026-04-29 14:31:02,567 - app.services.stock_fetcher - INFO - Watchlist fetch complete in 17.44s. Returning 3 stocks.
```

### Key Log Indicators

| Log Message | Meaning |
|-------------|---------|
| `Fetching watchlist with 3 symbols...` | Request started |
| `[1/3] Fetching AAPL...` | Fetching individual symbol |
| `[1/3] AAPL: 2.15% change` | Successfully got data |
| `AAPL: Failed` | Failed to fetch (check why) |
| `Approaching timeout (13.2s elapsed)` | Running out of time, switching to mock |
| `Using demonstration data` | Fell back to mock data |
| `Cache hit for watchlist:::` | Using cached data (good!) |
| `Watchlist fetch complete in 17.44s` | Total time for full request |

---

## Method 5: Python REPL Testing

### Interactive Testing

```bash
# Start Python with virtual environment active
cd backend_v2
python

# In Python shell:
>>> from app.services.stock_fetcher import StockFetcher
>>> import time

# Test 1: Get performance for one stock
>>> start = time.time()
>>> perf = StockFetcher.get_stock_performance("AAPL")
>>> print(f"Time: {time.time() - start:.2f}s")
>>> print(perf)
{
  'symbol': 'AAPL',
  'company_name': 'Apple Inc.',
  'percentage_change': 2.15,
  'current_price': 175.50,
  'previous_close': 171.22
}
Time: 3.21s

# Test 2: Get OHLC data
>>> ohlc = StockFetcher.get_ohlc_data("AAPL", "7d")
>>> print(f"Records: {len(ohlc)}")
Records: 7
>>> ohlc[0]  # First record
{
  'date': '2026-04-23',
  'open': 172.50,
  'high': 176.80,
  'low': 172.20,
  'close': 175.50
}

# Test 3: Full watchlist fetch
>>> start = time.time()
>>> result = StockFetcher.fetch_watchlist()
>>> print(f"Time: {time.time() - start:.2f}s")
>>> print(f"Stocks: {len(result['watchlist'])}")
Time: 15.23s
Stocks: 3

# Test 4: Check cache (should be instant)
>>> start = time.time()
>>> result2 = StockFetcher.fetch_watchlist()
>>> print(f"Time (cached): {time.time() - start:.2f}s")
Time (cached): 0.01s

# Exit
>>> exit()
```

---

## Method 6: Postman/Insomnia Testing

### Import API Collection

Create file: `backend_v2/api_tests.json`

```json
{
  "info": {
    "name": "Stock Dashboard API",
    "version": "1.0.0"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "url": "http://localhost:5000/api/health"
      }
    },
    {
      "name": "Fetch Watchlist",
      "request": {
        "method": "GET",
        "url": "http://localhost:5000/api/watchlist"
      }
    },
    {
      "name": "Fetch Top Stocks",
      "request": {
        "method": "GET",
        "url": "http://localhost:5000/api/top-stocks"
      }
    }
  ]
}
```

Then:
1. Open Postman/Insomnia
2. Import `api_tests.json`
3. Click "Send" on each request
4. View response in real-time

---

## Quick Test Checklist

Run through this checklist to verify everything is working:

### ✅ Direct Python Test
```bash
cd backend_v2
python test_stock_fetcher.py
```
- [ ] All tests pass
- [ ] No red errors (only yellow info is ok)
- [ ] Timing is reasonable (< 20s per full fetch)

### ✅ cURL/HTTP Test
```bash
curl http://localhost:5000/api/watchlist -H "accept: application/json"
```
- [ ] HTTP 200 response
- [ ] JSON is valid
- [ ] Contains stock data
- [ ] Completes in < 20s

### ✅ Browser Test
1. Open `http://localhost:3000`
2. Open DevTools (F12)
3. Go to Network tab
4. Refresh page
   - [ ] See `/api/watchlist` request
   - [ ] See `/api/top-stocks` request
   - [ ] Both return 200 status
   - [ ] Both complete in < 20s

### ✅ Backend Logs
While running any test, check backend logs:
```
- [ ] See "Fetching watchlist with X symbols..."
- [ ] See progress for each symbol
- [ ] See "OHLC fetched" messages
- [ ] See "fetch complete in X.XXs"
- [ ] NO "Approaching timeout" or "Using mock data" (unless testing that feature)
```

---

## Troubleshooting

### No data in response (empty arrays)
**Cause**: API calls failing silently  
**Fix**:
1. Check backend logs for errors
2. Verify internet connection
3. Check if Yahoo Finance is accessible: `curl https://finance.yahoo.com`

### Response time > 20 seconds
**Cause**: Rate limiting or slow network  
**Fix**:
1. Check logs for "Inter-request delay" messages
2. Try running at off-peak hours
3. Verify internet speed

### `is_demo_data: true` in response
**Cause**: Fell back to mock data (either rate limited or timeout approaching)  
**Fix**:
1. Check logs for timeout messages
2. Reduce number of symbols being fetched
3. Wait before retrying (rate limiting)

### Python import errors
**Cause**: Virtual environment not active  
**Fix**:
```bash
# Windows
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate

# Verify
python -c "import yfinance; print('OK')"
```

### yfinance hanging (no response)
**Cause**: Network issue or Yahoo blocking  
**Fix**:
1. Check internet connection
2. Try manual curl: `curl https://query1.finance.yahoo.com/`
3. Wait 5 minutes and retry (rate limited)

---

## Performance Benchmarks

These are healthy timings:

| Operation | Expected Time | Status |
|-----------|---------------|--------|
| Get company name | < 1s | ✅ Fast |
| Get stock performance | 2-5s | ✅ Good |
| Get OHLC (7 days) | 2-5s | ✅ Good |
| Fetch watchlist (3 stocks) | 8-15s | ✅ Good |
| Fetch top stocks (5 stocks) | 10-18s | ✅ Good |
| 2nd call (cached) | < 0.1s | ✅ Fast |

Any request > 20s = problematic

---

## Next Steps

1. **Run the direct Python test** to verify functions work
2. **Check cURL requests** to verify API endpoints work
3. **Monitor browser DevTools** to see real request/response
4. **Watch backend logs** to understand what's happening

If all tests pass, your backend is working correctly!
