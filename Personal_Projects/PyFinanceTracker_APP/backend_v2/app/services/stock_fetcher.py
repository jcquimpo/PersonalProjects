"""Stock data fetching service using yfinance."""

import yfinance as yf
import pandas as pd
import time
import asyncio
from datetime import datetime
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Show DEBUG and above
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Watchlist configuration
WATCHLIST = ["AAPL", "NVDA", "MSFT", "META", "GOOGL"]
SYMBOL_NAMES = {
    "AAPL": "Apple Inc.",
    "NVDA": "NVIDIA Corporation",
    "MSFT": "Microsoft Corporation",
    "META": "Meta Platforms",
    "GOOGL": "Alphabet Inc."
}

# Cache for failed symbols (to avoid re-requesting)
FAILED_SYMBOLS_CACHE = set()
CACHE_TIMEOUT = 300  # 5 minutes


class StockFetcher:
    """Service for fetching stock data with robust error handling."""

    @staticmethod
    def _retry_with_backoff(func, max_retries: int = 3, initial_delay: float = 1.0, backoff_factor: float = 2.0):
        """
        Retry a function with exponential backoff.
        
        Args:
            func: Function to retry
            max_retries: Maximum number of retry attempts
            initial_delay: Initial delay in seconds
            backoff_factor: Multiply delay by this factor after each retry
            
        Returns:
            Function result or None if all retries fail
        """
        delay = initial_delay
        
        for attempt in range(max_retries + 1):
            try:
                return func()
            except Exception as e:
                if attempt == max_retries:
                    logger.warning(f"Failed after {max_retries + 1} attempts. Last error: {e}")
                    return None
                
                logger.info(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                time.sleep(delay)
                delay *= backoff_factor

    @staticmethod
    def get_company_name(symbol: str) -> str:
        """Get company name for symbol with retry logic."""
        if symbol in SYMBOL_NAMES:
            return SYMBOL_NAMES[symbol]
        
        def fetch_name():
            ticker = yf.Ticker(symbol)
            info = ticker.info
            name = info.get("longName", symbol)
            if name and name != symbol:
                SYMBOL_NAMES[symbol] = name
            return name or symbol
        
        try:
            return StockFetcher._retry_with_backoff(fetch_name, max_retries=2, initial_delay=0.5)
        except Exception:
            return symbol

    @staticmethod
    def get_ohlc_data(symbol: str, period: str = "7d") -> List[Dict]:
        """Fetch OHLC data for a stock with retry logic and validation."""
        def fetch_ohlc():
            # Validate response
            ticker = yf.Ticker(symbol)
            logger.debug(f"Fetching OHLC for {symbol} with period={period}")
            df = ticker.history(period=period, timeout=10)  # Add timeout
            
            logger.debug(f"{symbol}: Got {len(df) if df is not None else 0} OHLC records")
            
            if df is None or df.empty:
                logger.warning(f"No OHLC data for {symbol} (period={period})")
                return []
            
            # Validate required columns exist
            required_columns = ["Open", "High", "Low", "Close"]
            if not all(col in df.columns for col in required_columns):
                logger.warning(f"Missing required OHLC columns for {symbol}. Got: {df.columns.tolist()}")
                return []
            
            ohlc = []
            for idx, row in df.iterrows():
                # Skip NaN values
                if pd.isna(row["Close"]):
                    logger.debug(f"{symbol}: Skipping NaN record for {idx}")
                    continue
                
                ohlc.append({
                    "date": idx.strftime("%Y-%m-%d"),
                    "open": round(float(row["Open"]), 2),
                    "high": round(float(row["High"]), 2),
                    "low": round(float(row["Low"]), 2),
                    "close": round(float(row["Close"]), 2)
                })
            
            if not ohlc:
                logger.warning(f"No valid OHLC records for {symbol}")
                return []
            
            logger.debug(f"{symbol}: Processed {len(ohlc)} OHLC records")
            return ohlc
        
        try:
            result = StockFetcher._retry_with_backoff(fetch_ohlc, max_retries=2, initial_delay=0.5)
            return result if result is not None else []
        except Exception as e:
            logger.error(f"Error fetching OHLC for {symbol}: {e}", exc_info=True)
            return []

    @staticmethod
    def get_stock_performance(symbol: str) -> Optional[Dict]:
        """Get current performance metrics for a stock with retry logic and validation."""
        # Check if symbol is in failed cache
        if symbol in FAILED_SYMBOLS_CACHE:
            logger.debug(f"Skipping {symbol} - recently failed")
            return None
        
        def fetch_performance():
            ticker = yf.Ticker(symbol)
            
            # Try 2 days first (market open/close comparison)
            hist = ticker.history(period="2d", interval="1d", timeout=10)
            logger.debug(f"{symbol}: Fetched 2d history - {len(hist)} records")
            
            # If we have at least 2 records, use them
            if hist is not None and not hist.empty and len(hist) >= 2:
                if "Close" not in hist.columns:
                    logger.warning(f"Missing 'Close' column for {symbol}")
                    return None
                
                prev_close = hist["Close"].iloc[-2]
                last_close = hist["Close"].iloc[-1]
            else:
                # Fallback: try 5d history if 2d not available (market might be closed)
                logger.debug(f"{symbol}: Fallback to 5d history")
                hist = ticker.history(period="5d", interval="1d", timeout=10)
                logger.debug(f"{symbol}: Fetched 5d history - {len(hist)} records")
                
                if hist is None or hist.empty or len(hist) < 2:
                    logger.warning(f"Insufficient data for {symbol} after fallback (got {len(hist) if hist is not None else 0} records)")
                    return None
                
                if "Close" not in hist.columns:
                    logger.warning(f"Missing 'Close' column for {symbol}")
                    return None
                
                # Use last 2 available records
                prev_close = hist["Close"].iloc[-2]
                last_close = hist["Close"].iloc[-1]
            
            # Validate prices are valid numbers
            if pd.isna(prev_close) or pd.isna(last_close):
                logger.warning(f"NaN price data for {symbol}: prev={prev_close}, last={last_close}")
                return None
            
            if prev_close == 0:
                logger.warning(f"Invalid previous close (0) for {symbol}")
                return None
            
            pct = (last_close - prev_close) / prev_close * 100
            
            result = {
                "symbol": symbol,
                "company_name": StockFetcher.get_company_name(symbol),
                "percentage_change": round(pct, 2),
                "current_price": round(float(last_close), 2),
                "previous_close": round(float(prev_close), 2)
            }
            logger.debug(f"{symbol}: Success - {result['percentage_change']}% change")
            return result
        
        try:
            result = StockFetcher._retry_with_backoff(fetch_performance, max_retries=2, initial_delay=0.8)
            if result is None:
                logger.warning(f"Adding {symbol} to failed cache")
                FAILED_SYMBOLS_CACHE.add(symbol)
            return result
        except Exception as e:
            logger.error(f"Error fetching performance for {symbol}: {e}", exc_info=True)
            FAILED_SYMBOLS_CACHE.add(symbol)
            return None

    @classmethod
    def fetch_top_stocks(cls, limit: int = 50, delay: float = 0.7) -> Dict:
        """Fetch top 5 stocks by daily percentage move."""
        logger.info(f"Fetching top stocks (limit={limit}, delay={delay})")
        performance = []
        
        # Limit to maximum 30 symbols to avoid excessive API calls and rate limiting
        safe_limit = min(limit, 30)
        
        # Try to get S&P 500 symbols, fallback to default list
        try:
            from pytickersymbols import PyTickerSymbols
            stock_data = PyTickerSymbols()
            symbol_list = list(stock_data.get_sp_500_nyc_yahoo_tickers())[:safe_limit]
            logger.info(f"Fetched {len(symbol_list)} S&P 500 symbols")
        except Exception as e:
            logger.warning(f"Failed to get S&P 500 symbols: {e}. Using default list.")
            symbol_list = ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN", "GOOGL", "META", "NFLX", "GOOG", "JPM"]
        
        # Fetch performance for each symbol with increased delay for rate limiting
        logger.info(f"Fetching performance for {len(symbol_list)} symbols...")
        for i, sym in enumerate(symbol_list, 1):
            perf = cls.get_stock_performance(sym)
            if perf:
                performance.append(perf)
                logger.debug(f"[{i}/{len(symbol_list)}] {sym}: {perf['percentage_change']}%")
            else:
                logger.debug(f"[{i}/{len(symbol_list)}] {sym}: Failed")
            
            # Adaptive delay: increase if we have few results (indicates rate limiting)
            adaptive_delay = delay + (0.5 if len(performance) < i * 0.3 else 0)
            time.sleep(adaptive_delay)
        
        # Sort and get top 5
        performance.sort(key=lambda x: x["percentage_change"], reverse=True)
        top_5 = performance[:5]
        logger.info(f"Found {len(top_5)} valid stocks, fetching OHLC data...")
        
        # Fetch OHLC data for top 5
        ohlc_data = {}
        for i, stock in enumerate(top_5, 1):
            ohlc_data[stock["symbol"]] = cls.get_ohlc_data(stock["symbol"], "7d")
            logger.debug(f"[{i}/{len(top_5)}] {stock['symbol']}: OHLC fetched")
            time.sleep(0.5)  # Delay between OHLC requests
        
        logger.info(f"Top stocks fetch complete. Returning {len(top_5)} stocks.")
        return {
            "top_stocks": top_5,
            "ohlc_data": ohlc_data,
            "fetched_at": datetime.now().isoformat()
        }

    @classmethod
    def fetch_watchlist(cls, delay: float = 0.5) -> Dict:
        """Fetch watchlist performance data."""
        logger.info(f"Fetching watchlist with {len(WATCHLIST)} symbols...")
        performance = []
        
        for i, sym in enumerate(WATCHLIST, 1):
            perf = cls.get_stock_performance(sym)
            if perf:
                performance.append(perf)
                logger.debug(f"[{i}/{len(WATCHLIST)}] {sym}: {perf['percentage_change']}%")
            else:
                logger.debug(f"[{i}/{len(WATCHLIST)}] {sym}: Failed")
            
            time.sleep(delay)
        
        performance.sort(key=lambda x: x["percentage_change"], reverse=True)
        
        # Fetch OHLC data for watchlist
        logger.info("Fetching OHLC data for watchlist...")
        ohlc_data = {}
        for i, sym in enumerate(WATCHLIST, 1):
            ohlc_data[sym] = cls.get_ohlc_data(sym, "7d")
            logger.debug(f"[{i}/{len(WATCHLIST)}] {sym}: OHLC fetched")
            time.sleep(0.5)
        
        logger.info("Watchlist fetch complete.")
        return {
            "watchlist": performance,
            "ohlc_data": ohlc_data,
            "fetched_at": datetime.now().isoformat()
        }

    @classmethod
    def fetch_stock_data(cls, symbol: str, period: str = "7d") -> Dict:
        """Fetch detailed OHLC data for a specific stock."""
        logger.info(f"Fetching detailed data for {symbol} (period={period})")
        try:
            ohlc = cls.get_ohlc_data(symbol, period)
            
            if not ohlc:
                logger.warning(f"No OHLC data returned for {symbol}")
            
            return {
                "symbol": symbol,
                "company_name": cls.get_company_name(symbol),
                "data": ohlc,
                "fetched_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error in fetch_stock_data for {symbol}: {e}")
            return {"error": str(e)}
