"""Внутренний дашборд возвратов для операционной команды."""

from datetime import date, timedelta

from flask import Blueprint, jsonify, request

from reports.aggregates import returns_by_store

bp = Blueprint("returns_dashboard", __name__)


@bp.get("/dashboard/returns/by-store")
def by_store():
    days = int(request.args.get("days", 7))
    today = date.today()
    rows = returns_by_store(today - timedelta(days=days), today)
    return jsonify(rows)
