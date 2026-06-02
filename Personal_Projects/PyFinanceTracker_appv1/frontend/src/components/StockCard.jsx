import React from 'react';
import '../styles/StockCard.css';

function StockCard({ stock }) {
  const isPositive = stock.percentage_change >= 0;

  return (
    <div className={`stock-card ${isPositive ? 'positive' : 'negative'}`}>
      <div className="stock-card-header">
        <h3>{stock.symbol}</h3>
        <p className="company-name">{stock.company_name}</p>
      </div>

      <div className="stock-card-body">
        <div className="stat">
          <label>Current Price</label>
          <span className="value">${stock.current_price.toFixed(2)}</span>
        </div>

        <div className="stat">
          <label>Previous Close</label>
          <span className="value">${stock.previous_close.toFixed(2)}</span>
        </div>

        <div className="stat">
          <label>Change</label>
          <span className={`value ${isPositive ? 'positive-text' : 'negative-text'}`}>
            {isPositive ? '↑' : '↓'} {Math.abs(stock.percentage_change).toFixed(2)}%
          </span>
        </div>

        <div className="stat full-width">
          <label>Price Movement</label>
          <div className="price-bar">
            <div 
              className={`price-bar-fill ${isPositive ? 'positive' : 'negative'}`}
              style={{ width: `${Math.min(Math.abs(stock.percentage_change) * 5, 100)}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default StockCard;
