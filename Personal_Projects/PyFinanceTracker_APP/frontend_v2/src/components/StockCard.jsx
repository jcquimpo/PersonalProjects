/**
 * StockCard Component - Displays individual stock information.
 */

import React from 'react';
import '../styles/StockCard.css';

const StockCard = ({ stock, isSelected, onClick }) => {
  const changeColor = stock.percentage_change >= 0 ? '#10b981' : '#ef4444';
  const changeIcon = stock.percentage_change >= 0 ? '↑' : '↓';

  return (
    <div
      className={`stock-card ${isSelected ? 'selected' : ''}`}
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyPress={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          onClick();
        }
      }}
    >
      <div className="stock-card-header">
        <div className="stock-card-symbol">{stock.symbol}</div>
        <div className="stock-card-company">{stock.company_name}</div>
      </div>

      <div className="stock-card-body">
        <div className="stock-card-price">
          <span className="label">Current Price</span>
          <span className="value">${stock.current_price.toFixed(2)}</span>
        </div>

        <div className="stock-card-change" style={{ color: changeColor }}>
          <span className="label">Change</span>
          <span className="value">
            {changeIcon} {Math.abs(stock.percentage_change).toFixed(2)}%
          </span>
        </div>
      </div>

      <div className="stock-card-previous">
        <span className="text-sm">Prev: ${stock.previous_close.toFixed(2)}</span>
      </div>
    </div>
  );
};

export default StockCard;
