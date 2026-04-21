# Quick Reference Card

## 🚀 Start Application (Choose One)

### Windows - Automatic
```
start.bat
```

### Mac/Linux - Automatic
```
chmod +x start.sh
./start.sh
```

### Windows - Manual
```bash
# Terminal 1
cd backend_v2
python main.py

# Terminal 2
cd frontend_v2
npm start
```

### Mac/Linux - Manual
```bash
# Terminal 1
cd backend_v2
source venv/bin/activate
python main.py

# Terminal 2
cd frontend_v2
npm start
```

---

## 📍 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Stock dashboard UI |
| Backend | http://localhost:5000 | API server |
| API Docs | http://localhost:5000/docs | Interactive testing |
| ReDoc | http://localhost:5000/redoc | API documentation |

---

## 🔧 First-Time Setup

```bash
# Backend
cd backend_v2
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd frontend_v2
npm install
```

---

## 🧪 Test API (Pick One)

### Option 1: Swagger UI (Easiest)
```
http://localhost:5000/docs
Click "Try it out" on any endpoint
```

### Option 2: curl Commands
```bash
# Health check
curl http://localhost:5000/api/health

# Top stocks
curl "http://localhost:5000/api/top-stocks?limit=50&delay=0.7"

# Watchlist
curl http://localhost:5000/api/watchlist

# Individual stock
curl "http://localhost:5000/api/stock/AAPL?period=7d"
```

### Option 3: Frontend
```
1. Open http://localhost:3000
2. Wait 20 seconds for data
3. Click stocks to see charts
4. Click refresh to update
```

---

## 📚 Key Files

| File | Purpose |
|------|---------|
| `backend_v2/main.py` | Backend entry point |
| `backend_v2/app/main.py` | FastAPI setup |
| `backend_v2/app/services/stock_fetcher.py` | Stock data logic |
| `backend_v2/app/routes/stocks.py` | API endpoints |
| `frontend_v2/src/App.jsx` | Main React component |
| `frontend_v2/src/services/api.js` | API client |

---

## 🔗 API Endpoints

```
GET /api/health              Health check
GET /api/top-stocks          Top 5 performers
GET /api/watchlist           Watchlist stocks
GET /api/stock/{symbol}      Individual stock data
```

---

## 📋 Documentation Files

```
README_V2.md          ← Full project documentation
SETUP_AND_TESTING.md  ← Setup & testing procedures
API_TESTING_GUIDE.md  ← How to test the API
MIGRATION_GUIDE.md    ← v1.0 → v2.0 comparison
REFACTOR_SUMMARY.md   ← What was delivered
```

---

## ⚡ Common Tasks

### Change Watchlist Stocks
Edit: `backend_v2/app/services/stock_fetcher.py`
```python
WATCHLIST = ["AAPL", "NVDA", "MSFT", "META", "GOOGL"]
```

### Change Backend Port
Edit: `backend_v2/.env`
```
PORT=5001
```

### Change Frontend API URL
Edit: `frontend_v2/.env`
```
REACT_APP_API_URL=http://localhost:5001/api
```

### Speed Up Initial Load
Use: `?limit=20&delay=0.3`
```bash
curl "http://localhost:5000/api/top-stocks?limit=20&delay=0.3"
```

---

## 🐛 Quick Fixes

| Problem | Solution |
|---------|----------|
| Python not found | Install Python 3.8+ |
| Port in use | Change PORT in .env |
| Module not found | `pip install -r requirements.txt` |
| npm not found | Install Node.js 16+ |
| No data loading | Wait 30 seconds; check logs |
| API not connecting | Verify backend running on 5000 |

---

## 📈 Expected Times

- **First load**: 20-30 seconds
- **Refresh**: 10-20 seconds
- **Health check**: <1 second
- **Individual stock**: 1-3 seconds

---

## 💾 Backend Technology Stack

- **Framework**: FastAPI
- **Language**: Python 3.8+
- **Server**: Uvicorn
- **Validation**: Pydantic
- **Data Source**: yfinance

---

## 🎨 Frontend Technology Stack

- **Framework**: React 18
- **Charts**: Recharts
- **Build Tool**: Create React App
- **Port**: 3000

---

## 🎯 Next Steps

1. Run: `start.bat` or `./start.sh`
2. Open: `http://localhost:3000`
3. Wait: 20-30 seconds for data
4. Test: Click stocks and refresh button
5. Docs: Visit `http://localhost:5000/docs`

---

## ✅ Verification Checklist

- [ ] Backend starts without errors
- [ ] Frontend loads at port 3000
- [ ] Stocks appear in sidebar
- [ ] Charts display on click
- [ ] Refresh button works
- [ ] Tabs switch correctly
- [ ] API docs at /docs
- [ ] No console errors

---

## 📞 Stuck? Check These Files

1. **Setup issues** → SETUP_AND_TESTING.md
2. **API not working** → API_TESTING_GUIDE.md
3. **How v2 differs** → MIGRATION_GUIDE.md
4. **Full details** → README_V2.md

---

**Status**: ✅ Ready to use
**Version**: 2.0
**Last Updated**: 2024
