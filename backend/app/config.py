"""
Configuration for the stock momentum/sentiment tracker - now covering
India + global markets, plus macro instruments used to explain *why*
a stock might be moving (oil, currency, rates, global indices).
"""

import os

# ---------------------------------------------------------------------------
# INDIA WATCHLIST (NSE, yfinance needs the ".NS" suffix)
# ---------------------------------------------------------------------------
INDIA_WATCHLIST = [
    {"ticker": "RELIANCE.NS", "name": "Reliance Industries", "sector": "Energy", "market": "IN"},
    {"ticker": "TCS.NS", "name": "Tata Consultancy Services", "sector": "IT Services", "market": "IN"},
    {"ticker": "HDFCBANK.NS", "name": "HDFC Bank", "sector": "Banking", "market": "IN"},
    {"ticker": "INFY.NS", "name": "Infosys", "sector": "IT Services", "market": "IN"},
    {"ticker": "ICICIBANK.NS", "name": "ICICI Bank", "sector": "Banking", "market": "IN"},
    {"ticker": "TATAMOTORS.NS", "name": "Tata Motors", "sector": "Automobiles", "market": "IN"},
    {"ticker": "HINDUNILVR.NS", "name": "Hindustan Unilever", "sector": "FMCG", "market": "IN"},
    {"ticker": "SBIN.NS", "name": "State Bank of India", "sector": "Banking", "market": "IN"},
    {"ticker": "BHARTIARTL.NS", "name": "Bharti Airtel", "sector": "Telecom", "market": "IN"},
    {"ticker": "ITC.NS", "name": "ITC", "sector": "FMCG", "market": "IN"},
    {"ticker": "KOTAKBANK.NS", "name": "Kotak Mahindra Bank", "sector": "Banking", "market": "IN"},
    {"ticker": "LT.NS", "name": "Larsen & Toubro", "sector": "Infrastructure", "market": "IN"},
    {"ticker": "AXISBANK.NS", "name": "Axis Bank", "sector": "Banking", "market": "IN"},
    {"ticker": "BAJFINANCE.NS", "name": "Bajaj Finance", "sector": "NBFC", "market": "IN"},
    {"ticker": "MARUTI.NS", "name": "Maruti Suzuki", "sector": "Automobiles", "market": "IN"},
    {"ticker": "SUNPHARMA.NS", "name": "Sun Pharma", "sector": "Pharma", "market": "IN"},
    {"ticker": "WIPRO.NS", "name": "Wipro", "sector": "IT Services", "market": "IN"},
    {"ticker": "ADANIENT.NS", "name": "Adani Enterprises", "sector": "Conglomerate", "market": "IN"},
    {"ticker": "TITAN.NS", "name": "Titan Company", "sector": "Consumer", "market": "IN"},
    {"ticker": "ULTRACEMCO.NS", "name": "UltraTech Cement", "sector": "Cement", "market": "IN"},
    {"ticker": "NTPC.NS", "name": "NTPC", "sector": "Power", "market": "IN"},
    {"ticker": "POWERGRID.NS", "name": "Power Grid Corp", "sector": "Power", "market": "IN"},
    {"ticker": "TATASTEEL.NS", "name": "Tata Steel", "sector": "Metals", "market": "IN"},
    {"ticker": "JSWSTEEL.NS", "name": "JSW Steel", "sector": "Metals", "market": "IN"},
    {"ticker": "HCLTECH.NS", "name": "HCLTech", "sector": "IT Services", "market": "IN"},
    {"ticker": "ASIANPAINT.NS", "name": "Asian Paints", "sector": "Consumer", "market": "IN"},
    {"ticker": "NESTLEIND.NS", "name": "Nestle India", "sector": "FMCG", "market": "IN"},
    {"ticker": "ONGC.NS", "name": "ONGC", "sector": "Energy Upstream", "market": "IN"},
    {"ticker": "TECHM.NS", "name": "Tech Mahindra", "sector": "IT Services", "market": "IN"},
    {"ticker": "COALINDIA.NS", "name": "Coal India", "sector": "Mining", "market": "IN"},
    {"ticker": "BPCL.NS", "name": "Bharat Petroleum", "sector": "Oil Marketing", "market": "IN"},
    {"ticker": "IOC.NS", "name": "Indian Oil Corp", "sector": "Oil Marketing", "market": "IN"},
]

