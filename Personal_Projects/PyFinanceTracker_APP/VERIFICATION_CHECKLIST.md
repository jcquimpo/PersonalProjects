# Frontend-Backend v2 Verification Checklist

## ✅ Pre-Flight Checks

### Environment Setup
- [ ] `backend_v2/.env` file exists with:
  - [ ] `HOST=0.0.0.0`
  - [ ] `PORT=5000`
  - [ ] `DEBUG=False`

- [ ] `frontend_v2/.env.local` file exists with:
  - [ ] `REACT_APP_API_URL=http://localhost:5000/api`

- [ ] `frontend_v2/.env.production` file exists with:
  - [ ] `REACT_APP_API_URL=https://your-production-api.com/api`

### Dependencies
- [ ] Backend: `requirements.txt` installed
  ```bash
  pip install -r backend_v2/requirements.txt
  ```
  
- [ ] Frontend: `npm install` run
  ```bash
  npm install  # from frontend_v2 folder
  ```

- [ ] Key packages present:
  - [ ] `fastapi` (backend)
  - [ ] `uvicorn` (backend)
  - [ ] `yfinance` (backend)
  - [ ] `react` (frontend)
  - [ ] `recharts` (frontend)

### Configuration Files
- [ ] `frontend_v2/src/setupProxy.js` exists
- [ ] `frontend_v2/src/services/api.js` has timeout/retry logic
- [ ] `backend_v2/app/main.py` has CORS middleware enabled

---

## 🚀 Startup Checks

### Backend Startup
- [ ] Terminal: Navigate to `backend_v2` folder
- [ ] Run: `python main.py`
- [ ] Output includes: `Uvicorn running on http://0.0.0.0:5000`
- [ ] No error messages in console
- [ ] No module import errors

### Frontend Startup
- [ ] Terminal: Navigate to `frontend_v2` folder
- [ ] Run: `npm start`
- [ ] Browser opens automatically to `http://localhost:3000`
- [ ] No "cannot find module" errors
- [ ] No TypeScript/JSX syntax errors
- [ ] DevTools console shows no red errors initially

---

## 🌐 Network Connectivity Checks

### Backend API Health
- [ ] Open browser: `http://localhost:5000/api/health`
- [ ] Should return JSON: `{"status":"ok","message":"Stock API is running"}`
- [ ] Status code: 200

### Backend Swagger UI
- [ ] Open browser: `http://localhost:5000/docs`
- [ ] Page loads (interactive API documentation)
- [ ] All endpoints visible:
  - [ ] GET /api/top-stocks
  - [ ] GET /api/watchlist
  - [ ] GET /api/stock/{symbol}
  - [ ] GET /api/health

### Frontend Load
- [ ] Open browser: `http://localhost:3000`
- [ ] Page title: "Stock Dashboard" 
- [ ] Header displays: "📈 Stock Dashboard"
- [ ] No white page or blank screen
- [ ] Console shows no CORS errors

---

## 🔌 API Communication Checks

### Health Check Status
- [ ] Green status badge shows "● API Connected"
- [ ] (Not red "● API Disconnected")

### Network Requests
- [ ] Open DevTools (F12)
- [ ] Go to Network tab
- [ ] Filter for XHR/Fetch
- [ ] Click "🔄 Refresh" button in frontend
- [ ] See network requests:
  - [ ] `/api/top-stocks` (status 200)
  - [ ] `/api/watchlist` (status 200)
  - [ ] Requests have response data (preview tab shows JSON)

### Response Data Structure
- [ ] Top stocks response has:
  - [ ] `top_stocks` array
  - [ ] `ohlc_data` object
  - [ ] `fetched_at` timestamp

- [ ] Watchlist response has:
  - [ ] `watchlist` array
  - [ ] `ohlc_data` object
  - [ ] `fetched_at` timestamp

