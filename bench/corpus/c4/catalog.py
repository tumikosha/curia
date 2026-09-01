"""Карточка товара с кэшем в Redis."""

import json
import logging

import redis
from flask import Flask, jsonify, request

from app.db import db

app = Flask(__name__)
log = logging.getLogger("catalog")
cache = redis.Redis()

CACHE_TTL = 600  # 10 минут


@app.get("/product/<int:pid>")
def get_product(pid):
    key = f"product:{pid}"
    try:
        cached = cache.get(key)
        if cached:
            return jsonify(json.loads(cached))
    except redis.RedisError:
        log.warning("redis unavailable, serving from db")

    product = db.execute(
        "SELECT id, title, description, price FROM products WHERE id = %s",
        [pid],
    ).fetchone()
    if product is None:
        return jsonify({"error": "not found"}), 404

    reviews = db.execute(
        "SELECT user_id, rating, text FROM reviews WHERE product_id = %s",
        [pid],
    ).fetchall()
    review_list = []
    for r in reviews:
        author = db.execute(
            "SELECT name FROM users WHERE id = %s", [r["user_id"]]
        ).scalar()
        review_list.append({"author": author, "rating": r["rating"], "text": r["text"]})

    card = {**dict(product), "reviews": review_list}
    try:
        # кэш best-effort: если Redis лежит, просто отдаём из БД
        cache.set(key, json.dumps(card), ex=CACHE_TTL)
    except redis.RedisError:
        pass
    return jsonify(card)


@app.put("/product/<int:pid>")
def update_product(pid):
    body = request.json
    db.execute(
        "UPDATE products SET title = %s, description = %s, price = %s WHERE id = %s",
        [body["title"], body["description"], body["price"], pid],
    )
    try:
        cache.delete(f"products:{pid}")
    except redis.RedisError:
        log.warning("redis unavailable, cache not invalidated")
    return jsonify({"status": "ok"})
