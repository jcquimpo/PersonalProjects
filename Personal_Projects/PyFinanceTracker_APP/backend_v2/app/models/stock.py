"""Data models for stock information."""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class OHLCData(BaseModel):
    """Open, High, Low, Close data for a stock."""
    date: str
    open: float
    high: float
    low: float
    close: float


class StockPerformance(BaseModel):
    """Stock performance metrics."""
    symbol: str
    company_name: str
    percentage_change: float
    current_price: float
    previous_close: float


class StockDetail(BaseModel):
    """Detailed stock information with OHLC data."""
    symbol: str
    company_name: str
    data: List[OHLCData]
    fetched_at: datetime


class TopStocksResponse(BaseModel):
    """Response for top performing stocks."""
    top_stocks: List[StockPerformance]
    ohlc_data: dict  # {symbol: [OHLCData]}
    fetched_at: datetime


class WatchlistResponse(BaseModel):
    """Response for watchlist data."""
    watchlist: List[StockPerformance]
    ohlc_data: dict  # {symbol: [OHLCData]}
    fetched_at: datetime


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
