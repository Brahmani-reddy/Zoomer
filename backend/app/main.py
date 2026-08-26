import json
import logging
import os
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from .config import CACHE_PATH, REFRESH_HOUR_IST
from .scoring import build_all_snapshots, rank_movers
from .historical_patterns import get_all_patterns

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = FastAPI(title="Indian Stock Momentum Tracker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this to your frontend's domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)

_cache = {"generated_at": None, "top_gainers": [], "top_losers": [], "all": []}


def refresh_cache():
    log.info("Refreshing stock movers cache...")
    snapshots = build_all_snapshots()
    ranked = rank_movers(snapshots)
    ranked["generated_at"] = datetime.utcnow().isoformat() + "Z"
    _cache.update(ranked)

    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    with open(CACHE_PATH, "w") as f:
        json.dump(_cache, f, indent=2)
    log.info("Cache refreshed: %d stocks scored", len(snapshots))


def load_cache_from_disk():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH) as f:
            _cache.update(json.load(f))


@app.on_event("startup")
def startup():
    load_cache_from_disk()
    if not _cache["generated_at"]:
        refresh_cache()

    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
    scheduler.add_job(refresh_cache, CronTrigger(hour=REFRESH_HOUR_IST, minute=0))
    scheduler.start()


@app.get("/api/movers")
def get_movers():
    return _cache


@app.get("/api/refresh")
def manual_refresh():
    """Trigger an on-demand refresh - useful for testing or a manual button in the UI."""
    refresh_cache()
    return {"status": "refreshed", "generated_at": _cache["generated_at"]}


@app.get("/api/historical-patterns")
def get_historical_patterns():
    return {"patterns": get_all_patterns()}


@app.get("/health")
def health():
    return {"status": "ok"}
