"""
Combines technical momentum, news sentiment, and macro-driver
correlation into a ranked list of expected gainers/losers, with a
projected price range and an explanation of *why* each stock scored
the way it did.

IMPORTANT HONESTY NOTE FOR ANYONE MAINTAINING THIS FILE:
composite_score is a heuristic ranking signal, not a validated,
backtested forecasting model. Do not present its output as a
guaranteed price prediction in the UI - always show the reasoning
(technical/news/macro breakdown) alongside it.
"""

import logging
from .config import WATCHLIST, WEIGHT_TECHNICAL, WEIGHT_NEWS, WEIGHT_MACRO, TOP_N
from .market_data import build_technical_snapshot
from .news_sentiment import build_news_snapshot, build_macro_news_snapshot
from .macro_data import build_macro_links_for_sector, build_macro_snapshot, clear_macro_cache
from .historical_patterns import match_patterns_by_sector

log = logging.getLogger(__name__)


def projected_range(price: float, daily_volatility: float, composite_score: float):
    """
    A transparent range estimate for the next session: center = current
    price nudged by a fraction of the composite score, width = ~1
    standard deviation of recent daily moves. Descriptive statistics,
    not a forecast - "moves of this size have been typical," not "the
    price will land here."
    """
    if daily_volatility <= 0:
        daily_volatility = 0.01

    drift = (composite_score / 100) * daily_volatility * 0.5
    center = price * (1 + drift)
    band = price * daily_volatility

    return {
        "low": round(center - band, 2),
        "center": round(center, 2),
        "high": round(center + band, 2),
    }


def macro_score_from_links(macro_links: list) -> float:
    """Turn the sector's macro correlations into a -100..100 contribution.
    A stock scores positively here when the macro drivers it's actually
    correlated with are currently trending in the direction that link
    says helps it - and the correlation itself must be real (>0.1 or
    <-0.1), not just assumed from the sector map."""
    if not macro_links:
        return 0.0

    contributions = []
    for link in macro_links:
        corr = link["computed_correlation_60d"]
        macro_trend = link.get("macro_current_trend", {})
        if not macro_trend.get("ok") or abs(corr) < 0.1:
            continue
        macro_day_change = macro_trend.get("day_change_pct", 0.0)
        # If correlation is positive, a rising macro instrument helps the stock;
        # if correlation is negative, a rising macro instrument hurts it.
        contributions.append(corr * macro_day_change * 8)  # scaled to a comparable range

    if not contributions:
        return 0.0
    return max(-100, min(100, sum(contributions) / len(contributions)))


def build_snapshot_for_stock(meta: dict) -> dict:
    tech = build_technical_snapshot(meta["ticker"])
    if not tech.get("ok"):
        return None

    close_series = tech.pop("_close_series")
    news = build_news_snapshot(meta["name"])
    macro_links = build_macro_links_for_sector(meta["sector"], close_series)
    macro_component = macro_score_from_links(macro_links)

    composite = (
        WEIGHT_TECHNICAL * tech["technical_score"]
        + WEIGHT_NEWS * news["news_score"]
        + WEIGHT_MACRO * macro_component
    )
    composite = round(max(-100, min(100, composite)), 1)

    rng = projected_range(tech["price"], tech["recent_daily_volatility"], composite)
    related_history = match_patterns_by_sector(meta["sector"])

    return {
        "ticker": meta["ticker"].replace(".NS", ""),
        "name": meta["name"],
        "sector": meta["sector"],
        "market": meta["market"],
        "price": tech["price"],
        "day_change_pct": tech["day_change_pct"],
        "rsi": tech["rsi"],
        "macd_histogram": tech["macd_histogram"],
        "sma50": tech["sma50"],
        "sma200": tech["sma200"],
        "low_52w": tech["low_52w"],
        "high_52w": tech["high_52w"],
        "technical_score": tech["technical_score"],
        "news_score": news["news_score"],
        "headline_count": news["headline_count"],
        "headlines": news["headlines"],
        "macro_score": round(macro_component, 1),
        "macro_links": macro_links,
        "composite_score": composite,
        "projected_range": rng,
        "related_historical_patterns": [
            {"id": p["id"], "title": p["title"], "lesson": p["lesson"]} for p in related_history
        ],
    }


def build_all_snapshots() -> list:
    clear_macro_cache()  # fresh macro data for this refresh cycle
    build_macro_news_snapshot(force_refresh=True)  # warm the macro news cache once

    results = []
    for meta in WATCHLIST:
        try:
            snap = build_snapshot_for_stock(meta)
            if snap:
                results.append(snap)
        except Exception as exc:
            log.error("Failed building snapshot for %s: %s", meta["ticker"], exc)
    return results


def rank_movers(snapshots: list) -> dict:
    ranked = sorted(snapshots, key=lambda s: s["composite_score"], reverse=True)
    top_gainers = ranked[:TOP_N]
    top_losers = list(reversed(ranked[-TOP_N:]))
    return {
        "top_gainers": top_gainers,
        "top_losers": top_losers,
        "all": ranked,
        "macro_snapshot": build_macro_snapshot(),
    }
