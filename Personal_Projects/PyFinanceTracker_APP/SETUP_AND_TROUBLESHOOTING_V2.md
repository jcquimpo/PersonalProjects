# Frontend-Backend v2 Setup & Troubleshooting Guide

## 📋 Quick Start

### Prerequisites
- Node.js (v14+) and npm
- Python 3.8+
- pip

### Option 1: Run Both Servers (Recommended for Development)

#### Terminal 1 - Backend
```bash
cd PyFinanceTracker_APP/backend_v2
pip install -r requirements.txt
python main.py
```
Backend runs on: http://localhost:5000

#### Terminal 2 - Frontend
```bash
cd PyFinanceTracker_APP/frontend_v2
npm install  # Run once
npm start
```
Frontend runs on: http://localhost:3000

---

## ✅ Verification Checklist

### Backend Health Check
- [ ] Backend starts without errors
- [ ] Visit http://localhost:5000/docs (Swagger UI should load)
- [ ] Click "Try it out" on `/api/health` endpoint
- [ ] Response shows: `{"status":"ok","message":"Stock API is running"}`

### Frontend Health Check
- [ ] Frontend loads at http://localhost:3000
- [ ] Page title shows "📈 Stock Dashboard"
- [ ] No CORS errors in browser console
- [ ] API health indicator shows "● API Connected" (green)

### API Communication Check
1. Open browser DevTools (F12)
2. Go to Network tab
3. In the app, click "🔄 Refresh" button
4. Look for network requests to `/api/top-stocks` and `/api/watchlist`
5. Verify they return 200 status with JSON data

---

## 🔍 Troubleshooting

### Issue 1: "CORS Error" or "No Access-Control-Allow-Origin"
**Symptoms**: 
- Browser console shows CORS error
- API requests fail
- Error: "Cannot load from..."

