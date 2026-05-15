"""Local exports for P8 Manus handoff packets."""

from __future__ import annotations

import json
from pathlib import Path

from keiji.manus_handoff.models import ManusHandoffPacket


def export_manus_handoff_packets_json(packets: list[ManusHandoffPacket], path: str | Path) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps([packet.to_dict() for packet in packets], ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def export_manus_handoff_packets_markdown(packets: list[ManusHandoffPacket], path: str | Path) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# P8 Manus Handoff Safety Contracts",
        "",
        "> Local-only handoff packetです。Manusへ自動送信せず、人間が必要な範囲だけ手動で確認します。",
        "> `BUY_CANDIDATE` / `TEST_BUY_CANDIDATE` は購入許可ではありません。人間確認候補として扱ってください。",
        "> Manusに任せてよいのは要約、チェックリスト説明、質問案、手動証跡の不足指摘のみです。",
        "",
    ]
    for packet in packets:
        data = packet.to_dict()
        source = data.get("source_review_packet", {})
        p3 = source.get("p3_profit_result", {})
        shipping = p3.get("shipping", {})
        risk_details = p3.get("risk_details", [])
        lines.extend(
            [
                f"## {data['candidate_id']}",
                "",
                "### Handoff Scope",
                "",
                f"- Handoff ID: `{data['handoff_id']}`",
                f"- Purpose: `{data['purpose']}`",
                f"- Source recommendation: `{source.get('recommendation', '')}` — 購入許可ではありません。",
                f"- Human approval required: `{data['safety_flags']['human_approval_required']}`",
                f"- Purchase execution disabled: `{data['safety_flags'].get('purchase_execution_disabled')}`",
                f"- Payment execution disabled: `{data['safety_flags'].get('payment_execution_disabled')}`",
                f"- Browser automation disabled: `{data['safety_flags'].get('browser_automation_disabled')}`",
                f"- Live external API disabled: `{data['safety_flags'].get('live_external_api_disabled')}`",
                "",
                "### P3 Snapshot for Human Review",
                "",
                f"- Decision: `{p3.get('decision', '')}`",
                f"- Net profit: `{p3.get('net_profit_yen', '')}` JPY",
                f"- Risk-adjusted profit: `{p3.get('risk_adjusted_profit_yen', '')}` JPY",
                f"- ROI: `{p3.get('roi_percent', '')}`%",
                f"- Shipping: inbound `{shipping.get('inbound_shipping_yen', 0)}` JPY / packaging `{shipping.get('packaging_cost_yen', 0)}` JPY / fulfillment `{shipping.get('fulfillment_fee_yen', 0)}` JPY",
                "- Risk details / risk_details:",
            ]
        )
        if risk_details:
            lines.extend(
                f"  - `{detail['name']}` penalty `{detail['penalty_yen']}` JPY / severity `{detail['severity']}` — {detail['explanation']}"
                for detail in risk_details
            )
        else:
            lines.append("  - No named risk buffer details recorded.")
        lines.extend(["", "### Allowed Manus Tasks", ""])
        lines.extend(f"- `{task}`" for task in data["allowed_tasks"])
        lines.extend(["", "### Forbidden Actions", ""])
        lines.extend(f"- `{action}`" for action in data["forbidden_actions"])
        lines.extend(["", "### Required Human Approvals", ""])
        lines.extend(f"- `{approval}`" for approval in data["required_human_approvals"])
        lines.extend(["", "### Human Checklist", ""])
        lines.extend(f"- [ ] {item}" for item in data["human_checklist"])
        lines.extend(["", data["human_readable_explanation"], ""])
    output_path.write_text("\n".join(lines), encoding="utf-8")
