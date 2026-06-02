#!/usr/bin/env python3
"""Stock data fetcher for dashboard backend."""

import sys
import json
import yfinance as yf
import pandas as pd
import time
from datetime import datetime

# Watchlist configuration
WATCHLIST = ["AAPL", "NVDA", "MSFT", "META", "GOOGL"]
SYMBOL_NAMES = {
    "AAPL": "Apple Inc.",
    "NVDA": "NVIDIA Corporation",
    "MSFT": "Microsoft Corporation",
    "META": "Meta Platforms",
    "GOOGL": "Alphabet Inc."
}

def get_company_name(symbol: str) -> str:
    """Get company name for symbol."""
    if symbol in SYMBOL_NAMES:
        return SYMBOL_NAMES[symbol]
    try:
        info = yf.Ticker(symbol).info
        name = info.get("longName", symbol)
        SYMBOL_NAMES[symbol] = name
        return name
    except:
        return symbol

def fetch_top_stocks(limit: int = 50, delay: float = 0.7) -> dict:
    """Fetch top 5 stocks by daily percentage move."""
    from pytickersymbols import PyTickerSymbols
    
    try:
        stock_data = PyTickerSymbols()
        symbol_list = list(stock_data.get_sp_500_nyc_yahoo_tickers())[:limit]
    except:
        symbol_list = ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN", "GOOGL", "META"]
    
    performance = []
    
    for sym in symbol_list:
        try:
            hist = yf.Ticker(sym).history(period="2d", interval="1d")
            
            if hist.empty or len(hist) < 2:
                continue
            
            prev_close = hist["Close"].iloc[-2]
            last_close = hist["Close"].iloc[-1]
            
            if pd.isna(prev_close) or pd.isna(last_close) or prev_close == 0:
                continue
            
            pct = (last_close - prev_close) / prev_close * 100
            performance.append({
                "symbol": sym,
                "company_name": get_company_name(sym),
                "percentage_change": round(pct, 2),
                "current_price": round(last_close, 2),
                "previous_close": round(prev_close, 2)
            })
        except:
            pass
        
        time.sleep(delay)
    
    performance.sort(key=lambda x: x["percentage_change"], reverse=True)
    
    result = {
        "top_stocks": performance[:5],
        "fetched_at": datetime.now().isoformat()
    }
    
    # Fetch OHLC data for top 5
    top_symbols = [s["symbol"] for s in result["top_stocks"]]
    ohlc_data = {}
    
    for sym in top_symbols:
        try:
            df = yf.Ticker(sym).history(period="7d", interval="1d")[["Open", "High", "Low", "Close"]]
            ohlc_data[sym] = [
                {
                    "date": idx.strftime("%Y-%m-%d"),
                    "open": round(row["Open"], 2),
                    "high": round(row["High"], 2),
                    "low": round(row["Low"], 2),
                    "close": round(row["Close"], 2)
                }
                for idx, row in df.iterrows()
            ]
        except:
            pass
    
    result["ohlc_data"] = ohlc_data
    return result

def fetch_watchlist(delay: float = 0.5) -> dict:
    """Fetch watchlist performance data."""
    performance = []
    
    for sym in WATCHLIST:
        try:
            hist = yf.Ticker(sym).history(period="2d")
            
            if len(hist) < 2:
                continue
            
            prev_close = hist["Close"].iloc[-2]
            last_close = hist["Close"].iloc[-1]
            pct = (last_close - prev_close) / prev_close * 100
            
            performance.append({
                "symbol": sym,
                "company_name": get_company_name(sym),
                "percentage_change": round(pct, 2),
                "current_price": round(last_close, 2),
                "previous_close": round(prev_close, 2)
            })
        except:
            pass
        
        time.sleep(delay)
    
    performance.sort(key=lambda x: x["percentage_change"], reverse=True)
    
    result = {
        "watchlist": performance,
        "fetched_at": datetime.now().isoformat()
    }
    
    # Fetch OHLC data for watchlist
    ohlc_data = {}
    
    for sym in WATCHLIST:
        try:
            df = yf.Ticker(sym).history(period="7d")[["Open", "High", "Low", "Close"]]
            ohlc_data[sym] = [
                {
                    "date": idx.strftime("%Y-%m-%d"),
                    "open": round(row["Open"], 2),
                    "high": round(row["High"], 2),
                    "low": round(row["Low"], 2),
                    "close": round(row["Close"], 2)
                }
                for idx, row in df.iterrows()
            ]
        except:
            pass
    
    result["ohlc_data"] = ohlc_data
    return result

def fetch_stock_data(symbol: str, period: str = "7d") -> dict:
    """Fetch OHLC data for a specific stock."""
    try:
        df = yf.Ticker(symbol).history(period=period)[["Open", "High", "Low", "Close"]]
        
        ohlc = [
            {
                "date": idx.strftime("%Y-%m-%d"),
                "open": round(row["Open"], 2),
                "high": round(row["High"], 2),
                "low": round(row["Low"], 2),
                "close": round(row["Close"], 2)
            }
            for idx, row in df.iterrows()
        ]
        
        return {
            "symbol": symbol,
            "company_name": get_company_name(symbol),
            "data": ohlc,
            "fetched_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No command provided"}))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "top-stocks":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        delay = float(sys.argv[3]) if len(sys.argv) > 3 else 0.7
        result = fetch_top_stocks(limit, delay)
    elif command == "watchlist":
        delay = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
        result = fetch_watchlist(delay)
    elif command == "stock-data":
        symbol = sys.argv[2] if len(sys.argv) > 2 else "AAPL"
        period = sys.argv[3] if len(sys.argv) > 3 else "7d"
        result = fetch_stock_data(symbol, period)
    else:
        result = {"error": "Unknown command"}
    
    print(json.dumps(result))
