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
        "> 確認専用レポートです。`BUY_CANDIDATE` や `TEST_BUY_CANDIDATE` でも購入許可ではなく、人間が確認する候補です。",
        "> 購入、決済、出品、checkout、login、cart操作、browser automation、scraping、external agent API、live external API は実行しません。外部通知送信も実行しません。",
        "> P3利益計算は運用上の概算です。税務・会計助言として扱わず、必ず人間が根拠を確認してください。",
        "",
        "## Recommendation Legend",
        "",
        "- `BUY_CANDIDATE`: 条件が比較的よい人間確認候補。購入許可ではありません。",
        "- `TEST_BUY_CANDIDATE`: 小さく試す余地のある人間確認候補。購入許可ではありません。",
        "- `WATCH_ONLY`: 今は監視のみ。購入しません。",
        "- `BLOCKED`: 制約違反または安全上の理由で止めます。",
        "- `NEEDS_HUMAN_REVIEW`: 商品同定・利益前提・市場情報などを人間が追加確認します。",
        "",
    ]
    for packet in packets:
        data = packet.to_dict()
        p4 = data["p4_identity_result"]
        p3 = data["p3_profit_result"]
        shipping = p3.get("shipping", {})
        risk_details = p3.get("risk_details", [])
        lines.extend([
            f"## Candidate `{data['candidate_id']}`",
            "",
            "### Owner Action Required",
            "",
            f"- Recommendation: `{data['recommendation']}` — 人間確認候補であり、購入許可ではありません。",
            f"- Human approval required: `{_required_label(p3['requires_human_approval'])}`",
            f"- Purchase execution disabled: `{_disabled_label(data['purchase_execution_disabled'])}`",
            f"- External send disabled: `{_disabled_label(data['external_send_disabled'])}`",
            "",
            "### Product / P4 Identity Summary",
            "",
            f"- 商品名: {data['product_name']}",
            f"- JAN / ASIN / 型番: `{data['jan']}` / `{data['asin']}` / `{data['model_number']}`",
            f"- P4 decision: `{p4['decision']}`",
            f"- P4 confidence: `{p4['confidence_score']}`",
            f"- P4 additional identity review: `{_p4_review_label(p4['requires_human_review'])}`",
            f"- P4 block reason: `{p4.get('block_reason') or '(none)'}`",
            "- Owner確認ポイント: JAN、ASIN、型番、ブランド、タイトル、状態、容量、色、セット数、edition、国内正規品/並行輸入品、付属品差。",
            "",
            "### P3 Profit Summary (Operational Estimate Only)",
            "",
            f"- P3 decision: `{p3['decision']}`",
            f"- Net profit: `{p3['net_profit_yen']}` JPY",
            f"- Risk-adjusted profit: `{p3['risk_adjusted_profit_yen']}` JPY",
            f"- ROI: `{p3['roi_percent']}`%",
            f"- Profit margin: `{p3['profit_margin_percent']}`%",
            f"- Break-even price: `{p3['break_even_price_yen']}` JPY",
            f"- P3 reasons: {', '.join(p3['reasons']) if p3['reasons'] else '(none)'}",
            "",
            "### Shipping / Fulfillment Assumptions",
            "",
            f"- Inbound shipping: `{shipping.get('inbound_shipping_yen', 0)}` JPY",
            f"- Packaging cost: `{shipping.get('packaging_cost_yen', 0)}` JPY",
            f"- Fulfillment fee: `{shipping.get('fulfillment_fee_yen', 0)}` JPY",
            "- Assumptions:",
        ])
        assumptions = shipping.get("assumptions") or ["(none recorded)"]
        lines.extend(f"  - {assumption}" for assumption in assumptions)
        lines.extend([
            "",
            "### Risk Details / risk_details",
            "",
        ])
        if risk_details:
            for detail in risk_details:
                lines.append(
                    f"- `{detail['name']}`: penalty `{detail['penalty_yen']}` JPY / severity `{detail['severity']}` — {detail['explanation']}"
                )
        else:
            lines.extend(
                [
                    "- 設定上の追加リスク控除はありません。",
                    "- ただし「リスクなし」という意味ではありません。価格変動、返品、状態差、出品者数などはownerが手動確認してください。",
                ]
            )
        lines.extend([
            "",
            "### P6 Score / Budget",
            "",
            f"- P6 total score: `{data['p6_score']['total_score']}`",
            f"- 初期仕入れ枠への影響: `{data['initial_budget_impact_yen']}` JPY",
            f"- 候補後の初期仕入れ枠残額: `{data['initial_budget_remaining_after_candidate_yen']}` JPY",
            f"- 1SKU 5,000 JPY上限: `{_ok_label(data['per_sku_limit_ok'])}`",
            "",
            "### Do Not Purchase Reasons / 購入してはいけない理由",
            "",
        ])
        lines.extend(f"- `{reason}`" for reason in data["do_not_purchase_reasons"])
        lines.extend([
            "",
            "### Human Approval Checklist",
            "",
        ])
        lines.extend(f"- [ ] {item}" for item in _dedupe(data["human_check_items"]))
        lines.extend([
            "- [ ] このレポートから購入・決済・出品・login・cart・checkout・browser automation・scraping・external agent API・live external API・外部通知送信を行っていない。",
            "",
        ])
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return len(packets)


def _required_label(value: bool) -> str:
    return "必須（購入許可ではありません）" if value else "不要"


def _disabled_label(value: bool) -> str:
    return "無効（このレポートから実行不可）" if value else "有効（要確認）"


def _p4_review_label(value: bool) -> str:
    return "必要" if value else "システム上は不要。ただしowner目視確認は必須"


def _ok_label(value: bool) -> str:
    return "OK" if value else "NG（購入しない）"


def _dedupe(items: list[str]) -> list[str]:
    return list(dict.fromkeys(items))
