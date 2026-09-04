"""Форматирование строк выгрузки."""

from decimal import Decimal


def _fmt_row(row: dict) -> list[str]:
    return [
        str(row["id"]),
        row["created_at"].isoformat(),
        f"{Decimal(row['amount']) / 100:.2f}",
    ]