- [ ] Each stock has:
  - [ ] `symbol` (e.g., "AAPL")
  - [ ] `company_name` (e.g., "Apple Inc.")
  - [ ] `percentage_change` (number)
  - [ ] `current_price` (number)
  - [ ] `previous_close` (number)

- [ ] Each OHLC data point has:
  - [ ] `date` (YYYY-MM-DD format)
  - [ ] `open` (number)
  - [ ] `high` (number)
  - [ ] `low` (number)
  - [ ] `close` (number)

---

## 📊 Frontend Display Checks

### Stock List Rendering
- [ ] "Top 5 Performers" tab shows:
  - [ ] At least 5 stock cards
  - [ ] Each card shows symbol, company name, price, and % change
  - [ ] Positive changes shown in green (↑)
  - [ ] Negative changes shown in red (↓)

- [ ] "📌 Watchlist" tab shows:
  - [ ] At least 5 stock cards (AAPL, NVDA, MSFT, META, GOOGL)
  - [ ] Same data structure as top performers

### Stock Selection
- [ ] Click on any stock card
- [ ] Card background changes (selected state)
- [ ] Right panel updates with chart
- [ ] Stock symbol and company name appear in chart header

### Chart Rendering
- [ ] "Closing Price Trend" line chart displays:
  - [ ] X-axis shows dates
  - [ ] Y-axis shows prices
  - [ ] Blue line shows price trend
  - [ ] Dots on data points
  - [ ] Tooltip appears on hover

- [ ] "OHLC Data" bar chart displays:
  - [ ] 4 bars per date (Open, High, Low, Close)
  - [ ] Different colors for each OHLC component
  - [ ] Legend shows color coding

### Loading States
- [ ] First load shows loading spinner
- [ ] "🔄 Refresh" button shows "⏳ Loading..." while fetching
- [ ] Button disabled during loading
- [ ] Spinner disappears when data loads

### Error Handling
- [ ] If backend is down, error banner appears at top
- [ ] Error message is readable and helpful
- [ ] No white screen or crash

---

## 🔄 Timeout & Retry Checks

### Test Timeout Protection
- [ ] Open DevTools Console
- [ ] In a different terminal, stop the backend server
- [ ] Wait up to 60 seconds
- [ ] After timeout, error appears with message like "Request timeout after 60000ms"
- [ ] Frontend doesn't crash (graceful error)

### Test Retry Logic
- [ ] Stop backend server
- [ ] Click "🔄 Refresh" in frontend
- [ ] Check console: Should see "Retry attempt" messages
- [ ] After 2 retries, shows error
- [ ] Restart backend
- [ ] Click "🔄 Refresh" again
- [ ] Works immediately (no retry needed)

---

## 🌍 CORS & Proxy Checks

### Development Proxy (setupProxy.js)
- [ ] With both servers running
- [ ] Open DevTools Network tab
- [ ] Click refresh in frontend
- [ ] Look at request URL in Network tab
  - [ ] Should be: `/api/top-stocks` (relative)
  - [ ] NOT: `http://localhost:5000/api/top-stocks` (absolute)
  - [ ] This means proxy is working

### CORS Headers
- [ ] Click on `/api/top-stocks` request in Network tab
- [ ] Click Response Headers tab
- [ ] Should see: `Access-Control-Allow-Origin: *`
- [ ] (Backend CORS is configured correctly)

---

## 🔐 Environment Variable Checks

### Development (npm start)
- [ ] Open DevTools Console
- [ ] Type: `fetch('/api/health').then(r => r.json()).then(console.log)`
- [ ] Should work without "http://localhost:5000" prefix
- [ ] Proves `setupProxy.js` is active

### Check Environment Variable
- [ ] Create a small test in App.jsx:
  ```javascript
  useEffect(() => {
    console.log('API URL:', process.env.REACT_APP_API_URL);
  }, []);
  ```
- [ ] Should log: `API URL: http://localhost:5000/api`
- [ ] (Proves .env.local is loaded)

---

## 📈 Performance Checks

