"""Models for local P8 Manus handoff packets."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from keiji.manus_handoff.policy import (
    ALLOWED_ACTIONS,
    FORBIDDEN_ACTIONS,
    FORBIDDEN_PACKET_FIELD_LABELS,
    HUMAN_APPROVAL_REQUIRED_ACTIONS,
)


@dataclass(frozen=True)
class ManusHandoffPacket:
    """Local packet prepared for human-controlled Manus handoff.

    This packet is a local review artifact only. It contains no credentials,
    payment details, cookies, sessions, or executable purchase instructions.
    """

    candidate_id: str
    product_name: str
    jan: str | None
    asin: str | None
    model_number: str | None
    source_url_or_reference: str
    sales_url_or_reference: str
    p4_identity_result: dict[str, Any]
    p3_profit_result: dict[str, Any]
    p5_market_data_summary: dict[str, Any]
    p6_score: dict[str, Any]
    p7_review_status: str
    recommended_action: str
    human_check_items: tuple[str, ...]
    per_sku_limit_ok: bool
    initial_budget_impact_yen: int
    initial_budget_remaining_after_candidate_yen: int
    forbidden_actions: tuple[str, ...] = field(default_factory=lambda: FORBIDDEN_ACTIONS)
    allowed_actions: tuple[str, ...] = field(default_factory=lambda: ALLOWED_ACTIONS)
    human_approval_required_actions: tuple[str, ...] = field(default_factory=lambda: HUMAN_APPROVAL_REQUIRED_ACTIONS)
    forbidden_packet_field_labels: tuple[str, ...] = field(default_factory=lambda: FORBIDDEN_PACKET_FIELD_LABELS)
    human_approval_required: bool = True
    local_file_only: bool = True
    external_send_disabled: bool = True
    purchase_execution_disabled: bool = True

    def to_dict(self) -> dict[str, Any]:
        """Serialize the packet without any executable external-operation data."""

        return {
            "candidate_id": self.candidate_id,
            "product_name": self.product_name,
            "jan": self.jan,
            "asin": self.asin,
            "model_number": self.model_number,
            "source_url_or_reference": self.source_url_or_reference,
            "sales_url_or_reference": self.sales_url_or_reference,
            "p4_identity_result": self.p4_identity_result,
            "p3_profit_result": self.p3_profit_result,
            "p5_market_data_summary": self.p5_market_data_summary,
            "p6_score": self.p6_score,
            "p7_review_status": self.p7_review_status,
            "recommended_action": self.recommended_action,
            "human_check_items": list(self.human_check_items),
            "per_sku_limit_ok": self.per_sku_limit_ok,
            "initial_budget_impact_yen": self.initial_budget_impact_yen,
            "initial_budget_remaining_after_candidate_yen": self.initial_budget_remaining_after_candidate_yen,
            "forbidden_actions": list(self.forbidden_actions),
            "allowed_actions": list(self.allowed_actions),
            "human_approval_required_actions": list(self.human_approval_required_actions),
            "forbidden_packet_field_labels": list(self.forbidden_packet_field_labels),
            "human_approval_required": self.human_approval_required,
            "local_file_only": self.local_file_only,
            "external_send_disabled": self.external_send_disabled,
            "purchase_execution_disabled": self.purchase_execution_disabled,
        }
