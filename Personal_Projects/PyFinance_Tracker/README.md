# Top 5 Daily Stocks

A Python application to track and display the top 5 performing stocks daily.

## Description

This project provides functionality to identify and display the top 5 daily performing stocks.
The goal of this program is to automate the process of monitoring market movements. Instead of manually checking financial news sites, this script:
1. Connects to the **Yahoo Finance API**.
2. Pulls the latest price data for a defined set of tickers.
3. Calculates the intraday percentage change.
4. Ranks and displays the **Top 5 Stocks**.

## TopStocksv2 Section

### What this script does
- Uses `pytickersymbols` to gather a set of stock symbols (US or S&P 500).  
- Uses `yfinance` to fetch the latest 2 days of close price history.  
- Computes the daily percentage change between today and yesterday.  
- Sorts by `Change %` and prints the top N performers (default 5).

### Usage
```bash
python TopStocksv2.py
python TopStocksv2.py --limit 100 --top 5 --source US
python TopStocksv2.py --limit 200 --top 10 --source SP500
```

### Requirements
```bash
pip install pandas yfinance pytickersymbols
```

