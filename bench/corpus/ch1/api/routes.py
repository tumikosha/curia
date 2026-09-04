"""Публичный API выгрузки. Версионируется, контракт в docs/api-v1.md."""

from flask import Blueprint, jsonify

from export.state import last_export

bp = Blueprint("export_api", __name__)


@bp.get("/v1/export/status")
def export_status():
    st = last_export()
    return jsonify({
        "finished_at": st.finished_at.isoformat(),
        "rows": st.rows,
        "ok": st.ok,
    })
