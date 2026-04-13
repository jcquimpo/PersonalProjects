import React, { useState, useEffect } from 'react';
import axios from 'axios';
import StockCard from './components/StockCard';
import StockChart from './components/StockChart';
import './App.css';

function App() {
  const [topStocks, setTopStocks] = useState([]);
  const [watchlist, setWatchlist] = useState([]);
  const [ohlcDataTop, setOhlcDataTop] = useState({});
  const [ohlcDataWatchlist, setOhlcDataWatchlist] = useState({});
  const [selectedStock, setSelectedStock] = useState(null);
  const [loadingTop, setLoadingTop] = useState(false);
  const [loadingWatchlist, setLoadingWatchlist] = useState(false);

  useEffect(() => {
    fetchTopStocks();
    fetchWatchlist();
  }, []);

  const fetchTopStocks = async () => {
    setLoadingTop(true);
    try {
      const response = await axios.get('/api/top-stocks');
      setTopStocks(response.data.top_stocks || []);
      setOhlcDataTop(response.data.ohlc_data || {});
      if (response.data.top_stocks?.length > 0) {
        setSelectedStock({
          symbol: response.data.top_stocks[0].symbol,
          type: 'top'
        });
      }
    } catch (error) {
      console.error('Error fetching top stocks:', error);
    }
    setLoadingTop(false);
  };

  const fetchWatchlist = async () => {
    setLoadingWatchlist(true);
    try {
      const response = await axios.get('/api/watchlist');
      setWatchlist(response.data.watchlist || []);
      setOhlcDataWatchlist(response.data.ohlc_data || {});
    } catch (error) {
      console.error('Error fetching watchlist:', error);
    }
    setLoadingWatchlist(false);
  };

  const getSelectedChartData = () => {
    if (!selectedStock) return null;
    const dataSet = selectedStock.type === 'top' ? ohlcDataTop : ohlcDataWatchlist;
    return dataSet[selectedStock.symbol] || null;
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>📈 Stock Dashboard</h1>
        <p>Real-time stock tracking and analysis</p>
      </header>

      <div className="dashboard-container">
        {/* Left Sidebar */}
        <aside className="sidebar">
          <div className="sidebar-section">
            <h2>Top 5 Performers</h2>
            <button 
              className="refresh-btn"
              onClick={fetchTopStocks}
              disabled={loadingTop}
            >
              {loadingTop ? '⏳ Loading...' : '🔄 Refresh'}
            </button>
            <div className="stock-list">
              {loadingTop ? (
                <p className="loading">Loading top stocks...</p>
              ) : topStocks.length > 0 ? (
                topStocks.map((stock) => (
                  <div
                    key={stock.symbol}
                    className={`stock-item ${selectedStock?.symbol === stock.symbol && selectedStock?.type === 'top' ? 'active' : ''}`}
                    onClick={() => setSelectedStock({ symbol: stock.symbol, type: 'top' })}
                  >
                    <div className="stock-item-symbol">{stock.symbol}</div>
                    <div className="stock-item-price">${stock.current_price}</div>
                    <div className={`stock-item-change ${stock.percentage_change >= 0 ? 'positive' : 'negative'}`}>
                      {stock.percentage_change >= 0 ? '↑' : '↓'} {Math.abs(stock.percentage_change).toFixed(2)}%
                    </div>
                  </div>
                ))
              ) : (
                <p className="no-data">No data available</p>
              )}
            </div>
          </div>

          <div className="sidebar-section">
            <h2>📌 Watchlist</h2>
            <button 
              className="refresh-btn"
              onClick={fetchWatchlist}
              disabled={loadingWatchlist}
            >
              {loadingWatchlist ? '⏳ Loading...' : '🔄 Refresh'}
            </button>
            <div className="stock-list">
              {loadingWatchlist ? (
                <p className="loading">Loading watchlist...</p>
              ) : watchlist.length > 0 ? (
                watchlist.map((stock) => (
                  <div
                    key={stock.symbol}
                    className={`stock-item ${selectedStock?.symbol === stock.symbol && selectedStock?.type === 'watchlist' ? 'active' : ''}`}
                    onClick={() => setSelectedStock({ symbol: stock.symbol, type: 'watchlist' })}
                  >
                    <div className="stock-item-symbol">{stock.symbol}</div>
                    <div className="stock-item-price">${stock.current_price}</div>
                    <div className={`stock-item-change ${stock.percentage_change >= 0 ? 'positive' : 'negative'}`}>
                      {stock.percentage_change >= 0 ? '↑' : '↓'} {Math.abs(stock.percentage_change).toFixed(2)}%
                    </div>
                  </div>
                ))
              ) : (
                <p className="no-data">No watchlist data</p>
              )}
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <main className="main-content">
          {selectedStock ? (
            <>
              <div className="chart-header">
                <h2>{selectedStock.symbol}</h2>
                <p className="chart-subheader">
                  {selectedStock.type === 'top' ? 'Top Performer' : 'Watchlist'}
                </p>
              </div>
              <div className="chart-container">
                {getSelectedChartData() ? (
                  <StockChart data={getSelectedChartData()} symbol={selectedStock.symbol} />
                ) : (
                  <p className="loading">Loading chart...</p>
                )}
              </div>

              {/* Stock Details Grid */}
              <div className="details-grid">
                {selectedStock.type === 'top' ? (
                  topStocks
                    .filter(s => s.symbol === selectedStock.symbol)
                    .map(stock => (
                      <StockCard key={stock.symbol} stock={stock} />
                    ))
                ) : (
                  watchlist
                    .filter(s => s.symbol === selectedStock.symbol)
                    .map(stock => (
                      <StockCard key={stock.symbol} stock={stock} />
                    ))
                )}
              </div>
            </>
          ) : (
            <div className="empty-state">
              <p>Select a stock to view details and chart</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
