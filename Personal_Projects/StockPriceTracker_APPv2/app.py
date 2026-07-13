#!/usr/bin/env python3
"""
================================================================================
STOCK PRICE TRACKER WEB APPLICATION
================================================================================

Flask web application for displaying real-time stock analysis and visualizations.

Features:
  • Real-time stock price data from Finnhub & yfinance
  • Interactive Plotly charts
  • Investment scoring & recommendations
  • Responsive Bootstrap UI
  • S&P 500 movers scanning
  • Watchlist monitoring

Requirements:
  • Flask
  • pandas, yfinance, plotly
  • Finnhub API key in .env

Run:
  python app.py
  Navigate to http://localhost:5000
================================================================================
"""

import os
import time
import json
import requests
# Lazy-import heavy numeric and plotting packages to avoid build-time C extensions
pd = None
yf = None
go = None
px = None
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from pytickersymbols import PyTickerSymbols
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# ============================================================================
# CONFIGURATION
# ============================================================================
load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['JSON_SORT_KEYS'] = False

# Production settings
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000
if os.getenv("FLASK_ENV") == "production":
    app.config['TESTING'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True

FINNHUB_API_KEY  = os.getenv("FINNHUB_API_KEY", "")
FINNHUB_BASE_URL = "https://finnhub.io/api/v1"
REQUEST_DELAY    = 2.0
MAX_REQUESTS     = 60
OHLC_DAYS        = 7
SCAN_LIMIT       = 50
TARGET_MOVERS    = 5

# US Market Configuration
US_EXCHANGES     = ["NYSE", "NASDAQ", "AMEX"]
MIN_PRICE        = 0.01
MAX_PRICE        = 100000.0
OTC_SUFFIXES     = ["F", "Q", "Y", "K", "U", "V"]

# Watchlist
WATCHLIST = ["AAPL", "NVDA", "MSFT", "META", "GOOGL"]

SYMBOL_NAMES = {
    "AAPL":  "Apple Inc.",
    "MSFT":  "Microsoft Corporation",
    "NVDA":  "NVIDIA Corporation",
    "TSLA":  "Tesla Inc.",
    "AMZN":  "Amazon Inc.",
    "GOOGL": "Alphabet Inc.",
    "META":  "Meta Platforms",
    "BRK.B": "Berkshire Hathaway",
    "JNJ":   "Johnson & Johnson",
    "V":     "Visa Inc.",
}

# For production: allow missing API key but warn
if not FINNHUB_API_KEY and os.getenv("FLASK_ENV") != "production":
    raise ValueError(
        "FINNHUB_API_KEY not set. Add it to .env file."
    )
elif not FINNHUB_API_KEY:
    print("⚠️  WARNING: FINNHUB_API_KEY is not set. Set it in Render environment variables.")

# Global state
_request_count = 0
_session = None
_cache = {}


# ============================================================================
# API HELPERS
# ============================================================================

def _get_session():
    """Create requests session with retry logic."""
    global _session
    if _session is None:
        _session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=10)
        _session.mount("http://", adapter)
        _session.mount("https://", adapter)
        _session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        # Connection pooling timeout
        _session.timeout = 15
    return _session


def get_company_name(symbol: str) -> str:
    """Return company name or symbol."""
    return SYMBOL_NAMES.get(symbol, symbol)


def _is_us_stock(symbol: str) -> bool:
    """Validate if symbol is US-listed."""
    if any(symbol.endswith(suffix) for suffix in [".L", ".TO", ".V", ".AX", ".HK", ".KL", ".T", ".SI"]):
        return False
    if any(symbol.endswith(suffix) for suffix in OTC_SUFFIXES):
        return False
    if any(pat in symbol.upper() for pat in ["=X", "BTC", "ETH", "DOGE", "USDT"]):
        return False
    return True


