# Stock Tracker Dashboard

A modern React dashboard for displaying stock market analysis, including top movers, OHLC data, and watchlist monitoring.

## Features

- **Top 5 Movers**: Display the top 5 stocks by percentage change with visual indicators
- **OHLC Charts**: Interactive line charts showing Open, High, Low, and Close prices over 7 days
- **Price Data Tables**: Detailed price tables for each stock with daily breakdowns
- **Watchlist Monitor**: Track custom watchlist with expandable detailed price information
- **Responsive Design**: Mobile-friendly layout that works on all devices
- **Dark Theme**: Modern dark UI with blue accent colors

## Project Structure

```
dashboard/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── TopMovers.jsx
│   │   ├── TopMovers.css
│   │   ├── OHLCData.jsx
│   │   ├── OHLCData.css
│   │   ├── WatchlistMonitor.jsx
│   │   └── WatchlistMonitor.css
│   ├── data/
│   │   └── mockData.js
│   ├── App.jsx
│   ├── App.css
│   ├── index.js
│   └── index.css
├── package.json
└── README.md
```

## Installation & Setup

### Prerequisites
- Node.js 14+ and npm installed
- Python script (`Top_Stocks.py`) running and accessible via API endpoint

### 1. Install Dependencies

```bash
cd dashboard
npm install
```

### 2. Start Development Server

```bash
npm start
```

The app will open at `http://localhost:3000`

### 3. Production Build

```bash
npm run build
```

Creates an optimized production build in the `build/` folder.

## Integration with Python Script

The dashboard currently uses mock data. To integrate with your `Top_Stocks.py` script:

### Option 1: Create a Backend API

Create a simple Express.js server in the `backend/` directory:

```javascript
// backend/server.js
const express = require('express');
const { spawn } = require('child_process');
const cors = require('cors');

const app = express();
app.use(cors());

app.get('/api/stocks', (req, res) => {
  const python = spawn('python', ['../Top_Stocks.py']);
  
  let data = '';
  python.stdout.on('data', (chunk) => {
    data += chunk.toString();
  });
  
  python.on('close', () => {
    // Parse data and send as JSON
    res.json(parseStockData(data));
  });
});

app.listen(5000, () => console.log('Server running on port 5000'));
```

### Option 2: Modify Python Script Output

Modify `Top_Stocks.py` to output JSON:

```python
import json

# At the end of Top_Stocks.py, add:
output = {
    'top5Symbols': top5_symbols,
    'top5Performance': top5_performance,
    'ohlcData': ohlc_dict,
    'watchlistPerformance': results,
    'watchlistOHLC': watchlist_ohlc_dict
}

print(json.dumps(output, default=str))
```

### Update mockData.js

Replace the mock data in `src/data/mockData.js` with actual API calls:

```javascript
// src/data/mockData.js
export const fetchStockData = async () => {
  const response = await fetch('http://localhost:5000/api/stocks');
  return response.json();
};
```

Then update `App.jsx`:

```javascript
useEffect(() => {
  fetchStockData().then(data => {
    setData(data);
    setLoading(false);
  });
}, []);
```

## Components

### TopMovers
Displays the top 5 stock movers in a card grid with:
- Rank indicator
- Stock symbol and company name
- Percentage change with visual indicators
- Color-coded positive (green) / negative (red)

### OHLCData
Interactive component with:
- Symbol selector buttons for switching between stocks
- Line chart showing Open, High, Low, Close prices
- Detailed price data table
- Responsive chart container

### WatchlistMonitor
Expandable watchlist items with:
- Quick view of symbol, company name, and daily performance
- Expandable sections showing detailed OHLC tables
- 7-day high/low statistics
- Collapsible design to reduce clutter

## Customization

### Colors
Edit the color variables in CSS files:
- Primary blue: `#3b82f6`, `#60a5fa`
- Success green: `#22c55e`
- Danger red: `#ef4444`
- Background: `#0f172a`, `#1e293b`

### Data Source
Update `mockData.js` to connect to your actual data source.

### Company Names
Edit the `SYMBOL_NAMES` object in components to add more stock symbols and company names.

## Performance Optimization

- Uses React hooks for efficient state management
- Lazy loads chart data when symbols are selected
- Memoization for expensive computations
- CSS-based animations instead of JavaScript

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers

## Dependencies

- **react**: UI framework
- **react-dom**: DOM rendering
- **chart.js**: Charting library
- **react-chartjs-2**: React wrapper for Chart.js

## Future Enhancements

- Real-time data updates with WebSockets
- Historical data comparison
- Custom alert notifications
- Portfolio tracking
- Export functionality (CSV, PDF)
- Dark/Light theme toggle
- Advanced technical indicators

## Troubleshooting

**Port 3000 already in use:**
```bash
PORT=3001 npm start
```

**CORS errors when fetching data:**
Ensure your backend has proper CORS headers configured.

**Charts not displaying:**
Check browser console for errors. Ensure Chart.js is properly imported.

## License

MIT
