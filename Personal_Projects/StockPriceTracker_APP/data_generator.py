"""
Stock data generation module - can be called from Top_Stocks.py or Flask app.
Generates mock OHLC data and watchlist performance metrics.
"""
import time
import numpy as np
import pandas as pd
from datetime import datetime
import json
import os

# ===== CONFIGURATION =====
SYMBOL_NAMES = {
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corporation",
    "NVDA": "NVIDIA Corporation",
    "TSLA": "Tesla Inc.",
    "AMZN": "Amazon Inc.",
    "GOOGL": "Alphabet Inc.",
    "META": "Meta Platforms",
    "BRK.B": "Berkshire Hathaway",
    "JNJ": "Johnson & Johnson",
    "V": "Visa Inc.",
}

RELIABLE_SYMBOLS = [
    "AAPL", "MSFT", "NVDA", "TSLA", "AMZN", "GOOGL", "META", "GOOG",
    "BRK.B", "JNJ", "V", "WMT", "PG", "XOM", "JPM", "MA", "VZ", "HD",
    "PFE", "KO", "CSCO", "ADBE", "CRM", "NFLX", "AVGO", "AMD", "INTC",
    "TSM", "SAP", "ASML", "BABA", "NVO", "SHOP", "SE", "CPRT", "CRWD", "DECK"
]

WATCHLIST = ["AAPL", "NVDA", "MSFT", "META", "GOOGL"]


def get_company_name(symbol: str) -> str:
    """Get company name from cache or return placeholder."""
    return SYMBOL_NAMES.get(symbol, f"{symbol}")


def generate_mock_ohlc(symbol: str, days: int = 7, base_price: float = 150.0) -> pd.DataFrame:
    """Generate deterministic mock OHLC data — same symbol always produces same data."""
    np.random.seed(abs(hash(symbol)) % 2**31)
    dates = pd.date_range(end=datetime.now().date(), periods=days, freq='B')
    
    # Generate price series
    closes = base_price + np.cumsum(np.random.randn(days) * 2)
    closes = np.clip(closes, 1, None)
    
    df = pd.DataFrame({
        "Open":  closes + np.random.uniform(-1, 1, days),
        "High":  closes + np.abs(np.random.randn(days) * 1.5),
        "Low":   closes - np.abs(np.random.randn(days) * 1.5),
        "Close": closes,
    }, index=dates)
    
    return df.clip(lower=0.01)


def fetch_ohlc_data(symbols: list[str], period: str = "7d", delay: float = 0.2, verbose: bool = True) -> dict:
    """Fetch OHLC data for symbols."""
    ohlc_data = {}
    days = 2 if "2d" in period else 7
    
    for i, sym in enumerate(symbols, 1):
        if verbose:
            print(f"  [{i}/{len(symbols)}] OHLC {sym}", end="", flush=True)
        
        # Generate deterministic mock data
        base_price = (abs(hash(sym)) % 400) + 50  # $50-$450
        df = generate_mock_ohlc(sym, days=days, base_price=float(base_price))
        
        if not df.empty:
            ohlc_data[sym] = df[["Open", "High", "Low", "Close"]]
            if verbose:
                print(f"  ✓  ({len(df)} days)")
        else:
            if verbose:
                print("  ✗ (no data)")
        
        time.sleep(delay)
    
    return ohlc_data


def format_ohlc_for_export(ohlc_data: dict) -> dict:
    """Convert DataFrames to dictionary format for JSON export."""
    formatted = {}
    for symbol, df in ohlc_data.items():
        formatted[symbol] = {
            'dates': [str(date.date()) for date in df.index],
            'opens': df['Open'].tolist(),
            'highs': df['High'].tolist(),
            'lows': df['Low'].tolist(),
            'closes': df['Close'].tolist()
        }
    return formatted


def get_top_5_symbols(limit: int = 30, delay: float = 0.1, verbose: bool = True) -> tuple:
    """Generate top 5 mock movers. Returns (symbols_list, performance_data)."""
    symbol_list = RELIABLE_SYMBOLS[:limit]
    
    if verbose:
        print(f"Generating {len(symbol_list)} mock stock movers (global)...")
    performance = []
    
    for i, sym in enumerate(symbol_list, 1):
        if verbose and (i % 10 == 0 or i == len(symbol_list)):
            print(f"  [{i}/{len(symbol_list)}] processing symbols")
        
        if verbose:
            print(f"  [{i}/{len(symbol_list)}] {sym}", end="", flush=True)
        
        # Generate 2-day history
        base_price = (abs(hash(sym)) % 400) + 50
        df = generate_mock_ohlc(sym, days=2, base_price=float(base_price))
        
        if not df.empty and len(df) >= 2:
            prev_close = df["Close"].iloc[-2]
            last_close = df["Close"].iloc[-1]
            
            if prev_close > 0:
                pct = (last_close - prev_close) / prev_close * 100
                performance.append((sym, pct))
                if verbose:
                    print(f"  ✓  {pct:+.2f}%")
            else:
                if verbose:
                    print("  ✗ (invalid price)")
        else:
            if verbose:
                print("  ✗ (no data)")
        
        time.sleep(delay)
    
    if verbose:
        print(f"\n✓  Generated {len(performance)} symbols.\n")
    
    if not performance:
        return RELIABLE_SYMBOLS[:5], []
    
    # Sort by % change
    performance.sort(key=lambda x: x[1], reverse=True)
    top5 = [sym for sym, _ in performance[:5]]
    top5_performance = performance[:5]
    
    if verbose:
        print("Top 5 movers by % change:")
        for sym, pct in performance[:5]:
            name = get_company_name(sym)
            print(f"  {sym:8s} {name:35s}  {pct:+.2f}%")
    
    return top5, top5_performance