def _validate_us_market_data(data: dict, symbol: str) -> bool:
    """Validate Finnhub response."""
    try:
        current_price = data.get("c", 0)
        prev_close = data.get("pc", 0)
        if current_price <= MIN_PRICE or current_price > MAX_PRICE:
            return False
        if prev_close is None or prev_close == 0:
            return False
        return True
    except:
        return False


def _api_get(endpoint: str, params: dict | None = None) -> dict:
    """Call Finnhub API with rate limiting."""
    global _request_count
    if _request_count >= MAX_REQUESTS:
        return {}
    
    _request_count += 1
    params = {**(params or {}), "token": FINNHUB_API_KEY}
    session = _get_session()
    
    try:
        r = session.get(
            f"{FINNHUB_BASE_URL}{endpoint}", 
            params=params, 
            timeout=15
        )
        r.raise_for_status()
        return r.json() or {}
    except:
        return {}
    finally:
        time.sleep(REQUEST_DELAY)


def fetch_quote(symbol: str) -> dict:
    """Fetch current quote."""
    if not _is_us_stock(symbol):
        return {"symbol": symbol, "current": 0, "prev_close": 0, "pct_change": 0}
    
    raw = _api_get("/quote", {"symbol": symbol})
    
    if raw and not _validate_us_market_data(raw, symbol):
        return {"symbol": symbol, "current": 0, "prev_close": 0, "pct_change": 0}
    
    c = raw.get("c", 0)
    pc = raw.get("pc", 0)
    pct = (c - pc) / pc * 100 if c > 0 and pc > 0 else 0
    
    return {
        "symbol": symbol,
        "current": c,
        "prev_close": pc,
        "pct_change": pct,
    }


def _lazy_load_pandas_yfinance_plotly():
    """Lazy-load pandas, yfinance, and plotly when needed."""
    global pd, yf, go, px
    if pd is None:
        import pandas as _pd
        pd = _pd
    if yf is None:
        import yfinance as _yf
        yf = _yf
    if go is None:
        import plotly.graph_objects as _go
        go = _go
    if px is None:
        import plotly.express as _px
        px = _px


def fetch_ohlc(symbol: str, days: int = OHLC_DAYS):
    """Fetch OHLC history. Returns a pandas DataFrame when available, otherwise empty dict.
    Uses lazy imports to avoid triggering C-extension builds during simple startup checks.
    """
    _lazy_load_pandas_yfinance_plotly()

    if not _is_us_stock(symbol):
        return pd.DataFrame()
    
    end = datetime.now()
    start = end - timedelta(days=days + 4)
    
    max_retries = 3
    backoff_base = 0.5
    
    for attempt in range(max_retries):
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(
                start=start.strftime("%Y-%m-%d"),
                end=end.strftime("%Y-%m-%d"),
                interval="1d",
                auto_adjust=True
            )
            
            if df.empty:
                return pd.DataFrame()

            df = df[["Open", "High", "Low", "Close"]].copy()
            df = df[(df["Close"] > MIN_PRICE) & (df["Close"] < MAX_PRICE)]

            if df.empty:
                return pd.DataFrame()

            df.index = pd.to_datetime(df.index).normalize().tz_localize(None)
            return df.tail(days)
            
        except:
            if attempt < max_retries - 1:
                time.sleep(backoff_base * (2 ** attempt))
                continue
    
    return pd.DataFrame()


# ============================================================================
# DATA PROCESSING
# ============================================================================

