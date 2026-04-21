# Stock Dashboard v2.0 - Refactored Architecture

## Overview

This is a completely refactored version of the Stock Dashboard application with the following improvements:

### **Architecture Changes**
- **Backend**: Node.js/Express → **FastAPI (Python)** ✅
- **Backend Task Runner**: Python subprocess → **Direct Python service** ✅
- **Frontend**: React with proxy → **React SPA** ✅
- **Single Language Stack**: Python + JavaScript/React ✅

---

## Project Structure

```
PyFinanceTracker_APP/
├── backend_v2/                    # FastAPI Backend (Python)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                # FastAPI app setup
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── stock.py           # Pydantic models
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── stock_fetcher.py   # Stock data service
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── stocks.py          # API endpoints
│   │   └── utils/                 # Utility functions (future)
│   ├── main.py                    # Entry point
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example               # Environment template
│   └── .env                       # Environment config
│
├── frontend_v2/                   # React SPA
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── index.js               # React entry point
│   │   ├── App.jsx                # Main app component
│   │   ├── components/
│   │   │   ├── StockCard.jsx      # Stock display card
│   │   │   ├── StockList.jsx      # Stock list container
│   │   │   └── StockChart.jsx     # Chart component
│   │   ├── services/
│   │   │   └── api.js             # API communication
│   │   ├── hooks/
│   │   │   └── useStockData.js    # Custom React hook
│   │   └── styles/
│   │       ├── index.css          # Global styles
│   │       ├── App.css
│   │       ├── StockCard.css
│   │       ├── StockList.css
│   │       └── StockChart.css
│   ├── package.json
│   ├── .env.example
│   └── .env
│
├── start.bat                      # Windows startup script
└── start.sh                       # Unix startup script
```

---

## Backend - FastAPI v2.0

### Key Features

1. **Unified Python Stack**: All backend logic in Python (no subprocess calls)
2. **Type Safety**: Pydantic models for request/response validation
3. **Auto Documentation**: Swagger UI at `/docs`
4. **Better Structure**: Modular design with services, models, routes
5. **Performance**: Async-ready FastAPI framework

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/top-stocks` | GET | Fetch top 5 performers with OHLC data |
| `/api/watchlist` | GET | Fetch watchlist stocks with OHLC data |
| `/api/stock/{symbol}` | GET | Get detailed OHLC data for a stock |
| `/api/health` | GET | Health check endpoint |
| `/docs` | GET | Swagger API documentation |

#### Query Parameters

- **top-stocks**:
  - `limit` (int, 10-500): Number of stocks to analyze (default: 50)
  - `delay` (float, 0.1-5.0): Delay between API calls in seconds (default: 0.7)

- **watchlist**:
  - `delay` (float, 0.1-5.0): Delay between API calls in seconds (default: 0.5)

- **stock/{symbol}**:
  - `period` (str): Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)

### Installation & Setup

```bash
# Navigate to backend directory
cd backend_v2

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (optional)
copy .env.example .env

# Run the server
python main.py
```

The backend will be available at `http://localhost:5000`

---

## Frontend - React SPA v2.0

### Key Features

1. **Single Page Application**: No proxy needed, direct API calls
2. **Modern React**: Functional components with hooks
3. **Dark Theme**: Professional dark UI with accent colors
4. **Responsive Design**: Works on desktop, tablet, and mobile
5. **Real-time Charts**: Using Recharts for OHLC visualization
6. **Error Handling**: Comprehensive error states and fallbacks

### Components

- **App.jsx**: Main application container with tab navigation
- **StockList**: Sidebar list of stocks with refresh functionality
- **StockCard**: Individual stock card with performance metrics
- **StockChart**: OHLC line chart and bar chart visualization

### Hooks

- **useStockData**: Custom hook for fetching and managing stock data

### Installation & Setup

```bash
# Navigate to frontend directory
cd frontend_v2

# Install dependencies
npm install

# Create .env file (optional)
copy .env.example .env

# Start development server
npm start
```

The frontend will be available at `http://localhost:3000`

---

## Quick Start

### Option 1: Using Batch Script (Windows)

```bash
# From PyFinanceTracker_APP directory
start.bat
```

This will:
1. Open a terminal for the FastAPI backend
2. Open a terminal for the React frontend
3. Automatically start both services

### Option 2: Using Shell Script (macOS/Linux)

```bash
# From PyFinanceTracker_APP directory
chmod +x start.sh
./start.sh
```

### Option 3: Manual Setup

