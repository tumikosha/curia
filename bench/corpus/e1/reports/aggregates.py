"""Агрегаты по возвратам за период. Используется отчётом и дашбордом."""

from datetime import date

from app.db import db


def returns_by_store(day_from: date, day_to: date) -> list[dict]:
    """Сумма и количество возвратов по магазинам за период."""
    return db.query(
        """
        SELECT store_id, count(*) AS cnt, sum(amount) AS total
        FROM returns
        WHERE created_at >= %s AND created_at < %s
        GROUP BY store_id
        ORDER BY store_id
        """,
        [day_from, day_to],
    )


def returns_rows(day_from: date, day_to: date) -> list[dict]:
    """Построчный список возвратов за период."""
    return db.query(
        """
        SELECT r.id, r.order_id, r.amount, r.reason, r.status, s.name AS store
        FROM returns r JOIN stores s ON s.id = r.store_id
        WHERE r.created_at >= %s AND r.created_at < %s
        ORDER BY r.created_at
        """,
        [day_from, day_to],
    )