def fetch_movers_data():
    """Fetch top movers and their OHLC data."""
    global _request_count
    
    print("🔍 Scanning S&P 500 for top movers...")
    
    sp500_tickers = list(PyTickerSymbols().get_sp_500_nyc_yahoo_tickers())[:SCAN_LIMIT]
    mover_scores = []

    for sym in sp500_tickers:
        if _request_count >= MAX_REQUESTS:
            break
        
        if not _is_us_stock(sym):
            continue
        
        q = fetch_quote(sym)
        pct = q.get("pct_change", 0)
        
        if pct != 0:
            mover_scores.append((sym, pct))

    mover_scores.sort(key=lambda x: x[1], reverse=True)

    # Fetch OHLC for top movers
    ohlc_data = {}
    top5_symbols = []
    scan_index = 0

    while len(ohlc_data) < TARGET_MOVERS and scan_index < len(mover_scores):
        sym, pct = mover_scores[scan_index]
        scan_index += 1
        
        df = fetch_ohlc(sym)
        
        if not df.empty:
            ohlc_data[sym] = df
            top5_symbols.append(sym)

    # Fallback
    if len(ohlc_data) < TARGET_MOVERS:
        for default_sym in ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN"]:
            if len(ohlc_data) >= TARGET_MOVERS:
                break
            if default_sym not in top5_symbols:
                df = fetch_ohlc(default_sym)
                if not df.empty:
                    ohlc_data[default_sym] = df
                    top5_symbols.append(default_sym)

    return top5_symbols, ohlc_data


def fetch_watchlist_data(top5_symbols: list):
    """Fetch watchlist quotes and OHLC."""
    watchlist_performance = []
    watchlist_ohlc_data = {}

    for sym in WATCHLIST:
        if not _is_us_stock(sym):
            continue
        
        q = fetch_quote(sym)
        pct = q.get("pct_change", 0)
        watchlist_performance.append((sym, pct, q["current"]))
        
        df = fetch_ohlc(sym)
        if not df.empty:
            watchlist_ohlc_data[sym] = df

    return watchlist_performance, watchlist_ohlc_data


def calculate_scores(top5_symbols: list, ohlc_data: dict, watchlist_ohlc_data: dict, watchlist_performance: list):
    """Calculate investment scores."""
    
    # Top movers
    mover_analysis = []
    for sym in top5_symbols:
        if sym in ohlc_data:
            df = ohlc_data[sym]
            close_prices = df["Close"].values
            
            daily_pct = fetch_quote(sym).get("pct_change", 0)
            seven_day_return = (close_prices[-1] / close_prices[0] - 1) * 100
            volatility = df["Close"].std() / df["Close"].mean() * 100
            high_low_range = (df["High"].max() - df["Low"].min()) / df["Close"].mean() * 100
            
            mover_analysis.append({
                "Symbol": sym,
                "Company": get_company_name(sym),
                "Today %": daily_pct,
                "7-Day %": seven_day_return,
                "Volatility %": volatility,
                "Price Range %": high_low_range,
                "Trend": "📈 UP" if seven_day_return > 0 else "📉 DOWN",
            })

    mover_scores_list = []
    for item in mover_analysis:
        momentum_score = (item["Today %"] + item["7-Day %"]) / 2 * 0.6
        stability_score = (100 / (item["Volatility %"] + 1)) * 0.4
        total_score = momentum_score + stability_score
        
        mover_scores_list.append({
            "Symbol": item["Symbol"],
            "Company": item["Company"],
            "Momentum": item["Today %"],
            "Score": total_score,
            "Recommendation": (
                "🟢 BUY" if total_score > 5 else 
                "🟡 HOLD" if total_score > 2 else 
                "🔴 AVOID"
            ),
            "7Day": item["7-Day %"],
            "Volatility": item["Volatility %"],
        })

    score_df = pd.DataFrame(mover_scores_list).sort_values("Score", ascending=False)

    # Watchlist
    watchlist_analysis = []
    for sym in WATCHLIST:
        if sym in watchlist_ohlc_data:
            df = watchlist_ohlc_data[sym]
            close_prices = df["Close"].values
            
            daily_pct = next(
                (p for s, p, _ in watchlist_performance if s == sym),
                0
            )
            seven_day_return = (close_prices[-1] / close_prices[0] - 1) * 100
            volatility = df["Close"].std() / df["Close"].mean() * 100
            sma_7 = close_prices[-7:].mean() if len(close_prices) >= 7 else close_prices.mean()
            current_price = close_prices[-1]
            ma_ratio = (current_price / sma_7 - 1) * 100 if sma_7 > 0 else 0
            
            watchlist_analysis.append({
                "Symbol": sym,
                "Company": get_company_name(sym),
                "Today %": daily_pct,
                "7-Day %": seven_day_return,
                "Volatility %": volatility,
                "vs 7-MA %": ma_ratio,
                "Current $": current_price,
            })

    watchlist_scores_list = []
    for item in watchlist_analysis:
        if item["Current $"] > 0:
            momentum_score = item["7-Day %"] * 0.5
            ma_score = item["vs 7-MA %"] * 0.5
            total_score = momentum_score + ma_score
            
            watchlist_scores_list.append({
                "Symbol": item["Symbol"],
                "Company": item["Company"],
                "Score": total_score,
                "Recommendation": (
                    "🟢 BUY/HOLD" if total_score > 1 else 
                    "🟡 HOLD" if total_score > -1 else 
                    "🔴 CONSIDER SELLING"
                ),
                "Today %": item["Today %"],
                "7-Day %": item["7-Day %"],
                "Current $": item["Current $"],
            })

    wl_score_df = pd.DataFrame(watchlist_scores_list).sort_values("Score", ascending=False)

    return score_df, wl_score_df


