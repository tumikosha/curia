"""Кэш агрегатов по магазинам, чтобы не пересчитывать суммы каждый раз."""

import json
from datetime import date, timedelta

import redis

from reports.aggregates import returns_by_store

_r = redis.Redis()
TTL = 6 * 3600


def cached_returns_by_store(day: date) -> list[dict]:
    key = f"returns:by_store:{day.isoformat()}"
    raw = _r.get(key)
    if raw:
        return json.loads(raw)
    rows = returns_by_store(day, day + timedelta(days=1))
    _r.setex(key, TTL, json.dumps(rows, default=str))
    return rows


def invalidate(day: date) -> None:
    _r.delete(f"returns:by_store:{day.isoformat()}")
