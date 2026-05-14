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
    lines = ["# P8 Manus Handoff Safety Contracts", ""]
    for packet in packets:
        data = packet.to_dict()
        lines.extend(
            [
                f"## {data['candidate_id']}",
                "",
                f"- Handoff ID: `{data['handoff_id']}`",
                f"- Purpose: `{data['purpose']}`",
                f"- Human approval required: `{data['safety_flags']['human_approval_required']}`",
                "- Forbidden actions:",
            ]
        )
        lines.extend(f"  - `{action}`" for action in data["forbidden_actions"])
        lines.append("- Required human approvals:")
        lines.extend(f"  - `{approval}`" for approval in data["required_human_approvals"])
        lines.append("- Human checklist:")
        lines.extend(f"  - {item}" for item in data["human_checklist"])
        lines.extend(["", data["human_readable_explanation"], ""])
    output_path.write_text("\n".join(lines), encoding="utf-8")
