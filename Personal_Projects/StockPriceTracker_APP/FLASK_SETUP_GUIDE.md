# Setup Guide: Flask Dashboard with Top_Stocks.py

Complete guide to setting up and running the Flask Stock Tracker Dashboard integrated with the Python script.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Running the Application](#running-the-application)
4. [Data Flow](#data-flow)
5. [Configuration](#configuration)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Setup](#advanced-setup)

## Prerequisites

- Python 3.7+
- pip (Python package manager)
- Web browser (Chrome, Firefox, Safari, Edge)
- ~100MB disk space

**Check Python version:**
```bash
python --version
```

## Installation

### Step 1: Navigate to Project Directory

```bash
cd c:\Users\dmjmq\VSCode_Projects\PersonalProjects\Personal_Projects\StockPriceTracker_APP
```

### Step 2: Install Python Dependencies

First, install the main script dependencies (pandas, numpy):

```bash
pip install pandas numpy
```

Then install Flask dependencies:

```bash
cd flask_app
pip install -r requirements.txt
```

Or install manually:
```bash
pip install Flask==2.3.3 Werkzeug==2.3.7
```

### Step 3: Verify Installation

Check Flask is installed:
```bash
python -c "import flask; print(flask.__version__)"
```

Output should show: `2.3.3`

## Running the Application

### Standard Workflow

#### Step 1: Generate Stock Data (Run Python Script)

From the project root directory:

```bash
python Top_Stocks.py
```

**Expected output:**
```
======================================================================
TOP MOVERS ANALYSIS  (using MOCK data - Global Stocks)
======================================================================
Generating 30 mock stock movers (global)...
...
EXPORTING DATA FOR FLASK DASHBOARD
======================================================================
✓ Data exported to flask_app/data/stock_data.json
✓ Analysis complete! Start Flask app with: python flask_app/app.py
```

#### Step 2: Start Flask Server

```bash
cd flask_app
python app.py
```

**Expected output:**
```
======================================================================
Stock Tracker Flask Dashboard
======================================================================
Starting Flask server on http://localhost:5000
Make sure to run Top_Stocks.py first to generate data.
======================================================================
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

#### Step 3: Open Dashboard

Open your web browser and visit:
```
http://localhost:5000
```

You should see the dashboard with:
- Top 5 Global Stocks (default tab)
- Separate tabs for Watchlist
- Interactive charts and data tables

### Stopping the Server

Press `Ctrl+C` in the terminal where Flask is running.

## Data Flow

```
┌─────────────────┐
│  Top_Stocks.py  │  ← Run first to generate data
│  (Python)       │
└────────┬────────┘
         │
         ↓
┌─────────────────────────┐
│ stock_data.json         │  ← Auto-generated JSON file
│ (flask_app/data/)       │
└────────┬────────────────┘
         │
         ↓
┌──────────────────────────┐
│  Flask App (app.py)      │  ← Reads JSON, serves HTML
│  http://localhost:5000   │
└────────┬─────────────────┘
         │
         ↓
┌──────────────────────────┐
│  Dashboard (Browser)     │  ← Interactive charts & tables
│  - Charts                │     - Chart.js
│  - Tables                │     - JavaScript functionality
│  - Statistics            │     - Responsive CSS
└──────────────────────────┘
```

## Configuration

### Change Dashboard Port

Edit `flask_app/app.py`:

```python
if __name__ == '__main__':
    # Change port from 5000 to your desired port
    app.run(debug=True, port=5001)
```

Access at: `http://localhost:5001`

### Change Watchlist

Edit `Top_Stocks.py`:

```python
# Line ~160 - Customize these symbols
WATCHLIST = ["AAPL", "NVDA", "MSFT", "META", "GOOGL"]
```

After changes, run:
```bash
python Top_Stocks.py  # Regenerate data with new watchlist
```

### Customize Stock Names

Edit `Top_Stocks.py`:

```python
SYMBOL_NAMES = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation",
    "NVDA": "NVIDIA Corporation",
    # Add more symbols
}
```

### Dashboard Colors

Edit `flask_app/static/css/style.css`:

```css
:root {
    --primary-color: #3b82f6;      /* Change primary color */
    --success-color: #22c55e;      /* Green for gains */
    --danger-color: #ef4444;       /* Red for losses */
    --warning-color: #f59e0b;      /* Orange accent */
    /* ... more variables ... */
}
```

## Troubleshooting

### Problem: "No stock data available"

**Cause**: Stock data JSON not generated

**Solution**:
```bash
# Make sure you're in the project root
python Top_Stocks.py
# Wait for completion, should see "✓ Data exported"
```

### Problem: "Address already in use" or Port 5000 Error

**Cause**: Port 5000 already in use by another application

**Solutions**:

Option 1 - Use different port:
```python
# In flask_app/app.py, change port to 5001, 5002, etc.
app.run(debug=True, port=5001)
```

Option 2 - Find and stop the process using port 5000:

**Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Mac/Linux:**
```bash
lsof -i :5000
kill -9 <PID>
```

### Problem: Blank Dashboard or "Error" Message

**Cause**: Browser JavaScript error

**Solution**:
1. Open browser Developer Tools (F12)
2. Check Console tab for errors
3. Common issues:
   - Chart.js CDN not loading (check internet connection)
   - Stock data file missing (run `Top_Stocks.py`)
   - JavaScript syntax error (check `static/js/script.js`)

### Problem: Charts Not Displaying

**Causes and Solutions**:

1. **No internet connection**
   - Chart.js requires internet (uses CDN)
   - Charts require CDN access

2. **Stock data not generated**
   ```bash
   python Top_Stocks.py
   ```

3. **JavaScript errors**
   - Open browser console (F12)
   - Look for red error messages
   - Fix any issues in `static/js/script.js`

4. **Browser cache issue**
   - Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)

### Problem: Data Not Updating After Running Python Script

**Cause**: Browser caching old data

**Solution**:
1. Click 🔄 Refresh button in dashboard
2. Or hard refresh browser (Ctrl+Shift+R)
3. Or clear browser cache and reload

### Problem: Python Script Error: "ModuleNotFoundError"

**Cause**: Missing Python dependencies

**Solution**:
```bash
# Install required packages
pip install pandas numpy
```

## Advanced Setup

### Auto-Refresh Data

Create a batch file (Windows) or shell script (Mac/Linux) to auto-run Python script:

**Windows - `run_dashboard.bat`:**
```batch
@echo off
echo Generating stock data...
python Top_Stocks.py
echo.
echo Starting Flask dashboard...
cd flask_app
python app.py
```

Then double-click the .bat file to run both in sequence.

**Mac/Linux - `run_dashboard.sh`:**
```bash
#!/bin/bash
echo "Generating stock data..."
python Top_Stocks.py
echo ""
echo "Starting Flask dashboard..."
cd flask_app
python app.py
```

Make executable:
```bash
chmod +x run_dashboard.sh
./run_dashboard.sh
```

### Schedule Regular Updates

**Windows Task Scheduler:**
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily (set time)
4. Action: Run `python Top_Stocks.py`

**Mac/Linux Cron Job:**
```bash
# Edit crontab
crontab -e

# Add this line to run daily at 9 AM:
0 9 * * * cd /path/to/project && python Top_Stocks.py
```

### Production Deployment

For production, use Gunicorn instead of Flask's development server:

```bash
pip install gunicorn

# Run with Gunicorn
cd flask_app
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Environment Variables

Create `flask_app/.env`:
```
FLASK_ENV=production
FLASK_DEBUG=0
PORT=5000
```

Load in `app.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()
port = int(os.getenv('PORT', 5000))
app.run(port=port)
```

## Quick Commands Reference

```bash
# Generate stock data
python Top_Stocks.py

# Install dependencies
pip install -r flask_app/requirements.txt

# Start dashboard
cd flask_app && python app.py

# Check Flask version
python -c "import flask; print(flask.__version__)"

# Stop server
Ctrl+C (in terminal)

# Test API endpoint
curl http://localhost:5000/api/stock-data

# View data
python -c "import json; print(json.dumps(json.load(open('flask_app/data/stock_data.json')), indent=2))"
```

## Recommended Workflow

1. **First Time Setup**
   ```bash
   pip install pandas numpy
   cd flask_app && pip install -r requirements.txt
   cd ..
   ```

2. **Daily Use**
   ```bash
   python Top_Stocks.py
   cd flask_app
   python app.py
   # Open http://localhost:5000 in browser
   ```

3. **Maintenance**
   - Update data daily by running `Top_Stocks.py`
   - Monitor dashboard for any errors
   - Review logs in terminal

## File Checklist

Verify these files exist:

```
StockPriceTracker_APP/
├── Top_Stocks.py                           ✓ Updated with JSON export
├── flask_app/
│   ├── app.py                              ✓ Main Flask app
│   ├── config.py                           ✓ Configuration
│   ├── __init__.py                         ✓ Package init
│   ├── requirements.txt                    ✓ Dependencies
│   ├── .gitignore                          ✓ Git ignore
│   ├── README.md                           ✓ Full documentation
│   ├── QUICKSTART.md                       ✓ Quick start guide
│   ├── data/
│   │   └── stock_data.json                 ✓ (Generated by Top_Stocks.py)
│   ├── templates/
│   │   └── index.html                      ✓ Dashboard template
│   └── static/
│       ├── css/
│       │   └── style.css                   ✓ Styling
│       └── js/
│           └── script.js                   ✓ Interactivity
```

## Next Steps

1. ✅ Complete setup above
2. 📊 Run `python Top_Stocks.py` to generate data
3. 🚀 Run `python flask_app/app.py` to start dashboard
4. 📈 Visit http://localhost:5000 to view dashboard
5. 🎨 Customize colors, stocks, and settings as needed
6. 📱 Access from mobile: Use your computer's IP address

## Getting Help

1. Check the README.md in `flask_app/` directory
2. Review QUICKSTART.md for common tasks
3. Check browser console (F12) for JavaScript errors
4. Review Flask documentation: https://flask.palletsprojects.com
5. Check Python script output for any error messages

---

**You're all set! Happy tracking! 📈**
