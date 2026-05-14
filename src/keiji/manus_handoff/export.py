"""Local exporters for P8 Manus handoff packets."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from keiji.manus_handoff.models import ManusHandoffPacket


def export_handoff_packets_json(packets: list[ManusHandoffPacket], path: str | Path) -> int:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps([packet.to_dict() for packet in packets], ensure_ascii=False, indent=2), encoding="utf-8")
    return len(packets)


def export_handoff_packets_csv(packets: list[ManusHandoffPacket], path: str | Path) -> int:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "candidate_id",
        "product_name",
        "jan",
        "asin",
        "model_number",
        "p7_review_status",
        "recommended_action",
        "per_sku_limit_ok",
        "initial_budget_impact_yen",
        "human_approval_required",
        "external_send_disabled",
        "purchase_execution_disabled",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for packet in packets:
            row = packet.to_dict()
            writer.writerow({field: row[field] for field in fields})
    return len(packets)


def export_handoff_packets_markdown(packets: list[ManusHandoffPacket], path: str | Path) -> int:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# KEIJI P8 Manus Handoff Packets",
        "",
        "> ローカル確認専用です。Manus に購入、決済、出品、checkout、login、cart 操作、browser automation、scraping、live external API access は許可しません。",
        "",
    ]
    for packet in packets:
        data = packet.to_dict()
        lines.extend(
            [
                f"## Candidate `{data['candidate_id']}`",
                "",
                f"- 商品名: {data['product_name']}",
                f"- JAN / ASIN / 型番: `{data['jan']}` / `{data['asin']}` / `{data['model_number']}`",
                f"- 仕入候補reference: `{data['source_url_or_reference']}`",
                f"- 販売候補reference: `{data['sales_url_or_reference']}`",
                f"- P7 review status: `{data['p7_review_status']}`",
                f"- Recommended action: `{data['recommended_action']}`",
                f"- P4 decision: `{data['p4_identity_result'].get('decision')}`",
                f"- P3 decision: `{data['p3_profit_result'].get('decision')}` / net `{data['p3_profit_result'].get('net_profit_yen')}` JPY / ROI `{data['p3_profit_result'].get('roi_percent')}`%",
                f"- P5 market data: `{data['p5_market_data_summary'].get('status')}` / observations `{data['p5_market_data_summary'].get('observation_count')}`",
                f"- P6 recommendation: `{data['p6_score'].get('decision')}` / total score `{data['p6_score'].get('total_score')}`",
                f"- 1SKU 5,000円上限OK: `{data['per_sku_limit_ok']}`",
                f"- 初期仕入れ枠への影響: `{data['initial_budget_impact_yen']}` JPY / 残り `{data['initial_budget_remaining_after_candidate_yen']}` JPY",
                f"- Human approval required: `{data['human_approval_required']}`",
                "- Manusに許可される作業:",
            ]
        )
        lines.extend(f"  - {item}" for item in data["allowed_actions"])
        lines.append("- 禁止操作:")
        lines.extend(f"  - {item}" for item in data["forbidden_actions"])
        lines.append("- 人間確認チェックリスト:")
        lines.extend(f"  - {item}" for item in data["human_check_items"])
        lines.append("")
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return len(packets)
