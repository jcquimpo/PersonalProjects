"""Stock data fetching service using yfinance."""

import yfinance as yf
import pandas as pd
import time
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor
import logging
from .mock_data import MOCK_WATCHLIST, MOCK_OHLC, MOCK_TOP_STOCKS
from threading import Lock, Semaphore
import signal
from contextlib import contextmanager

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Show DEBUG and above
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Watchlist configuration - reduced to minimize API calls
WATCHLIST = ["AAPL", "MSFT", "GOOGL"]  # Reduced from 5 to 3 symbols
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

# Global request rate limiter - max 20 requests per minute
MAX_REQUESTS_PER_MINUTE = 20
REQUEST_QUEUE_LOCK = Lock()
REQUEST_TIMES = []  # Track request timestamps for rate limiting
GLOBAL_REQUEST_SEMAPHORE = Semaphore(1)  # Allow only 1 concurrent request to yfinance
LAST_REQUEST_TIME = 0.0  # Track time of last request for inter-request delay
MIN_REQUEST_DELAY = 2.0  # Minimum 2 seconds between yfinance requests (reduced from 3s)
FETCH_TIMEOUT = 18.0  # Overall fetch timeout in seconds (leaves 2s buffer from 20s client timeout)

# Response cache - avoid re-fetching same data
RESPONSE_CACHE = {}  # {cache_key: (data, timestamp)}
RESPONSE_HISTORY = {}  # {cache_key: [(data, timestamp), ...]} - keep last 5 successful responses
CACHE_LOCK = Lock()


class TimeoutException(Exception):
    """Exception raised when operation exceeds timeout."""
    pass


