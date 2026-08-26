"""
Fetches recent news headlines - both company-specific and broad
macro/geopolitical - and scores sentiment with VADER (local, no key
needed for scoring itself).

Runs in a degraded no-op mode if NEWSAPI_KEY isn't set, so the rest
of the app still works on technicals + macro correlations alone.
"""

import logging
import requests
from datetime import datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from .config import NEWSAPI_KEY, NEWSAPI_BASE_URL, MACRO_NEWS_QUERIES

log = logging.getLogger(__name__)
_analyzer = SentimentIntensityAnalyzer()

_macro_news_cache = None


def _fetch_newsapi(query: str, max_results: int = 8) -> list:
    if not NEWSAPI_KEY:
        return []

    since = (datetime.utcnow() - timedelta(days=3)).strftime("%Y-%m-%d")
    params = {
        "q": query,
        "from": since,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": max_results,
        "apiKey": NEWSAPI_KEY,
    }
    try:
        resp = requests.get(NEWSAPI_BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        articles = resp.json().get("articles", [])
        return [
            {
                "title": a["title"],
                "source": a.get("source", {}).get("name", "unknown"),
                "url": a.get("url"),
                "published_at": a.get("publishedAt"),
            }
            for a in articles
            if a.get("title")
        ]
    except Exception as exc:
        log.error("News fetch failed for query '%s': %s", query, exc)
        return []


def fetch_headlines(company_name: str, max_results: int = 8) -> list:
    return _fetch_newsapi(f'"{company_name}"', max_results)


def score_sentiment(headlines: list) -> dict:
    """Average VADER compound score across headlines, scaled to -100..100.
    Headline-level keyword/heuristic sentiment, not deep NLP - sarcasm,
    negation nuance and financial jargon can fool it."""
    if not headlines:
        return {"news_score": 0.0, "headline_count": 0}

    scores = [_analyzer.polarity_scores(h["title"])["compound"] for h in headlines]
    avg = sum(scores) / len(scores)
    return {"news_score": round(avg * 100, 1), "headline_count": len(headlines)}


def build_news_snapshot(company_name: str) -> dict:
    headlines = fetch_headlines(company_name)
    sentiment = score_sentiment(headlines)
    return {
        "headlines": headlines[:5],
        "news_score": sentiment["news_score"],
        "headline_count": sentiment["headline_count"],
    }


def build_macro_news_snapshot(force_refresh: bool = False) -> dict:
    """Fetch each broad macro/geopolitical query once per refresh cycle
    and score its aggregate sentiment - shared across all stocks rather
    than re-fetched per stock."""
    global _macro_news_cache
    if _macro_news_cache is not None and not force_refresh:
        return _macro_news_cache

    result = {}
    for query in MACRO_NEWS_QUERIES:
        headlines = _fetch_newsapi(query, max_results=6)
        sentiment = score_sentiment(headlines)
        result[query] = {
            "headlines": headlines[:4],
            "news_score": sentiment["news_score"],
            "headline_count": sentiment["headline_count"],
        }

    _macro_news_cache = result
    return result


def clear_macro_news_cache():
    global _macro_news_cache
    _macro_news_cache = None
