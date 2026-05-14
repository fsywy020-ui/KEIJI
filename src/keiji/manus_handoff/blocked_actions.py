"""Local blocked-action audit contract for P8 Manus handoff safety.

This module is intentionally limited to recording that forbidden actions are
blocked. It never executes purchase, payment, listing, checkout, login, cart,
browser automation, scraping, or live external API behavior.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any
from uuid import uuid4

from keiji.audit.jsonl import append_audit_event, create_audit_event

FORBIDDEN_MANUS_ACTIONS: tuple[str, ...] = (
    "login",
    "cart",
    "checkout",
    "payment",
    "purchase",
    "listing",
    "browser_automation",
    "scraping",
    "live_external_api",
)


@dataclass(frozen=True)
class BlockedActionDecision:
    """Machine-readable decision proving a forbidden handoff action was blocked."""

    action: str
    allowed: bool
    decision: str
    reason_code: str
    explanation: str
    requested_by: str = "system"
    target_id: str | None = None
    audit_event_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "allowed": self.allowed,
            "decision": self.decision,
            "reason_code": self.reason_code,
            "explanation": self.explanation,
            "requested_by": self.requested_by,
            "target_id": self.target_id,
            "audit_event_id": self.audit_event_id,
        }


def record_blocked_action(
    *,
    action: str,
    requested_by: str = "system",
    target_id: str | None = None,
    audit_path: str | Path | None = None,
) -> BlockedActionDecision:
    """Return a blocked decision and optionally append its JSONL audit payload.

    The optional audit payload and returned decision always share the same
    ``audit_event_id``. This keeps the local JSONL audit record joinable to the
    caller-visible decision.
    """

    normalized_action = _normalize_action(action)
    if normalized_action not in FORBIDDEN_MANUS_ACTIONS:
        normalized_action = "unknown_forbidden_action"
    decision = BlockedActionDecision(
        action=normalized_action,
        allowed=False,
        decision="blocked",
        reason_code=f"p8_forbidden_action:{normalized_action}",
        explanation=(
            "P8 Manus handoff is limited to purchase-adjacent human assistance; "
            f"{normalized_action} is prohibited in the initial KEIJI MVP."
        ),
        requested_by=requested_by,
        target_id=target_id,
    )
    if audit_path is None:
        return decision

    audit_event_id = f"p8-blocked-action:{uuid4()}"
    audited_decision = replace(decision, audit_event_id=audit_event_id)
    payload = {
        **audited_decision.to_dict(),
        # Keep this assignment after the dict expansion so future to_dict changes
        # cannot overwrite the generated ID with None in the JSONL payload.
        "audit_event_id": audit_event_id,
    }
    event = create_audit_event(
        event_type="p8_blocked_action",
        actor=requested_by,
        target_type="manus_handoff_action",
        target_id=target_id or normalized_action,
        payload=payload,
    )
    append_audit_event(audit_path, event)
    return audited_decision


def _normalize_action(action: str) -> str:
    return action.strip().lower().replace("-", "_").replace(" ", "_")
