"""
Market Data Agent
-----------------
Fetches live stock indices, crypto, commodities, and treasury yields.
Uses yfinance - free, no API key required.
"""
import yfinance as yf
from datetime import datetime
from config.settings import INDICES, ASSETS, TREASURIES

def get_price_data(symbol: str) -> dict:
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="5d")
        if hist.empty or len(hist) < 2:
            return None
        current_price = hist["Close"].iloc[-1]
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
    print("Fetching market data...")
    data = {
        "indices": {},
        "assets": {},
        "treasuries": {},
        "timestamp": datetime.now().strftime("%B %d, %Y at %I:%M %p"),
    }
    for name, symbol in INDICES.items():
        result = get_price_data(symbol)
        if result:
            data["indices"][name] = result
            print(f"  ✓ {name}: {result['direction']} {result['change_pct']}%")
    for name, symbol in ASSETS.items():
        result = get_price_data(symbol)
        if result:
            data["assets"][name] = result
            print(f"  ✓ {name}: ${result['price']:,}")
    for name, symbol in TREASURIES.items():
        result = get_price_data(symbol)
        if result:
            data["treasuries"][name] = result
            print(f"  ✓ {name}: {result['price']}%")
    return data

def format_market_data_for_prompt(market_data: dict) -> str:
    lines = [f"Market data as of {market_data['timestamp']}:\n"]
    lines.append("MAJOR INDICES:")
    for name, d in market_data["indices"].items():
        lines.append(f"  {name}: {d['price']:,} ({d['direction']} {abs(d['change_pct'])}%)")
    lines.append("\nASSETS:")
    for name, d in market_data["assets"].items():
        lines.append(f"  {name}: ${d['price']:,} ({d['direction']} {abs(d['change_pct'])}%)")
    lines.append("\nTREASURY YIELDS:")
    for name, d in market_data["treasuries"].items():
        lines.append(f"  {name}: {d['price']}% ({d['direction']} {abs(d['change'])} bps)")
    return "\n".join(lines)
