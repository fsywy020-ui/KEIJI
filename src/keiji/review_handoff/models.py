"""P8 Codex review-assist handoff safety contract models.

These models describe local handoff artifacts only. They never execute purchase,
payment, listing, checkout, login, cart, browser automation, scraping, or live
external API actions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


FORBIDDEN_ACTIONS: tuple[str, ...] = (
    "login",
    "add_to_cart",
    "cart_operation",
    "checkout",
    "confirm_checkout",
    "place_order",
    "purchase_execution",
    "execute_payment",
    "payment",
    "listing_creation",
    "browser_automation",
    "scraping",
    "live_external_api",
)

ALLOWED_HANDOFF_TASKS: tuple[str, ...] = (
    "summarize_local_review_packet",
    "explain_human_checklist",
    "prepare_human_questions",
    "flag_missing_manual_evidence",
)

REQUIRED_HUMAN_APPROVALS: tuple[str, ...] = (
    "human_confirms_product_identity",
    "human_confirms_profit_assumptions",
    "human_confirms_budget_and_per_sku_limit",
    "human_records_purchase_approval",
    "human_executes_any_purchase_or_payment_outside_keiji",
)


@dataclass(frozen=True)
class ReviewHandoffPacket:
    """Local packet that defines exactly what Codex may and may not assist with."""

    handoff_id: str
    candidate_id: str
    purpose: str
    source_review_packet: dict[str, Any]
    allowed_tasks: tuple[str, ...] = ALLOWED_HANDOFF_TASKS
    forbidden_actions: tuple[str, ...] = FORBIDDEN_ACTIONS
    required_human_approvals: tuple[str, ...] = REQUIRED_HUMAN_APPROVALS
    human_checklist: tuple[str, ...] = field(default_factory=tuple)
    safety_flags: dict[str, bool] = field(default_factory=dict)
    machine_readable_reasons: tuple[str, ...] = field(default_factory=tuple)
    human_readable_explanation: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "handoff_id": self.handoff_id,
            "candidate_id": self.candidate_id,
            "purpose": self.purpose,
            "source_review_packet": self.source_review_packet,
            "allowed_tasks": list(self.allowed_tasks),
            "forbidden_actions": list(self.forbidden_actions),
            "required_human_approvals": list(self.required_human_approvals),
            "human_checklist": list(self.human_checklist),
            "safety_flags": self.safety_flags,
            "machine_readable_reasons": list(self.machine_readable_reasons),
            "human_readable_explanation": self.human_readable_explanation,
        }


@dataclass(frozen=True)
class BlockedActionDecision:
    """Decision record for a requested review-assist action."""

    requested_action: str
    target_id: str
    allowed: bool
    decision: str
    machine_readable_reasons: tuple[str, ...]
    human_readable_explanation: str
    requires_human_approval: bool = True
    audit_event_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "requested_action": self.requested_action,
            "target_id": self.target_id,
            "allowed": self.allowed,
            "decision": self.decision,
            "machine_readable_reasons": list(self.machine_readable_reasons),
            "human_readable_explanation": self.human_readable_explanation,
            "requires_human_approval": self.requires_human_approval,
            "audit_event_id": self.audit_event_id,
        }
