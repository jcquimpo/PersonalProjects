"""
Direct testing of stock_fetcher service without running the full API server.
Run this from backend_v2 directory: python test_stock_fetcher.py
"""

import sys
import time
from datetime import datetime
from app.services.stock_fetcher import StockFetcher

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
END = '\033[0m'

def print_test(name: str):
    print(f"\n{BLUE}{'='*70}")
    print(f"TEST: {name}")
    print(f"{'='*70}{END}")

def print_success(msg: str):
    print(f"{GREEN}✓ {msg}{END}")

def print_error(msg: str):
    print(f"{RED}✗ {msg}{END}")

def print_info(msg: str):
    print(f"{YELLOW}ℹ {msg}{END}")

def test_get_company_name():
    """Test getting company names."""
    print_test("Get Company Names")
    
    symbols = ["AAPL", "MSFT", "GOOGL", "UNKNOWN_SYMBOL"]
    for symbol in symbols:
        start = time.time()
        name = StockFetcher.get_company_name(symbol)
        elapsed = time.time() - start
        
        if name and name != symbol:
            print_success(f"{symbol} → {name} ({elapsed:.2f}s)")
        else:
            print_info(f"{symbol} → {name or 'N/A'} ({elapsed:.2f}s)")

def test_get_stock_performance():
    """Test getting stock performance data."""
    print_test("Get Stock Performance")
    
    symbols = ["AAPL", "MSFT", "GOOGL"]
    for symbol in symbols:
        start = time.time()
        perf = StockFetcher.get_stock_performance(symbol)
        elapsed = time.time() - start
        
        if perf:
            print_success(f"{symbol}")
            print(f"  Price: ${perf['current_price']}")
            print(f"  Change: {perf['percentage_change']:+.2f}%")
            print(f"  Time: {elapsed:.2f}s")
        else:
            print_error(f"{symbol} - No data")

def test_get_ohlc_data():
    """Test getting OHLC (price history) data."""
    print_test("Get OHLC Data")
    
    symbols = ["AAPL", "MSFT"]
    for symbol in symbols:
        start = time.time()
        ohlc = StockFetcher.get_ohlc_data(symbol, period="7d")
        elapsed = time.time() - start
        
        if ohlc:
            print_success(f"{symbol} - {len(ohlc)} days of data ({elapsed:.2f}s)")
            # Show first and last entry
            print(f"  First: {ohlc[0]['date']} → Close: ${ohlc[0]['close']}")
            print(f"  Last:  {ohlc[-1]['date']} → Close: ${ohlc[-1]['close']}")
        else:
            print_error(f"{symbol} - No OHLC data")

def test_fetch_watchlist():
    """Test fetching entire watchlist with OHLC data."""
    print_test("Fetch Watchlist (Full)")
    
    start = time.time()
    result = StockFetcher.fetch_watchlist()
    elapsed = time.time() - start
    
    if result:
        watchlist = result.get("watchlist", [])
        ohlc_data = result.get("ohlc_data", {})
        is_demo = result.get("is_demo_data", False)
        
        print_success(f"Watchlist fetched in {elapsed:.2f}s")
        print_info(f"Data type: {'DEMO' if is_demo else 'LIVE'}")
        print(f"  Stocks: {len(watchlist)}")
        
        for stock in watchlist:
            symbol = stock['symbol']
            ohlc_count = len(ohlc_data.get(symbol, []))
            print(f"    {symbol}: {stock['percentage_change']:+.2f}% | {ohlc_count} OHLC records")
    else:
        print_error("Failed to fetch watchlist")

