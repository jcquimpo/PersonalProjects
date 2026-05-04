/**
 * Custom hook for fetching stock data.
 */

import { useState, useEffect } from 'react';
import * as api from '../services/api';

export const useStockData = () => {
  const [topStocks, setTopStocks] = useState([]);
  const [watchlist, setWatchlist] = useState([]);
  const [ohlcDataTop, setOhlcDataTop] = useState({});
  const [ohlcDataWatchlist, setOhlcDataWatchlist] = useState({});
  const [loadingTop, setLoadingTop] = useState(false);
  const [loadingWatchlist, setLoadingWatchlist] = useState(false);
  const [error, setError] = useState(null);

  const isExtensionError = (err) => {
    if (!err || !err.message) return false;
    return (
      err.message.includes('Extension context') ||
      err.message.includes('port closed') ||
      err.message.includes('message channel')
    );
  };

  const loadTopStocks = async (limit = 50, delay = 0.7) => {
    setLoadingTop(true);
    setError(null);
    try {
      const data = await api.fetchTopStocks(limit, delay);
      setTopStocks(data.top_stocks || []);
      setOhlcDataTop(data.ohlc_data || {});
    } catch (err) {
      // Suppress extension errors
      if (!isExtensionError(err)) {
        setError(err.message);
        console.error('Failed to load top stocks:', err);
      } else {
        console.debug('[Extension Error - Suppressed]', err.message);
      }
    } finally {
      setLoadingTop(false);
    }
  };

  const loadWatchlist = async (delay = 0.5) => {
    setLoadingWatchlist(true);
    setError(null);
    try {
      const data = await api.fetchWatchlist(delay);
      setWatchlist(data.watchlist || []);
      setOhlcDataWatchlist(data.ohlc_data || {});
    } catch (err) {
      // Suppress extension errors
      if (!isExtensionError(err)) {
        setError(err.message);
        console.error('Failed to load watchlist:', err);
      } else {
        console.debug('[Extension Error - Suppressed]', err.message);
      }
    } finally {
      setLoadingWatchlist(false);
    }
  };

  useEffect(() => {
    loadTopStocks();
    loadWatchlist();
  }, []);

  return {
    topStocks,
    watchlist,
    ohlcDataTop,
    ohlcDataWatchlist,
    loadingTop,
    loadingWatchlist,
    error,
    refreshTopStocks: loadTopStocks,
    refreshWatchlist: loadWatchlist,
  };
};
