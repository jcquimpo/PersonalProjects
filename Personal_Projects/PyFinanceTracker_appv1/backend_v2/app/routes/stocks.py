"""API routes for stock data."""

from fastapi import APIRouter, Query
from app.services.stock_fetcher import StockFetcher
from app.models.stock import (
    TopStocksResponse,
    WatchlistResponse,
    StockDetail,
    ErrorResponse
)

router = APIRouter(prefix="/api", tags=["stocks"])


@router.get("/top-stocks", response_model=TopStocksResponse)
async def get_top_stocks(
    limit: int = Query(10, ge=5, le=100),
    delay: float = Query(0.3, ge=0.1, le=2.0)
):
    """
    Get top 5 performing stocks.
    
    RATE LIMITING: Max 10 symbols analyzed (10 + 5 OHLC = 15 requests max).
    This ensures compliance with 20 requests/minute global limit.
    
    Args:
        limit: Number of stocks to analyze (5-100, capped at 10)
        delay: Delay between API calls in seconds (0.1-2.0)
    
    Returns:
        TopStocksResponse with top 5 stocks and OHLC data
    """
    return StockFetcher.fetch_top_stocks(limit=limit, delay=delay)


@router.get("/watchlist", response_model=WatchlistResponse)
async def get_watchlist(delay: float = Query(0.3, ge=0.1, le=2.0)):
    """
    Get watchlist performance data.
    
    RATE LIMITING: Fetches 5 watchlist symbols (5 + 5 OHLC = 10 requests max).
    This ensures compliance with 20 requests/minute global limit.
    
    Args:
        delay: Delay between API calls in seconds (0.1-2.0)
    
    Returns:
        WatchlistResponse with watchlist stocks and OHLC data
    """
    return StockFetcher.fetch_watchlist(delay=delay)

@router.get("/quick-watchlist")
async def get_quick_watchlist(delay: float = Query(0.2, ge=0.1, le=1.0)):
    """
    Get watchlist performance data quickly (without OHLC data).
    
    RATE LIMITING: Fetches only 5 watchlist symbols (5 requests only).
    No OHLC data means this completes in 3-5 seconds.
    This is the fastest endpoint for quick updates.
    
    Args:
        delay: Delay between API calls in seconds (0.1-1.0)
    
    Returns:
        Quick watchlist with symbols and performance metrics only
    """
    import time
    from datetime import datetime
    from app.services.stock_fetcher import StockFetcher, WATCHLIST
    
    # Check cache first
    cache_key = StockFetcher._get_cache_key("quick_watchlist", "", "")
    cached = StockFetcher._get_cached_response(cache_key)
    if cached:
        return cached
    
    performance = []
    
    for i, sym in enumerate(WATCHLIST, 1):
        perf = StockFetcher.get_stock_performance(sym)
        if perf:
            performance.append(perf)
        time.sleep(delay)
    
    performance.sort(key=lambda x: x["percentage_change"], reverse=True)
    
    result = {
        "watchlist": performance,
        "ohlc_data": {},  # Empty for quick endpoint
        "fetched_at": datetime.now().isoformat()
    }
    
    # Cache the result
    StockFetcher._set_cache(cache_key, result)
    return result

@router.get("/stock/{symbol}", response_model=StockDetail)
async def get_stock_data(
    symbol: str,
    period: str = Query("7d", regex="^(1d|5d|1mo|3mo|6mo|1y|2y|5y|10y|ytd|max)$")
):
    """
    Get detailed stock data for a specific symbol.
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL)
        period: Time period for OHLC data
    
    Returns:
        StockDetail with OHLC data for the specified period
    """
    result = StockFetcher.fetch_stock_data(symbol, period)
    
    if "error" in result:
        return {"error": result["error"]}
    
    return result


@router.get("/diagnostic")
async def diagnostic():
    """
    Diagnostic endpoint to test if yfinance is working.
    Tries to fetch a single stock and returns detailed info.
    """
    import yfinance as yf
    
    diagnostics = {
        "status": "ok",
        "message": "Diagnostic test complete",
        "tests": {}
    }
    
    # Test 1: Can we import yfinance?
    diagnostics["tests"]["yfinance_import"] = "ok"
    
    # Test 2: Can we fetch a ticker?
    try:
        ticker = yf.Ticker("AAPL")
        diagnostics["tests"]["yfinance_connection"] = "ok"
    except Exception as e:
        diagnostics["tests"]["yfinance_connection"] = f"failed: {e}"
        diagnostics["status"] = "error"
    
    # Test 3: Can we get history?
    try:
        hist = ticker.history(period="2d")
        if hist.empty:
            diagnostics["tests"]["history_2d"] = "empty (market may be closed)"
        else:
            diagnostics["tests"]["history_2d"] = f"ok ({len(hist)} records)"
    except Exception as e:
        diagnostics["tests"]["history_2d"] = f"failed: {e}"
        diagnostics["status"] = "error"
    
    # Test 4: Can we get 5d history?
    try:
        hist_5d = ticker.history(period="5d")
        if hist_5d.empty:
            diagnostics["tests"]["history_5d"] = "empty"
        else:
            diagnostics["tests"]["history_5d"] = f"ok ({len(hist_5d)} records)"
    except Exception as e:
        diagnostics["tests"]["history_5d"] = f"failed: {e}"
        diagnostics["status"] = "error"
    
    # Test 5: Can we get info?
    try:
        info = ticker.info
        if info:
            diagnostics["tests"]["info"] = f"ok ({len(info)} fields)"
        else:
            diagnostics["tests"]["info"] = "empty"
    except Exception as e:
        diagnostics["tests"]["info"] = f"failed: {e}"
    
    # Test 6: Test StockFetcher directly
    try:
        perf = StockFetcher.get_stock_performance("AAPL")
        if perf:
            diagnostics["tests"]["stock_fetcher"] = f"ok - {perf['percentage_change']}% change"
        else:
            diagnostics["tests"]["stock_fetcher"] = "returned None (may need to check logs)"
    except Exception as e:
        diagnostics["tests"]["stock_fetcher"] = f"failed: {e}"
        diagnostics["status"] = "error"
    
    return diagnostics


@router.post("/reset-cache")
async def reset_cache():
    """
    Reset the failed symbols cache.
    Useful if symbols were temporarily unavailable due to market hours.
    """
    from app.services.stock_fetcher import FAILED_SYMBOLS_CACHE
    cache_size = len(FAILED_SYMBOLS_CACHE)
    FAILED_SYMBOLS_CACHE.clear()
    return {
        "status": "ok",
        "message": f"Cache cleared ({cache_size} symbols removed)"
    }


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "Stock API is running"}