**Solutions**:
1. Verify backend is running: http://localhost:5000
2. Check CORS is enabled in `backend_v2/app/main.py`:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```
3. Try using the development proxy:
   - Ensure `setupProxy.js` exists in `frontend_v2/src/`
   - Update `api.js` to use relative URLs:
     ```javascript
     const API_BASE_URL = '/api'; // Use proxy instead of http://localhost:5000/api
     ```

---

### Issue 2: "API Disconnected" Status
**Symptoms**:
- Status badge shows "● API Disconnected" (red)
- Health check fails

**Solutions**:
1. Verify backend is running:
   ```bash
   curl http://localhost:5000/api/health
   ```
2. Check if port 5000 is in use:
   ```powershell
   # Windows
   netstat -ano | findstr :5000
   ```
3. Kill process on port 5000 and restart backend
4. Check backend logs for errors

---

### Issue 3: "No Stocks Available" or Empty Lists
**Symptoms**:
- Frontend loads but no stock data
- Loading spinner shows but never completes
- Lists are empty

**Solutions**:
1. Check backend API endpoint directly:
   ```bash
   curl http://localhost:5000/api/top-stocks
   curl http://localhost:5000/api/watchlist
   ```
2. If API returns errors:
   - Check internet connection (yfinance requires external API)
   - Verify `requirements.txt` packages are installed:
     ```bash
     pip install -r backend_v2/requirements.txt
     ```
   - Check backend logs for yfinance errors

3. If API returns data but frontend doesn't show it:
   - Open browser DevTools Network tab
   - Check if requests are being made
   - Check the Response tab to see actual API response
   - Compare response structure with models in `backend_v2/app/models/stock.py`

---

### Issue 4: "Request Timeout" Error
**Symptoms**:
- Error message: "Request timeout after 60000ms"
- Stocks take too long to load

**Solutions**:
1. This is normal for the first load (yfinance takes time)
2. Increase timeout in `frontend_v2/src/services/api.js`:
   ```javascript
   const DEFAULT_TIMEOUT = 90000; // 90 seconds instead of 60
   ```
3. Check your internet speed
4. Check backend logs for slow responses

---

### Issue 5: Module Not Found Errors
**Symptoms**:
- Backend errors like "ModuleNotFoundError: No module named 'yfinance'"
- Frontend errors like "Cannot find module 'recharts'"

**Solutions**:
Backend:
```bash
cd backend_v2
pip install -r requirements.txt
```

Frontend:
```bash
cd frontend_v2
npm install
# or specific package
npm install recharts
```

---

### Issue 6: Port Already in Use
**Symptoms**:
- Error: "Address already in use" port 5000 or 3000
- Cannot start backend or frontend

**Solutions**:
Backend (port 5000):
```powershell
# Find process using port 5000
netstat -ano | findstr :5000
# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or change port in backend_v2/.env
PORT=5001
```

Frontend (port 3000):
```powershell
# Set custom port before starting
$env:PORT=3001
npm start
```

---

### Issue 7: Environment Variables Not Loaded
**Symptoms**:
- `process.env.REACT_APP_API_URL` is undefined
- API calls fail

**Solutions**:
1. Verify `.env.local` exists in `frontend_v2/`:
   ```
   REACT_APP_API_URL=http://localhost:5000/api
   ```
2. Restart `npm start` after creating `.env.local`
3. Verify variable name starts with `REACT_APP_`

---

## 📊 Expected Data Structure

### Top Stocks Response
```json
{
  "top_stocks": [
    {
      "symbol": "AAPL",
      "company_name": "Apple Inc.",
      "percentage_change": 2.45,
      "current_price": 173.50,
      "previous_close": 169.45
    }
  ],
  "ohlc_data": {
    "AAPL": [
      {
        "date": "2025-04-18",
        "open": 170.00,
        "high": 174.50,
        "low": 169.80,
        "close": 173.50
      }
    ]
  },
  "fetched_at": "2025-04-20T10:30:00"
}
```

### Watchlist Response
```json
{
  "watchlist": [
    {
      "symbol": "NVDA",
      "company_name": "NVIDIA Corporation",
      "percentage_change": -1.23,
      "current_price": 485.20,
      "previous_close": 491.20
    }
  ],
  "ohlc_data": {
    "NVDA": [
      {
        "date": "2025-04-18",
        "open": 490.00,
        "high": 495.50,
        "low": 485.00,
        "close": 485.20
      }
    ]
  },
  "fetched_at": "2025-04-20T10:30:00"
}
```

---

## 🔧 Configuration Files

### `backend_v2/.env`
```env
HOST=0.0.0.0          # Server host
PORT=5000             # Server port
DEBUG=False           # Debug mode
```

### `frontend_v2/.env.local` (Development)
```env
REACT_APP_API_URL=http://localhost:5000/api
```

### `frontend_v2/.env.production` (Production)
```env
REACT_APP_API_URL=https://your-api.com/api
```

---

## 📚 API Endpoints Reference

| Endpoint | Method | Purpose | Params |
|----------|--------|---------|--------|
| `/api/top-stocks` | GET | Top 5 performing stocks | `limit`, `delay` |
| `/api/watchlist` | GET | Watchlist stocks | `delay` |
| `/api/stock/{symbol}` | GET | Specific stock OHLC data | `period` |
| `/api/health` | GET | API health check | None |

---

## 🚀 Production Deployment

### Backend
1. Update `backend_v2/.env`:
   ```env
   DEBUG=False
   HOST=0.0.0.0
   PORT=5000
   ```

2. Deploy using Gunicorn (production server):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app.main:app
   ```

3. Update CORS for production:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://your-frontend-domain.com"],
       allow_credentials=True,
       allow_methods=["GET"],
       allow_headers=["*"],
   )
   ```

### Frontend
1. Build for production:
   ```bash
   cd frontend_v2
   npm run build
   ```

2. Update `.env.production` with production API URL:
   ```env
   REACT_APP_API_URL=https://your-api-domain.com/api
   ```

3. Deploy build folder to hosting (Vercel, Netlify, etc.)

---

## 🎯 Common Workflows

### Development Workflow
```bash
# Terminal 1 - Backend
cd PyFinanceTracker_APP/backend_v2
pip install -r requirements.txt
python main.py

# Terminal 2 - Frontend
cd PyFinanceTracker_APP/frontend_v2
npm install  # Run once
npm start

# Terminal 3 - Optional: View backend logs
tail -f <backend-log-file>
```

### Testing Workflow
```bash
# Test backend API
curl http://localhost:5000/api/health
curl http://localhost:5000/api/top-stocks?limit=10&delay=0.7

# Test frontend data fetching
# Open DevTools → Network tab → Click refresh button in app
```

### Debugging Workflow
1. Backend: Check `backend_v2` logs for exceptions
2. Frontend: Open DevTools (F12) → Console for JS errors
3. Network: DevTools → Network tab to see HTTP requests/responses
4. API Docs: Visit http://localhost:5000/docs to test endpoints

---

## 📞 Additional Resources

- **FastAPI Docs**: http://localhost:5000/docs (when running)
- **React DevTools**: Browser extension for React debugging
- **yfinance Docs**: https://finance.yahoo.com/
- **Recharts Docs**: https://recharts.org/

