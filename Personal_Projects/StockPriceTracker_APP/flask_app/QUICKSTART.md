# Flask Dashboard Quick Start

Get your stock tracker dashboard running in 3 steps!

## 🚀 Quick Setup (5 minutes)

### Step 1: Generate Stock Data
From the main directory, run the Python script:

```bash
python Top_Stocks.py
```

This creates `flask_app/data/stock_data.json` with stock analysis data.

### Step 2: Install Flask
```bash
cd flask_app
pip install -r requirements.txt
```

Or just:
```bash
pip install Flask
```

### Step 3: Start Dashboard
```bash
python app.py
```

Open your browser to: **http://localhost:5000** ✨

## 📊 Using the Dashboard

### Tabs
- **🚀 Top Global Stocks** - View top 5 movers with charts
- **👀 Watchlist** - Monitor your custom watchlist

### Features
1. Click symbol buttons to switch between stocks
2. View 7-day OHLC line charts
3. See detailed price tables
4. Check price statistics (high, low, current, average)
5. Click 🔄 Refresh to reload data

## 🔄 Updating Data

To get the latest stock data:

```bash
# Run Python script to regenerate data
python Top_Stocks.py

# Data is automatically reloaded in dashboard
# Or click the Refresh button in the dashboard
```

## ⚙️ Configuration

### Change Watchlist
Edit `Top_Stocks.py`:

```python
WATCHLIST = ["AAPL", "NVDA", "MSFT", "META", "GOOGL"]  # Your symbols here
```

### Change Port
Edit `app.py`:

```python
app.run(debug=True, port=5001)  # Use port 5001 instead
```

Then access at: **http://localhost:5001**

## 📁 File Structure

```
flask_app/
├── app.py                 # Main Flask app
├── requirements.txt       # Dependencies
├── data/
│   └── stock_data.json   # Auto-generated data
├── templates/
│   └── index.html        # Dashboard
└── static/
    ├── css/style.css     # Styling
    └── js/script.js      # Interactivity
```

## 🐛 Troubleshooting

**"No stock data available"**
- Run: `python Top_Stocks.py`

**Port 5000 already in use**
```bash
# Use a different port
python flask_app/app.py  # Edit app.py and change port to 5001
```

**Charts not showing**
- Check browser console (F12 → Console tab)
- Make sure internet connection is active (Chart.js uses CDN)

**Data not updating**
- Click 🔄 Refresh button in dashboard
- Or restart Flask server

## 📱 Mobile Access

Access from another device on your network:

1. Get your computer's IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
2. Visit: `http://YOUR_IP:5000` from any device

## 🎨 Customization

### Colors
Edit `static/css/style.css` variables:
- Green (gains): `#22c55e`
- Red (losses): `#ef4444`
- Blue (primary): `#3b82f6`

### Add More Symbols
Edit `SYMBOL_NAMES` in `Top_Stocks.py`:

```python
SYMBOL_NAMES = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation",
    "AMZN": "Amazon Inc.",  # Add more
}
```

## 📈 Next Steps

1. **React Styling Migration**: Fully Migrate frontend to React
2. **Schedule Updates**: Set up a cron job to run `Top_Stocks.py` daily
3. **Deploy Online**: Host on Heroku, PythonAnywhere, or AWS
4. **Add Features**: Extend with more stocks, indicators, or alerts

## 🔗 Useful Commands

```bash
# Generate fresh data
python Top_Stocks.py

# Start dashboard
python flask_app/app.py

# Stop server
Ctrl+C

# Check Flask version
pip show Flask

# Update Flask
pip install --upgrade Flask
```

## 📚 Full Documentation

See `README.md` in this directory for:
- Complete feature list
- API endpoints
- Advanced configuration
- Deployment guides
- Troubleshooting help

## 🎯 Common Tasks

### View data via API
```bash
curl http://localhost:5000/api/stock-data
```

### Change refresh rate
Edit `Top_Stocks.py` and adjust the `delay` parameters in function calls

### Export dashboard as screenshot
Use browser's Print to PDF (Ctrl+P or Cmd+P)

## 💡 Tips

- **Keyboard shortcut**: Press Tab to navigate between symbols
- **Dark mode**: Dashboard uses dark theme by default
- **Responsive**: Automatically adapts to screen size
- **No database**: Everything stored in simple JSON file

---

**Happy trading! 📊📈**

Need help? Check `README.md` for detailed documentation.
