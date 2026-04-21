/**
 * API service for communicating with the FastAPI backend.
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

/**
 * Fetch top performing stocks.
 */
export const fetchTopStocks = async (limit = 50, delay = 0.7) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/top-stocks?limit=${limit}&delay=${delay}`
    );
    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching top stocks:', error);
    throw error;
  }
};

/**
 * Fetch watchlist stocks.
 */
export const fetchWatchlist = async (delay = 0.5) => {
  try {
    const response = await fetch(`${API_BASE_URL}/watchlist?delay=${delay}`);
    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching watchlist:', error);
    throw error;
  }
};

/**
 * Fetch detailed stock data for a specific symbol.
 */
export const fetchStockData = async (symbol, period = '7d') => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/stock/${symbol}?period=${period}`
    );
    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`Error fetching stock data for ${symbol}:`, error);
    throw error;
  }
};

/**
 * Check API health.
 */
export const checkHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error checking health:', error);
    throw error;
  }
};
