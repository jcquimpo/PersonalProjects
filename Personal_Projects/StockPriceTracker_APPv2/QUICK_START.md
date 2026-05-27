# Quick Start Guide

Get the Stock Price Tracker web app running in 5 minutes!

## Step 1: Get Finnhub API Key (2 min)

1. Visit [https://finnhub.io](https://finnhub.io)
2. Click "Sign up" (free tier available)
3. Copy your API key from dashboard

## Step 2: Setup Environment (1 min)

```bash
# Navigate to project folder
cd StockPriceTracker_APPv2

# Create .env file with your API key
echo FINNHUB_API_KEY=your_key_here > .env
```

### Windows (PowerShell):
```powershell
"FINNHUB_API_KEY=your_key_here" | Out-File -Encoding utf8 .env
```

## Step 3: Install Dependencies (2 min)

```bash
pip install -r requirements.txt
```

## Step 4: Run the App

```bash
python app.py
```

**Output:**
```
================================================================================
 📊 STOCK PRICE TRACKER WEB APPLICATION
================================================================================

  Starting Flask app...
  🌐 Navigate to: http://localhost:5000
  📊 Dashboard: http://localhost:5000/dashboard

  Press Ctrl+C to stop
```

## Step 5: Open in Browser

- **Home**: [http://localhost:5000](http://localhost:5000)
- **Dashboard**: [http://localhost:5000/dashboard](http://localhost:5000/dashboard)

## What You'll See

### Home Page
- 🔥 Top 5 daily movers with scores
- 💼 Your watchlist (AAPL, NVDA, MSFT, META, GOOGL)
- ⭐ Top pick recommendations
- 📊 Portfolio strategy tips

### Dashboard
- 📈 Interactive price charts (7-day)
- 📊 Rebased performance comparison
- 💹 Watchlist daily changes
- 📋 Detailed data tables

## Features in Action

### 1. Refresh Data
Click "Refresh Data" button to get latest quotes (respects 2s delays)

### 2. View Charts
- Hover over charts for details
- Charts auto-update every 5 minutes
- Click legend to show/hide symbols

### 3. Read Recommendations
- 🟢 **BUY**: Score > 5 (strong momentum)
- 🟡 **HOLD**: Score 2-5 (moderate)
- 🔴 **AVOID**: Score < 2 (weak)

## Common Issues & Solutions

### Issue: API Key Error
```
ValueError: FINNHUB_API_KEY not set.
```
**Fix**: Make sure `.env` file exists and contains your key

### Issue: Slow Loading
- **Cause**: First API call scans 50 S&P 500 stocks
- **Fix**: Wait 2 minutes for first scan (rate limiting)
- **Workaround**: Reduce `SCAN_LIMIT` in `app.py`

### Issue: Port Already in Use
```
Address already in use
```
**Fix**: Kill Flask or change port:
```python
# In app.py, change:
app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead
```

### Issue: No Charts Display
- **Cause**: Plotly CDN not loading
- **Fix**: Ensure internet connection
- **Alternative**: Refresh page

## Configuration Tips

### Change Watchlist
Edit `app.py`:
```python
WATCHLIST = ["AAPL", "NVDA", "MSFT", "META", "GOOGL"]
# Add/remove symbols here
```

### Change Lookback Period
```python
OHLC_DAYS = 7  # Change to 5, 10, 14, 30, etc.
```

### Change Scan Size
```python
SCAN_LIMIT = 50  # Reduce to 30 for faster loading
TARGET_MOVERS = 5  # Top N movers to display
```

## Next Steps

✅ **Getting comfortable?** Try these:

1. **Customize Watchlist** → Edit `WATCHLIST` variable
2. **Change Chart Type** → Edit Plotly functions
3. **Add Email Alerts** → Integrate email service
4. **Deploy Online** → Use Heroku, AWS, DigitalOcean

📖 **Learn more:**
- Read `README.md` for full documentation
- Check `app.py` for API endpoints
- Review scoring methodology section

## Need Help?

1. **Check logs**: Flask prints errors to console
2. **Browser console**: Press F12 for JavaScript errors
3. **Verify setup**: Make sure `.env` file exists
4. **Test API**: Visit [http://localhost:5000/api/data](http://localhost:5000/api/data)

## Performance Expectations

| First Load | Refresh | Charts | Notes |
|-----------|---------|--------|-------|
| 2-3 min | 30-60s | 10-15s | Rate-limited API calls |

💡 **Tip**: Use Dashboard for faster browsing (data cached)

---

## API Endpoints for Testing

```bash
# Get latest data
curl http://localhost:5000/api/data

# Get recommendations
curl http://localhost:5000/api/recommendations

# Get chart data
curl http://localhost:5000/api/charts

# Health check
curl http://localhost:5000/health
```

---

**Ready to invest? 📈 Good luck and remember to do your own research!**

⚠️ Disclaimer: This is educational analysis only. Always consult a financial advisor.
