# Flask Stock Tracker Dashboard - Complete Setup

A professional Flask web dashboard for displaying stock market analysis from the `Top_Stocks.py` Python script.

## 🎉 What's Been Created

### Updated Python Script
- **Top_Stocks.py** - Enhanced with JSON export functionality to generate `stock_data.json`

### Flask Application
```
flask_app/
├── app.py                    # Main Flask application
├── config.py                 # Configuration management
├── __init__.py              # Package initialization
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore file
├── README.md               # Complete documentation
├── QUICKSTART.md           # Quick start guide
├── data/
│   └── stock_data.json     # Generated stock data (auto-created)
├── templates/
│   └── index.html          # Dashboard template with tabs
└── static/
    ├── css/
    │   └── style.css       # Professional dark theme styling
    └── js/
        └── script.js       # Interactive functionality
```

## ⚡ Quick Start (3 Steps)

### 1. Generate Stock Data
```bash
python Top_Stocks.py
```
Creates: `flask_app/data/stock_data.json`

### 2. Install Flask
```bash
pip install -r flask_app/requirements.txt
```

### 3. Start Dashboard
```bash
python flask_app/app.py
```
Open: **http://localhost:5000**

## 📊 Dashboard Features

✨ **Two Tabs**
- 🚀 Top Global Stocks - Top 5 movers with performance
- 👀 Watchlist - Custom monitored stocks

📈 **Interactive Charts**
- 7-day OHLC line charts (Open, High, Low, Close)
- Symbol switching buttons
- Detailed price tables
- Price statistics (high, low, current, average)

🎨 **Professional Design**
- Dark theme with blue accents
- Responsive for desktop, tablet, mobile
- Smooth animations and transitions
- Color-coded gains (green) and losses (red)

## 📁 File Structure

```
StockPriceTracker_APP/
├── Top_Stocks.py                 # Updated with JSON export
├── FLASK_SETUP_GUIDE.md          # Complete setup instructions
├── flask_app/
│   ├── app.py                    # Flask application
│   ├── config.py                 # Configuration
│   ├── __init__.py              # Package init
│   ├── requirements.txt          # Dependencies
│   ├── .gitignore               # Git ignore
│   ├── README.md                # Full docs
│   ├── QUICKSTART.md            # Quick start
│   ├── data/
│   │   └── stock_data.json      # Stock data (auto-generated)
│   ├── templates/
│   │   └── index.html           # Dashboard
│   └── static/
│       ├── css/style.css        # Styling
│       └── js/script.js         # JavaScript
```

## 🔄 How It Works

1. **Data Generation**: `Top_Stocks.py` analyzes stocks and creates JSON
2. **Data Storage**: JSON saved to `flask_app/data/stock_data.json`
3. **Flask Server**: Reads JSON and serves dashboard
4. **Dashboard**: Browser displays interactive charts and tables

## 🚀 Usage Workflow

### First Time
```bash
# Install dependencies
pip install pandas numpy
pip install -r flask_app/requirements.txt

# Generate data
python Top_Stocks.py

# Start dashboard
cd flask_app
python app.py

# Open browser
# http://localhost:5000
```

### Daily Use
```bash
# Run Python script to update data
python Top_Stocks.py

# Start Flask (if not already running)
python flask_app/app.py

# Open http://localhost:5000
```

## 📊 Dashboard Pages

### Top Global Stocks
- 5 cards showing top performers
- Performance percentage with color indicators
- Symbol selector buttons
- 7-day OHLC chart
- Price data table

### Watchlist
- Summary cards for each watched stock
- Performance indicator
- Symbol selector buttons
- 7-day OHLC chart
- Price data table
- Price statistics (high, low, current, average)

## 🎯 Key Components

### `Top_Stocks.py` (Updated)
- Generates stock analysis
- **NEW**: Exports data as `stock_data.json`
- Analyzes top 5 movers
- Analyzes custom watchlist
- Generates OHLC data for 7 days

### `app.py`
- Serves Flask application
- Loads stock data from JSON
- Renders HTML template
- Provides API endpoints
- Handles data refresh

### `index.html`
- Main dashboard template
- Tab navigation (Top Movers / Watchlist)
- Symbol selector buttons
- Chart containers
- Data tables
- Statistics display

### `script.js`
- Tab switching functionality
- Chart rendering with Chart.js
- Table population
- Data manipulation
- API communication

### `style.css`
- Professional dark theme
- Responsive grid layouts
- Color-coded elements
- Smooth animations
- Mobile-friendly design

