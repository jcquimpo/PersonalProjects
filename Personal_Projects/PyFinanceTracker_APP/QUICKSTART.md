# Quick Start Guide for Stock Dashboard

## 🚀 Getting Started

### Step 1: Install Dependencies

**Backend:**
```bash
cd backend
npm install
pip install yfinance pandas pytickersymbols
```

**Frontend:**
```bash
cd frontend
npm install
```

### Step 2: Start Backend

```bash
cd backend
npm start
```

Expected output:
```
Stock Dashboard Backend running on http://localhost:5000
```

### Step 3: Start Frontend (in new terminal)

```bash
cd frontend
npm start
```

Your browser should open to `http://localhost:3000`

## 📊 Dashboard Overview

- **Left Sidebar**: Quick view and selection of stocks
  - Top 5 performers
  - Your watchlist
- **Main Area**: Detailed view with charts
  - OHLC trend line chart
  - Closing price bar chart
  - Stock statistics

## 🎯 Key Features

1. **Real-time Data**: Fetches latest stock data from Yahoo Finance
2. **7-Day Charts**: Visualize historical trends
3. **Two Views**: Separate top performers and watchlist sections
4. **Responsive Design**: Works on desktop and tablets
5. **One-Click Refresh**: Update all data instantly

## 🛠 Development

- Modify watchlist in `backend/stock_fetcher.py`
- Customize colors in `frontend/src/App.css`
- Add new components in `frontend/src/components/`

## 📝 Notes

- First load takes time while fetching from Yahoo Finance API
- Rate limiting protects against API throttling
- Data is live and real-time

Happy tracking! 📈
