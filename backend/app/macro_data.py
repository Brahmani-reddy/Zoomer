"""
Fetches macro instruments (oil, currency, rates, indices) and computes
each stock's rolling correlation to the macro drivers relevant to its
sector. This is what lets the dashboard say *why* a stock might be
moving, grounded in an actual computed number rather than a guess.

Correlation != causation, and a 60-day rolling window is a small
sample - treat the correlation as "these two have been moving
together lately," not proof of a causal mechanism.
"""

import logging
import pandas as pd
import yfinance as yf

from .config import MACRO_INSTRUMENTS, SECTOR_MACRO_LINKS, CORRELATION_WINDOW_DAYS, LOOKBACK_DAYS

log = logging.getLogger(__name__)

_macro_cache = {}


def fetch_macro_series(macro_key: str) -> pd.Series:
    """Fetch and cache one macro instrument's daily close series for this refresh cycle."""
    if macro_key in _macro_cache:
        return _macro_cache[macro_key]

    ticker = MACRO_INSTRUMENTS[macro_key]["ticker"]
    try:
        df = yf.Ticker(ticker).history(period=f"{LOOKBACK_DAYS}d", interval="1d")
        series = df["Close"] if not df.empty else pd.Series(dtype=float)
    except Exception as exc:
        log.error("Failed to fetch macro instrument %s (%s): %s", macro_key, ticker, exc)
        series = pd.Series(dtype=float)

    _macro_cache[macro_key] = series
    return series


def build_macro_snapshot() -> dict:
    """Current level + recent % change for every tracked macro instrument."""
    snapshot = {}
    for key, meta in MACRO_INSTRUMENTS.items():
        series = fetch_macro_series(key)
        if series.empty or len(series) < 2:
            snapshot[key] = {"label": meta["label"], "ok": False}
            continue
        price = float(series.iloc[-1])
        prev = float(series.iloc[-2])
        change_pct = (price - prev) / prev * 100 if prev else 0.0
        week_ago = float(series.iloc[-6]) if len(series) >= 6 else prev
        week_change_pct = (price - week_ago) / week_ago * 100 if week_ago else 0.0
        snapshot[key] = {
            "label": meta["label"],
            "ok": True,
            "value": round(price, 2),
            "day_change_pct": round(change_pct, 2),
            "week_change_pct": round(week_change_pct, 2),
        }
    return snapshot


def compute_correlation(stock_close: pd.Series, macro_key: str) -> float:
    macro_series = fetch_macro_series(macro_key)
    if macro_series.empty or len(stock_close) < 10 or len(macro_series) < 10:
        return 0.0

    stock_returns = stock_close.pct_change().dropna()
    macro_returns = macro_series.pct_change().dropna()

    # Align on the trailing correlation window by position (both are daily
    # trading-day series from the same lookback period).
    n = min(len(stock_returns), len(macro_returns), CORRELATION_WINDOW_DAYS)
    if n < 10:
        return 0.0

    s = stock_returns.tail(n).reset_index(drop=True)
    m = macro_returns.tail(n).reset_index(drop=True)
    corr = s.corr(m)
    return round(float(corr), 2) if pd.notna(corr) else 0.0


def build_macro_links_for_sector(sector: str, stock_close: pd.Series) -> list:
    """For a stock's sector, compute real correlation against each linked
    macro instrument and return an explanatory list for the UI."""
    links = SECTOR_MACRO_LINKS.get(sector, [])
    results = []
    for link in links:
        macro_key = link["macro"]
        macro_meta = MACRO_INSTRUMENTS[macro_key]
        corr = compute_correlation(stock_close, macro_key)
        macro_snap = build_macro_snapshot().get(macro_key, {})

        # Does the recent computed correlation actually agree with the
        # textbook "expected direction"? Flag it either way - a mismatch
        # is itself informative (the usual relationship isn't holding
        # right now).
        expected_sign = 1 if link["expected_direction"] == "positive" else -1
        agrees_with_prior = (corr * expected_sign) > 0.1

        results.append({
            "macro": macro_meta["label"],
            "expected_direction": link["expected_direction"],
            "note": link["note"],
            "computed_correlation_60d": corr,
            "matches_typical_pattern": agrees_with_prior,
            "macro_current_trend": macro_snap,
        })
    return results


def clear_macro_cache():
    """Call once per refresh cycle so each daily run fetches fresh macro data."""
    _macro_cache.clear()
