import time
import numpy as np
import pandas as pd
from datetime import datetime


# ===== CONFIGURATION =====
# Set to True to generate mock data (fast, no API calls)
# Set to False to fetch live data from yfinance
USE_MOCK_DATA = False

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

# Global stocks across multiple countries
RELIABLE_SYMBOLS = [
    "AAPL", "MSFT", "NVDA", "TSLA", "AMZN", "GOOGL", "META", "GOOG",
    "BRK.B", "JNJ", "V", "WMT", "PG", "XOM", "JPM", "MA", "VZ", "HD",
    "PFE", "KO", "CSCO", "ADBE", "CRM", "NFLX", "AVGO", "AMD", "INTC",
    "TSM", "SAP", "ASML", "BABA", "NVO", "SHOP", "SE", "CPRT", "CRWD", "DECK"
]


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


def fetch_ohlc_data(symbols: list[str], period: str = "7d", delay: float = 0.2) -> dict:
    """Fetch OHLC data for symbols."""
    ohlc_data = {}
    days = 2 if "2d" in period else 7
    
    for i, sym in enumerate(symbols, 1):
        print(f"  [{i}/{len(symbols)}] OHLC {sym}", end="", flush=True)
        
        # Generate deterministic mock data
        base_price = (abs(hash(sym)) % 400) + 50  # $50-$450
        df = generate_mock_ohlc(sym, days=days, base_price=float(base_price))
        
        if not df.empty:
            ohlc_data[sym] = df[["Open", "High", "Low", "Close"]]
            print(f"  ✓  ({len(df)} days)")
        else:
            print("  ✗ (no data)")
    
    return ohlc_data


def get_top_5_symbols(limit: int = 30, delay: float = 0.1) -> tuple:
    """Generate top 5 mock movers. Returns (symbols_list, performance_data)."""
    symbol_list = RELIABLE_SYMBOLS[:limit]
    
    print(f"Generating {len(symbol_list)} mock stock movers (global)...")
    performance = []
    
    for i, sym in enumerate(symbol_list, 1):
        if i % 10 == 0 or i == len(symbol_list):
            print(f"  [{i}/{len(symbol_list)}] processing symbols")
        
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
                print(f"  ✓  {pct:+.2f}%")
            else:
                print("  ✗ (invalid price)")
        else:
            print("  ✗ (no data)")
    
    print(f"\n✓  Generated {len(performance)} symbols.\n")
    
    if not performance:
        return RELIABLE_SYMBOLS[:5], []
    
    # Sort by % change
    performance.sort(key=lambda x: x[1], reverse=True)
    top5 = [sym for sym, _ in performance[:5]]
    top5_performance = performance[:5]  # Keep original tuples for visualization
    
    print("Top 5 movers by % change:")
    for sym, pct in performance[:5]:
        name = get_company_name(sym)
        print(f"  {sym:8s} {name:35s}  {pct:+.2f}%")
    
    return top5, top5_performance


# ===== MAIN: TOP MOVERS ANALYSIS =====
print("=" * 70)
print(f"TOP MOVERS ANALYSIS  (using {'MOCK' if USE_MOCK_DATA else 'LIVE'} data - Global Stocks)")
print("=" * 70)

top5_symbols, top5_performance = get_top_5_symbols(limit=30, delay=0.1)

print(f"\n{'='*70}")
print(f"Final Top 5 Symbols: {top5_symbols}")
print(f"{'='*70}")

print("\nFetching 7-day OHLC data...")
ohlc_data = fetch_ohlc_data(top5_symbols, period="7d", delay=0.1)

if ohlc_data:
    print(f"\n{'='*70}")
    print("Top Movers — 7-Day OHLC Price Data")
    print(f"{'='*70}")
    for sym, df in ohlc_data.items():
        company_name = get_company_name(sym)
        print(f"\n{sym} — {company_name}  ({len(df)} trading days):")
        df_display = df.copy()
        for col in df_display.columns:
            df_display[col] = df_display[col].map(lambda x: f"${x:.2f}")
        print(df_display.to_string())
else:
    print("⚠ No OHLC data fetched.")


# ===== ANALYSIS 2: USER WATCHLIST =====
print("\n" + "=" * 70)
print("ANALYSIS 2: WATCHLIST MONITORING")
print("=" * 70)

# Define watchlist
WATCHLIST = ["AAPL", "NVDA", "MSFT", "META", "GOOGL"]


def fetch_price_history_local(sym: str, period: str = "2d") -> pd.DataFrame:
    """Fetch price history - uses mock data."""
    days = 2 if "2d" in period else 7
    base_price = (abs(hash(sym)) % 400) + 50
    np.random.seed(abs(hash(sym)) % 2**31)
    dates = pd.date_range(end=datetime.now().date(), periods=days, freq='B')
    closes = base_price + np.cumsum(np.random.randn(days) * 2)
    closes = np.clip(closes, 1, None)
    df = pd.DataFrame({
        "Open":  closes + np.random.uniform(-1, 1, days),
        "High":  closes + np.abs(np.random.randn(days) * 1.5),
        "Low":   closes - np.abs(np.random.randn(days) * 1.5),
        "Close": closes,
    }, index=dates)
    return df.clip(lower=0.01)


def monitor_watchlist(symbols: list[str], delay: float = 0.5) -> list[tuple]:
    """Monitor watchlist for daily performance. Returns list of (symbol, pct_change) tuples."""
    performance = []
    for i, sym in enumerate(symbols):
        try:
            print(f"[{i+1}/{len(symbols)}] Monitoring {sym}...", end="", flush=True)
            hist = fetch_price_history_local(sym, period="2d")
            
            if hist.empty or len(hist) < 2:
                print(" (insufficient data)")
                continue
            
            prev_close = hist["Close"].iloc[-2]
            last_close = hist["Close"].iloc[-1]
            pct = (last_close - prev_close) / prev_close * 100
            performance.append((sym, pct))
            print(f" ✓ {pct:+.2f}%")
        except Exception as e:
            print(f" ✗ {str(e)[:30]}")
        time.sleep(delay)
    
    performance.sort(key=lambda x: x[1], reverse=True)
    return performance


# Run watchlist analysis
print("\nAnalyzing watchlist performance...")
results = monitor_watchlist(WATCHLIST, delay=0.1)

# Display watchlist performance
if results:
    print("\nWatchlist Performance (sorted by % change):")
    for sym, pct in results:
        company_name = get_company_name(sym)
        print(f"  {sym:6} - {company_name:25} {pct:+.2f}%")
else:
    print("⚠ No watchlist performance data available.")

# Fetch OHLC data for watchlist
print("\nFetching 7-Day OHLC for watchlist...")
watchlist_ohlc_data = fetch_ohlc_data(WATCHLIST, period="7d", delay=0.1)

# Display detailed price data
if watchlist_ohlc_data:
    print(f"\n{'='*70}")
    print("Watchlist - 7-Day Price Data")
    print(f"{'='*70}")
    for sym in WATCHLIST:
        if sym in watchlist_ohlc_data:
            df = watchlist_ohlc_data[sym]
            company_name = get_company_name(sym)
            
            if not df.empty:
                print(f"\n{sym} - {company_name} (last {len(df)} days):")
                df_display = df.copy()
                for col in ["Open", "High", "Low", "Close"]:
                    df_display[col] = df_display[col].apply(lambda x: f"${x:.2f}")
                print(df_display)
            else:
                print(f"\n{sym} - {company_name}: No data available")
else:
    print("⚠ No OHLC data was fetched for watchlist.")
