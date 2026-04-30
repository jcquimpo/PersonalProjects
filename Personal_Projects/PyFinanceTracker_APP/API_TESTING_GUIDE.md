# API Testing Guide - Stock Dashboard v2.0

## Overview
This guide explains how to test the FastAPI backend to ensure proper communication with the stock data source (yfinance).

---

## Method 1: Using Swagger UI (Easiest)

### Steps
1. Start the backend: `python backend_v2/main.py`
2. Open browser: http://localhost:5000/docs
3. You'll see the interactive API documentation

### Testing Endpoints
Each endpoint has a "Try it out" button:

#### Test `/api/health`
1. Click on GET /api/health
2. Click "Try it out"
3. Click "Execute"
4. Look for response code **200** with `{"status":"ok"}`

#### Test `/api/top-stocks`
1. Click on GET /api/top-stocks
2. Click "Try it out"
3. Modify parameters if desired:
   - `limit`: 50 (or any value 10-500)
   - `delay`: 0.7 (or any value 0.1-5.0)
4. Click "Execute"
5. Wait 15-30 seconds (it's fetching from Yahoo Finance)
6. Look for response code **200** with array of stocks

#### Test `/api/watchlist`
1. Click on GET /api/watchlist
2. Click "Try it out"
3. Modify delay parameter if desired
4. Click "Execute"
5. Look for AAPL, NVDA, MSFT, META, GOOGL in response

#### Test `/api/stock/{symbol}`
1. Click on GET /api/stock/{symbol}
2. Click "Try it out"
3. Enter symbol in the field (e.g., "AAPL")
4. Keep period as "7d" or change to other periods
5. Click "Execute"
6. Look for OHLC data with dates and prices

---

## Method 2: Using curl Command Line

### Windows (Command Prompt or PowerShell)

#### Health Check
```cmd
curl http://localhost:5000/api/health
```

#### Top Stocks (Default)
```cmd
curl "http://localhost:5000/api/top-stocks"
```

#### Top Stocks (Custom Parameters)
```cmd
curl "http://localhost:5000/api/top-stocks?limit=20&delay=0.5"
```

#### Watchlist
```cmd
curl "http://localhost:5000/api/watchlist?delay=0.5"
```

#### Individual Stock (AAPL, 7 days)
```cmd
curl "http://localhost:5000/api/stock/AAPL?period=7d"
```

#### Individual Stock (MSFT, 30 days)
```cmd
curl "http://localhost:5000/api/stock/MSFT?period=1mo"
```

### macOS/Linux

Same commands as above, may need to quote the URL:
```bash
curl 'http://localhost:5000/api/health'
curl 'http://localhost:5000/api/top-stocks?limit=50&delay=0.7'
```

---

## Method 3: Using Postman

### Setup
1. Download Postman: https://www.postman.com/
2. Create a new request
3. Set method to GET
4. Enter URL: `http://localhost:5000/api/health`
5. Click Send

### Testing Each Endpoint

| Endpoint | Method | URL |
|----------|--------|-----|
| Health Check | GET | `http://localhost:5000/api/health` |
| Top Stocks | GET | `http://localhost:5000/api/top-stocks?limit=50&delay=0.7` |
| Watchlist | GET | `http://localhost:5000/api/watchlist?delay=0.5` |
| Stock Data | GET | `http://localhost:5000/api/stock/AAPL?period=7d` |

---

## Checking Backend API Calls to yfinance

### Method 1: Backend Console Logs

When you run `python backend_v2/main.py`, the console shows:

```
INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
```

When you make an API call, you'll see:
```
INFO:     127.0.0.1:XXXXX - "GET /api/top-stocks?limit=50&delay=0.7 HTTP/1.1" 200 OK
```

If there's an error fetching from yfinance:
```
ERROR:     Exception in ASGI application
Traceback (most recent call last):
  ...
  ConnectionError: Unable to connect to yfinance
```

### Method 2: Check Python Logs

The stock_fetcher.py service uses print statements:
- Look for "Error fetching..." messages
- These indicate yfinance API issues

### Method 3: Add Debug Mode

Edit `backend_v2/main.py` to enable DEBUG:

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=5000,
        reload=True,  # Hot reload
        log_level="debug"  # More verbose logs
    )
