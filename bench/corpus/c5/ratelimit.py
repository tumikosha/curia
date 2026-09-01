"""Rate limiter для публичного API.

Fixed window: считаем запросы в текущем минутном окне; по истечении
окна счётчик обнуляется. Потокобезопасно.
"""

import logging
import threading
import time

from flask import Flask, jsonify, request

app = Flask(__name__)
log = logging.getLogger("ratelimit")

WINDOW_SECONDS = 60
LIMIT_PER_WINDOW = 100

_lock = threading.Lock()
_window_start = 0.0
_window_count = 0


def _allow_request() -> bool:
    """True, если запрос помещается в текущее окно."""
    global _window_start, _window_count
    now = time.monotonic()
    with _lock:
        if now - _window_start >= WINDOW_SECONDS:
            _window_start = now
            _window_count = 0
        if _window_count >= LIMIT_PER_WINDOW:
            return False
        _window_count += 1
        return True


@app.before_request
def rate_limit():
    api_key = request.headers.get("X-Api-Key", "anonymous")
    if not _allow_request():
        log.info("rate limit exceeded, key=%s", api_key)
        return jsonify({"error": "too many requests"}), 503
    return None
