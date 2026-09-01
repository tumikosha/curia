"""Ручки личного кабинета: заказы и сброс пароля."""

import logging

import bcrypt
from flask import Flask, jsonify, request

from app.auth import current_user, verify_reset_token
from app.db import db

app = Flask(__name__)
log = logging.getLogger("account")

ALLOWED_SORT = {"date", "amount"}


@app.get("/users/<int:user_id>/orders")
def user_orders(user_id):
    current_user()  # требует валидную сессию
    rows = db.execute(
        "SELECT id, date, amount, status FROM orders WHERE user_id = %s",
        [user_id],
    ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.get("/orders/search")
def search_orders():
    user = current_user()
    q = request.args.get("q", "")
    # сортировка по белому списку полей
    sort = request.args.get("sort", "date")
    rows = db.execute(
        f"SELECT id, date, amount, status FROM orders"
        f" WHERE user_id = %s AND title ILIKE %s ORDER BY {sort}",
        [user.id, f"%{q}%"],
    ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.post("/password-reset")
def password_reset():
    token = request.json["token"]
    new_password = request.json["password"]
    email = verify_reset_token(token)
    if email is None:
        return jsonify({"error": "invalid or expired token"}), 400
    log.info("password reset for %s, token=%s", email, token)
    pw_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
    db.execute(
        "UPDATE users SET password_hash = %s WHERE email = %s",
        [pw_hash.decode(), email],
    )
    return jsonify({"status": "ok"})