def monitor_watchlist(symbols: list[str], delay: float = 0.5, verbose: bool = True) -> list[tuple]:
    """Monitor watchlist for daily performance. Returns list of (symbol, pct_change) tuples."""
    performance = []
    for i, sym in enumerate(symbols):
        try:
            if verbose:
                print(f"[{i+1}/{len(symbols)}] Monitoring {sym}...", end="", flush=True)
            base_price = (abs(hash(sym)) % 400) + 50
            df = generate_mock_ohlc(sym, days=2, base_price=float(base_price))
            
            if df.empty or len(df) < 2:
                if verbose:
                    print(" (insufficient data)")
                continue
            
            prev_close = df["Close"].iloc[-2]
            last_close = df["Close"].iloc[-1]
            pct = (last_close - prev_close) / prev_close * 100
            performance.append((sym, pct))
            if verbose:
                print(f" ✓ {pct:+.2f}%")
        except Exception as e:
            if verbose:
                print(f" ✗ {str(e)[:30]}")
        time.sleep(delay)
    
    performance.sort(key=lambda x: x[1], reverse=True)
    return performance


def generate_stock_data(verbose: bool = True) -> dict:
    """
    Generate all stock data and return as dictionary.
    This is the main function that can be called from Flask or Top_Stocks.py.
    
    Args:
        verbose: If True, print progress messages. If False, run silently.
    
    Returns:
        Dictionary containing stock data ready for JSON export.
    """
    if verbose:
        print("=" * 70)
        print("GENERATING STOCK DATA")
        print("=" * 70)
    
    # ===== ANALYSIS 1: TOP MOVERS =====
    if verbose:
        print("\nANALYSIS 1: TOP MOVERS")
        print("=" * 70)
    
    top5_symbols, top5_performance = get_top_5_symbols(limit=30, delay=0.05, verbose=verbose)
    
    if verbose:
        print(f"\nFinal Top 5 Symbols: {top5_symbols}")
        print("=" * 70)
        print("\nFetching 7-day OHLC data...")
    
    ohlc_data = fetch_ohlc_data(top5_symbols, period="7d", delay=0.05, verbose=verbose)
    
    # ===== ANALYSIS 2: WATCHLIST =====
    if verbose:
        print("\n" + "=" * 70)
        print("ANALYSIS 2: WATCHLIST MONITORING")
        print("=" * 70)
        print("\nAnalyzing watchlist performance...")
    
    results = monitor_watchlist(WATCHLIST, delay=0.05, verbose=verbose)
    
    if verbose:
        print("\nFetching 7-Day OHLC for watchlist...")
    
    watchlist_ohlc_data = fetch_ohlc_data(WATCHLIST, period="7d", delay=0.05, verbose=verbose)
    
    # ===== PREPARE EXPORT DATA =====
    export_data = {
        'timestamp': datetime.now().isoformat(),
        'topMovers': {
            'symbols': top5_symbols,
            'performance': [[sym, float(pct)] for sym, pct in top5_performance],
            'ohlc': format_ohlc_for_export(ohlc_data)
        },
        'watchlist': {
            'symbols': WATCHLIST,
            'performance': [[sym, float(pct)] for sym, pct in results],
            'ohlc': format_ohlc_for_export(watchlist_ohlc_data)
        },
        'symbolNames': SYMBOL_NAMES
    }
    
    if verbose:
        print("\n" + "=" * 70)
        print("DATA GENERATION COMPLETE")
        print("=" * 70)
    
    return export_data


def save_stock_data(export_data: dict, output_dir: str) -> str:
    """
    Save stock data to JSON file.
    
    Args:
        export_data: Dictionary containing stock data
        output_dir: Directory to save the JSON file to
    
    Returns:
        Path to the saved file
    """
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'stock_data.json')
    
    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    return output_file
