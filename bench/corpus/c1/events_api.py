"""GET /events — курсорная пагинация по created_at."""

from flask import Flask, jsonify, request

from app.db import db

app = Flask(__name__)


@app.get("/events")
def list_events():
    cursor = request.args.get("cursor")  # ISO timestamp последнего элемента
    limit = int(request.args.get("limit", 100))

    query = "SELECT id, created_at, payload FROM events"
    params = []
    if cursor:
        query += " WHERE created_at > %s"
        params.append(cursor)
    query += " ORDER BY created_at LIMIT %s"
    params.append(limit)

    rows = db.execute(query, params).fetchall()
    next_cursor = rows[-1]["created_at"].isoformat() if rows else None
    return jsonify(
        {
            "items": [dict(r) for r in rows],
            "next_cursor": next_cursor,
        }
    )


@app.get("/events/pages")
def total_pages():
    limit = int(request.args.get("limit", 100))
    total = db.execute("SELECT count(*) FROM events").scalar()
    return jsonify({"pages": total // limit})