**Terminal 1 - Backend:**
```bash
cd backend_v2
pip install -r requirements.txt
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend_v2
npm install
npm start
```

### Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000/api
- **API Documentation**: http://localhost:5000/docs
- **API ReDoc**: http://localhost:5000/redoc

---

## Testing the API

### Using curl (Windows Command Prompt)

```bash
# Test backend health
curl http://localhost:5000/api/health

# Get top stocks
curl "http://localhost:5000/api/top-stocks?limit=50&delay=0.7"

# Get watchlist
curl "http://localhost:5000/api/watchlist?delay=0.5"

# Get specific stock data
curl "http://localhost:5000/api/stock/AAPL?period=7d"
```

### Using Swagger UI

1. Navigate to http://localhost:5000/docs
2. Click on each endpoint to see documentation
3. Use the "Try it out" button to test endpoints
4. View request/response formats and parameters

### Expected Response Format

```json
{
  "top_stocks": [
    {
      "symbol": "NVDA",
      "company_name": "NVIDIA Corporation",
      "percentage_change": 3.45,
      "current_price": 875.30,
      "previous_close": 847.50
    }
  ],
  "ohlc_data": {
    "NVDA": [
      {
        "date": "2024-01-15",
        "open": 840.00,
        "high": 880.50,
        "low": 835.00,
        "close": 875.30
      }
    ]
  },
  "fetched_at": "2024-01-16T14:30:00.123456"
}
```

---

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'yfinance'`
```bash
cd backend_v2
pip install -r requirements.txt
```

**Problem**: Port 5000 already in use
```bash
# Change port in .env or command line
PORT=5001 python main.py
```

**Problem**: Python not found
- Ensure Python 3.8+ is installed
- On Windows, add Python to PATH or use full path to python.exe

### Frontend Issues

**Problem**: `npm: command not found`
- Install Node.js and npm from https://nodejs.org/

**Problem**: Module not found errors
```bash
cd frontend_v2
rm -rf node_modules package-lock.json
npm install
```

**Problem**: Port 3000 already in use
```bash
# Set custom port
set PORT=3001 && npm start  # Windows
PORT=3001 npm start         # macOS/Linux
```

**Problem**: API connection failed
- Ensure backend is running on port 5000
- Check `.env` file for `REACT_APP_API_URL`

---

## Performance Tips

1. **Backend Delay**: Increase `delay` parameter to respect API rate limits
   - Default 0.7s is safe for yfinance
   - Reduce to 0.5s for faster responses
   - Increase to 1.0s if hitting rate limits

2. **Stock Limit**: Balance between data coverage and speed
   - Default 50 stocks
   - Increase to 100-500 for more data (slower)
   - Decrease to 20 for faster responses

3. **Chart Updates**: Charts are cached until refresh button clicked
   - Reduces unnecessary API calls
   - Improves UI responsiveness

---

## Environment Variables

### Backend (.env)
```
HOST=0.0.0.0
PORT=5000
DEBUG=False
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:5000/api
```

---

## Dependencies

### Backend
- **fastapi**: Modern async web framework
- **uvicorn**: ASGI server
- **pydantic**: Data validation
- **yfinance**: Stock data fetching
- **pandas**: Data manipulation
- **python-dotenv**: Environment config

### Frontend
- **react**: UI library
- **react-dom**: DOM rendering
- **react-scripts**: Build tools
- **recharts**: Chart library
- **web-vitals**: Performance metrics

---

## Future Enhancements

1. **Database**: Add SQLite/PostgreSQL for caching historical data
2. **Authentication**: User accounts and personalized watchlists
3. **Notifications**: Alert users to stock price changes
4. **Advanced Charts**: More chart types and technical indicators
5. **Mobile App**: React Native mobile version
6. **WebSocket**: Real-time price updates
7. **Export**: Download stock data as CSV/Excel
8. **Comparison**: Compare multiple stocks side-by-side

---

## Differences from v1.0

| Aspect | v1.0 | v2.0 |
|--------|------|------|
| Backend | Node.js/Express | FastAPI (Python) |
| Task Running | Child process | Direct service |
| Architecture | Proxy pattern | Direct SPA |
| Type Safety | Minimal | Pydantic models |
| API Docs | Manual | Auto-generated Swagger |
| Performance | Good | Better (async) |
| Code Structure | Monolithic | Modular |
| Development | JavaScript | Python unified stack |

---

## License & Credits

Stock data sourced from yfinance (Yahoo Finance)

---

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Check application logs in terminal windows
4. Verify all dependencies are installed correctly
