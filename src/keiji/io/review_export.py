"""Export pending review candidates without purchase execution."""

from __future__ import annotations

import csv
import sqlite3
from pathlib import Path


REVIEW_COLUMNS = [
    "candidate_id",
    "status",
    "profit_estimate_id",
    "decision",
    "net_profit_yen",
    "roi_percent",
    "total_purchase_amount_yen",
    "requires_human_approval",
]


def export_pending_review_csv(connection: sqlite3.Connection, path: str | Path) -> int:
    """Export pending purchase candidates for human review."""

    rows = list(
        connection.execute(
            """
            SELECT pc.id AS candidate_id, pc.status, pc.profit_estimate_id, pe.decision,
                   pe.net_profit_yen, pe.roi_percent, pc.total_purchase_amount_yen,
                   pc.requires_human_approval
            FROM purchase_candidates pc
            JOIN profit_estimates pe ON pe.id = pc.profit_estimate_id
            WHERE pc.status = 'pending_review'
            ORDER BY pc.created_at, pc.id
            """
        )
    )
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=REVIEW_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row[column] for column in REVIEW_COLUMNS})
    return len(rows)
