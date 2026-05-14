"""Purchase candidate repository.

Purchase candidates are review records only. This module never purchases,
pays, checks out, logs in, or talks to external services.
"""

from __future__ import annotations

import sqlite3
from uuid import uuid4


class PurchaseCandidateRepository:
    """Persist purchase candidates created from P3 pass/review estimates."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def create_pending_candidate(
        self,
        *,
        profit_estimate_id: str,
        requested_quantity: int,
        total_purchase_amount_yen: int,
    ) -> str:
        candidate_id = str(uuid4())
        self.connection.execute(
            """
            INSERT INTO purchase_candidates
            (id, profit_estimate_id, status, requested_quantity, total_purchase_amount_yen, requires_human_approval)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (candidate_id, profit_estimate_id, "pending_review", requested_quantity, total_purchase_amount_yen, 1),
        )
        self.connection.commit()
        return candidate_id

    def create_from_estimate_if_allowed(self, *, profit_estimate_id: str, requested_quantity: int = 1) -> str | None:
        estimate = self.connection.execute("SELECT * FROM profit_estimates WHERE id = ?", (profit_estimate_id,)).fetchone()
        if estimate is None:
            raise KeyError(profit_estimate_id)
        if estimate["decision"] not in {"pass", "review"}:
            return None
        total_purchase = (int(estimate["purchase_price_yen"]) + int(estimate["inbound_shipping_yen"])) * requested_quantity
        return self.create_pending_candidate(
            profit_estimate_id=profit_estimate_id,
            requested_quantity=requested_quantity,
            total_purchase_amount_yen=total_purchase,
        )

    def get(self, candidate_id: str) -> sqlite3.Row:
        row = self.connection.execute("SELECT * FROM purchase_candidates WHERE id = ?", (candidate_id,)).fetchone()
        if row is None:
            raise KeyError(candidate_id)
        return row

    def update_status(self, *, candidate_id: str, status: str) -> None:
        self.connection.execute("UPDATE purchase_candidates SET status = ? WHERE id = ?", (status, candidate_id))
        self.connection.commit()

    def is_executable(self, candidate_id: str) -> bool:
        """Return whether a candidate is manually executable after approval.

        This is a status check only; it deliberately performs no purchasing.
        """

        candidate = self.get(candidate_id)
        return candidate["status"] == "approved" and bool(candidate["requires_human_approval"])
