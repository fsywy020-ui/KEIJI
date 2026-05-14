"""Audit log exports for local offline review."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


def audit_rows(connection: sqlite3.Connection) -> list[sqlite3.Row]:
    """Return audit log rows in insertion order."""

    return list(connection.execute("SELECT * FROM audit_logs ORDER BY rowid"))


def export_audit_json(connection: sqlite3.Connection, path: str | Path) -> int:
    """Export audit logs as JSON array."""

    rows = audit_rows(connection)
    payload = [_row_to_dict(row) for row in rows]
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    return len(rows)


def export_audit_markdown(connection: sqlite3.Connection, path: str | Path) -> int:
    """Export audit logs as Markdown."""

    rows = audit_rows(connection)
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(_render_markdown(rows), encoding="utf-8")
    return len(rows)


def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "event_type": row["event_type"],
        "actor": row["actor"],
        "target_type": row["target_type"],
        "target_id": row["target_id"],
        "payload": json.loads(row["payload_json"]),
        "created_at": row["created_at"],
    }


def _render_markdown(rows: list[sqlite3.Row]) -> str:
    lines = ["# KEIJI Audit Log", ""]
    if not rows:
        lines.append("No audit events.")
        return "\n".join(lines) + "\n"
    for row in rows:
        payload = json.dumps(json.loads(row["payload_json"]), ensure_ascii=False, sort_keys=True)
        lines.extend(
            [
                f"## {row['event_type']} `{row['id']}`",
                "",
                f"- Actor: `{row['actor']}`",
                f"- Target: `{row['target_type']}:{row['target_id']}`",
                f"- Created at: `{row['created_at']}`",
                f"- Payload: `{payload}`",
                "",
            ]
        )
    return "\n".join(lines)
