import React from 'react';
import './TopMovers.css';

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

function TopMovers({ symbols, performance }) {
  const getCompanyName = (symbol) => {
    return SYMBOL_NAMES[symbol] || symbol;
  };

  return (
    <section className="section top-movers-section">
      <h2>🚀 Top 5 Movers</h2>
      <div className="movers-grid">
        {performance && performance.map((item, index) => {
          const [symbol, percentChange] = item;
          const isPositive = percentChange > 0;
          
          return (
            <div key={symbol} className={`mover-card ${isPositive ? 'positive' : 'negative'}`}>
              <div className="mover-rank">#{index + 1}</div>
              <div className="mover-symbol">{symbol}</div>
              <div className="mover-name">{getCompanyName(symbol)}</div>
              <div className={`mover-change ${isPositive ? 'up' : 'down'}`}>
                <span className="change-icon">{isPositive ? '📈' : '📉'}</span>
                <span className="change-value">{percentChange > 0 ? '+' : ''}{percentChange.toFixed(2)}%</span>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}

export default TopMovers;