def test_fetch_top_stocks():
    """Test fetching top stocks with OHLC data."""
    print_test("Fetch Top Stocks (Full)")
    
    start = time.time()
    result = StockFetcher.fetch_top_stocks()
    elapsed = time.time() - start
    
    if result:
        top_stocks = result.get("top_stocks", [])
        ohlc_data = result.get("ohlc_data", {})
        is_demo = result.get("is_demo_data", False)
        
        print_success(f"Top stocks fetched in {elapsed:.2f}s")
        print_info(f"Data type: {'DEMO' if is_demo else 'LIVE'}")
        print(f"  Top stocks: {len(top_stocks)}")
        
        for i, stock in enumerate(top_stocks, 1):
            symbol = stock['symbol']
            ohlc_count = len(ohlc_data.get(symbol, []))
            print(f"    #{i} {symbol}: {stock['percentage_change']:+.2f}% | {ohlc_count} OHLC records")
    else:
        print_error("Failed to fetch top stocks")

def test_cache_effectiveness():
    """Test that caching is working."""
    print_test("Cache Effectiveness")
    
    print_info("Fetching watchlist twice (should be cached second time)...")
    
    # First call - hits API
    start1 = time.time()
    result1 = StockFetcher.fetch_watchlist()
    time1 = time.time() - start1
    
    # Second call - should use cache
    start2 = time.time()
    result2 = StockFetcher.fetch_watchlist()
    time2 = time.time() - start2
    
    print(f"  First call:  {time1:.2f}s (hits API)")
    print(f"  Second call: {time2:.2f}s (should use cache)")
    
    if time2 < time1 * 0.5:  # Second call should be < 50% of first
        print_success(f"Cache is working! Speed improvement: {time1/time2:.1f}x faster")
    else:
        print_info("Cache may not be effective or API is still fast")
    
    # Verify data is identical
    if result1 == result2:
        print_success("Cached data matches original data")
    else:
        print_info("Data differs (might be expected due to real-time updates)")

def test_error_handling():
    """Test error handling with invalid symbols."""
    print_test("Error Handling")
    
    print_info("Testing with invalid/non-existent symbols...")
    
    bad_symbols = ["INVALID_SYMBOL_XYZ", "FAKECOMPANY123", "DOESNOTEXIST"]
    for symbol in bad_symbols:
        result = StockFetcher.get_stock_performance(symbol)
        if result is None:
            print_success(f"{symbol} → Handled gracefully (returned None)")
        else:
            print_info(f"{symbol} → Got data: {result}")

def test_rate_limiting():
    """Test rate limiting functionality."""
    print_test("Rate Limiting")
    
    print_info("Making rapid requests to test rate limiting...")
    symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]
    
    start = time.time()
    for i, symbol in enumerate(symbols, 1):
        req_start = time.time()
        result = StockFetcher.get_stock_performance(symbol)
        req_time = time.time() - req_start
        
        if result:
            print(f"  [{i}/{len(symbols)}] {symbol} in {req_time:.2f}s")
        else:
            print(f"  [{i}/{len(symbols)}] {symbol} FAILED in {req_time:.2f}s")
    
    total = time.time() - start
    print_success(f"Total time for 5 requests: {total:.2f}s")
    print_info(f"Average per request: {total/len(symbols):.2f}s")

def main():
    """Run all tests."""
    print(f"\n{BLUE}╔{'='*68}╗")
    print(f"║ STOCK FETCHER SERVICE TEST SUITE                              ║")
    print(f"║ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                                          ║")
    print(f"╚{'='*68}╝{END}")
    
    try:
        # Individual component tests
        test_get_company_name()
        time.sleep(0.5)
        
        test_get_stock_performance()
        time.sleep(0.5)
        
        test_get_ohlc_data()
        time.sleep(0.5)
        
        # Full integration tests
        test_fetch_watchlist()
        time.sleep(0.5)
        
        test_fetch_top_stocks()
        time.sleep(0.5)
        
        # Feature tests
        test_cache_effectiveness()
        time.sleep(0.5)
        
        test_error_handling()
        time.sleep(0.5)
        
        test_rate_limiting()
        
        print(f"\n{BLUE}{'='*70}")
        print(f"TEST SUITE COMPLETE{END}")
        print(f"{'='*70}\n")
        
    except Exception as e:
        print(f"\n{RED}FATAL ERROR: {e}{END}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
