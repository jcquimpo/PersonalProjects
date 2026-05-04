# 🚀 Quick Start Guide - Fixed Version

## One-Command Startup

### Terminal 1: Backend
```powershell
cd PyFinanceTracker_APP/backend_v2
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
```

### Terminal 2: Frontend
```powershell
cd PyFinanceTracker_APP/frontend_v2
npm start
```

Browser opens to: http://localhost:3000

---

## ✅ Verification Checklist

- [ ] Backend terminal shows "Uvicorn running on http://0.0.0.0:5000"
- [ ] Frontend browser opens to http://localhost:3000
- [ ] Green badge shows "🟢 API Connected"
- [ ] Data appears within 5-15 seconds
- [ ] No timeout or disconnection errors

---

## 🧪 Quick Test

### In Browser Console (F12):
```javascript
// Test API connection
fetch('/api/health').then(r => r.json()).then(console.log)

// Should output: {status: "ok", message: "..."}
```

### In Terminal (PowerShell):
```powershell
# Test backend directly
curl http://localhost:5000/api/health

# Should return JSON response
```

---

## 📊 What's Been Fixed

| Issue | Before | After |
|-------|--------|-------|
| Timeout | 60 seconds | 20 seconds |
| API Disconnected | Doesn't reconnect | Auto-checks every 30s |
| Initial Load | 30-60 seconds | 5-10 seconds |
| Watchlist | Full data (slow) | Quick option (3-5s) |

---

## ⚡ Performance Tips

### Use Quick Endpoints (Fastest)
```bash
# Returns in 3-5 seconds
curl http://localhost:5000/api/quick-watchlist
```

### Use Standard Endpoints (Faster)
```bash
# Returns in 10-20 seconds
curl http://localhost:5000/api/watchlist
```

### Use Longer Delays if Rate Limited
```bash
# Slower but more reliable
curl "http://localhost:5000/api/watchlist?delay=1.0"
```

---

## 🛠️ If Something Goes Wrong

### "API Disconnected" Badge
```powershell
# Check backend is running
netstat -ano | findstr :5000

# If not, start it
cd backend_v2
python main.py
```

### "Request Timeout" Error
```powershell
# Try quick endpoint first
curl http://localhost:5000/api/quick-watchlist

# If that works, full endpoint might be slow
# Check backend diagnostics
curl http://localhost:5000/api/diagnostic
```

### Nothing Works
```powershell
# Run full connection test
python test_connection.py

# This tells you exactly what's working/broken
```

---

## 📚 Full Documentation

- **[CONNECTION_TROUBLESHOOTING.md](CONNECTION_TROUBLESHOOTING.md)** - Detailed troubleshooting
- **[FIXES_COMPLETE_SUMMARY.md](FIXES_COMPLETE_SUMMARY.md)** - All changes explained
- **[EMPTY_WATCHLIST_FIX.md](backend_v2/EMPTY_WATCHLIST_FIX.md)** - Data fetching issues
- **[STOCK_FETCHER_FIX_GUIDE.md](backend_v2/STOCK_FETCHER_FIX_GUIDE.md)** - Backend optimization

---

## 🎯 Expected Timeline

```
0s   → Load page at localhost:3000
5s   → API health check completes, badge turns green
10s  → Watchlist data appears
15s  → Charts display
```

**Total from fresh start: 15-20 seconds** ✅

---

## 🆘 Emergency Commands

```powershell
# Kill stuck backend
taskkill /PID 12345 /F

# Or kill by port
netstat -ano | findstr :5000
taskkill /PID [PID] /F

# Reset cache if stuck
curl -X POST http://localhost:5000/api/reset-cache

# Full system restart
# 1. Stop frontend (Ctrl+C)
# 2. Stop backend (Ctrl+C)
# 3. Restart backend: python main.py
# 4. Restart frontend: npm start
```

---

## 📞 Need Help?

1. Check browser console (F12 → Console)
2. Check backend terminal output
3. Run: `python test_connection.py`
4. Check: `curl http://localhost:5000/api/diagnostic`

**Most issues are easily fixed!** 🎉

