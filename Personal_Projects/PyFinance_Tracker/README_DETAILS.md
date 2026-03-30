# PyFinance_Tracker Detailed Explanation

This file explains the behavior of each function in `TopStocksv2.py`.

## get_top_n_stocks(limit=100, top_n=5, source="US")
- Fetches ticker symbols using `pytickersymbols`:
  - `source == "US"` uses `get_stocks_by_country("US")`
  - `source == "SP500"` uses `get_sp_500_nyc_yahoo_tickers()`
- Limits the number of symbols with `limit` to avoid large API loads.
- For each symbol:
  - fetches 2 days of data via `yfinance` with `history(period="2d", interval="1d")`
  - checks data validity (non-empty, has "Close", at least 2 rows)
  - computes yesterday and today close
  - skips bad or zero/NaN values
  - calculates daily percent change
- Assembles results into a pandas `DataFrame` of columns:
  - `Symbol`, `Price`, `Change %`
- If DataFrame is empty or missing column, returns empty standard DataFrame.
- Sorts by `Change %` descending, selects top `top_n`, resets index.

## display_results(df)
- If `df` is empty: prints a friendly message.
- Otherwise prints a table with each row:
  - `Symbol`, formatted `Price`, formatted `Change %`.

## main block
- Uses `argparse` to allow command-line options:
  - `--limit` (100 by default)
  - `--top` (5 by default)
  - `--source` (`US` or `SP500`)
- Calls `get_top_n_stocks(...)` and then `display_results(...)`.

## Usage
```
python TopStocksv2.py
python TopStocksv2.py --limit 120 --top 5 --source SP500
```

## Package requirements
```
pip install pandas yfinance pytickersymbols
```
