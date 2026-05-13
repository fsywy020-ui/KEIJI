#!/usr/bin/env python3
"""Export local KEIJI DB status reports."""

from __future__ import annotations

import argparse

from keiji.db.connection import connect
from keiji.io.status_report import export_status_json, export_status_markdown


def main() -> int:
    parser = argparse.ArgumentParser(description="Export local KEIJI status report")
    parser.add_argument("--db", default="storage/keiji.sqlite3")
    parser.add_argument("--json", default="storage/status.json")
    parser.add_argument("--markdown", default="storage/status.md")
    args = parser.parse_args()
    connection = connect(args.db)
    export_status_json(connection, args.json)
    export_status_markdown(connection, args.markdown)
    print(f"status_json={args.json} status_markdown={args.markdown}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
