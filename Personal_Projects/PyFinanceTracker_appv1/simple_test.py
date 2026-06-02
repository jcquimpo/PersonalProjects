#!/usr/bin/env python3
import requests
import json
import time

# Test quick-watchlist endpoint
print("Testing /api/quick-watchlist endpoint...")
start = time.time()
try:
    resp = requests.get("http://localhost:5000/api/quick-watchlist", timeout=60)
    elapsed = time.time() - start
    
    print(f"✅ Response time: {elapsed:.1f}s")
    print(f"Status code: {resp.status_code}")
    
    data = resp.json()
    print(f"Watchlist entries: {len(data.get('watchlist', []))}")
    print(f"Is demo data: {data.get('is_demo_data', False)}")
    
    if "note" in data:
        print(f"Note: {data['note']}")
    
    # Show first entry
    if data.get('watchlist'):
        print(f"\nFirst entry:")
        print(json.dumps(data['watchlist'][0], indent=2))
    
    print("\n✅ SUCCESS - API is working!")
    
except Exception as e:
    print(f"❌ Error: {e}")
