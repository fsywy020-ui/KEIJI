#!/usr/bin/env python3
"""Export local KEIJI audit logs."""

from __future__ import annotations

import argparse

from keiji.db.connection import connect
from keiji.io.audit_export import export_audit_json, export_audit_markdown


def main() -> int:
    parser = argparse.ArgumentParser(description="Export local KEIJI audit logs")
    parser.add_argument("--db", default="storage/keiji.sqlite3")
    parser.add_argument("--json", default="storage/audit_log.json")
    parser.add_argument("--markdown", default="storage/audit_log.md")
    args = parser.parse_args()
    connection = connect(args.db)
    try:
        json_count = export_audit_json(connection, args.json)
        markdown_count = export_audit_markdown(connection, args.markdown)
    finally:
        connection.close()
    print(f"audit_json={json_count} audit_markdown={markdown_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