# ---------------------------------------------------------------------------
# GLOBAL WATCHLIST (for tracking only - see README on brokerage access)
# ---------------------------------------------------------------------------
GLOBAL_WATCHLIST = [
    {"ticker": "AAPL", "name": "Apple", "sector": "Technology", "market": "US"},
    {"ticker": "MSFT", "name": "Microsoft", "sector": "Technology", "market": "US"},
    {"ticker": "NVDA", "name": "Nvidia", "sector": "Semiconductors", "market": "US"},
    {"ticker": "GOOGL", "name": "Alphabet", "sector": "Technology", "market": "US"},
    {"ticker": "AMZN", "name": "Amazon", "sector": "E-commerce", "market": "US"},
    {"ticker": "META", "name": "Meta Platforms", "sector": "Technology", "market": "US"},
    {"ticker": "TSLA", "name": "Tesla", "sector": "Automobiles", "market": "US"},
    {"ticker": "JPM", "name": "JPMorgan Chase", "sector": "Banking", "market": "US"},
    {"ticker": "XOM", "name": "Exxon Mobil", "sector": "Energy", "market": "US"},
    {"ticker": "JNJ", "name": "Johnson & Johnson", "sector": "Pharma", "market": "US"},
    {"ticker": "TSM", "name": "Taiwan Semiconductor", "sector": "Semiconductors", "market": "Global-ADR"},
    {"ticker": "BABA", "name": "Alibaba", "sector": "E-commerce", "market": "Global-ADR"},
    {"ticker": "ASML", "name": "ASML Holding", "sector": "Semiconductors", "market": "Global-ADR"},
]

WATCHLIST = INDIA_WATCHLIST + GLOBAL_WATCHLIST

# ---------------------------------------------------------------------------
# MACRO INSTRUMENTS - used to explain *why*, not just *what*
# ---------------------------------------------------------------------------
MACRO_INSTRUMENTS = {
    "crude_oil_wti": {"ticker": "CL=F", "label": "WTI Crude Oil"},
    "crude_oil_brent": {"ticker": "BZ=F", "label": "Brent Crude Oil"},
    "gold": {"ticker": "GC=F", "label": "Gold"},
    "usd_inr": {"ticker": "INR=X", "label": "USD/INR"},
    "us_10y_yield": {"ticker": "^TNX", "label": "US 10-Year Yield"},
    "us_vix": {"ticker": "^VIX", "label": "US VIX (fear gauge)"},
    "nifty50": {"ticker": "^NSEI", "label": "Nifty 50"},
    "sensex": {"ticker": "^BSESN", "label": "Sensex"},
    "sp500": {"ticker": "^GSPC", "label": "S&P 500"},
    "nasdaq": {"ticker": "^IXIC", "label": "Nasdaq Composite"},
}

# Which macro instruments plausibly drive which sector, and roughly how.
# This is a *starting heuristic map* based on well-established economic
# relationships (e.g. IT exporters benefit from a weaker rupee), not a
# fitted or backtested model. Treat the "direction" as a prior, and let
# the computed correlation (in macro_data.py) confirm or challenge it.
SECTOR_MACRO_LINKS = {
    "Energy": [{"macro": "crude_oil_brent", "expected_direction": "positive",
                "note": "Reliance's refining margins tend to benefit from firm crude/product cracks."}],
    "Energy Upstream": [{"macro": "crude_oil_brent", "expected_direction": "positive",
                          "note": "Explorers like ONGC earn more per barrel when crude rises."}],
    "Oil Marketing": [{"macro": "crude_oil_brent", "expected_direction": "negative",
                        "note": "OMCs buy crude but can't always pass costs on - margins get squeezed when crude spikes."}],
    "IT Services": [{"macro": "usd_inr", "expected_direction": "positive",
                      "note": "A weaker rupee raises the rupee value of dollar-billed revenue."},
                     {"macro": "nasdaq", "expected_direction": "positive",
                      "note": "Tracks US tech spending sentiment since most revenue is US-client driven."}],
    "Banking": [{"macro": "us_10y_yield", "expected_direction": "negative",
                 "note": "Rising global rates often precede FII outflows and costlier funding."}],
    "NBFC": [{"macro": "us_10y_yield", "expected_direction": "negative",
              "note": "NBFCs are rate-sensitive borrowers; global rate spikes raise funding costs."}],
    "Automobiles": [{"macro": "crude_oil_brent", "expected_direction": "negative",
                      "note": "Higher fuel costs can dampen vehicle demand and raise input costs."}],
    "Metals": [{"macro": "sp500", "expected_direction": "positive",
                "note": "Industrial metals demand tracks the global growth cycle."}],
    "Semiconductors": [{"macro": "nasdaq", "expected_direction": "positive",
                         "note": "Tightly linked to global tech capex and AI-spend sentiment."}],
    "Technology": [{"macro": "nasdaq", "expected_direction": "positive",
                     "note": "Broad US tech sentiment proxy."}],
}

NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY", "")
NEWSAPI_BASE_URL = "https://newsapi.org/v2/everything"

MACRO_NEWS_QUERIES = [
    "crude oil price",
    "Middle East conflict oil",
    "US Federal Reserve interest rate",
    "India rupee dollar",
    "OPEC oil supply",
]

LOOKBACK_DAYS = 260
CORRELATION_WINDOW_DAYS = 60

WEIGHT_TECHNICAL = 0.45
WEIGHT_NEWS = 0.30
WEIGHT_MACRO = 0.25

TOP_N = 7

CACHE_PATH = os.path.join(os.path.dirname(__file__), "..", "cache", "latest_movers.json")
REFRESH_HOUR_IST = 8
