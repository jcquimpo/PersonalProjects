# Stock Analysis Flask Dashboard

A professional web-based investment analysis tool that displays stock price data, market movers, and AI-powered investment recommendations.

## Features

- 🔥 **Daily Movers Analysis**: Identify top-performing S&P 500 stocks
- 📊 **OHLC Data Visualization**: 7-day price charts with multiple chart types
- ⭐ **Watchlist Tracking**: Monitor AAPL, NVDA, MSFT, META, GOOGL
- 🎯 **Investment Scoring**: AI-powered momentum and stability analysis
- 💡 **Smart Recommendations**: Buy/Hold/Avoid signals
- 📈 **Interactive Dashboards**: Real-time data visualization with Chart.js

## Project Structure

```
StockPriceTracker_APPv2/
├── flask_app.py                 # Main Flask application
├── StockPriceTracker_appv2.py  # Analysis engine
├── requirements-flask.txt        # Python dependencies
├── static/
│   ├── style.css               # Dashboard styling
│   └── main.js                 # Frontend JavaScript
└── templates/
    ├── base.html               # Base template (navbar, layout)
    ├── index.html              # Home page
    ├── dashboard.html          # Main dashboard
    ├── movers.html             # Top movers page
    ├── watchlist.html          # Watchlist page
    ├── recommendations.html    # Investment recommendations
    ├── about.html              # About page
    └── error.html              # Error page
```

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements-flask.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the project directory:

```
FINNHUB_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

Get your free Finnhub API key at: https://finnhub.io

### 3. Run the Flask App

```bash
python flask_app.py
```

The app will start on `http://localhost:5000`

## Usage

### Home Page (`/`)
- Click "Start Analysis" to begin the stock analysis
- View stats about data sources and features
- Access different sections via navigation menu

### Running Analysis
1. Click the "Start Analysis" or "Run New Analysis" button
2. Analysis runs in the background (takes 2-3 minutes)
3. Dashboard updates automatically when complete

### Dashboard (`/dashboard`)
- View top 5 movers rankings
- See investment scores with charts
- Monitor daily performance

### Top Movers (`/movers`)
- Explore S&P 500 daily movers
- View performance charts
- Check investment scores and recommendations

### Watchlist (`/watchlist`)
- Track favorite stocks: AAPL, NVDA, MSFT, META, GOOGL
- Compare daily % changes
- View trend analysis vs moving averages

### Recommendations (`/recommendations`)
- Get top mover pick with rationale
- Get watchlist pick with analysis
- View complete portfolio strategy guide
- See full ranking of all stocks

### About (`/about`)
- Learn how the algorithm works
- Understand scoring methodology
- Read important disclaimer
- View technology stack

## API Endpoints

- `GET /` - Home page
- `GET /dashboard` - Main dashboard
- `GET /movers` - Top movers page
- `GET /watchlist` - Watchlist page
- `GET /recommendations` - Recommendations page
- `GET /about` - About page
- `POST /api/run-analysis` - Start analysis
- `GET /api/status` - Get analysis status
- `GET /api/results` - Get analysis results
- `GET /api/chart-data/<type>` - Get chart data

## Scoring Algorithm

### Movers Score
```
Score = (Daily % + 7-Day %) × 0.6 + (100 / Volatility) × 0.4
BUY: Score > 5
HOLD: Score > 2
AVOID: Score ≤ 2
```

### Watchlist Score
```
Score = (7-Day % × 0.5) + (vs 7-MA % × 0.5)
BUY/HOLD: Score > 1
HOLD: Score > -1
SELL: Score ≤ -1
```

## Portfolio Strategy

**Recommended allocation:**
- **Movers (5-10%)**: High-risk, high-reward opportunities
- **Watchlist (40-60%)**: Stable, established holdings
- **Cash (10-20%)**: Reserves and opportunities

## Important Disclaimer

⚠️ **EDUCATIONAL USE ONLY**

This tool is for educational purposes only and is NOT financial advice. Past performance does not guarantee future results. Always:
- Conduct your own independent research
- Understand your risk tolerance
- Diversify your portfolio
- Consult with a qualified financial advisor
- Only invest money you can afford to lose

## Data Sources

- **Finnhub API**: Real-time stock quotes (https://finnhub.io)
- **yfinance**: Historical OHLC data from Yahoo Finance
- **PyTickerSymbols**: S&P 500 ticker list

## Requirements

- Python 3.8+
- Flask 2.3.3+
- pandas 2.1.1+
- yfinance 0.2.32+
- requests 2.31.0+
- Finnhub API key (free tier available)

## Troubleshooting

### "FINNHUB_API_KEY not set"
- Create a `.env` file with your API key
- Or set environment variable: `export FINNHUB_API_KEY=your_key`

### Analysis takes too long
- Normal analysis takes 2-3 minutes
- Free Finnhub tier has rate limits
- Watchlist stock limits to 5 to avoid timeouts

### Charts not loading
- Check browser console for errors
- Ensure JavaScript is enabled
- Try clearing browser cache

### No data available
- Click "Run New Analysis" first
- Wait for analysis to complete
- Check if Finnhub API is accessible

## Performance Tips

- Run analysis during market hours (9:30 AM - 4:00 PM ET)
- Avoid running multiple analyses simultaneously
- Cache analysis results for 30 minutes
- Use Chrome/Firefox for best visualization

## Future Enhancements

- [ ] Real-time data streaming
- [ ] Custom watchlist management
- [ ] Historical analysis trends
- [ ] Export to CSV/PDF reports
- [ ] Mobile responsive improvements
- [ ] Dark mode theme
- [ ] Email alerts for recommendations
- [ ] Multi-user support with authentication

## License

Educational Use Only - Not for Commercial Use

## Support

For issues or questions:
1. Check the About page for algorithm details
2. Review the Disclaimer and Risk Warning
3. Verify Finnhub API key and rate limits
4. Check browser console for JavaScript errors

## Version

Dashboard Version: 1.0
Last Updated: 2026-05-27