class StockFetcher:
    """Service for fetching stock data with robust error handling and rate limiting."""

    @staticmethod
    def _check_rate_limit():
        """Check and enforce global rate limit with inter-request delays."""
        global REQUEST_TIMES, LAST_REQUEST_TIME
        
        with REQUEST_QUEUE_LOCK:
            current_time = time.time()
            
            # Enforce minimum delay between requests to yfinance
            time_since_last = current_time - LAST_REQUEST_TIME
            if time_since_last < MIN_REQUEST_DELAY:
                wait_time = MIN_REQUEST_DELAY - time_since_last
                logger.debug(f"Inter-request delay: sleeping {wait_time:.2f}s...")
                time.sleep(wait_time)
                current_time = time.time()
            
            # Remove timestamps older than 60 seconds
            REQUEST_TIMES = [t for t in REQUEST_TIMES if current_time - t < 60]
            
            # If we've hit the limit, wait
            if len(REQUEST_TIMES) >= MAX_REQUESTS_PER_MINUTE:
                oldest_request = REQUEST_TIMES[0]
                wait_time = 60 - (current_time - oldest_request)
                if wait_time > 0:
                    logger.info(f"Rate limit hit: {len(REQUEST_TIMES)}/{MAX_REQUESTS_PER_MINUTE} requests. Waiting {wait_time:.1f}s...")
                    time.sleep(wait_time + 0.1)
                    # Recursively check again after waiting
                    return StockFetcher._check_rate_limit()
            
            # Record this request
            LAST_REQUEST_TIME = current_time
            REQUEST_TIMES.append(current_time)
            logger.debug(f"Rate limit check passed. Requests in last minute: {len(REQUEST_TIMES)}/{MAX_REQUESTS_PER_MINUTE}")

    @staticmethod
    def _get_cache_key(cache_type: str, symbol: str = "", period: str = "") -> str:
        """Generate cache key for storing responses."""
        return f"{cache_type}:{symbol}:{period}".lower()

    @staticmethod
    def _get_cached_response(cache_key: str, fallback_to_history: bool = True) -> Optional[Dict]:
        """Get cached response if available and not expired. Fallback to history if enabled."""
        with CACHE_LOCK:
            # Try current cache first
            if cache_key in RESPONSE_CACHE:
                cached_data, timestamp = RESPONSE_CACHE[cache_key]
                age = (datetime.now() - timestamp).total_seconds()
                if age < 60:  # Cache valid for 60 seconds
                    logger.debug(f"Cache hit for {cache_key} (age: {age:.1f}s)")
                    return cached_data
                else:
                    logger.debug(f"Cache expired for {cache_key} (age: {age:.1f}s)")
                    del RESPONSE_CACHE[cache_key]
            
            # If fallback enabled and current cache miss, check history
            if fallback_to_history and cache_key in RESPONSE_HISTORY and RESPONSE_HISTORY[cache_key]:
                old_data, old_timestamp = RESPONSE_HISTORY[cache_key][-1]  # Get most recent
                age = (datetime.now() - old_timestamp).total_seconds()
                logger.warning(f"Cache miss, fallback to history for {cache_key} (age: {age:.1f}s)")
                # Add flag to indicate this is cached/stale data
                if isinstance(old_data, dict):
                    old_data["is_cached"] = True
                    old_data["cached_age_seconds"] = int(age)
                return old_data
            
            return None

    @staticmethod
    def _set_cache(cache_key: str, data: Dict):
        """Store response in cache and keep history of last 5 successful responses."""
        with CACHE_LOCK:
            timestamp = datetime.now()
            RESPONSE_CACHE[cache_key] = (data, timestamp)
            
            # Keep history of last 5 responses
            if cache_key not in RESPONSE_HISTORY:
                RESPONSE_HISTORY[cache_key] = []
            
            RESPONSE_HISTORY[cache_key].append((data.copy(), timestamp))
            
            # Keep only last 5 responses
            if len(RESPONSE_HISTORY[cache_key]) > 5:
                RESPONSE_HISTORY[cache_key] = RESPONSE_HISTORY[cache_key][-5:]
            
            logger.debug(f"Cache set for {cache_key} (history size: {len(RESPONSE_HISTORY[cache_key])})")

    @staticmethod
    def _retry_with_backoff(func, max_retries: int = 1, initial_delay: float = 0.5, backoff_factor: float = 2.0):
        """
        Retry a function with exponential backoff.
        Handles rate limiting (429) errors with increased backoff.
        
        Args:
            func: Function to retry
            max_retries: Maximum number of retry attempts (reduced to 1 for faster fallback to mock data)
            initial_delay: Initial delay in seconds
            backoff_factor: Multiply delay by this factor after each retry
            
        Returns:
            Function result or None if all retries fail
        """
        delay = initial_delay
        
        for attempt in range(max_retries + 1):
            try:
                # Check global rate limit before each request
                StockFetcher._check_rate_limit()
                
                # Limit concurrent requests with semaphore
                with GLOBAL_REQUEST_SEMAPHORE:
                    return func()
            except Exception as e:
                error_str = str(e).lower()
                
                # Check if it's a rate limiting error (429)
                is_rate_limit = "429" in error_str or "too many requests" in error_str
                
                if attempt == max_retries:
                    logger.warning(f"Failed after {max_retries + 1} attempts. Last error: {e}")
                    return None
                
                # For rate limits, give up quickly to show mock data faster
                if is_rate_limit:
                    logger.warning(f"Rate limit hit (429). Giving up quickly to show demo data. Error: {e}")
                    return None
                
                # For other errors, retry with backoff
                logger.info(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                delay *= backoff_factor
                
                time.sleep(delay)

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
            df = ticker.history(period=period, timeout=20)  # Increased timeout from 10 to 20 seconds
            
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
            hist = ticker.history(period="2d", interval="1d", timeout=20)  # Increased timeout from 10 to 20
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
                hist = ticker.history(period="5d", interval="1d", timeout=20)  # Increased timeout
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
    def fetch_top_stocks(cls, limit: int = 50, delay: float = 0.3) -> Dict:
        """
        Fetch top 5 stocks by daily percentage move.
        
        Note: This method uses a quick fallback to mock data if live data
        takes too long, to avoid exceeding client timeout (20s).
        """
        logger.info(f"Fetching top stocks (limit={limit}, delay={delay})")
        start_time = time.time()
        
        # Check cache first
        cache_key = cls._get_cache_key("top_stocks", "", "")
        cached = cls._get_cached_response(cache_key)
        if cached:
            return cached
        
        performance = []
        
        # Limit to maximum 5 symbols to avoid rate limiting
        safe_limit = min(limit, 5)
        logger.debug(f"Safe limit: {safe_limit} symbols (rate limiting: {MIN_REQUEST_DELAY}s between requests)")
        
        # Use hardcoded symbol list - pytickersymbols is unreliable and slow
        symbol_list = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"][:safe_limit]
        logger.debug(f"Using symbol list: {symbol_list}")
        
        # Fetch performance for each symbol with timeout check
        logger.info(f"Fetching performance for {len(symbol_list)} symbols...")
        for i, sym in enumerate(symbol_list, 1):
            # Check if we're approaching the overall timeout
            elapsed = time.time() - start_time
            if elapsed > FETCH_TIMEOUT - 5:  # Leave 5s buffer for OHLC fetching
                logger.warning(f"Approaching timeout ({elapsed:.1f}s elapsed). Using mock data.")
                return cls._get_mock_top_stocks()
            
            logger.debug(f"[{i}/{len(symbol_list)}] Fetching {sym}...")
            perf = cls.get_stock_performance(sym)
            if perf:
                performance.append(perf)
                logger.debug(f"[{i}/{len(symbol_list)}] {sym}: {perf['percentage_change']}%")
            else:
                logger.debug(f"[{i}/{len(symbol_list)}] {sym}: Failed")
            
            # Use minimal delay between requests
            time.sleep(0.5)
        
        # Sort and get top 5
        performance.sort(key=lambda x: x["percentage_change"], reverse=True)
        top_5 = performance[:5]
        logger.info(f"Found {len(top_5)} valid stocks, fetching OHLC data...")
        
        # If no valid top stocks found, use mock data
        if not top_5:
            logger.warning("No valid stocks obtained - using mock data for demonstration")
            return cls._get_mock_top_stocks()
        
        # Fetch OHLC data for top 5 (5 requests max) - with timeout check
        ohlc_data = {}
        for i, stock in enumerate(top_5, 1):
            elapsed = time.time() - start_time
            if elapsed > FETCH_TIMEOUT - 2:  # Abort if running out of time
                logger.warning(f"Running out of time ({elapsed:.1f}s). Skipping OHLC for remaining stocks.")
                break
            
            ohlc_data[stock["symbol"]] = cls.get_ohlc_data(stock["symbol"], "7d")
            logger.debug(f"[{i}/{len(top_5)}] {stock['symbol']}: OHLC fetched")
        
        result = {
            "top_stocks": top_5,
            "ohlc_data": ohlc_data,
            "fetched_at": datetime.now().isoformat()
        }
        
        # Cache the result
        cls._set_cache(cache_key, result)
        elapsed = time.time() - start_time
        logger.info(f"Top stocks fetch complete in {elapsed:.1f}s. Returning {len(top_5)} stocks.")
        return result
    
    @classmethod
    def _get_mock_top_stocks(cls) -> Dict:
        """Return mock data for top stocks as fast fallback."""
        top_5 = MOCK_TOP_STOCKS[:5]
        ohlc_data = {}
        for stock in top_5:
            ohlc_data[stock["symbol"]] = MOCK_OHLC.get(stock["symbol"], [])
        
        result = {
            "top_stocks": top_5,
            "ohlc_data": ohlc_data,
            "fetched_at": datetime.now().isoformat(),
            "is_demo_data": True,
            "note": "Using demonstration data - Yahoo Finance rate limited or timed out"
        }
        logger.info("Top stocks using mock data (due to rate limiting or timeout)")
        return result

    @classmethod
    def fetch_watchlist(cls, delay: float = 0.3) -> Dict:
        """
        Fetch watchlist performance data.
        
        Note: This method uses a quick fallback to mock data if live data
        takes too long, to avoid exceeding client timeout (20s).
        """
        logger.info(f"Fetching watchlist with {len(WATCHLIST)} symbols...")
        start_time = time.time()
        
        # Check cache first
        cache_key = cls._get_cache_key("watchlist", "", "")
        cached = cls._get_cached_response(cache_key)
        if cached:
            return cached
        
        performance = []
        
        for i, sym in enumerate(WATCHLIST, 1):
            # Check if we're approaching the overall timeout
            elapsed = time.time() - start_time
            if elapsed > FETCH_TIMEOUT - 5:  # Leave 5s buffer for OHLC fetching
                logger.warning(f"Approaching timeout ({elapsed:.1f}s elapsed). Using mock data.")
                return cls._get_mock_watchlist()
            
            perf = cls.get_stock_performance(sym)
            if perf:
                performance.append(perf)
                logger.debug(f"[{i}/{len(WATCHLIST)}] {sym}: {perf['percentage_change']}%")
            else:
                logger.debug(f"[{i}/{len(WATCHLIST)}] {sym}: Failed")
            
            time.sleep(0.5)
        
        performance.sort(key=lambda x: x["percentage_change"], reverse=True)
        
        # If no valid performance data, use mock data (for demonstration)
        if not performance:
            logger.warning("No performance data obtained - using mock data for demonstration")
            return cls._get_mock_watchlist()
        
        # Fetch OHLC data for watchlist (5 requests max) - with timeout check
        logger.info("Fetching OHLC data for watchlist...")
        ohlc_data = {}
        for i, sym in enumerate(WATCHLIST, 1):
            elapsed = time.time() - start_time
            if elapsed > FETCH_TIMEOUT - 2:  # Abort if running out of time
                logger.warning(f"Running out of time ({elapsed:.1f}s). Skipping OHLC for remaining stocks.")
                break
            
            ohlc_data[sym] = cls.get_ohlc_data(sym, "7d")
            logger.debug(f"[{i}/{len(WATCHLIST)}] {sym}: OHLC fetched")
        
        result = {
            "watchlist": performance,
            "ohlc_data": ohlc_data,
            "fetched_at": datetime.now().isoformat()
        }
        
        # Cache the result
        cls._set_cache(cache_key, result)
        elapsed = time.time() - start_time
        logger.info(f"Watchlist fetch complete in {elapsed:.1f}s.")
        return result
    
    @classmethod
    def _get_mock_watchlist(cls) -> Dict:
        """Return mock data for watchlist as fast fallback."""
        watchlist = MOCK_WATCHLIST
        ohlc_data = MOCK_OHLC
        
        result = {
            "watchlist": watchlist,
            "ohlc_data": ohlc_data,
            "fetched_at": datetime.now().isoformat(),
            "is_demo_data": True,
            "note": "Using demonstration data - Yahoo Finance rate limited or timed out"
        }
        logger.info("Watchlist using mock data (due to rate limiting or timeout)")
        return result

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
