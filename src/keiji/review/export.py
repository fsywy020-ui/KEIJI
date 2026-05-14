"""Local P7 review packet exporters."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from keiji.review.packet import CandidateReviewPacket


def export_review_packets_json(packets: list[CandidateReviewPacket], path: str | Path) -> int:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps([packet.to_dict() for packet in packets], ensure_ascii=False, indent=2), encoding="utf-8")
    return len(packets)


def export_review_packets_csv(packets: list[CandidateReviewPacket], path: str | Path) -> int:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "candidate_id",
        "product_name",
        "jan",
        "asin",
        "model_number",
        "recommendation",
        "initial_budget_impact_yen",
        "initial_budget_remaining_after_candidate_yen",
        "per_sku_limit_ok",
        "do_not_purchase_reasons",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for packet in packets:
            row = packet.to_dict()
            row["do_not_purchase_reasons"] = ";".join(row["do_not_purchase_reasons"])
            writer.writerow({field: row[field] for field in fields})
    return len(packets)


def export_review_packets_markdown(packets: list[CandidateReviewPacket], path: str | Path) -> int:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# KEIJI P7 Human Approval Review Packets",
        "",
        "> 確認専用レポートです。購入、決済、出品、checkout、login、cart操作、browser automation、scraping、live external API は実行しません。",
        "",
    ]
    for packet in packets:
        data = packet.to_dict()
        lines.extend([
            f"## Candidate `{data['candidate_id']}`",
            "",
            f"- 商品名: {data['product_name']}",
            f"- JAN/ASIN/型番: `{data['jan']}` / `{data['asin']}` / `{data['model_number']}`",
            f"- 推奨判断: `{data['recommendation']}`",
            f"- P4: `{data['p4_identity_result']['decision']}` confidence `{data['p4_identity_result']['confidence_score']}`",
            f"- P3: `{data['p3_profit_result']['decision']}` net `{data['p3_profit_result']['net_profit_yen']}` JPY ROI `{data['p3_profit_result']['roi_percent']}`%",
            f"- P6 total score: `{data['p6_score']['total_score']}`",
            f"- 初期仕入れ枠への影響: `{data['initial_budget_impact_yen']}` JPY / 残り `{data['initial_budget_remaining_after_candidate_yen']}` JPY",
            f"- 1SKU上限OK: `{data['per_sku_limit_ok']}`",
            "- 購入してはいけない理由: " + ", ".join(data["do_not_purchase_reasons"]),
            "- 人間確認項目:",
        ])
        lines.extend(f"  - {item}" for item in data["human_check_items"])
        lines.append("")
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return len(packets)
