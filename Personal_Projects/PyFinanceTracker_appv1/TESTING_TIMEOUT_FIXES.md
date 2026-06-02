# Testing the Timeout Fixes

## Quick Start

### 1. Restart the Backend
```bash
# Navigate to backend directory
cd PyFinanceTracker_APP/backend_v2

# Stop any running instance (Ctrl+C if running)

# Start fresh with updated code
python main.py
```

You should see in logs:
```
DEBUG - Min request delay: 2.0s
DEBUG - Fetch timeout: 18.0s
```

### 2. Test Top Stocks Endpoint

#### Browser/cURL
```bash
curl -X GET "http://localhost:5000/api/top-stocks" -H "accept: application/json"
```

#### Expected Behavior
1. **Fast network (< 10s yfinance response)**
   - ✅ Returns live data within ~8 seconds
   - Includes `is_demo_data: false`

2. **Slow network (10-20s yfinance response)**
   - ✅ Switches to mock data at ~15 second mark
   - Includes `is_demo_data: true`
   - Completes within ~15 seconds

3. **Rate limited / Unavailable**
   - ✅ Falls back to mock data immediately
   - Includes `is_demo_data: true` and explanatory note
   - Completes in ~2 seconds

#### Response Examples

**Live Data (Success)**
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
    ...
  ],
  "ohlc_data": {
    "AAPL": [
      {"date": "2026-04-28", "open": 171.50, "high": 176.00, "low": 171.22, "close": 175.50},
      ...
    ]
  },
  "fetched_at": "2026-04-29T14:23:45.123456",
  "is_demo_data": false
}
```

**Mock Data (Fallback)**
```json
{
  "top_stocks": [
    {
      "symbol": "AAPL",
      "company_name": "Apple Inc.",
      "percentage_change": 3.15,
      "current_price": 180.45,
      "previous_close": 174.85
    },
    ...
  ],
  "ohlc_data": { ... },
  "fetched_at": "2026-04-29T14:23:45.123456",
  "is_demo_data": true,
  "note": "Using demonstration data - Yahoo Finance rate limited or timed out"
}
```

### 3. Watch Backend Logs

Look for these log messages indicating timeout handling:

**Normal execution**:
```
INFO - Fetching top stocks (limit=50, delay=0.3)
DEBUG - Safe limit: 5 symbols (rate limiting: 2.0s between requests)
DEBUG - Using symbol list: ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN']
INFO - Fetching performance for 5 symbols...
DEBUG - [1/5] Fetching AAPL...
DEBUG - [1/5] AAPL: 2.15% change
... (4 more symbols)
INFO - Found 5 valid stocks, fetching OHLC data...
INFO - Top stocks fetch complete in 12.45s. Returning 5 stocks.
```

**Timeout approaching**:
```
WARNING - Approaching timeout (13.2s elapsed). Using mock data.
INFO - Top stocks using mock data (due to rate limiting or timeout)
```

**Rate limited**:
```
WARNING - Rate limit hit (429). Giving up quickly to show demo data.
WARNING - No valid stocks obtained - using mock data for demonstration
INFO - Top stocks using mock data (due to rate limiting or timeout)
```

## 4. Test Watchlist Endpoint

```bash
curl -X GET "http://localhost:5000/api/watchlist" -H "accept: application/json"
```

Same behavior as top stocks - should complete within 15-20 seconds.

Expected response:
```json
{
  "watchlist": [
    {
      "symbol": "AAPL",
      "company_name": "Apple Inc.",
      "percentage_change": 2.5,
      "current_price": 175.50,
      "previous_close": 171.22
    },
    ...
  ],
  "ohlc_data": { ... },
  "fetched_at": "2026-04-29T14:23:45.123456",
  "is_demo_data": false or true
}
```

## 5. Frontend Testing

### Start Frontend
```bash
cd frontend_v2
npm start
```

### Navigate to Dashboard
1. Open `http://localhost:3000`
2. Should see stock data loading
3. **No error popup** - instead shows data (live or demo)

### Check Network Tab
1. Open DevTools (F12)
2. Go to Network tab
3. Filter: `/api`
4. Click on `/api/top-stocks` request
5. Check Response time - should be < 20 seconds

## 6. Performance Benchmarks

### Timing Expectations

| Scenario | Expected Time | Notes |
|----------|---------------|----|
| Fast network | 6-10s | All yfinance calls < 5s each |
| Normal network | 10-15s | Some yfinance calls 10-15s each |
| Slow network | ~15s | Timeout triggers, mock data returned |
| Rate limited | 2-3s | Instant fallback to mock |
| No internet | 2-3s | All requests fail, mock data |

### What NOT to See
❌ 20+ second wait
❌ `Request timeout` error on frontend
❌ Empty stock list
❌ Failed API requests

## 7. Debugging Tips

### Enable Full Debug Logging
Edit `backend_v2/main.py`:
```python
uvicorn.run(
    "app.main:app",
    host=host,
    port=port,
    reload=debug,
    log_level="debug"  # Changed from "info"
)
```

### Monitor Rate Limiting
Watch logs for:
```
DEBUG - Rate limit check passed. Requests in last minute: 3/20
DEBUG - Inter-request delay: sleeping 1.23s...
```

### Check Cache Effectiveness
```
DEBUG - Cache hit for top_stocks::: (age: 45.3s)
```
- If you see this, cache is working (good!)
- If you don't, each request hits the API

## 8. Rollback (if needed)

If issues arise, revert to previous version:
```bash
# From project root
git checkout HEAD -- backend_v2/app/services/stock_fetcher.py
cd backend_v2
python main.py
```

## ✅ Success Criteria

Your refactoring is successful when:
1. ✅ `/api/top-stocks` completes in < 20 seconds (always)
2. ✅ `/api/watchlist` completes in < 20 seconds (always)
3. ✅ Frontend shows data (live or demo) without errors
4. ✅ `is_demo_data` flag correctly indicates data source
5. ✅ No timeout errors in browser console
6. ✅ Backend logs show elapsed time tracking

## 🚨 Troubleshooting

### Still seeing timeouts?
1. Check network latency to Yahoo Finance
2. Increase `FETCH_TIMEOUT` in `stock_fetcher.py` (max 18s)
3. Check if rate limited: look for `429` errors in logs
4. Verify yfinance version: `pip list | grep yfinance`

### Mock data always showing?
1. Check if `is_demo_data: true` is being set
2. Verify timeout thresholds:
   - Performance fetch timeout: ~13s
   - OHLC fetch timeout: ~16s
3. Check yfinance API status (external issue)

### Performance still slow?
1. Verify `MIN_REQUEST_DELAY = 2.0` (not higher)
2. Check backend logs for `Inter-request delay` messages
3. Confirm Python virtual environment is active
4. Check system resources (CPU, memory)
