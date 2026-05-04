import React, { useState, useEffect } from 'react';
import './App.css';
import TopMovers from './components/TopMovers';
import OHLCData from './components/OHLCData';
import WatchlistMonitor from './components/WatchlistMonitor';
import mockData from './data/mockData';

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate data fetching from the Python script
    // In production, you'd fetch from your backend API endpoint
    setTimeout(() => {
      setData(mockData);
      setLoading(false);
    }, 500);
  }, []);

  if (loading) {
    return <div className="loading">Loading stock data...</div>;
  }

  return (
    <div className="app">
      <header className="header">
        <h1>📈 Stock Tracker Dashboard</h1>
        <p>Real-time market analysis and watchlist monitoring</p>
      </header>

      <main className="container">
        {data && (
          <>
            <TopMovers symbols={data.top5Symbols} performance={data.top5Performance} />
            <OHLCData ohlcData={data.ohlcData} title="Top Movers - 7-Day OHLC" />
            <WatchlistMonitor 
              watchlist={data.watchlist}
              performance={data.watchlistPerformance}
              ohlcData={data.watchlistOHLC}
            />
          </>
        )}
      </main>

      <footer className="footer">
        <p>Stock Tracker • Updated {new Date().toLocaleString()}</p>
      </footer>
    </div>
  );
}

export default App;
