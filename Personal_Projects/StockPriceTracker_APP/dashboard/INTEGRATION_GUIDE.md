# Integration Guide: Connecting React Dashboard to Python Script

This guide explains how to connect your React dashboard to the `Top_Stocks.py` script.

## Option 1: JSON File Export (Simplest)

### Step 1: Modify Python Script

Add this to the end of `Top_Stocks.py`:

```python
import json
from datetime import datetime

# ... existing code ...

# At the very end of the script, export data as JSON
def format_ohlc_for_export(ohlc_data):
    """Convert DataFrame to dictionary format for JSON export"""
    formatted = {}
    for symbol, df in ohlc_data.items():
        formatted[symbol] = {
            'dates': [date.isoformat() for date in df.index],
            'opens': df['Open'].tolist(),
            'highs': df['High'].tolist(),
            'lows': df['Low'].tolist(),
            'closes': df['Close'].tolist()
        }
    return formatted

# Export data
export_data = {
    'top5Symbols': top5_symbols,
    'top5Performance': top5_performance,
    'ohlcData': format_ohlc_for_export(ohlc_data),
    'watchlist': WATCHLIST,
    'watchlistPerformance': results,
    'watchlistOHLC': format_ohlc_for_export(watchlist_ohlc_data),
    'timestamp': datetime.now().isoformat()
}

# Save to JSON file in dashboard directory
with open('dashboard/src/data/stockData.json', 'w') as f:
    json.dump(export_data, f, indent=2, default=str)

print("\n✓ Data exported to dashboard/src/data/stockData.json")
```

### Step 2: Update Dashboard Mock Data

Replace `dashboard/src/data/mockData.js`:

```javascript
// src/data/mockData.js
// Import actual data from Python export
import stockData from './stockData.json';

export default stockData;
```

### Step 3: Run Python Script

```bash
python Top_Stocks.py
```

The dashboard will now display real data from your script!

---

## Option 2: Backend API (Recommended for Production)

### Step 1: Create Express Backend

Create `backend/server.js`:

```javascript
const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');
const path = require('path');

const app = express();
app.use(cors());

// Run Python script and return JSON data
app.get('/api/stocks', (req, res) => {
  const pythonPath = path.join(__dirname, '..', 'Top_Stocks.py');
  
  exec(`python "${pythonPath}"`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error: ${error.message}`);
      return res.status(500).json({ error: 'Failed to fetch stock data' });
    }
    
    try {
      // Parse JSON from Python script output
      const jsonMatch = stdout.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const data = JSON.parse(jsonMatch[0]);
        res.json(data);
      } else {
        res.status(500).json({ error: 'Invalid data format' });
      }
    } catch (e) {
      res.status(500).json({ error: 'JSON parse error' });
    }
  });
});

app.listen(5000, () => {
  console.log('Stock API running on http://localhost:5000');
});
```

### Step 2: Install Backend Dependencies

```bash
cd backend
npm install express cors
```

### Step 3: Update Dashboard to Use API

Create `dashboard/src/services/stockService.js`:

```javascript
// src/services/stockService.js
const API_URL = 'http://localhost:5000/api';

export const fetchStockData = async () => {
  try {
    const response = await fetch(`${API_URL}/stocks`);
    if (!response.ok) throw new Error('Failed to fetch');
    return await response.json();
  } catch (error) {
    console.error('Error fetching stock data:', error);
    return null;
  }
};
```

Update `dashboard/src/App.jsx`:

```javascript
import { fetchStockData } from './services/stockService';
import mockData from './data/mockData';

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      const result = await fetchStockData();
      setData(result || mockData); // Fallback to mock data
      setLoading(false);
    };
    
    loadData();
  }, []);

  // ... rest of component
}
```

### Step 4: Run Both Servers

Terminal 1 (Backend):
```bash
cd backend
node server.js
```

Terminal 2 (Frontend):
```bash
cd dashboard
npm start
```

---

## Option 3: Direct Python Integration (Advanced)

Use Python's built-in HTTP server or Flask to serve data directly:

```python
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/stocks')
def get_stocks():
    # Run your stock analysis
    top5_symbols, top5_performance = get_top_5_symbols()
    ohlc_data = fetch_ohlc_data(top5_symbols)
    
    return jsonify({
        'top5Symbols': top5_symbols,
        'top5Performance': top5_performance,
        'ohlcData': format_data(ohlc_data),
        # ... other data
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)
```

---

## Comparison Table

| Option | Setup | Real-time | Production | Complexity |
|--------|-------|-----------|-----------|-----------|
| JSON Export | ⭐ Easy | ❌ No | ⭐⭐ | Low |
| Express API | ⭐⭐ Medium | ⭐ Manual | ⭐⭐⭐⭐ | Medium |
| Flask | ⭐ Easy | ✅ Yes* | ⭐⭐⭐ | Medium |
| Docker | ⭐⭐⭐ Hard | ✅ Yes | ⭐⭐⭐⭐⭐ | High |

*With WebSockets

---

## Testing Your Integration

1. **Check Python Output**:
   ```bash
   python Top_Stocks.py
   ```
   Verify JSON is generated correctly.

2. **Test API Endpoint** (if using backend):
   ```bash
   curl http://localhost:5000/api/stocks
   ```

3. **Check Dashboard**:
   - Open http://localhost:3000
   - Verify data matches your Python script output
   - Check browser console (F12) for errors

4. **Common Issues**:
   - **CORS errors**: Ensure backend has CORS enabled
   - **Port conflicts**: Change port in backend/server.js
   - **JSON parse errors**: Check Python output format
   - **Missing data**: Verify file paths are correct

---

## Next Steps

1. Choose an integration option
2. Follow the steps for that option
3. Test the connection
4. Deploy to your server (see deployment guides)

For questions, refer to the main [README.md](../README.md)
