#!/usr/bin/env python3
"""Quick test of watchlist endpoint."""

import requests
import time
import json

def test_endpoint(endpoint, timeout=45):
    """Test a single endpoint."""
    url = f"http://localhost:5000{endpoint}"
    print(f"\nTesting: {endpoint}")
    print(f"URL: {url}")
    print("Starting request...", flush=True)
    
    start = time.time()
    try:
        resp = requests.get(url, timeout=timeout)
        elapsed = time.time() - start
        
        print(f"✅ Status: {resp.status_code}")
        print(f"⏱️  Time: {elapsed:.1f}s")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"Data keys: {list(data.keys())}")
            if "watchlist" in data:
                print(f"  Watchlist entries: {len(data['watchlist'])}")
            if "error" in data:
                print(f"  ⚠️  Error in response: {data['error']}")
        else:
            print(f"Response: {resp.text[:200]}")
        
        return True
    except Exception as e:
        elapsed = time.time() - start
        print(f"❌ Error after {elapsed:.1f}s: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Stock API Quick Test")
    print("=" * 60)
    
    # Test health
    test_endpoint("/api/health", timeout=10)
    
    # Test quick watchlist (should be fast)
    print("\n--- Testing Quick Watchlist (should be faster) ---")
    test_endpoint("/api/quick-watchlist", timeout=30)
    
    # Test full watchlist (might be slower due to OHLC data)
    print("\n--- Testing Full Watchlist (includes OHLC data) ---")
    test_endpoint("/api/watchlist", timeout=60)
