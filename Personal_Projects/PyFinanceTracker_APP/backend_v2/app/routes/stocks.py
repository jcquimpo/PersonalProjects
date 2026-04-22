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
    limit: int = Query(50, ge=10, le=500),
    delay: float = Query(0.7, ge=0.1, le=5.0)
):
    """
    Get top 5 performing stocks.
    
    Args:
        limit: Number of stocks to analyze (10-500)
        delay: Delay between API calls in seconds (0.1-5.0)
    
    Returns:
        TopStocksResponse with top 5 stocks and OHLC data
    """
    return StockFetcher.fetch_top_stocks(limit=limit, delay=delay)


@router.get("/watchlist", response_model=WatchlistResponse)
async def get_watchlist(delay: float = Query(0.5, ge=0.1, le=5.0)):
    """
    Get watchlist performance data.
    
    Args:
        delay: Delay between API calls in seconds (0.1-5.0)
    
    Returns:
        WatchlistResponse with watchlist stocks and OHLC data
    """
    return StockFetcher.fetch_watchlist(delay=delay)


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
