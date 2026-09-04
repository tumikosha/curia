"""Состояние последней выгрузки."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExportState:
    finished_at: datetime
    rows: int
    ok: bool


def last_export() -> ExportState:
    from app.db import db
    row = db.query_one("SELECT finished_at, rows, ok FROM export_attempts_v2 ORDER BY id DESC LIMIT 1")
    return ExportState(**row)
