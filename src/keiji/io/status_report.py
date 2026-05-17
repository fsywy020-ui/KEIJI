"""Local operations status reports for KEIJI."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


def build_status_summary(connection: sqlite3.Connection) -> dict[str, Any]:
    """Build a local DB status summary for operations review."""

    return {
        "counts": {
            "source_offers": _count(connection, "source_offers"),
            "market_listings": _count(connection, "market_listings"),
            "p4_identity_runs": _count(connection, "p4_identity_runs"),
            "product_identity_decisions": _count(connection, "product_identity_decisions"),
            "p3_profit_runs": _count(connection, "p3_profit_runs"),
            "profit_estimates": _count(connection, "profit_estimates"),
            "purchase_candidates": _count(connection, "purchase_candidates"),
            "human_approvals": _count(connection, "human_approvals"),
            "audit_logs": _count(connection, "audit_logs"),
        },
        "p4_decisions": _group_count(connection, "product_identity_decisions", "decision"),
        "p3_decisions": _group_count(connection, "profit_estimates", "decision"),
        "candidate_statuses": _group_count(connection, "purchase_candidates", "status"),
        "budget": _budget_summary(connection),
    }


def export_status_json(connection: sqlite3.Connection, path: str | Path) -> None:
    """Export status summary as JSON."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(build_status_summary(connection), ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def export_status_markdown(connection: sqlite3.Connection, path: str | Path) -> None:
    """Export status summary as Markdown."""

    summary = build_status_summary(connection)
    lines = [
        "# KEIJI Local Status",
        "",
        "> 確認専用の集計です。`purchase_candidates` は購入許可ではなく、人間確認候補の件数です。",
        "> この集計から購入、決済、出品、login、cart、checkout、browser automation、scraping、external agent API、live external API、外部通知送信は実行しません。",
        "",
    ]
    lines.append("## Counts")
    for key, value in summary["counts"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Decisions", "", "### P4"])
    for key, value in summary["p4_decisions"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "### P3"])
    for key, value in summary["p3_decisions"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Candidate Statuses"])
    for key, value in summary["candidate_statuses"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Budget"])
    for key, value in summary["budget"].items():
        lines.append(f"- {key}: `{value}`")
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _count(connection: sqlite3.Connection, table: str) -> int:
    return int(connection.execute(f"SELECT COUNT(*) AS count FROM {table}").fetchone()["count"])


def _group_count(connection: sqlite3.Connection, table: str, column: str) -> dict[str, int]:
    rows = connection.execute(f"SELECT {column} AS key, COUNT(*) AS count FROM {table} GROUP BY {column} ORDER BY {column}").fetchall()
    return {str(row["key"]): int(row["count"]) for row in rows}


def _budget_summary(connection: sqlite3.Connection) -> dict[str, int]:
    row = connection.execute(
        """
        SELECT COALESCE(SUM(total_purchase_amount_yen), 0) AS pending_amount
        FROM purchase_candidates
        WHERE status = 'pending_review'
        """
    ).fetchone()
    approved_row = connection.execute(
        """
        SELECT COALESCE(SUM(total_purchase_amount_yen), 0) AS approved_amount
        FROM purchase_candidates
        WHERE status = 'approved'
        """
    ).fetchone()
    return {
        "pending_review_amount_yen": int(row["pending_amount"]),
        "approved_amount_yen": int(approved_row["approved_amount"]),
        "initial_budget_yen": 50000,
        "remaining_after_approved_yen": 50000 - int(approved_row["approved_amount"]),
    }
