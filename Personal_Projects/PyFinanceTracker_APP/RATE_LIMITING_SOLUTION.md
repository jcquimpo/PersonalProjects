# Stock API Rate Limiting Issue - Diagnosis & Solutions

## Current Problem

**Symptom**: HTTP 429 "Too Many Requests" errors from Yahoo Finance

**Root Cause**: 
- Yahoo Finance detects rapid consecutive requests from a single IP
- Each `yfinance.Ticker().history()` call makes 3+ internal HTTP requests:
  1. GET cookie from query1.finance.yahoo.com
  2. GET crumb token from query1.finance.yahoo.com
  3. GET data from query2.finance.yahoo.com
  4. Sometimes retry with different cookie strategy

Even though we add 3-second delays between our requests, Yahoo's crumb token itself returns "Edge: Too Many Requests", indicating rate limiting at Yahoo's server level.

## What We've Tried

1. ✅ Added global rate limiter (20 requests/minute max)
2. ✅ Added Semaphore (1 concurrent request only)
3. ✅ Reduced watchlist from 5 → 3 symbols
4. ✅ Reduced top stocks from 10 → 5 symbols  
5. ✅ Added inter-request delays: 1.5s → 3.0s between requests
6. ✅ Implemented response caching (60s TTL)
7. ❌ **Still getting 429 errors** - the problem is at Yahoo's end

## Why It's Not Working

Yahoo Finance implements **strict cookie/session rate limiting** specifically designed to prevent automated scraping. Our careful request spacing doesn't help because:
- Each request needs a new cookie + crumb pair
- Getting the crumb itself is rate-limited
- Multiple consecutive crumb requests trigger 429

## Recommended Solutions (In Priority Order)

### Option 1: Implement Graceful Degradation (RECOMMENDED - EASIEST)
**Effort**: Low | **Impact**: Immediate fix

When yfinance fails with 429 or timeout:
- Return cached data from previous call (if available)
- Return empty data with "Rate limited" message
- Frontend shows "Last updated: X seconds ago" instead of live data

**Benefit**: App stays responsive, data degradation is transparent

### Option 2: Increase Request Spacing Further (MODERATE)
**Effort**: Low | **Impact**: Partial fix

- Increase MIN_REQUEST_DELAY from 3s to 5-10s
- Fetch fewer symbols (watchlist: 2, top stocks: 3)
- This slows down the app but may reduce 429 errors

**Tradeoff**: Watchlist takes 30-60 seconds to load

### Option 3: Use Batch Download (MODERATE)  
**Effort**: Medium | **Impact**: Good improvement

Replace individual `yf.Ticker()` calls with `yf.download()`:
```python
# Instead of:
for symbol in symbols:
    ticker = yf.Ticker(symbol)  # Makes 3+ HTTP requests
    
# Use:
data = yf.download(symbols, ...)  # Makes 1 HTTP request per symbol
```

**Benefit**: Fewer total HTTP requests to Yahoo

### Option 4: Switch to Different API (COMPLEX)
**Effort**: High | **Impact**: Permanent fix

Use alternative APIs:
- **Polygon.io** (free tier: 5 API calls/min, requires key)
- **Alpha Vantage** (free tier: 5 API calls/min, requires key) 
- **IEX Cloud** (free tier: 100/day, requires key)
- **Finnhub** (free tier: 60/min, requires key)

**Benefit**: No rate limiting issues

---

## Quick Fix: Graceful Degradation (Recommended)

Current status: API returns 200 OK but with empty watchlist arrays
- The app already handles this gracefully
- Frontend shows "Loading..." then "No data available"

**What we need**: Better cache fallback + error messages

### Implementation:
1. Keep the last 5 successful responses in memory (not just 1)
2. When yfinance fails, return most recent cached data
3. Add `is_cached: true` flag to response
4. Frontend displays "Loaded from cache (3 mins ago)" message

---

## Immediate Workaround: Reduce Load

### Current limits:
- Watchlist: 3 symbols (AAPL, MSFT, GOOGL)
- Top Stocks: 5 symbols

### Propose reducing to:
- Watchlist: 1-2 symbols (just AAPL or AAPL + MSFT)
- Top Stocks: 2-3 symbols
- Add "Refresh" button (manual pull) instead of auto-refresh

---

## Testing the Fix

Once updated, test with:
```bash
# Terminal 1: Start backend
cd backend_v2
python main.py

# Terminal 2: Run load test
python quick_test.py
```

Expected results:
- `/api/health` - **instant** ✅
- `/api/quick-watchlist` - **<5s** (may be cached)
- `/api/watchlist` - **30-60s** (multiple requests)
- Status: **200** (even if data is cached/empty)

---

## Next Steps

1. Decide which solution fits your use case
2. Implement graceful degradation for better UX
3. (Optional) Reduce symbols further for faster responses
4. Test with frontend to verify connection works

**Recommendation**: Use Option 1 (Graceful Degradation) + Option 2 (Fewer Symbols)
This gives quick fix + reduced rate limiting pressure simultaneously.
