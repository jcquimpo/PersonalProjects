import React, { useState } from 'react';
import './WatchlistMonitor.css';

const SYMBOL_NAMES = {
  "AAPL": "Apple Inc.",
  "MSFT": "Microsoft Corporation",
  "NVDA": "NVIDIA Corporation",
  "TSLA": "Tesla Inc.",
  "AMZN": "Amazon Inc.",
  "GOOGL": "Alphabet Inc.",
  "META": "Meta Platforms",
  "BRK.B": "Berkshire Hathaway",
  "JNJ": "Johnson & Johnson",
  "V": "Visa Inc.",
};

function WatchlistMonitor({ watchlist, performance, ohlcData }) {
  const [expandedSymbol, setExpandedSymbol] = useState(null);

  const getCompanyName = (symbol) => {
    return SYMBOL_NAMES[symbol] || symbol;
  };

  const formatCurrency = (value) => {
    return `$${parseFloat(value).toFixed(2)}`;
  };

  if (!watchlist || watchlist.length === 0) {
    return (
      <section className="section watchlist-section">
        <h2>👀 Watchlist Monitor</h2>
        <p className="no-data">No watchlist data available</p>
      </section>
    );
  }

  const performanceMap = {};
  if (performance) {
    performance.forEach(([symbol, pct]) => {
      performanceMap[symbol] = pct;
    });
  }

  return (
    <section className="section watchlist-section">
      <h2>👀 Watchlist Monitor</h2>

      <div className="watchlist-container">
        {watchlist.map((symbol) => {
          const pct = performanceMap[symbol] || 0;
          const isPositive = pct > 0;
          const isExpanded = expandedSymbol === symbol;
          const symbolOHLC = ohlcData && ohlcData[symbol];

          return (
            <div
              key={symbol}
              className={`watchlist-item ${isExpanded ? 'expanded' : ''}`}
            >
              <div
                className="watchlist-header"
                onClick={() =>
                  setExpandedSymbol(isExpanded ? null : symbol)
                }
              >
                <div className="watchlist-info">
                  <div className="watchlist-symbol">{symbol}</div>
                  <div className="watchlist-name">
                    {getCompanyName(symbol)}
                  </div>
                </div>

                <div className={`watchlist-performance ${isPositive ? 'positive' : 'negative'}`}>
                  <span className="performance-icon">
                    {isPositive ? '📈' : '📉'}
                  </span>
                  <span className="performance-value">
                    {pct > 0 ? '+' : ''}{pct.toFixed(2)}%
                  </span>
                </div>

                <div className="expand-icon">
                  {isExpanded ? '▼' : '▶'}
                </div>
              </div>

              {isExpanded && symbolOHLC && symbolOHLC.dates && (
                <div className="watchlist-details">
                  <table className="details-table">
                    <thead>
                      <tr>
                        <th>Date</th>
                        <th>Open</th>
                        <th>High</th>
                        <th>Low</th>
                        <th>Close</th>
                      </tr>
                    </thead>
                    <tbody>
                      {symbolOHLC.dates.map((date, index) => (
                        <tr key={index}>
                          <td>{new Date(date).toLocaleDateString()}</td>
                          <td>{formatCurrency(symbolOHLC.opens[index])}</td>
                          <td className="high">
                            {formatCurrency(symbolOHLC.highs[index])}
                          </td>
                          <td className="low">
                            {formatCurrency(symbolOHLC.lows[index])}
                          </td>
                          <td className="close">
                            {formatCurrency(symbolOHLC.closes[index])}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>

                  <div className="price-stats">
                    <div className="stat">
                      <span className="stat-label">Current</span>
                      <span className="stat-value">
                        {formatCurrency(
                          symbolOHLC.closes[symbolOHLC.closes.length - 1]
                        )}
                      </span>
                    </div>
                    <div className="stat">
                      <span className="stat-label">7-Day High</span>
                      <span className="stat-value">
                        {formatCurrency(Math.max(...symbolOHLC.highs))}
                      </span>
                    </div>
                    <div className="stat">
                      <span className="stat-label">7-Day Low</span>
                      <span className="stat-value">
                        {formatCurrency(Math.min(...symbolOHLC.lows))}
                      </span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}

export default WatchlistMonitor;
