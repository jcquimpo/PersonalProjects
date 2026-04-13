const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 5000;

// Python script executor
function runPythonScript(scriptName, args = []) {
  return new Promise((resolve, reject) => {
    const pythonPath = path.join(__dirname, 'stock_fetcher.py');
    const python = spawn('python', [pythonPath, scriptName, ...args], {
      timeout: 60000 // 60 second timeout
    });
    
    let dataString = '';
    let errorString = '';
    let hasResolved = false;

    python.stdout.on('data', (data) => {
      dataString += data.toString();
    });

    python.stderr.on('data', (data) => {
      errorString += data.toString();
    });

    python.on('close', (code) => {
      if (hasResolved) return;
      hasResolved = true;
      
      if (code !== 0) {
        reject(new Error(`Python error (code ${code}): ${errorString}`));
      } else if (!dataString.trim()) {
        reject(new Error('Python script produced no output'));
      } else {
        try {
          resolve(JSON.parse(dataString));
        } catch (e) {
          reject(new Error(`Failed to parse Python output: ${dataString.substring(0, 100)}`));
        }
      }
    });

    python.on('error', (err) => {
      if (hasResolved) return;
      hasResolved = true;
      reject(new Error(`Failed to spawn Python process: ${err.message}`));
    });

    // Timeout handler
    const timer = setTimeout(() => {
      if (!hasResolved) {
        hasResolved = true;
        python.kill();
        reject(new Error('Python script execution timeout'));
      }
    }, 60000);

    python.on('exit', () => clearTimeout(timer));
  });
}

// Root endpoint
app.get('/', (req, res) => {
  res.json({ message: 'Stock Dashboard Backend is running' });
});

// API Endpoints
app.get('/api/top-stocks', async (req, res) => {
  try {
    const limit = req.query.limit || 50;
    const delay = req.query.delay || 0.7;
    const data = await runPythonScript('top-stocks', [limit.toString(), delay.toString()]);
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/watchlist', async (req, res) => {
  try {
    const delay = req.query.delay || 0.5;
    const data = await runPythonScript('watchlist', [delay.toString()]);
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/stock/:symbol', async (req, res) => {
  try {
    const { symbol } = req.params;
    const period = req.query.period || '7d';
    const data = await runPythonScript('stock-data', [symbol, period]);
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Stock Dashboard Backend running on http://localhost:${PORT}`);
});