## 🔌 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Dashboard HTML |
| `/api/stock-data` | GET | Stock data JSON |
| `/api/refresh` | GET | Refresh data |

## ⚙️ Configuration

### Change Port
Edit `flask_app/app.py`:
```python
app.run(debug=True, port=5001)  # Change from 5000 to 5001
```

### Change Watchlist
Edit `Top_Stocks.py`:
```python
WATCHLIST = ["AAPL", "NVDA", "MSFT", "META", "GOOGL"]
```

### Customize Colors
Edit `flask_app/static/css/style.css`:
```css
--primary-color: #3b82f6;    /* Primary color */
--success-color: #22c55e;    /* Gains color */
--danger-color: #ef4444;     /* Losses color */
```

## 📚 Documentation

- **FLASK_SETUP_GUIDE.md** - Complete setup guide with troubleshooting
- **flask_app/README.md** - Full documentation and API reference
- **flask_app/QUICKSTART.md** - Quick start guide

## 🐛 Troubleshooting

### "No stock data available"
```bash
python Top_Stocks.py
```

### Port 5000 already in use
```bash
# Use different port or kill process
python flask_app/app.py  # Edit app.py to change port
```

### Charts not showing
1. Check internet connection (Chart.js uses CDN)
2. Open browser console (F12) for errors
3. Hard refresh (Ctrl+Shift+R)
4. Verify data file exists: `flask_app/data/stock_data.json`

## 📦 Dependencies

### Python
- Flask (2.3.3) - Web framework
- Pandas - Data analysis
- NumPy - Numerical computing

### JavaScript/CSS
- Chart.js (CDN) - Charting library
- Vanilla CSS - No frameworks needed
- Vanilla JavaScript - No dependencies

## 🎨 Customization

### Add More Stocks
1. Edit WATCHLIST in `Top_Stocks.py`
2. Run `python Top_Stocks.py`
3. Refresh dashboard

### Change Dashboard Title
Edit `flask_app/templates/index.html`:
```html
<h1>📈 Your Custom Title</h1>
```

### Modify Chart Colors
Edit `flask_app/static/js/script.js` in the `updateChart()` function

## 🚀 Next Steps

1. ✅ Run `python Top_Stocks.py` to generate data
2. ✅ Start Flask with `python flask_app/app.py`
3. ✅ Open http://localhost:5000
4. 🎨 Customize colors, symbols, and styling
5. 📱 Access from mobile devices
6. 📊 Schedule auto-updates with cron/Task Scheduler
7. ☁️ Deploy to production (Heroku, PythonAnywhere, AWS)

## 💡 Features Highlight

✨ **Modern Design**
- Professional dark theme
- Responsive layout
- Smooth animations
- Color-coded performance

📊 **Data Visualization**
- Interactive line charts
- Detailed price tables
- Performance statistics
- Symbol-switching

🔄 **Real-Time Updates**
- One-click data refresh
- Auto-updated timestamp
- Live chart rendering
- Responsive to data changes

📱 **Mobile Friendly**
- Works on all devices
- Touch-friendly buttons
- Responsive charts
- Mobile-optimized layout

## 🔐 Security Notes

- No authentication required (local dashboard)
- Data only from local JSON file
- No external API calls to stock data
- Safe for local network access

## 📈 Performance

- Lightweight (~60 KB total)
- Fast load times
- Efficient chart rendering
- Minimal memory usage

## 🎯 Supported Browsers

- Chrome/Chromium (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers

## 📞 Support Resources

1. **Flask Documentation**: https://flask.palletsprojects.com
2. **Chart.js Docs**: https://www.chartjs.org
3. **Python Pandas**: https://pandas.pydata.org
4. **Browser DevTools**: Press F12 for console

## 🎓 Learning Resources

- Flask web development tutorials
- Chart.js visualization guide
- JavaScript event handling
- CSS responsive design
- Python data analysis

## 🏆 Best Practices Implemented

✅ Modular code structure
✅ Separate concerns (templates, static, logic)
✅ Responsive design
✅ Accessibility
✅ Error handling
✅ Configuration management
✅ Clean code organization
✅ Comprehensive documentation

---

**Everything is set up and ready to use!** 🚀

Start with the FLASK_SETUP_GUIDE.md for detailed setup instructions, or dive straight in with:

```bash
python Top_Stocks.py
cd flask_app
python app.py
```

Then open http://localhost:5000 in your browser! 📊📈
