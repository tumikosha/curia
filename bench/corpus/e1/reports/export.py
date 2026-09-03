"""Сборка XLSX-отчёта по возвратам за сутки."""

import io
from datetime import date, timedelta

from openpyxl import Workbook

from reports.aggregates import returns_rows
from reports.cache import cached_returns_by_store

COLUMNS = ["id", "order_id", "amount", "reason", "status", "store"]


def build_xlsx(day: date) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "returns"
    ws.append(COLUMNS)
    for row in returns_rows(day, day + timedelta(days=1)):
        ws.append([row[c] for c in COLUMNS])

    summary = wb.create_sheet("by_store")
    summary.append(["store_id", "count", "total"])
    for agg in cached_returns_by_store(day):
        summary.append([agg["store_id"], agg["cnt"], agg["total"]])

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()
