from __future__ import annotations

import argparse
import pandas as pd
import yfinance as yf
from typing import Literal
from pytickersymbols import PyTickerSymbols

def get_top_n_stocks(limit: int = 100, top_n: int = 5, source: Literal["US", "SP500"] = "US") -> pd.DataFrame:
    """Fetch top N stocks by daily percent gain using yfinance."""

    stock_data = PyTickerSymbols()

    if source == "SP500":
        symbols = list(stock_data.get_sp_500_nyc_yahoo_tickers())[:limit]
    else:
        symbols = [entry["symbol"] for entry in list(stock_data.get_stocks_by_country("US"))[:limit]]

    performance_rows = []

    for symbol in symbols:
        try:
            hist = yf.Ticker(symbol).history(period="2d", interval="1d")

            if hist.empty or "Close" not in hist.columns or len(hist) < 2:
                continue

            prev_close = hist["Close"].iloc[-2]
            last_close = hist["Close"].iloc[-1]

            if pd.isna(prev_close) or pd.isna(last_close) or prev_close == 0:
                continue

            change_pct = (last_close - prev_close) / prev_close * 100

            performance_rows.append({
                "Symbol": symbol,
                "Price": float(last_close),
                "Change %": float(change_pct),
            })

        except Exception as error:
            print(f"Skipping {symbol}: {error}")

    df = pd.DataFrame(performance_rows)

    if df.empty or "Change %" not in df.columns:
        return pd.DataFrame(columns=["Symbol", "Price", "Change %"])

    return df.sort_values(by="Change %", ascending=False).head(top_n).reset_index(drop=True)


def display_results(df: pd.DataFrame) -> None:
    if df.empty:
        print("No top performers found (empty dataset).")
        return

    print("\n" + "=" * 60)
    print("TOP 5 PERFORMING STOCKS TODAY")
    print("=" * 60 + "\n")

    for _, row in df.iterrows():
        print(f"{row['Symbol']:<10} | Price: ${row['Price']:>8.2f} | Change: {row['Change %']:>+6.2f}%")

    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Show top N performing stocks from Yahoo Finance")
    parser.add_argument("--limit", type=int, default=100, help="How many symbols to request")
    parser.add_argument("--top", type=int, default=5, help="How many top performers to show")
    parser.add_argument("--source", choices=["US", "SP500"], default="US", help="Symbol source list")
    args = parser.parse_args()

    print("Fetching stock data (this may take a minute)...")
    top_df = get_top_n_stocks(limit=args.limit, top_n=args.top, source=args.source)
    display_results(top_df)
