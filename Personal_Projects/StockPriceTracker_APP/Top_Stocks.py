"""
Stock Data Generator - Generates mock OHLC data and watchlist performance.
Run this script to generate initial data, or use data_generator.py for programmatic access.

Usage:
    python Top_Stocks.py          # Generate and display data, save to JSON
    
The generated data is saved to: flask_app/data/stock_data.json
You can then start the Flask dashboard with: python flask_app/app.py

For live refresh without rerunning this script:
    Use the Flask dashboard's "Refresh" button, which triggers /api/refresh endpoint.
"""

import os
from datetime import datetime
from data_generator import generate_stock_data, save_stock_data, SYMBOL_NAMES, WATCHLIST


def display_top_movers_data(data: dict) -> None:
    """Display top movers OHLC data in formatted table."""
    print("\n" + "="*70)
    print("Top Movers — 7-Day OHLC Price Data")
    print("="*70)
    
    symbols = data['topMovers']['symbols']
    ohlc = data['topMovers']['ohlc']
    
    for sym in symbols:
        if sym in ohlc:
            company_name = SYMBOL_NAMES.get(sym, sym)
            sym_data = ohlc[sym]
            dates = sym_data['dates']
            
            print(f"\n{sym} — {company_name}  ({len(dates)} trading days):")
            print(f"{'Date':<12} {'Open':<12} {'High':<12} {'Low':<12} {'Close':<12}")
            print("-" * 62)
            
            for i, date in enumerate(dates):
                print(f"{date:<12} ${sym_data['opens'][i]:<11.2f} ${sym_data['highs'][i]:<11.2f} ${sym_data['lows'][i]:<11.2f} ${sym_data['closes'][i]:<11.2f}")


def display_watchlist_data(data: dict) -> None:
    """Display watchlist OHLC data in formatted table."""
    print("\n" + "="*70)
    print("Watchlist - 7-Day Price Data")
    print("="*70)
    
    symbols = WATCHLIST
    ohlc = data['watchlist']['ohlc']
    
    for sym in symbols:
        if sym in ohlc:
            company_name = SYMBOL_NAMES.get(sym, sym)
            sym_data = ohlc[sym]
            dates = sym_data['dates']
            
            print(f"\n{sym} - {company_name} (last {len(dates)} days):")
            print(f"{'Date':<12} {'Open':<12} {'High':<12} {'Low':<12} {'Close':<12}")
            print("-" * 62)
            
            for i, date in enumerate(dates):
                print(f"{date:<12} ${sym_data['opens'][i]:<11.2f} ${sym_data['highs'][i]:<11.2f} ${sym_data['lows'][i]:<11.2f} ${sym_data['closes'][i]:<11.2f}")


def display_performance(data: dict) -> None:
    """Display performance metrics."""
    print("\n" + "="*70)
    print("Top Movers Performance (sorted by % change)")
    print("="*70)
    for sym, pct in data['topMovers']['performance']:
        company_name = SYMBOL_NAMES.get(sym, sym)
        print(f"  {sym:8s} {company_name:35s}  {pct:+.2f}%")
    
    print("\n" + "="*70)
    print("Watchlist Performance (sorted by % change)")
    print("="*70)
    for sym, pct in data['watchlist']['performance']:
        company_name = SYMBOL_NAMES.get(sym, sym)
        print(f"  {sym:6} - {company_name:25} {pct:+.2f}%")


if __name__ == '__main__':
    # Generate fresh stock data
    data = generate_stock_data(verbose=True)
    
    # Display the data
    print("\n" + "="*70)
    print("GENERATED DATA SUMMARY")
    print("="*70)
    display_performance(data)
    display_top_movers_data(data)
    display_watchlist_data(data)
    
    # Export data for Flask dashboard
    print("\n" + "="*70)
    print("EXPORTING DATA FOR FLASK DASHBOARD")
    print("="*70)
    
    data_dir = os.path.join(os.path.dirname(__file__), 'flask_app', 'data')
    output_file = save_stock_data(data, data_dir)
    
    print(f"✓ Data exported to {output_file}")
    print(f"✓ Analysis complete! Start Flask app with: python flask_app/app.py")
    print(f"✓ Use the Flask dashboard's 'Refresh' button to update data without rerunning this script.")
    print("="*70)

