#!/usr/bin/env python3
"""Export pending review candidates from a local DB."""

from __future__ import annotations

import argparse

from keiji.db.connection import connect
from keiji.io.review_export import export_pending_review_csv


def main() -> int:
    parser = argparse.ArgumentParser(description="Export pending review CSV")
    parser.add_argument("--db", default="storage/keiji.sqlite3")
    parser.add_argument("--out", default="storage/pending_review.csv")
    args = parser.parse_args()
    connection = connect(args.db)
    count = export_pending_review_csv(connection, args.out)
    print(f"pending_review_exported={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