# ============================================================================
# CHART GENERATORS (PLOTLY)
# ============================================================================

def create_movers_ohlc_chart(ohlc_data: dict):
    """Create OHLC line chart for movers."""
    fig = go.Figure()
    
    for sym, df in ohlc_data.items():
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df["Close"],
            mode="lines+markers",
            name=sym,
            line=dict(width=2),
        ))
    
    fig.update_layout(
        title="Top Movers — Close Price (7-Day)",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        hovermode="x unified",
        height=500,
        template="plotly_white"
    )
    
    return fig.to_json()


def create_movers_rebased_chart(ohlc_data: dict):
    """Create rebased performance chart."""
    fig = go.Figure()
    
    for sym, df in ohlc_data.items():
        rebased = df["Close"] / df["Close"].iloc[0] * 100
        fig.add_trace(go.Scatter(
            x=df.index,
            y=rebased,
            mode="lines+markers",
            name=sym,
            line=dict(width=2),
        ))
    
    fig.add_hline(y=100, line_dash="dash", line_color="gray", annotation_text="Start")
    
    fig.update_layout(
        title="Top Movers — Rebased Performance (Start = 100)",
        xaxis_title="Date",
        yaxis_title="Rebased Price",
        hovermode="x unified",
        height=500,
        template="plotly_white"
    )
    
    return fig.to_json()


def create_watchlist_bar_chart(watchlist_performance: list):
    """Create watchlist % change bar chart."""
    data = []
    for sym, pct, _ in watchlist_performance:
        data.append({"Symbol": sym, "Change %": pct, "Color": "#2ecc71" if pct >= 0 else "#e74c3c"})
    
    df = pd.DataFrame(data)
    
    fig = go.Figure(data=[
        go.Bar(
            x=df["Change %"],
            y=df["Symbol"],
            orientation="h",
            marker_color=df["Color"],
            text=df["Change %"].apply(lambda x: f"{x:+.2f}%"),
            textposition="auto",
        )
    ])
    
    fig.update_layout(
        title="Watchlist — Daily % Change",
        xaxis_title="Change (%)",
        yaxis_title="",
        height=400,
        template="plotly_white"
    )
    
    return fig.to_json()


def create_watchlist_ohlc_chart(watchlist_ohlc_data: dict):
    """Create watchlist close price chart."""
    fig = go.Figure()
    
    for sym, df in watchlist_ohlc_data.items():
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df["Close"],
            mode="lines+markers",
            name=sym,
            line=dict(width=2),
        ))
    
    fig.update_layout(
        title="Watchlist — Close Price (7-Day)",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        hovermode="x unified",
        height=500,
        template="plotly_white"
    )
    
    return fig.to_json()


# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')


@app.route('/api/data')
def get_data():
    """Fetch and return all stock data."""
    try:
        top5_symbols, ohlc_data = fetch_movers_data()
        watchlist_performance, watchlist_ohlc_data = fetch_watchlist_data(top5_symbols)
        score_df, wl_score_df = calculate_scores(top5_symbols, ohlc_data, watchlist_ohlc_data, watchlist_performance)
        
        return jsonify({
            "status": "success",
            "top_movers": score_df.to_dict('records'),
            "watchlist": wl_score_df.to_dict('records'),
            "timestamp": datetime.now().isoformat(),
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/charts')
def get_charts():
    """Generate and return charts."""
    try:
        top5_symbols, ohlc_data = fetch_movers_data()
        watchlist_performance, watchlist_ohlc_data = fetch_watchlist_data(top5_symbols)
        
        charts = {
            "movers_price": create_movers_ohlc_chart(ohlc_data),
            "movers_rebased": create_movers_rebased_chart(ohlc_data),
            "watchlist_bar": create_watchlist_bar_chart(watchlist_performance),
            "watchlist_price": create_watchlist_ohlc_chart(watchlist_ohlc_data),
        }
        
        return jsonify({"status": "success", "charts": charts})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/dashboard')
def dashboard():
    """Dashboard page."""
    return render_template('dashboard.html')


@app.route('/api/recommendations')
def get_recommendations():
    """Get investment recommendations."""
    try:
        top5_symbols, ohlc_data = fetch_movers_data()
        watchlist_performance, watchlist_ohlc_data = fetch_watchlist_data(top5_symbols)
        score_df, wl_score_df = calculate_scores(top5_symbols, ohlc_data, watchlist_ohlc_data, watchlist_performance)
        
        best_mover = score_df.iloc[0] if not score_df.empty else None
        best_watchlist = wl_score_df.iloc[0] if not wl_score_df.empty else None
        
        recommendations = {
            "top_mover": {
                "symbol": best_mover["Symbol"] if best_mover is not None else "N/A",
                "recommendation": best_mover["Recommendation"] if best_mover is not None else "No data",
                "score": float(best_mover["Score"]) if best_mover is not None else 0,
                "momentum": float(best_mover["Momentum"]) if best_mover is not None else 0,
            },
            "top_watchlist": {
                "symbol": best_watchlist["Symbol"] if best_watchlist is not None else "N/A",
                "recommendation": best_watchlist["Recommendation"] if best_watchlist is not None else "No data",
                "score": float(best_watchlist["Score"]) if best_watchlist is not None else 0,
            },
            "strategy": {
                "movers": "Buy only if score > 5 (strong momentum + stability). Use 5-10% of portfolio.",
                "watchlist": "Hold if score > 1 (positive trend). Add on dips below 7-day moving average.",
                "cash": "Keep 10-20% cash for buying opportunities. Rebalance when any position > 20%.",
            }
        }
        
        return jsonify({"status": "success", "recommendations": recommendations})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/health')
def health():
    """Health check."""
    return jsonify({"status": "healthy"})


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "=" * 75)
    print(" 📊 STOCK PRICE TRACKER WEB APPLICATION")
    print("=" * 75)
    print("\n  Starting Flask app...")
    
    # Get port from environment or default to 5000
    port = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("FLASK_ENV") == "development"
    
    if debug_mode:
        print("  🌐 Navigate to: http://localhost:{}".format(port))
        print("  📊 Dashboard: http://localhost:{}/dashboard".format(port))
    else:
        print("  Running in production mode on port {}".format(port))
    
    print("\n  Press Ctrl+C to stop\n")
    
    # Use development server only in development mode
    app.run(debug=debug_mode, host='0.0.0.0', port=port, use_reloader=False)
