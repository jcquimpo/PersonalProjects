/**
 * API service for communicating with the FastAPI backend.
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';
const DEFAULT_TIMEOUT = 60000; // 60 seconds timeout for stock fetching
const MAX_RETRIES = 2;
const RETRY_DELAY = 1000; // 1 second between retries

/**
 * Fetch with timeout and retry logic.
 * @param {string} url - The URL to fetch
 * @param {number} timeout - Timeout in milliseconds
 * @param {number} retries - Number of retry attempts
 * @returns {Promise<Response>} - The fetch response
 */
const fetchWithTimeout = async (url, timeout = DEFAULT_TIMEOUT, retries = MAX_RETRIES) => {
  let lastError;

  for (let attempt = 0; attempt <= retries; attempt++) {
    let timeoutId; // Declare outside try-catch for scope access
    try {
      const controller = new AbortController();
      timeoutId = setTimeout(() => controller.abort(), timeout);

      const response = await fetch(url, { signal: controller.signal });
      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      return response;
    } catch (error) {
      clearTimeout(timeoutId);
      lastError = error;

      // Check if it's a timeout or abort error
      if (error.name === 'AbortError') {
        lastError = new Error(`Request timeout after ${timeout}ms`);
      }

      // Only retry on network errors, not on HTTP errors
      if (attempt < retries && (error.name === 'AbortError' || !error.message.startsWith('HTTP'))) {
        console.warn(`Retry attempt ${attempt + 1}/${retries} for ${url}. Error: ${error.message}`);
        await new Promise(resolve => setTimeout(resolve, RETRY_DELAY));
        continue;
      }

      break;
    }
  }

  throw lastError || new Error('Unknown fetch error');
};

/**
 * Fetch top performing stocks.
 */
export const fetchTopStocks = async (limit = 50, delay = 0.7) => {
  try {
    const response = await fetchWithTimeout(
      `${API_BASE_URL}/top-stocks?limit=${limit}&delay=${delay}`,
      DEFAULT_TIMEOUT,
      MAX_RETRIES
    );
    return await response.json();
  } catch (error) {
    console.error('Error fetching top stocks:', error);
    throw new Error(`Failed to fetch top stocks: ${error.message}`);
  }
};

/**
 * Fetch watchlist stocks.
 */
export const fetchWatchlist = async (delay = 0.5) => {
  try {
    const response = await fetchWithTimeout(
      `${API_BASE_URL}/watchlist?delay=${delay}`,
      DEFAULT_TIMEOUT,
      MAX_RETRIES
    );
    return await response.json();
  } catch (error) {
    console.error('Error fetching watchlist:', error);
    throw new Error(`Failed to fetch watchlist: ${error.message}`);
  }
};

/**
 * Fetch detailed stock data for a specific symbol.
 */
export const fetchStockData = async (symbol, period = '7d') => {
  try {
    const response = await fetchWithTimeout(
      `${API_BASE_URL}/stock/${symbol}?period=${period}`,
      DEFAULT_TIMEOUT,
      MAX_RETRIES
    );
    return await response.json();
  } catch (error) {
    console.error(`Error fetching stock data for ${symbol}:`, error);
    throw new Error(`Failed to fetch stock data for ${symbol}: ${error.message}`);
  }
};

/**
 * Check API health.
 */
export const checkHealth = async () => {
  try {
    const response = await fetchWithTimeout(
      `${API_BASE_URL}/health`,
      5000, // Shorter timeout for health check
      1 // Fewer retries for health check
    );
    return await response.json();
  } catch (error) {
    console.error('Error checking health:', error);
    throw new Error(`API health check failed: ${error.message}`);
  }
};
