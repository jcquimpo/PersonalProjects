import pandas as pd
import yfinance as yf
from pytickersymbols import PyTickerSymbols

stock_data = PyTickerSymbols()

sp500_tickers = stock_data.get_sp_500_nyc_yahoo_tickers()

print(f"Fetching data for {len(sp500_tickers)} stocks...")

data = yf.download(sp500_tickers, period="2d", interval="1d")['Close']

performance = ((data.iloc[-1] - data.iloc[0]) / data.iloc[0]) * 100

top_5 = performance.dropna().sort_values(ascending=False).head(5)

print("\n--- TOP 5 PERFORMING S&P 500 STOCKS ---")
print(top_5)