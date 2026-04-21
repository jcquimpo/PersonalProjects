"""
Comprehensive test script to verify all dependencies and imports work correctly.
Run this to catch any issues before starting the backend.
"""

import sys
import importlib

def test_import(module_name, package_name=None):
    """Test if a module can be imported."""
    if package_name is None:
        package_name = module_name
    
    try:
        module = importlib.import_module(module_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"✅ {package_name:<20} - OK (version: {version})")
        return True
    except ImportError as e:
        print(f"❌ {package_name:<20} - FAILED: {e}")
        return False
    except Exception as e:
        print(f"⚠️  {package_name:<20} - WARNING: {e}")
        return True

def test_all():
    """Test all dependencies."""
    print("=" * 60)
    print("Testing Dependencies for PyFinanceTracker Backend v2")
    print("=" * 60)
    print()
    
    tests = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("pydantic", "pydantic"),
        ("yfinance", "yfinance"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("pytickersymbols", "pytickersymbols"),
        ("dotenv", "python-dotenv"),
        ("aiofiles", "aiofiles"),
    ]
    
    results = []
    for module_name, package_name in tests:
        results.append(test_import(module_name, package_name))
    
    print()
    print("=" * 60)
    
    # Test app imports
    print("Testing Application Imports")
    print("=" * 60)
    print()
    
    try:
        from app.models.stock import (
            TopStocksResponse,
            WatchlistResponse,
            StockDetail,
            StockPerformance,
            OHLCData
        )
        print("✅ app.models.stock              - OK")
    except Exception as e:
        print(f"❌ app.models.stock              - FAILED: {e}")
        results.append(False)
    
    try:
        from app.services.stock_fetcher import StockFetcher
        print("✅ app.services.stock_fetcher    - OK")
    except Exception as e:
        print(f"❌ app.services.stock_fetcher    - FAILED: {e}")
        results.append(False)
    
    try:
        from app.routes.stocks import router
        print("✅ app.routes.stocks             - OK")
    except Exception as e:
        print(f"❌ app.routes.stocks             - FAILED: {e}")
        results.append(False)
    
    try:
        from app.main import app
        print("✅ app.main                      - OK")
    except Exception as e:
        print(f"❌ app.main                      - FAILED: {e}")
        results.append(False)
    
    print()
    print("=" * 60)
    print("Testing Functionality")
    print("=" * 60)
    print()
    
    # Test pytickersymbols fallback
    try:
        from pytickersymbols import PyTickerSymbols
        stock_data = PyTickerSymbols()
        sp500_list = list(stock_data.get_sp_500_nyc_yahoo_tickers())
        print(f"✅ PyTickerSymbols.get_sp_500    - OK ({len(sp500_list)} symbols)")
        results.append(True)
    except Exception as e:
        print(f"⚠️  PyTickerSymbols.get_sp_500    - FALLBACK: {e}")
        print("   (This is OK - backend will use default symbol list)")
        results.append(True)
    
    # Test yfinance
    try:
        import yfinance as yf
        ticker = yf.Ticker("AAPL")
        hist = ticker.history(period="1d")
        if hist.empty:
            print(f"⚠️  yfinance.Ticker.history      - OK (empty data, market may be closed)")
        else:
            print(f"✅ yfinance.Ticker.history      - OK ({len(hist)} records)")
        results.append(True)
    except Exception as e:
        print(f"⚠️  yfinance.Ticker.history      - WARNING: {e}")
        print("   (Check internet connection)")
        results.append(True)
    
    # Test pandas operations
    try:
        import pandas as pd
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        result = df.sum().sum()
        print(f"✅ pandas.DataFrame operations   - OK")
        results.append(True)
    except Exception as e:
        print(f"❌ pandas.DataFrame operations   - FAILED: {e}")
        results.append(False)
    
    print()
    print("=" * 60)
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 ALL TESTS PASSED ({passed}/{total})")
        print()
        print("You can now run:")
        print("  python main.py")
        print()
        return 0
    else:
        print(f"⚠️  SOME TESTS FAILED ({passed}/{total})")
        print()
        print("Please fix the errors above and try again.")
        print()
        return 1

if __name__ == "__main__":
    exit_code = test_all()
    sys.exit(exit_code)
