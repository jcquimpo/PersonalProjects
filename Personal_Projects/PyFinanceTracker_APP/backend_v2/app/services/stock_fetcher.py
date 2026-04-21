"""Stock data fetching service using yfinance."""

import yfinance as yf
import pandas as pd
import time
import asyncio
from datetime import datetime
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor

# Watchlist configuration
WATCHLIST = ["AAPL", "NVDA", "MSFT", "META", "GOOGL"]
SYMBOL_NAMES = {
    "AAPL": "Apple Inc.",
    "NVDA": "NVIDIA Corporation",
    "MSFT": "Microsoft Corporation",
    "META": "Meta Platforms",
    "GOOGL": "Alphabet Inc."
}


class StockFetcher:
    """Service for fetching stock data."""

    @staticmethod
    def get_company_name(symbol: str) -> str:
        """Get company name for symbol."""
        if symbol in SYMBOL_NAMES:
            return SYMBOL_NAMES[symbol]
        try:
            info = yf.Ticker(symbol).info
            name = info.get("longName", symbol)
            SYMBOL_NAMES[symbol] = name
            return name
        except Exception:
            return symbol

    @staticmethod
    def get_ohlc_data(symbol: str, period: str = "7d") -> List[Dict]:
        """Fetch OHLC data for a stock."""
        try:
            df = yf.Ticker(symbol).history(period=period)[["Open", "High", "Low", "Close"]]
            
            ohlc = [
                {
                    "date": idx.strftime("%Y-%m-%d"),
                    "open": round(float(row["Open"]), 2),
                    "high": round(float(row["High"]), 2),
                    "low": round(float(row["Low"]), 2),
                    "close": round(float(row["Close"]), 2)
                }
                for idx, row in df.iterrows()
            ]
            return ohlc
        except Exception as e:
            print(f"Error fetching OHLC for {symbol}: {e}")
            return []

    @staticmethod
    def get_stock_performance(symbol: str) -> Optional[Dict]:
        """Get current performance metrics for a stock."""
        try:
            hist = yf.Ticker(symbol).history(period="2d", interval="1d")
            
            if hist.empty or len(hist) < 2:
                return None
            
            prev_close = hist["Close"].iloc[-2]
            last_close = hist["Close"].iloc[-1]
            
            if pd.isna(prev_close) or pd.isna(last_close) or prev_close == 0:
                return None
            
            pct = (last_close - prev_close) / prev_close * 100
            
            return {
                "symbol": symbol,
                "company_name": StockFetcher.get_company_name(symbol),
                "percentage_change": round(pct, 2),
                "current_price": round(float(last_close), 2),
                "previous_close": round(float(prev_close), 2)
            }
        except Exception as e:
            print(f"Error fetching performance for {symbol}: {e}")
            return None

    @classmethod
    def fetch_top_stocks(cls, limit: int = 50, delay: float = 0.7) -> Dict:
        """Fetch top 5 stocks by daily percentage move."""
        performance = []
        
        # Try to get S&P 500 symbols, fallback to default list
        try:
            from pytickersymbols import PyTickerSymbols
            stock_data = PyTickerSymbols()
            symbol_list = list(stock_data.get_sp_500_nyc_yahoo_tickers())[:limit]
        except Exception:
            symbol_list = ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN", "GOOGL", "META"]
        
        # Fetch performance for each symbol
        for sym in symbol_list:
            perf = cls.get_stock_performance(sym)
            if perf:
                performance.append(perf)
            time.sleep(delay)
        
        # Sort and get top 5
        performance.sort(key=lambda x: x["percentage_change"], reverse=True)
        top_5 = performance[:5]
        
        # Fetch OHLC data for top 5
        ohlc_data = {}
        for stock in top_5:
            ohlc_data[stock["symbol"]] = cls.get_ohlc_data(stock["symbol"], "7d")
            time.sleep(0.3)
        
        return {
            "top_stocks": top_5,
            "ohlc_data": ohlc_data,
            "fetched_at": datetime.now().isoformat()
        }

    @classmethod
    def fetch_watchlist(cls, delay: float = 0.5) -> Dict:
        """Fetch watchlist performance data."""
        performance = []
        
        for sym in WATCHLIST:
            perf = cls.get_stock_performance(sym)
            if perf:
                performance.append(perf)
            time.sleep(delay)
        
        performance.sort(key=lambda x: x["percentage_change"], reverse=True)
        
        # Fetch OHLC data for watchlist
        ohlc_data = {}
        for sym in WATCHLIST:
            ohlc_data[sym] = cls.get_ohlc_data(sym, "7d")
            time.sleep(0.3)
        
        return {
            "watchlist": performance,
            "ohlc_data": ohlc_data,
            "fetched_at": datetime.now().isoformat()
        }

    @classmethod
    def fetch_stock_data(cls, symbol: str, period: str = "7d") -> Dict:
        """Fetch detailed OHLC data for a specific stock."""
        try:
            ohlc = cls.get_ohlc_data(symbol, period)
            
            return {
                "symbol": symbol,
                "company_name": cls.get_company_name(symbol),
                "data": ohlc,
                "fetched_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}
