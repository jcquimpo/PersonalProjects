/**
 * Main App Component - Single Page Application for Stock Dashboard
 */

import React, { useState, useEffect } from 'react';
import StockList from './components/StockList';
import StockChart from './components/StockChart';
import { useStockData } from './hooks/useStockData';
import * as api from './services/api';
import './styles/App.css';

// Error Boundary to catch and suppress extension-related errors
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, errorMessage: null };
  }

  static getDerivedStateFromError(error) {
    // Suppress extension-related errors
    if (
      error &&
      error.message &&
      (error.message.includes('Extension context') ||
        error.message.includes('port closed') ||
        error.message.includes('message channel'))
    ) {
      console.debug('[Extension Error - Boundary Suppressed]', error.message);
      return { hasError: false };
    }
    return { hasError: true, errorMessage: error?.message };
  }

  componentDidCatch(error, errorInfo) {
    // Log to console for debugging
    if (error.message && error.message.includes('Extension')) {
      console.debug('[Extension Error Caught]', error.message);
    } else {
      console.error('Error caught by boundary:', error, errorInfo);
    }
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '20px', color: 'red' }}>
          <h2>Something went wrong</h2>
          <details style={{ whiteSpace: 'pre-wrap' }}>
            {this.state.errorMessage}
          </details>
        </div>
      );
    }

    return this.props.children;
  }
}

function App() {
  const {
    topStocks,
    watchlist,
    ohlcDataTop,
    ohlcDataWatchlist,
    loadingTop,
    loadingWatchlist,
    error,
    refreshTopStocks,
    refreshWatchlist,
  } = useStockData();

  const [selectedStock, setSelectedStock] = useState(null);
  const [selectedChartData, setSelectedChartData] = useState(null);
  const [activeTab, setActiveTab] = useState('top'); // 'top' or 'watchlist'
  const [apiHealth, setApiHealth] = useState(null);

  // Check API health on mount and periodically
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const health = await api.checkHealth();
        console.log('[HEALTH CHECK]', health);
        setApiHealth(health);
      } catch (err) {
        // Suppress extension errors in health check
        if (
          err &&
          err.message &&
          !(
            err.message.includes('Extension context') ||
            err.message.includes('port closed')
          )
        ) {
          console.error('[HEALTH CHECK FAILED]', err.message);
          setApiHealth({ status: 'error', message: err.message });
        } else {
          console.debug('[Health check - Extension error suppressed]');
        }
      }
    };

    // Check health immediately
    checkHealth();

    // Check health every 30 seconds
    const healthCheckInterval = setInterval(checkHealth, 30000);

    return () => clearInterval(healthCheckInterval);
  }, []);

  // Update selected chart data when stocks or tab change
  useEffect(() => {
    if (!selectedStock) {
      // Auto-select first stock if available
      if (activeTab === 'top' && topStocks.length > 0) {
        setSelectedStock(topStocks[0].symbol);
      } else if (activeTab === 'watchlist' && watchlist.length > 0) {
        setSelectedStock(watchlist[0].symbol);
      }
    }

    // Get chart data
    const dataMap = activeTab === 'top' ? ohlcDataTop : ohlcDataWatchlist;
    setSelectedChartData(dataMap[selectedStock] || null);
  }, [selectedStock, activeTab, topStocks, watchlist, ohlcDataTop, ohlcDataWatchlist]);

  const getSelectedStockData = () => {
    const stocks = activeTab === 'top' ? topStocks : watchlist;
    return stocks.find((s) => s.symbol === selectedStock);
  };

  const handleTabChange = (tab) => {
    setActiveTab(tab);
    setSelectedStock(null); // Reset selected stock when changing tabs
  };

  return (
    <ErrorBoundary>
      <div className="app">
        {/* Header */}
        <header className="app-header">
          <div className="header-content">
            <h1>📈 Stock Dashboard</h1>
            <p>Real-time stock tracking and analysis</p>
          </div>
          <div className="header-status">
            {apiHealth?.status === 'ok' ? (
              <span className="status-badge success">● API Connected</span>
            ) : (
              <span className="status-badge error">● API Disconnected</span>
            )}
          </div>
        </header>

        {/* Error Message */}
        {error && (
          <div className="error-banner">
            <span>⚠️ {error}</span>
          </div>
        )}

      {/* Main Content */}
      <div className="dashboard-container">
        {/* Sidebar */}
        <aside className="sidebar">
          <div className="tab-selector">
            <button
              className={`tab-button ${activeTab === 'top' ? 'active' : ''}`}
              onClick={() => handleTabChange('top')}
            >
              Top 5 Performers
            </button>
            <button
              className={`tab-button ${activeTab === 'watchlist' ? 'active' : ''}`}
              onClick={() => handleTabChange('watchlist')}
            >
              📌 Watchlist
            </button>
          </div>

          {activeTab === 'top' ? (
            <StockList
              stocks={topStocks}
              title="Top 5 Stocks by % Change"
              selectedStock={selectedStock ? { symbol: selectedStock } : null}
              onSelectStock={setSelectedStock}
              onRefresh={refreshTopStocks}
              isLoading={loadingTop}
            />
          ) : (
            <StockList
              stocks={watchlist}
              title="Your Watchlist"
              selectedStock={selectedStock ? { symbol: selectedStock } : null}
              onSelectStock={setSelectedStock}
              onRefresh={refreshWatchlist}
              isLoading={loadingWatchlist}
            />
          )}
        </aside>

        {/* Main Content Area */}
        <main className="main-content">
          {selectedChartData && getSelectedStockData() ? (
            <StockChart
              data={selectedChartData}
              symbol={selectedStock}
              company_name={getSelectedStockData().company_name}
            />
          ) : (
            <div className="content-placeholder">
              <div className="placeholder-icon">📊</div>
              <p>Select a stock to view detailed chart</p>
            </div>
          )}
        </main>
      </div>

      {/* Footer */}
      <footer className="app-footer">
        <p>Last updated: {new Date().toLocaleTimeString()}</p>
        <p>Stock data powered by yfinance</p>
      </footer>
      </div>
    </ErrorBoundary>
  );
}

export default App;
