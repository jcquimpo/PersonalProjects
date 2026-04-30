/**
 * StockList Component - Displays a list of stocks.
 */

import React from 'react';
import StockCard from './StockCard';
import '../styles/StockList.css';

const StockList = ({
  stocks,
  title,
  selectedStock,
  onSelectStock,
  onRefresh,
  isLoading,
}) => {
  return (
    <div className="stock-list-container">
      <div className="stock-list-header">
        <h2>{title}</h2>
        <button
          className="refresh-button"
          onClick={onRefresh}
          disabled={isLoading}
          aria-label="Refresh stocks"
        >
          {isLoading ? '⏳ Loading...' : '🔄 Refresh'}
        </button>
      </div>

      <div className="stock-list">
        {isLoading && stocks.length === 0 ? (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Loading stocks...</p>
          </div>
        ) : stocks.length > 0 ? (
          stocks.map((stock) => (
            <StockCard
              key={stock.symbol}
              stock={stock}
              isSelected={selectedStock?.symbol === stock.symbol}
              onClick={() => onSelectStock(stock.symbol)}
            />
          ))
        ) : (
          <div className="empty-state">
            <p>No stocks available</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default StockList;
