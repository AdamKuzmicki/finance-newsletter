Market Data Agent
  -----------------
  Fetches live stock indices, crypto, commodities, and treasury yields.
  Uses yfinance — free, no API key required.
Uses yfinance — free, no API key required.
Key concept: yfinance downloads historical OHLCV data from Yahoo Finance.
We grab the last 2 days so we can calculate the daily change (today vs yesterday).
"""
import yfinance as yf
from datetime import datetime, timedelta
from config.settings import INDICES, ASSETS, TREASURIES
def get_price_data(symbol: str) -> dict:
    """
    Fetch price data for a single ticker symbol.
    Returns a dict with current price, previous close, change, and % change.
    Returns None if the fetch fails (markets closed, bad symbol, etc.)
    """
    try:
        ticker = yf.Ticker(symbol)
        # Download last 5 days of data (we need 2, but weekends/holidays can skip da
        hist = ticker.history(period="5d")
        if hist.empty or len(hist) < 2:
            return None
        # Most recent close price
        current_price = hist["Close"].iloc[-1]
        # Previous close (day before)
        prev_price = hist["Close"].iloc[-2]
        change = current_price - prev_price
        change_pct = (change / prev_price) * 100
        return {
            "price": round(current_price, 2),
            "change": round(change, 2),
            "change_pct": round(change_pct, 2),
              "direction": "▲" if change >= 0 else "▼",
        }
    except Exception as e:
        print(f"Warning: Could not fetch {symbol}: {e}")
        return None
def get_market_data() -> dict:
    """
    Fetch all market data: indices, assets, and treasury yields.
    Returns a structured dictionary that gets passed to Claude.
    """
    print("Fetching market data...")
    data = {
        "indices": {},
        "assets": {},
        "treasuries": {},
        "timestamp": datetime.now().strftime("%B %d, %Y at %I:%M %p"),
}
    # Fetch major indices
    for name, symbol in INDICES.items():
        result = get_price_data(symbol)
        if result:
            data["indices"][name] = result
            print(f"  ✓ {name}: {result['direction']} {result['change_pct']}%")
    # Fetch crypto and commodities
    for name, symbol in ASSETS.items():
        result = get_price_data(symbol)
        if result:
            data["assets"][name] = result
            print(f"  ✓ {name}: ${result['price']:,}")
    # Fetch treasury yields