### Request Speed
- [ ] Open DevTools Network tab
- [ ] Click refresh
- [ ] Check response times:
  - [ ] `/api/top-stocks`: Should complete within 60 seconds (often takes 10-30s)
  - [ ] `/api/watchlist`: Should complete within 60 seconds
- [ ] No request timeouts

### Memory Usage
- [ ] Open DevTools Performance tab
- [ ] Start recording
- [ ] Click refresh
- [ ] Let page load completely
- [ ] Stop recording
- [ ] Check memory usage:
  - [ ] Should not exceed 100-150 MB
  - [ ] No memory leaks (memory doesn't keep growing)

### Component Rendering
- [ ] Open React DevTools (browser extension)
- [ ] Select `<App>` component
- [ ] Initial load should show hooks:
  - [ ] `useState` for various states
  - [ ] `useEffect` for data fetching
- [ ] Clicking refresh shouldn't show excessive re-renders

---

## 🚨 Error Scenarios Checks

### Backend Down
- [ ] Stop backend server
- [ ] Frontend still shows (doesn't crash)
- [ ] Status badge shows "● API Disconnected" (red)
- [ ] Error banner appears with helpful message
- [ ] "🔄 Refresh" button visible but shows error after retry
- [ ] Console shows retry attempts

### No Internet
- [ ] Temporarily disable network
- [ ] Frontend still loads (or shows cached data)
- [ ] Error message appears after timeout
- [ ] No JavaScript errors in console
- [ ] UI remains functional (can still click buttons)

### Invalid API Response
- [ ] Manually modify backend response
- [ ] Frontend handles gracefully
- [ ] Shows error message
- [ ] Doesn't crash

### Port Conflicts
- [ ] Try running another app on port 3000 or 5000
- [ ] Should get clear error message
- [ ] Instructions for fixing (change port or kill process)

---

## 📋 Final Verification Checklist

Before declaring the system ready:

- [ ] All pre-flight checks passed ✅
- [ ] Both servers start without errors ✅
- [ ] All API endpoints respond (200 status) ✅
- [ ] Frontend displays all data correctly ✅
- [ ] Charts render properly ✅
- [ ] Stock data updates on refresh ✅
- [ ] No CORS errors in console ✅
- [ ] No timeout errors during normal usage ✅
- [ ] Retry logic works when network falters ✅
- [ ] Environment variables load correctly ✅
- [ ] setupProxy.js routes requests properly ✅
- [ ] Error handling is graceful ✅
- [ ] Loading states display properly ✅
- [ ] Performance is acceptable ✅

---

## 🎉 Success Criteria

System is working correctly if:

1. **Data Flow**: User sees stock data within 30 seconds of opening app
2. **Updates**: Clicking refresh fetches new data and displays it
3. **Charts**: Charts render without errors or blank displays
4. **Responsiveness**: UI updates immediately after data arrives
5. **Reliability**: System works consistently across multiple refresh cycles
6. **Error Handling**: If backend goes down, frontend shows helpful error (no crash)
7. **Performance**: Average response time under 30 seconds
8. **Environment**: Switching between dev/production URLs works smoothly

---

## 📞 Troubleshooting Quick Links

If checks fail, refer to:
- **Setup Issues**: See `SETUP_AND_TROUBLESHOOTING_V2.md`
- **Communication Issues**: See `COMMUNICATION_ANALYSIS.md`
- **Implementation Details**: See `IMPROVEMENTS_SUMMARY.md`
- **API Reference**: http://localhost:5000/docs (when backend running)

---

## 🎯 Recommended Verification Order

1. Environment Setup ✅
2. Startup Checks ✅
3. Network Connectivity ✅
4. API Communication ✅
5. Frontend Display ✅
6. Timeout & Retry ✅
7. CORS & Proxy ✅
8. Environment Variables ✅
9. Performance ✅
10. Error Scenarios ✅

Good luck! 🚀

