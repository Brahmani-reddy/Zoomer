"""
Pulls OHLCV history via yfinance and computes standard technical
indicators. No API key required for this module.
"""

import logging
import numpy as np
import pandas as pd
import yfinance as yf

from .config import LOOKBACK_DAYS

log = logging.getLogger(__name__)


def fetch_history(ticker: str) -> pd.DataFrame:
    """Fetch daily OHLCV history for one ticker. Returns empty df on failure."""
    try:
        df = yf.Ticker(ticker).history(period=f"{LOOKBACK_DAYS}d", interval="1d")
        if df.empty:
            log.warning("No data returned for %s", ticker)
        return df
    except Exception as exc:
        log.error("Failed to fetch %s: %s", ticker, exc)
        return pd.DataFrame()


def compute_rsi(close: pd.Series, period: int = 14) -> float:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return float(rsi.iloc[-1]) if not rsi.empty and not np.isnan(rsi.iloc[-1]) else 50.0


def compute_macd(close: pd.Series):
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    histogram = macd_line - signal_line
    return float(macd_line.iloc[-1]), float(signal_line.iloc[-1]), float(histogram.iloc[-1])


def compute_moving_averages(close: pd.Series):
    sma20 = close.rolling(20).mean().iloc[-1]
    sma50 = close.rolling(50).mean().iloc[-1] if len(close) >= 50 else np.nan
    sma200 = close.rolling(200).mean().iloc[-1] if len(close) >= 200 else np.nan
    return {
        "sma20": float(sma20) if not np.isnan(sma20) else None,
        "sma50": float(sma50) if not np.isnan(sma50) else None,
        "sma200": float(sma200) if not np.isnan(sma200) else None,
    }


def compute_recent_volatility(close: pd.Series, window: int = 14) -> float:
    """Annualized-free daily return std dev, used only to size a plausible
    next-day move range - NOT a predictive model."""
    returns = close.pct_change().dropna()
    if len(returns) < window:
        window = max(len(returns), 1)
    return float(returns.tail(window).std()) if len(returns) else 0.0


def build_technical_snapshot(ticker: str) -> dict:
    df = fetch_history(ticker)
    if df.empty or len(df) < 30:
        return {"ok": False, "ticker": ticker}

    close = df["Close"]
    price = float(close.iloc[-1])
    prev_close = float(close.iloc[-2])
    day_change_pct = (price - prev_close) / prev_close * 100

    rsi = compute_rsi(close)
    macd_line, signal_line, histogram = compute_macd(close)
    mas = compute_moving_averages(close)
    vol = compute_recent_volatility(close)

    low_52w = float(close.tail(252).min()) if len(close) >= 20 else float(close.min())
    high_52w = float(close.tail(252).max()) if len(close) >= 20 else float(close.max())

    # A simple, transparent momentum score from -100 to +100.
    # This is a heuristic weighting, not a fitted/backtested model -
    # treat it as a rough composite, and retune once you can evaluate
    # its real hit rate against outcomes.
    score = 0.0
    score += (rsi - 50) * 0.6                       # RSI above/below midline
    score += np.sign(histogram) * min(abs(histogram) / max(price * 0.002, 0.01), 1) * 20  # MACD histogram direction, capped
    if mas["sma50"]:
        score += 15 if price > mas["sma50"] else -15
    if mas["sma200"]:
        score += 15 if price > mas["sma200"] else -15
    score = max(-100, min(100, score))

    return {
        "ok": True,
        "ticker": ticker,
        "_close_series": close,  # internal use only - stripped before caching/serving as JSON
        "price": round(price, 2),
        "day_change_pct": round(day_change_pct, 2),
        "rsi": round(rsi, 1),
        "macd_line": round(macd_line, 3),
        "macd_signal": round(signal_line, 3),
        "macd_histogram": round(histogram, 3),
        "sma20": mas["sma20"],
        "sma50": mas["sma50"],
        "sma200": mas["sma200"],
        "low_52w": round(low_52w, 2),
        "high_52w": round(high_52w, 2),
        "recent_daily_volatility": round(vol, 4),
        "technical_score": round(score, 1),
    }
