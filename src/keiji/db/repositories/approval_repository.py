"""Human approval repository."""

from __future__ import annotations

import sqlite3
from uuid import uuid4


ALLOWED_APPROVAL_DECISIONS = {"approved", "rejected", "needs_more_info"}


class ApprovalRepository:
    """Persist human approvals and validate reviewer identity."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def record(
        self,
        *,
        target_type: str,
        target_id: str,
        decision: str,
        reviewer_name: str,
        comment: str | None = None,
    ) -> str:
        if decision not in ALLOWED_APPROVAL_DECISIONS:
            raise ValueError(f"unsupported approval decision: {decision}")
        if not reviewer_name.strip():
            raise ValueError("reviewer_name is required")
        approval_id = str(uuid4())
        self.connection.execute(
            """
            INSERT INTO human_approvals (id, target_type, target_id, decision, reviewer_name, comment)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (approval_id, target_type, target_id, decision, reviewer_name.strip(), comment),
        )
        self.connection.commit()
        return approval_id

    def latest_for(self, *, target_type: str, target_id: str) -> sqlite3.Row | None:
        return self.connection.execute(
            """
            SELECT * FROM human_approvals
            WHERE target_type = ? AND target_id = ?
            ORDER BY approved_at DESC, id DESC
            LIMIT 1
            """,
            (target_type, target_id),
        ).fetchone()
