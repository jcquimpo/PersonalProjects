# Quick Start Guide - Stock Tracker Dashboard

Get your React dashboard up and running in 3 steps!

## Step 1: Install Dependencies

Navigate to the dashboard folder and install all required packages:

```bash
cd dashboard
npm install
```

This installs React, React DOM, Chart.js, and other dependencies listed in `package.json`.

## Step 2: Start the Development Server

```bash
npm start
```

This will:
- Start the React development server
- Automatically open http://localhost:3000 in your browser
- Enable hot reloading (changes save automatically)

## Step 3: Explore the Dashboard

You should see:
1. **Top 5 Movers** - Cards showing the top performing stocks
2. **OHLC Charts** - Interactive price charts with data tables
3. **Watchlist Monitor** - Expandable watchlist items

## Available Scripts

- `npm start` - Start development server
- `npm build` - Create production build
- `npm test` - Run tests (if configured)

## Connecting to Your Python Script

Currently, the dashboard uses mock data. To connect it to your actual `Top_Stocks.py`:

### Simple Option: Redirect Output to JSON File

Modify your Python script to output JSON:

```python
# At the end of Top_Stocks.py
import json

output = {
    'top5Symbols': top5_symbols,
    'top5Performance': top5_performance,
    'ohlcData': ohlc_data,
    'watchlistPerformance': results,
    'watchlistOHLC': watchlist_ohlc_data
}

with open('stock_data.json', 'w') as f:
    json.dump(output, f, default=str)
```

Then in `src/data/mockData.js`, load this JSON file:

```javascript
import stockData from '../../stock_data.json';
export default stockData;
```

### Advanced Option: Create a Backend API

See the Integration section in [README.md](./README.md) for setting up a Node.js backend server.

## File Structure Overview

```
dashboard/
├── public/          # Static files
├── src/
│   ├── components/  # React components (TopMovers, OHLCData, WatchlistMonitor)
│   ├── data/        # Mock data and data utilities
│   ├── App.jsx      # Main app component
│   └── index.js     # Entry point
├── package.json     # Dependencies
└── README.md        # Full documentation
```

## Troubleshooting

**"npm: command not found"**
- Install Node.js from https://nodejs.org/

**Port 3000 is already in use**
- Use: `PORT=3001 npm start`
- Or kill the process using port 3000

**Charts not showing**
- Check browser console (F12) for errors
- Ensure all dependencies installed correctly with `npm install`

**Hot reload not working**
- Try stopping and restarting the server with `npm start`

## Next Steps

1. **Customize mock data** in `src/data/mockData.js`
2. **Connect to your Python script** following the integration guide
3. **Modify styling** in the `.css` files to match your preferences
4. **Add more features** like real-time updates or additional metrics

## Additional Resources

- React docs: https://react.dev
- Chart.js docs: https://www.chartjs.org
- Tailwind CSS (optional styling): https://tailwindcss.com

Need help? Check [README.md](./README.md) for detailed documentation!
