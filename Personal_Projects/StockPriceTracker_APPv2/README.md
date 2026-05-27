# Stock Price Tracker Web Application

A modern Flask-based web application for real-time stock analysis, visualization, and investment recommendations.

## Features

✨ **Core Features:**
- 📊 Real-time S&P 500 daily movers scanning
- 📈 Interactive Plotly charts
- 💼 Watchlist monitoring (AAPL, NVDA, MSFT, META, GOOGL)
- 🎯 AI-powered investment scoring & recommendations
- 💡 Portfolio strategy guidance
- 🎨 Responsive Bootstrap UI

## Architecture

```
StockPriceTracker_APPv2/
├── app.py                    # Flask application & API endpoints
├── requirements.txt          # Python dependencies
├── templates/
│   ├── base.html            # Base template with navbar/footer
│   ├── index.html           # Home page with data tables
│   └── dashboard.html       # Dashboard with interactive charts
└── static/                  # CSS/JS assets (optional)
```

## Installation

### 1. Get API Key

Visit [Finnhub.io](https://finnhub.io) and sign up for a free API key.

### 2. Setup Environment

```bash
# Navigate to project directory
cd StockPriceTracker_APPv2

# Create .env file
echo FINNHUB_API_KEY=<your_key_here> > .env
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Application

```bash
python app.py
```

Access the app at: **http://localhost:5000**

## Pages & Routes

### Home Page (`/`)
- Overview of top movers & watchlist
- Quick recommendations
- Portfolio strategy tips
- Data tables with investment scores

### Dashboard (`/dashboard`)
- Interactive Plotly charts:
  - Top movers close price (7-day)
  - Rebased performance comparison
  - Watchlist daily % change
  - Watchlist price trends
- Detailed data tables
- Auto-refresh every 5 minutes

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/data` | GET | Returns top movers & watchlist data |
| `/api/charts` | GET | Returns Plotly chart JSON |
| `/api/recommendations` | GET | Returns investment recommendations |
| `/health` | GET | Health check |

## Data Flow

```
1. S&P 500 Scanning (Finnhub API)
   └─ Fetch top daily movers
   
2. OHLC Data Fetching (yfinance)
   └─ 7-day historical price data
   
3. Analysis & Scoring
   ├─ Momentum calculation (60% weight)
   ├─ Trend stability (40% weight)
   └─ Investment recommendations
   
4. Visualization
   └─ Interactive Plotly charts
   
5. Web Display
   └─ Bootstrap responsive UI
```

## Scoring Methodology

### Top Movers Score
```
Score = (Momentum × 0.6) + (Stability × 0.4)

Where:
  Momentum = (Today% + 7Day%) / 2
  Stability = 100 / (Volatility% + 1)
```

**Recommendations:**
- 🟢 **BUY**: Score > 5 (strong momentum + low volatility)
- 🟡 **HOLD**: Score 2-5 (moderate momentum)
- 🔴 **AVOID**: Score < 2 (weak signals)

### Watchlist Score
```
Score = (7Day% × 0.5) + (vs MA% × 0.5)
```

**Recommendations:**
- 🟢 **BUY/HOLD**: Score > 1 (positive trend)
- 🟡 **HOLD**: Score -1 to 1 (neutral)
- 🔴 **CONSIDER SELLING**: Score < -1 (downtrend)

## Configuration

Edit `app.py` to customize:

```python
# Data parameters
OHLC_DAYS = 7              # Historical lookback (days)
SCAN_LIMIT = 50            # S&P 500 tickers to scan
TARGET_MOVERS = 5          # Top movers to display

# Watchlist
WATCHLIST = ["AAPL", "NVDA", "MSFT", "META", "GOOGL"]

# Price filters
MIN_PRICE = 0.01
MAX_PRICE = 100000.0
```

## Rate Limiting

- **Finnhub**: Free tier limited to 60 requests/minute
- **Automatic backoff**: Exponential retry with 2s delays
- **Monitoring**: Request count displayed in output

## Performance Tips

1. **Increase refresh interval**: Edit dashboard auto-refresh (5 min default)
2. **Reduce scan limit**: Fewer S&P 500 tickers = faster load
3. **Cache data**: Add Redis/database layer for production
4. **Async processing**: Use Celery for background tasks

## Troubleshooting

### API Key Error
```
ValueError: FINNHUB_API_KEY not set.
```
**Solution**: Create `.env` file with your Finnhub API key

### Data Loading Issues
```
Error loading data. Please check the console.
```
**Solutions**:
- Check Finnhub API key validity
- Verify internet connection
- Check request count (max 60/min)
- Review browser console for errors

### Chart Rendering Issues
- Ensure Plotly CDN is accessible
- Check browser console for errors
- Try refreshing the page

## Deployment

### Heroku
```bash
heroku create stock-tracker-app
git push heroku main
heroku config:set FINNHUB_API_KEY=<your_key>
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## Security Notes

⚠️ **Important:**
- Never commit `.env` file to version control
- Use environment variables in production
- Validate user inputs on API endpoints
- Implement CSRF protection for forms
- Use HTTPS in production

## API Data Sources

- **Finnhub**: Real-time quotes, S&P 500 screener
- **Yahoo Finance**: Historical OHLC data
- **PyTickerSymbols**: S&P 500 ticker list

## Disclaimer

⚠️ **Educational Purpose Only**

This application provides analysis and recommendations for educational purposes only. It is **NOT financial advice**. 

- Always consult a licensed financial advisor
- Conduct thorough research before investing
- Past performance ≠ future results
- Manage risk appropriately
- Start with small positions

## License

MIT License - Feel free to use and modify

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review browser console for errors
3. Check Flask server logs
4. Verify API key and limits

## Future Enhancements

📝 Planned features:
- User authentication & portfolios
- Email alerts for price changes
- Advanced technical indicators
- Machine learning predictions
- Mobile app
- Database persistence
- Backtesting engine
- Options analysis

---

**Happy Trading! 📈**

Remember: Invest responsibly, do your research, and never risk more than you can afford to lose.
