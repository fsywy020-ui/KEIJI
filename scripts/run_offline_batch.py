#!/usr/bin/env python3
"""Run a local offline KEIJI batch from JSON or CSV input.

This script does not call external APIs and does not purchase/pay.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from keiji.db.connection import connect, initialize_schema
from keiji.io.local_candidates import load_candidates_csv, load_candidates_json
from keiji.io.review_export import export_pending_review_csv
from keiji.pipeline.offline_runner import OfflinePipelineRunner


def main() -> int:
    parser = argparse.ArgumentParser(description="Run offline KEIJI P4/P3 batch")
    parser.add_argument("--input", required=True, help="JSON or CSV candidate file")
    parser.add_argument("--db", default="storage/keiji.sqlite3", help="SQLite DB path")
    parser.add_argument("--review-csv", default="storage/pending_review.csv", help="Pending review CSV output")
    parser.add_argument("--product-rules", default="config/product_identity_rules.v1.yaml")
    parser.add_argument("--profit-rules", default="config/profit_rules.v1.yaml")
    args = parser.parse_args()

    input_path = Path(args.input)
    candidates = load_candidates_json(input_path) if input_path.suffix.lower() == ".json" else load_candidates_csv(input_path)
    connection = connect(args.db)
    initialize_schema(connection)
    runner = OfflinePipelineRunner(
        connection=connection,
        product_identity_rules_path=args.product_rules,
        profit_rules_path=args.profit_rules,
    )
    for candidate in candidates:
        runner.run_one(candidate)
    exported = export_pending_review_csv(connection, args.review_csv)
    print(f"processed={len(candidates)} pending_review_exported={exported}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
