#!/usr/bin/env python3
"""
Connection Verification Script
Tests all components of the Stock Dashboard connection.
"""

import requests
import json
import time
import sys
from urllib.parse import urljoin

# Configuration
BACKEND_URL = "http://localhost:5000"
FRONTEND_URL = "http://localhost:3000"
TIMEOUT = 5

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_info(text):
    print(f"{BLUE}ℹ️  {text}{RESET}")

def test_backend_health():
    """Test if backend is running and healthy."""
    print_header("Testing Backend Health")
    
    try:
        url = urljoin(BACKEND_URL, "/api/health")
        print_info(f"Testing: {url}")
        
        response = requests.get(url, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Backend is running")
            print_info(f"Response: {json.dumps(data, indent=2)}")
            return True
        else:
            print_error(f"Backend returned status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error(f"Cannot connect to backend at {BACKEND_URL}")
        print_info("Make sure backend is running: python main.py")
        return False
    except requests.exceptions.Timeout:
        print_error(f"Backend request timed out after {TIMEOUT}s")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False

def test_quick_watchlist():
    """Test quick watchlist endpoint."""
    print_header("Testing Quick Watchlist Endpoint")
    
    try:
        url = urljoin(BACKEND_URL, "/api/quick-watchlist")
        print_info(f"Testing: {url}")
        print_info("Starting timer...")
        
        start = time.time()
        response = requests.get(url, timeout=15)
        elapsed = time.time() - start
        
        if response.status_code == 200:
            data = response.json()
            watchlist = data.get('watchlist', [])
            print_success(f"Quick watchlist returned in {elapsed:.1f}s")
            print_info(f"Stocks returned: {len(watchlist)}")
            
            if watchlist:
                print_info("Sample stocks:")
                for stock in watchlist[:3]:
                    print(f"  - {stock['symbol']}: {stock['percentage_change']:+.2f}%")
            else:
                print_warning("No stocks in watchlist (market may be closed)")
            
            return True
        else:
            print_error(f"Endpoint returned status {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print_error(f"Request timed out after 15s")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_watchlist_with_ohlc():
    """Test full watchlist endpoint with OHLC data."""
    print_header("Testing Full Watchlist Endpoint (with OHLC)")
    
    try:
        url = urljoin(BACKEND_URL, "/api/watchlist?delay=0.3")
        print_info(f"Testing: {url}")
        print_info("This may take 10-30 seconds...")
        print_info("Starting timer...")
        
        start = time.time()
        response = requests.get(url, timeout=60)
        elapsed = time.time() - start
        
        if response.status_code == 200:
            data = response.json()
            watchlist = data.get('watchlist', [])
            ohlc_data = data.get('ohlc_data', {})
            
            print_success(f"Full watchlist returned in {elapsed:.1f}s")
            print_info(f"Stocks: {len(watchlist)}, OHLC data points: {sum(len(v) for v in ohlc_data.values())}")
            
            if watchlist:
                print_info("Stocks:")
                for stock in watchlist:
                    ohlc_count = len(ohlc_data.get(stock['symbol'], []))
                    print(f"  - {stock['symbol']}: {stock['percentage_change']:+.2f}% ({ohlc_count} data points)")
            else:
                print_warning("No stocks returned")
            
            return True
        else:
            print_error(f"Endpoint returned status {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print_error(f"Request timed out after 60s")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_diagnostic():
    """Test diagnostic endpoint."""
    print_header("Running Diagnostic Tests")
    
    try:
        url = urljoin(BACKEND_URL, "/api/diagnostic")
        print_info(f"Testing: {url}")
        
        response = requests.get(url, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            print_info(f"Status: {data.get('status')}")
            
            tests = data.get('tests', {})
            for test_name, result in tests.items():
                if 'ok' in str(result).lower():
                    print_success(f"{test_name}: {result}")
                else:
                    print_warning(f"{test_name}: {result}")
            
            return data.get('status') == 'ok'
        else:
            print_error(f"Diagnostic returned status {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_frontend():
    """Test if frontend is running."""
    print_header("Testing Frontend")
    
    try:
        print_info(f"Testing: {FRONTEND_URL}")
        
        response = requests.get(FRONTEND_URL, timeout=TIMEOUT)
        
        if response.status_code == 200:
            print_success(f"Frontend is running at {FRONTEND_URL}")
            if 'React' in response.text or 'stock' in response.text.lower():
                print_success("Frontend appears to be loaded correctly")
                return True
            else:
                print_warning("Frontend loaded but content is unexpected")
                return True
        else:
            print_error(f"Frontend returned status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error(f"Cannot connect to frontend at {FRONTEND_URL}")
        print_info("Make sure frontend is running: npm start (in frontend_v2)")
        return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def main():
    """Run all tests."""
    print(f"\n{BLUE}Stock Dashboard Connection Test Suite{RESET}")
    print(f"Testing Backend: {BACKEND_URL}")
    print(f"Testing Frontend: {FRONTEND_URL}\n")
    
    results = {}
    
    # Test backend health first
    results['Backend Health'] = test_backend_health()
    
    if not results['Backend Health']:
        print_error("\nBackend is not responding. Please start it first:")
        print(f"  cd backend_v2")
        print(f"  python main.py")
        return 1
    
    # Test endpoints
    results['Quick Watchlist'] = test_quick_watchlist()
    results['Full Watchlist'] = test_watchlist_with_ohlc()
    results['Diagnostics'] = test_diagnostic()
    results['Frontend'] = test_frontend()
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        symbol = "✅" if result else "❌"
        print(f"{symbol} {test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print_success("\nAll systems operational! 🎉")
        return 0
    else:
        print_warning("\nSome tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Test interrupted by user{RESET}")
        sys.exit(130)
