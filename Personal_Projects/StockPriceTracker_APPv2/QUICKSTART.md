# 🚀 Quick Start Guide - Flask Dashboard

## Step 1: Install Dependencies

Open PowerShell in the `StockPriceTracker_APPv2` directory and run:

```powershell
pip install -r requirements-flask.txt
```

## Step 2: Get Finnhub API Key

1. Visit https://finnhub.io
2. Sign up for a free account
3. Get your API key from the dashboard

## Step 3: Create .env File

Create a file named `.env` in the `StockPriceTracker_APPv2` directory with:

```
FINNHUB_API_KEY=your_api_key_here
SECRET_KEY=dev-secret-key-change-in-production
```

Replace `your_api_key_here` with your actual Finnhub API key.

## Step 4: Run the Flask App

In PowerShell, from the `StockPriceTracker_APPv2` directory:

```powershell
python flask_app.py
```

You should see:
```
================================================================================
 🌐 Stock Analysis Flask Dashboard
================================================================================

  Starting Flask app on http://localhost:5000
  Press Ctrl+C to stop
```

## Step 5: Open in Browser

Open your browser and go to:
```
http://localhost:5000
```

## Step 6: Run Analysis

1. Click the **"Start Analysis"** button on the home page
2. Wait 2-3 minutes for analysis to complete
3. View results on the Dashboard

## File Structure

```
StockPriceTracker_APPv2/
├── flask_app.py                    ← Main Flask app (run this)
├── StockPriceTracker_appv2.py     ← Analysis engine (imported by flask_app.py)
├── requirements-flask.txt          ← Python packages
├── .env                            ← Your API key (create this)
├── static/
│   ├── style.css                  ← Dashboard styling
│   └── main.js                    ← Frontend JavaScript
└── templates/
    ├── base.html                  ← Layout template
    ├── index.html                 ← Home page
    ├── dashboard.html             ← Main dashboard
    ├── movers.html                ← Top movers
    ├── watchlist.html             ← Watchlist
    ├── recommendations.html       ← Recommendations
    ├── about.html                 ← About/Help
    └── error.html                 ← Error pages
```

## Dashboard Pages

### Home (http://localhost:5000/)
- Start analysis
- View quick stats
- Learn about features

### Dashboard (http://localhost:5000/dashboard)
- View top 5 movers
- See investment scores
- Check daily performance

### Top Movers (http://localhost:5000/movers)
- High momentum stocks
- Performance charts
- Investment recommendations

### Watchlist (http://localhost:5000/watchlist)
- AAPL, NVDA, MSFT, META, GOOGL
- Compare daily changes
- Trend analysis

### Recommendations (http://localhost:5000/recommendations)
- Investment signals
- Portfolio strategy
- Complete rankings

### About (http://localhost:5000/about)
- Algorithm explanation
- Technology stack
- Important disclaimer

## Features

✅ Real-time stock data from Finnhub  
✅ 7-day historical price analysis  
✅ AI-powered investment scoring  
✅ Interactive charts and visualizations  
✅ Buy/Hold/Avoid recommendations  
✅ Professional web interface  
✅ Background analysis processing  

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
```powershell
pip install Flask==2.3.3
```

### "FINNHUB_API_KEY not set"
- Create `.env` file with your API key
- Make sure it's in the same directory as `flask_app.py`

### Port 5000 already in use
```powershell
# Use a different port
$env:FLASK_ENV='development'
python flask_app.py --port=5001
```

### Analysis timing out
- Run during market hours
- Free Finnhub tier has 60 calls/minute limit
- Analysis should take 2-3 minutes max

### No data showing
- Click "Run New Analysis" first
- Wait for analysis to complete
- Check browser console (F12) for errors

## Tips

💡 **Best time to run analysis**: During market hours (9:30 AM - 4:00 PM ET)  
💡 **First run takes longer**: 2-3 minutes for initial analysis  
💡 **Results cached**: New analyses update automatically  
💡 **Mobile view**: Dashboard works on mobile browsers  
💡 **Dark theme**: Coming in future version  

## Performance

| Task | Time |
|------|------|
| Initial Analysis | 2-3 minutes |
| Page Load | < 1 second |
| Chart Rendering | 1-2 seconds |
| Data Refresh | < 500ms |

## Next Steps

1. ✅ Run your first analysis
2. 📊 Explore the dashboard
3. 🎯 Check investment recommendations
4. 💼 Review portfolio strategy guide
5. 📖 Read the About page for methodology

## Support

📖 **Help:** Click "About" in the navigation menu  
⚠️ **Disclaimer:** Educational use only - NOT financial advice  
🔗 **Data Source:** Finnhub API + yfinance  
📧 **Issues:** Check browser console (F12) for error messages  

---

Happy analyzing! 📈
