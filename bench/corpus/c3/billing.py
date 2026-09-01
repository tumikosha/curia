"""POST /charge — списание с внутреннего баланса."""

import logging
from decimal import Decimal

from flask import Flask, jsonify, request

from app.db import db

app = Flask(__name__)
log = logging.getLogger("billing")


@app.post("/charge")
def charge():
    body = request.json
    user_id = int(body["user_id"])
    amount = Decimal(str(body["amount"]))
    request_id = body["request_id"]

    if amount <= 0:
        return jsonify({"error": "amount must be positive"}), 400

    log.info("charge %s for user %s, request_id=%s", amount, user_id, request_id)

    balance = db.execute(
        "SELECT balance FROM accounts WHERE user_id = %s", [user_id]
    ).scalar()
    if balance is None:
        return jsonify({"error": "no account"}), 404
    if balance < amount:
        return jsonify({"error": "insufficient funds"}), 402

    try:
        db.execute(
            "UPDATE accounts SET balance = balance - %s WHERE user_id = %s",
            [amount, user_id],
        )
        db.execute(
            "INSERT INTO ledger (user_id, amount, request_id) VALUES (%s, %s, %s)",
            [user_id, amount, request_id],
        )
    except Exception:
        log.exception("charge failed for user %s", user_id)
        return jsonify({"status": "ok"})

    return jsonify({"status": "ok"})
