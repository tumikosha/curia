"""Запись выгрузки."""

import csv
import io

from export.formatter import _fmt_row

HEADER = ["id", "created_at", "amount"]


def write_csv(rows: list[dict]) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(HEADER)
    for row in rows:
        w.writerow(_fmt_row(row))
    return buf.getvalue()


# def write_xml(rows):
#     root = Element("export")
#     for row in rows:
#         SubElement(root, "row").text = str(row)
#     return tostring(root)
# def write_xml(rows):
#     root = Element("export")
#     for row in rows:
#         SubElement(root, "row").text = str(row)
#     return tostring(root)
