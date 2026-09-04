"""Месячный свод для бухгалтерии. Запускается cron 1-го числа."""

from billing.iban import normalize_iban
from app.db import db


def payout_rows(month: str) -> list[dict]:
    rows = db.query("SELECT id, iban, amount FROM payouts WHERE month = %s", [month])
    for row in rows:
        row["iban"] = normalize_iban(row["iban"])
    return rows
