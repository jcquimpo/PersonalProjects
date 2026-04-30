"""Mock data for demonstration when yfinance fails."""

MOCK_WATCHLIST = [
    {
        "symbol": "AAPL",
        "price": 150.25,
        "percentage_change": 2.5,
        "company_name": "Apple Inc."
    },
    {
        "symbol": "MSFT",
        "price": 380.50,
        "percentage_change": 1.8,
        "company_name": "Microsoft Corporation"
    },
    {
        "symbol": "GOOGL",
        "price": 140.75,
        "percentage_change": 3.2,
        "company_name": "Alphabet Inc."
    }
]

MOCK_OHLC = {
    "AAPL": [
        {"date": "2026-04-20", "open": 146.5, "high": 151.0, "low": 146.2, "close": 150.0},
        {"date": "2026-04-21", "open": 150.1, "high": 152.5, "low": 149.5, "close": 150.25},
    ],
    "MSFT": [
        {"date": "2026-04-20", "open": 375.0, "high": 380.0, "low": 374.5, "close": 378.0},
        {"date": "2026-04-21", "open": 378.5, "high": 382.0, "low": 378.0, "close": 380.50},
    ],
    "GOOGL": [
        {"date": "2026-04-20", "open": 136.0, "high": 140.0, "low": 135.5, "close": 136.5},
        {"date": "2026-04-21", "open": 136.8, "high": 141.5, "low": 136.5, "close": 140.75},
    ]
}

MOCK_TOP_STOCKS = [
    {
        "symbol": "NVDA",
        "price": 875.50,
        "percentage_change": 5.2,
        "company_name": "NVIDIA Corporation"
    },
    {
        "symbol": "TSLA",
        "price": 245.75,
        "percentage_change": 4.8,
        "company_name": "Tesla Inc."
    },
    {
        "symbol": "AMZN",
        "price": 195.25,
        "percentage_change": 3.5,
        "company_name": "Amazon.com Inc."
    },
    {
        "symbol": "META",
        "price": 505.50,
        "percentage_change": 3.1,
        "company_name": "Meta Platforms"
    },
    {
        "symbol": "AAPL",
        "price": 150.25,
        "percentage_change": 2.5,
        "company_name": "Apple Inc."
    }
]
