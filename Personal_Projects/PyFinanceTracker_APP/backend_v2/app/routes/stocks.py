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


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "Stock API is running"}