```

---

## Expected Response Formats

### `/api/health`
```json
{
  "status": "ok",
  "message": "Stock API is running"
}
```

### `/api/top-stocks`
```json
{
  "top_stocks": [
    {
      "symbol": "NVDA",
      "company_name": "NVIDIA Corporation",
      "percentage_change": 3.45,
      "current_price": 875.30,
      "previous_close": 847.50
    },
    {
      "symbol": "AAPL",
      "company_name": "Apple Inc.",
      "percentage_change": 2.15,
      "current_price": 189.50,
      "previous_close": 185.50
    }
  ],
  "ohlc_data": {
    "NVDA": [
      {
        "date": "2024-01-10",
        "open": 850.00,
        "high": 860.00,
        "low": 840.00,
        "close": 855.00
      }
    ],
    "AAPL": [...]
  },
  "fetched_at": "2024-01-16T14:30:00.123456"
}
```

### `/api/stock/AAPL?period=7d`
```json
{
  "symbol": "AAPL",
  "company_name": "Apple Inc.",
  "data": [
    {
      "date": "2024-01-10",
      "open": 185.00,
      "high": 188.50,
      "low": 184.00,
      "close": 187.50
    },
    {
      "date": "2024-01-11",
      "open": 187.50,
      "high": 189.50,
      "low": 186.00,
      "close": 189.00
    }
  ],
  "fetched_at": "2024-01-16T14:30:00.123456"
}
```

---

## Debugging yfinance Issues

### Problem: "No data available for SYMBOL"

**Causes**:
- Invalid ticker symbol
- Market closed
- Ticker doesn't exist

**Solution**:
- Verify ticker is correct (AAPL, MSFT, etc.)
- Try again during market hours
- Check yfinance status

### Problem: Timeout (>60 seconds)

**Causes**:
- Too many API calls too fast
- Internet connection slow
- yfinance API overloaded

**Solution**:
- Increase delay parameter (0.7 → 1.0 or higher)
- Reduce limit parameter (50 → 20)
- Wait and try again

### Problem: Empty data response

**Causes**:
- All stocks failed to fetch
- Network issue
- API rate limiting

**Solution**:
- Check backend logs for errors
- Verify internet connection
- Retry with smaller dataset

---

## Testing API Communication Flow

### Step-by-Step Test

1. **Start Backend**
   ```bash
   cd backend_v2
   python main.py
   ```
   Wait for: `Uvicorn running on http://0.0.0.0:5000`

2. **Test Health**
   ```bash
   curl http://localhost:5000/api/health
   ```
   Expect: `{"status":"ok","message":"Stock API is running"}`

3. **Test Simple Query**
   ```bash
   curl "http://localhost:5000/api/top-stocks?limit=10&delay=0.3"
   ```
   Wait 5-10 seconds, expect JSON with top_stocks array

4. **Test Watchlist**
   ```bash
   curl http://localhost:5000/api/watchlist
   ```
   Should contain AAPL, NVDA, MSFT, META, GOOGL

5. **Test Individual Stock**
   ```bash
   curl http://localhost:5000/api/stock/AAPL?period=7d
   ```
   Should have 7 days of OHLC data

6. **Check All Working**
   - All responses are JSON
   - No error codes (200 OK)
   - Data contains expected fields

---

## Monitoring API Performance

### Timing Each Request

#### Using PowerShell (Windows)
```powershell
Measure-Command {
  curl "http://localhost:5000/api/top-stocks?limit=50&delay=0.7"
}
```

#### Using time Command (Mac/Linux)
```bash
time curl "http://localhost:5000/api/top-stocks?limit=50&delay=0.7"
```

### Expected Times
- Health check: <100ms
- Top stocks (50 limit, 0.7 delay): 40-60 seconds
- Top stocks (20 limit, 0.3 delay): 10-15 seconds
- Watchlist (5 stocks, 0.5 delay): 5-10 seconds
- Individual stock: 1-3 seconds

---

## Advanced Testing

### Test Different Time Periods

```bash
# 1 day
curl "http://localhost:5000/api/stock/AAPL?period=1d"

# 1 month
curl "http://localhost:5000/api/stock/AAPL?period=1mo"

# 1 year
curl "http://localhost:5000/api/stock/AAPL?period=1y"

# Max available data
curl "http://localhost:5000/api/stock/AAPL?period=max"
```

### Test Different Stocks

```bash
curl "http://localhost:5000/api/stock/MSFT?period=7d"
curl "http://localhost:5000/api/stock/GOOGL?period=7d"
curl "http://localhost:5000/api/stock/TSLA?period=7d"
```

### Test Parameter Limits

```bash
# Minimum
curl "http://localhost:5000/api/top-stocks?limit=10&delay=0.1"

# Maximum
curl "http://localhost:5000/api/top-stocks?limit=500&delay=5.0"

# Invalid (will error)
curl "http://localhost:5000/api/top-stocks?limit=5&delay=0.1"
```

---

## Checklist for Verifying Backend

- [ ] Health endpoint returns status "ok"
- [ ] Top stocks endpoint returns 5 stocks with data
- [ ] Watchlist endpoint returns AAPL, NVDA, MSFT, META, GOOGL
- [ ] Individual stock endpoint returns 7+ days of OHLC data
- [ ] All responses are valid JSON
- [ ] No HTTP error codes (all 200)
- [ ] Data contains expected fields (symbol, price, change, etc.)
- [ ] Timestamps are recent (within 1 minute)
- [ ] Charts would have data to display (multiple OHLC points)

---

## Next: Testing Frontend Communication

Once backend tests pass, test frontend:
1. Open http://localhost:3000
2. Stocks should load in sidebar
3. Charts should display when clicked
4. Refresh button should update data

If frontend doesn't show data, check:
1. Browser Network tab (F12 → Network)
2. Frontend console for errors
3. Backend logs for API errors
