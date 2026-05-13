"""Audit log repository."""

from __future__ import annotations

import json
import sqlite3
from uuid import uuid4
from typing import Any


class AuditRepository:
    """Persist immutable audit events."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def record(self, *, event_type: str, actor: str, target_type: str, target_id: str, payload: dict[str, Any]) -> str:
        audit_id = str(uuid4())
        self.connection.execute(
            """
            INSERT INTO audit_logs (id, event_type, actor, target_type, target_id, payload_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (audit_id, event_type, actor, target_type, target_id, json.dumps(payload, ensure_ascii=False, sort_keys=True)),
        )
        self.connection.commit()
        return audit_id

    def list_events(self) -> list[sqlite3.Row]:
        return list(self.connection.execute("SELECT * FROM audit_logs ORDER BY rowid"))
