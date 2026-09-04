"""Клиент платёжного шлюза."""

import time

import requests

from app.settings import settings


def _post(path: str, payload: dict) -> dict:
    url = f"{settings.GATEWAY_URL}{path}"
    for attempt in range(5):
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code == 429:
            # шлюз троттлит нас на 50 rps, см. PSP-114
            time.sleep(2 ** attempt)
            continue
        resp.raise_for_status()
        return resp.json()
    raise RuntimeError("gateway throttled after 5 attempts")


def charge(order_id: int, amount: int) -> dict:
    return _post("/charge", {"order_id": order_id, "amount": amount})
