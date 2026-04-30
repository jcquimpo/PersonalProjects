#!/bin/bash
# Quick Backend Testing Script
# Windows: Run in PowerShell
# Linux/Mac: Run in Terminal
# This script tests all API endpoints and shows what data is being fetched

echo "=================================="
echo "Stock Dashboard Backend Test"
echo "=================================="
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if backend is running
echo -e "${BLUE}[1/5] Checking if backend is running...${NC}"
curl -s -m 2 http://localhost:5000/api/health > /dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Backend is running on http://localhost:5000${NC}"
else
    echo -e "${RED}✗ Backend is NOT running${NC}"
    echo "Start backend with: cd backend_v2 && python main.py"
    exit 1
fi
echo ""

# Test 1: Health check
echo -e "${BLUE}[2/5] Health Check${NC}"
RESPONSE=$(curl -s http://localhost:5000/api/health)
echo "Response: $RESPONSE"
echo ""

# Test 2: Fetch watchlist
echo -e "${BLUE}[3/5] Fetch Watchlist${NC}"
echo "Making request to /api/watchlist..."
START=$(date +%s%N)
RESPONSE=$(curl -s -w "\n%{http_code}" http://localhost:5000/api/watchlist)
END=$(date +%s%N)
ELAPSED=$(( (END - START) / 1000000 ))

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

echo "HTTP Status: $HTTP_CODE"
echo "Time: ${ELAPSED}ms"

# Check if response contains stock data
if echo "$BODY" | grep -q "AAPL"; then
    echo -e "${GREEN}✓ Received stock data (AAPL found in response)${NC}"
else
    echo -e "${YELLOW}⚠ No stock data in response${NC}"
fi

# Check if demo data
if echo "$BODY" | grep -q "is_demo_data.*true"; then
    echo -e "${YELLOW}⚠ Using demo data (Yahoo Finance is slow/rate limited)${NC}"
elif echo "$BODY" | grep -q "is_demo_data.*false"; then
    echo -e "${GREEN}✓ Using live data from Yahoo Finance${NC}"
fi

# Show first stock from response
echo ""
echo "Sample data:"
echo "$BODY" | grep -o '"symbol":"[^"]*","company_name":"[^"]*","percentage_change":[^,]*' | head -1
echo ""

# Test 3: Fetch top stocks
echo -e "${BLUE}[4/5] Fetch Top Stocks${NC}"
echo "Making request to /api/top-stocks..."
START=$(date +%s%N)
RESPONSE=$(curl -s -w "\n%{http_code}" http://localhost:5000/api/top-stocks)
END=$(date +%s%N)
ELAPSED=$(( (END - START) / 1000000 ))

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

echo "HTTP Status: $HTTP_CODE"
echo "Time: ${ELAPSED}ms"

if echo "$BODY" | grep -q "top_stocks"; then
    NUM_STOCKS=$(echo "$BODY" | grep -o '"symbol":"[^"]*"' | wc -l)
    echo -e "${GREEN}✓ Received $NUM_STOCKS stocks${NC}"
else
    echo -e "${RED}✗ No top_stocks in response${NC}"
fi

if echo "$BODY" | grep -q "is_demo_data.*true"; then
    echo -e "${YELLOW}⚠ Using demo data${NC}"
else
    echo -e "${GREEN}✓ Using live data${NC}"
fi

echo ""

# Test 4: Response time check
echo -e "${BLUE}[5/5] Response Time Analysis${NC}"
echo "Testing response times (should be < 20 seconds)..."

for endpoint in "/api/watchlist" "/api/top-stocks"; do
    START=$(date +%s%3N)
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000${endpoint})
    END=$(date +%s%3N)
    ELAPSED=$(( END - START ))
    
    if [ $ELAPSED -lt 20000 ]; then
        echo -e "${GREEN}✓ $endpoint: ${ELAPSED}ms (OK)${NC}"
    else
        echo -e "${RED}✗ $endpoint: ${ELAPSED}ms (TOO SLOW)${NC}"
    fi
done

echo ""
echo -e "${GREEN}=================================="
echo "Test Complete!"
echo "==================================${NC}"
echo ""
echo "Summary:"
echo "- Backend running: YES"
echo "- Endpoints responding: Check above"
echo "- Response times: Check above"
echo ""
echo "Next steps:"
echo "1. Open http://localhost:3000 in your browser"
echo "2. Check browser DevTools Network tab for /api requests"
echo "3. Verify data is displayed correctly"
