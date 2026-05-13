#!/usr/bin/env python3
"""Export pending review HTML/Markdown reports from a local DB."""

from __future__ import annotations

import argparse

from keiji.db.connection import connect
from keiji.io.review_report import export_pending_review_html, export_pending_review_markdown


def main() -> int:
    parser = argparse.ArgumentParser(description="Export pending review reports")
    parser.add_argument("--db", default="storage/keiji.sqlite3")
    parser.add_argument("--html", default="storage/pending_review.html")
    parser.add_argument("--markdown", default="storage/pending_review.md")
    args = parser.parse_args()
    connection = connect(args.db)
    html_count = export_pending_review_html(connection, args.html)
    markdown_count = export_pending_review_markdown(connection, args.markdown)
    print(f"pending_review_html={html_count} pending_review_markdown={markdown_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
