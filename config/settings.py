import os
from dotenv import load_dotenv
load_dotenv()  # reads your .env file
# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
FRED_API_KEY = os.getenv("FRED_API_KEY")
# Email
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
# Market symbols to track
INDICES = {
    "S&P 500": "^GSPC",
    "Nasdaq": "^IXIC",
    "Dow Jones": "^DJI",
}
ASSETS = {
    "Bitcoin": "BTC-USD",
    "Gold": "GC=F",
    "Oil (WTI)": "CL=F",
}
TREASURIES = {
    "2-Year Treasury": "^IRX",
    "10-Year Treasury": "^TNX",
    "30-Year Treasury": "^TYX",
}
# Education settings
TOPICS_IN_ORDER = [
    "Time Value of Money",
    "Financial Statements Basics",
"Financial Statements Basics",
"Income Statement Deep Dive",
"Balance Sheet Deep Dive",
"Cash Flow Statement",
"Financial Ratios",
"Net Present Value (NPV)",
"Internal Rate of Return (IRR)",
"Cost of Capital (WACC)",
"Capital Structure",
"Bonds and Fixed Income Basics",
"Duration and Convexity",
"Yield Curves",
"Stock Valuation: DDM",
"Stock Valuation: DCF",
"Stock Valuation: Multiples",
"Portfolio Theory",
"CAPM",
"Risk and Return",
"Options Basics",
"Black-Scholes Intuition",
"Futures and Forwards",
"Financial Modeling Principles",
"M&A Basics",
"Behavioral Finance",
"FinTech and Modern Markets",
 ]
  # How many lessons before advancing difficulty
LESSONS_PER_LEVEL = 5
