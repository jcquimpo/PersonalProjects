# Stock Dashboard

A full-featured React dashboard for real-time stock tracking and analysis, built from your TopStocksv3.ipynb project.

## Features

- 📈 **Real-time Stock Data**: Fetch and display top 5 performing stocks
- 📌 **Watchlist Tracking**: Monitor your favorite stocks (AAPL, NVDA, MSFT, META, GOOGL)
- 📊 **Interactive Charts**: Visualize OHLC (Open, High, Low, Close) data with 7-day trends
- 🎨 **Beautiful UI**: Dark theme dashboard with responsive design
- 🔄 **Live Updates**: Refresh data with one click
- 📱 **Mobile Friendly**: Fully responsive layout

## Project Structure

```
StockDashboard/
├── frontend/              # React application
│   ├── public/           # Static assets
│   ├── src/
│   │   ├── components/   # React components (StockCard, StockChart)
│   │   ├── styles/       # CSS files
│   │   ├── App.jsx       # Main app component
│   │   └── index.jsx     # Entry point
│   └── package.json
└── backend/              # Node.js/Express API server
    ├── server.js         # Express server
    ├── stock_fetcher.py  # Python script for stock data fetching
    └── package.json
```

## Setup Instructions

### Prerequisites

- Node.js (v14+)
- Python 3.7+
- Required Python packages: `yfinance`, `pandas`, `pytickersymbols`

### Installation

#### 1. Backend Setup

```bash
cd backend

# Install Node dependencies
npm install

# Install Python dependencies
pip install yfinance pandas pytickersymbols
```

#### 2. Frontend Setup

```bash
cd frontend

# Install React dependencies
npm install
```

### Running the Application

#### Terminal 1: Start Backend Server

```bash
cd backend
npm start
```

The backend will run on `http://localhost:5000`

#### Terminal 2: Start React Frontend

```bash
cd frontend
npm start
```

The React app will open at `http://localhost:3000`

## Usage

1. **View Top 5 Performers**: The dashboard automatically displays the top 5 stocks by daily percentage change
2. **Check Watchlist**: See your monitored stocks in the separate watchlist section
3. **Refresh Data**: Click the "🔄 Refresh" button to update stock data
4. **View Charts**: Select any stock to see detailed OHLC charts and 7-day trends
5. **Symbol Selection**: Click on any stock in the sidebar to view its details

## API Endpoints

### `/api/top-stocks`
Fetches top 5 performing stocks with OHLC data
- Query params: `limit` (default: 50), `delay` (default: 0.7)

### `/api/watchlist`
Fetches watchlist stocks with OHLC data
- Query params: `delay` (default: 0.5)

### `/api/stock/:symbol`
Fetches specific stock OHLC data
- Query params: `period` (default: '7d')

## Customization

### Change Watchlist

Edit `backend/stock_fetcher.py`:

```python
WATCHLIST = ["AAPL", "NVDA", "MSFT", "META", "GOOGL"]
SYMBOL_NAMES = {
    "AAPL": "Apple Inc.",
    "NVDA": "NVIDIA Corporation",
    # Add/modify symbols here
}
```

### Modify Colors and Themes

Edit `frontend/src/App.css` to customize colors, spacing, and layouts.

## Performance Notes

- First load may take 30-60 seconds while fetching data from Yahoo Finance
- Rate limiting is built in (0.5-0.7s delay between API calls)
- Data is cached in the browser for smooth interactions

## Troubleshooting

**Backend won't start**
- Ensure Python and Node.js are installed
- Check if port 5000 is available
- Verify Python dependencies: `pip install yfinance pandas pytickersymbols`

**No stock data displaying**
- Front-end will display "no data" if the Python script fails
- Check browser console for API errors
- Verify internet connection for Yahoo Finance API

**Charts not showing**
- Recharts library should auto-install with npm
- Try clearing browser cache and reloading

## Future Enhancements

- [ ] Real-time WebSocket updates
- [ ] Historical data export (CSV/PDF)
- [ ] Custom alerts and notifications
- [ ] Portfolio tracking
- [ ] Advanced technical indicators (RSI, MACD, Bollinger Bands)
- [ ] User authentication and settings persistence

## License

MIT
