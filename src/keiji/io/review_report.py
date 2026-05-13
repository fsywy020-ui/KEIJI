"""Human-readable pending review report exports.

Reports are view-only. They contain no order flow, browser control, or external API
actions.
"""

from __future__ import annotations

import html
import sqlite3
from pathlib import Path
from typing import Any


REVIEW_QUERY = """
SELECT pc.id AS candidate_id, pc.status, pc.profit_estimate_id,
       pc.requested_quantity, pc.total_purchase_amount_yen, pc.requires_human_approval,
       pe.decision AS p3_decision, pe.net_profit_yen, pe.roi_percent,
       pe.profit_margin_percent, pe.break_even_price_yen, pe.risk_adjusted_profit_yen,
       pe.decision_reason, pe.expected_sale_price_yen,
       pid.id AS identity_decision_id, pid.decision AS p4_decision,
       pid.confidence_score, pid.requires_human_review, pid.block_reason,
       so.title AS source_title, so.brand AS source_brand, so.model AS source_model,
       so.jan AS source_jan, so.purchase_price_yen, so.domestic_shipping_yen,
       ml.title AS listing_title, ml.brand AS listing_brand, ml.model AS listing_model,
       ml.jan AS listing_jan, ml.asin AS listing_asin, ml.marketplace
FROM purchase_candidates pc
JOIN profit_estimates pe ON pe.id = pc.profit_estimate_id
JOIN product_identity_decisions pid ON pid.id = pe.identity_decision_id
JOIN source_offers so ON so.id = pid.source_offer_id
JOIN market_listings ml ON ml.id = pid.market_listing_id
WHERE pc.status = 'pending_review'
ORDER BY pc.created_at, pc.id
"""


def pending_review_rows(connection: sqlite3.Connection) -> list[sqlite3.Row]:
    """Return enriched pending review rows for human reports."""

    return list(connection.execute(REVIEW_QUERY))


def export_pending_review_html(connection: sqlite3.Connection, path: str | Path) -> int:
    """Export a static HTML report for pending review candidates."""

    rows = pending_review_rows(connection)
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(_render_html(rows), encoding="utf-8")
    return len(rows)


def export_pending_review_markdown(connection: sqlite3.Connection, path: str | Path) -> int:
    """Export a Markdown report for pending review candidates."""

    rows = pending_review_rows(connection)
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(_render_markdown(rows), encoding="utf-8")
    return len(rows)


def _render_html(rows: list[sqlite3.Row]) -> str:
    cards = "\n".join(_render_html_card(row) for row in rows) or "<p>No pending review candidates.</p>"
    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <title>KEIJI Pending Review</title>
  <style>
    body {{ font-family: sans-serif; margin: 2rem; background: #f7f7f7; color: #222; }}
    .warning {{ padding: 1rem; background: #fff3cd; border: 1px solid #ffe08a; margin-bottom: 1rem; }}
    .card {{ background: white; border: 1px solid #ddd; border-radius: 8px; padding: 1rem; margin: 1rem 0; }}
    .metrics {{ display: grid; grid-template-columns: repeat(4, minmax(120px, 1fr)); gap: .5rem; }}
    .metric {{ background: #f1f5f9; padding: .5rem; border-radius: 4px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: .75rem; }}
    th, td {{ text-align: left; border-bottom: 1px solid #eee; padding: .4rem; }}
    code {{ background: #eee; padding: .1rem .25rem; }}
  </style>
</head>
<body>
  <h1>KEIJI Pending Review</h1>
  <div class="warning">
    <strong>安全注意:</strong> このレポートは確認専用です。購入、決済、外部サイト操作、ブラウザ自動操作、API呼び出しは実行しません。
  </div>
  {cards}
</body>
</html>
"""


def _render_html_card(row: sqlite3.Row) -> str:
    values = {key: html.escape(str(row[key] if row[key] is not None else "")) for key in row.keys()}
    return f"""
  <section class="card">
    <h2>Candidate <code>{values['candidate_id']}</code></h2>
    <div class="metrics">
      <div class="metric"><strong>P3</strong><br>{values['p3_decision']}</div>
      <div class="metric"><strong>Net Profit</strong><br>{values['net_profit_yen']} JPY</div>
      <div class="metric"><strong>ROI</strong><br>{values['roi_percent']}%</div>
      <div class="metric"><strong>Purchase</strong><br>{values['total_purchase_amount_yen']} JPY</div>
    </div>
    <table>
      <tr><th>Status</th><td>{values['status']}</td></tr>
      <tr><th>Human Approval Required</th><td>{values['requires_human_approval']}</td></tr>
      <tr><th>P4 Decision</th><td>{values['p4_decision']} / confidence {values['confidence_score']}</td></tr>
      <tr><th>Source</th><td>{values['source_title']} / {values['source_brand']} / {values['source_model']} / JAN {values['source_jan']}</td></tr>
      <tr><th>Listing</th><td>{values['listing_title']} / {values['listing_brand']} / {values['listing_model']} / ASIN {values['listing_asin']}</td></tr>
      <tr><th>Reason</th><td>{values['decision_reason']}</td></tr>
      <tr><th>Checklist</th><td>JAN/型番/色/容量/状態/販売価格/手数料/仕入れ上限を目視確認してください。</td></tr>
    </table>
  </section>
"""


def _render_markdown(rows: list[sqlite3.Row]) -> str:
    lines = [
        "# KEIJI Pending Review",
        "",
        "> 安全注意: このレポートは確認専用です。購入、決済、外部サイト操作、ブラウザ自動操作、API呼び出しは実行しません。",
        "",
    ]
    if not rows:
        lines.append("No pending review candidates.")
        return "\n".join(lines) + "\n"
    for row in rows:
        lines.extend(
            [
                f"## Candidate `{row['candidate_id']}`",
                "",
                f"- Status: `{row['status']}`",
                f"- P4: `{row['p4_decision']}` confidence `{row['confidence_score']}`",
                f"- P3: `{row['p3_decision']}`",
                f"- Net profit: `{row['net_profit_yen']}` JPY",
                f"- ROI: `{row['roi_percent']}`%",
                f"- Total purchase amount: `{row['total_purchase_amount_yen']}` JPY",
                f"- Source: {row['source_title']}",
                f"- Listing: {row['listing_title']}",
                f"- Reason: {row['decision_reason'] or ''}",
                "- Checklist: JAN / model / variant / condition / price / fees / budget cap",
                "",
            ]
        )
    return "\n".join(lines)
