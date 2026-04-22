/**
 * API service for communicating with the FastAPI backend.
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';
const HEALTH_TIMEOUT = 5000; // 5 seconds for health check
const DATA_TIMEOUT = 20000; // 20 seconds for data fetching (reduced from 60s)
const MAX_RETRIES = 2;
const RETRY_DELAY = 500; // 500ms between retries

// Cache for API responses
const responseCache = new Map();
const CACHE_TTL = 60000; // 60 seconds cache

/**
 * Fetch with timeout and retry logic, with caching support.
 */
const fetchWithTimeout = async (url, timeout = DATA_TIMEOUT, retries = MAX_RETRIES) => {
  let lastError;

  for (let attempt = 0; attempt <= retries; attempt++) {
    let timeoutId;
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
        const backoffDelay = RETRY_DELAY * Math.pow(2, attempt); // Exponential backoff
        console.warn(`Retry attempt ${attempt + 1}/${retries} for ${url} in ${backoffDelay}ms. Error: ${error.message}`);
        await new Promise(resolve => setTimeout(resolve, backoffDelay));
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
      DATA_TIMEOUT,
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
      DATA_TIMEOUT,
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
      DATA_TIMEOUT,
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
      HEALTH_TIMEOUT, // Use shorter timeout for health check
      1 // Fewer retries for health check
    );
    return await response.json();
  } catch (error) {
    console.error('Error checking health:', error);
    return { status: 'error', message: error.message };
  }
};
