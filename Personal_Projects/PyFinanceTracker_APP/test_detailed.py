#!/usr/bin/env python3
"""Comprehensive API test with rate limiting diagnostics."""

import requests
import time
import json
from datetime import datetime

def test_watchlist():
    """Test watchlist endpoint with detailed diagnostics."""
    print("\n" + "="*70)
    print("TESTING: /api/watchlist (Full watchlist with OHLC data)")
    print("="*70)
    
    url = "http://localhost:5000/api/watchlist"
    print(f"URL: {url}")
    print(f"Request started: {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        start = time.time()
        resp = requests.get(url, timeout=60)
        elapsed = time.time() - start
        
        print(f"Response time: {elapsed:.1f}s")
        print(f"Status code: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"\n✅ SUCCESS - Response structure:")
            print(f"  - Top-level keys: {list(data.keys())}")
            print(f"  - Watchlist entries: {len(data.get('watchlist', []))}")
            print(f"  - OHLC entries: {len(data.get('ohlc_data', {}))}")
            print(f"  - Fetched at: {data.get('fetched_at', 'N/A')}")
            
            # Check if data is cached
            is_cached = data.get('is_cached', False)
            if is_cached:
                cache_age = data.get('cached_age_seconds', 'unknown')
                print(f"\n⚠️  DATA IS CACHED (age: {cache_age}s)")
                print("    This means yfinance failed, returning previous response")
            
            # Show watchlist if available
            watchlist = data.get('watchlist', [])
            if watchlist:
                print(f"\n📊 Watchlist data:")
                for item in watchlist[:3]:  # Show first 3
                    print(f"    {item.get('symbol', '?')}: "
                          f"{item.get('price', 'N/A')} "
                          f"({item.get('percentage_change', 'N/A')}%)")
                if len(watchlist) > 3:
                    print(f"    ... and {len(watchlist) - 3} more")
            else:
                print(f"\n⚠️  No watchlist data (likely cached or failed)")
            
            return resp.status_code == 200
        else:
            print(f"❌ ERROR Status {resp.status_code}")
            print(f"Response: {resp.text[:200]}")
            return False
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_quick_watchlist():
    """Test quick watchlist (should be faster)."""
    print("\n" + "="*70)
    print("TESTING: /api/quick-watchlist (Fast response without OHLC)")
    print("="*70)
    
    url = "http://localhost:5000/api/quick-watchlist"
    print(f"URL: {url}")
    
    try:
        start = time.time()
        resp = requests.get(url, timeout=30)
        elapsed = time.time() - start
        
        print(f"Response time: {elapsed:.1f}s")
        print(f"Status code: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            watchlist_count = len(data.get('watchlist', []))
            print(f"✅ Watchlist entries: {watchlist_count}")
            return True
        else:
            print(f"❌ ERROR Status {resp.status_code}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_top_stocks():
    """Test top stocks endpoint."""
    print("\n" + "="*70)
    print("TESTING: /api/top-stocks (Top moving stocks)")
    print("="*70)
    
    url = "http://localhost:5000/api/top-stocks?limit=50&delay=0.7"
    print(f"URL: {url}")
    
    try:
        start = time.time()
        resp = requests.get(url, timeout=90)
        elapsed = time.time() - start
        
        print(f"Response time: {elapsed:.1f}s")
        print(f"Status code: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            stocks_count = len(data.get('top_stocks', []))
            print(f"✅ Top stocks found: {stocks_count}")
            return True
        else:
            print(f"❌ ERROR Status {resp.status_code}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*70)
    print("STOCK API COMPREHENSIVE TEST")
    print("="*70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # Test quick watchlist first (should be fast)
    results['quick_watchlist'] = test_quick_watchlist()
    
    # Test full watchlist (main test)
    results['watchlist'] = test_watchlist()
    
    # Test top stocks (slower)
    results['top_stocks'] = test_top_stocks()
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    all_pass = all(results.values())
    print("\n" + ("✅ ALL TESTS PASSED" if all_pass else "❌ SOME TESTS FAILED"))
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
