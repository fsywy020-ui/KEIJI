"""Blocked-action guard for P8 Manus handoff requests."""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from keiji.audit.jsonl import append_audit_event, create_audit_event
from keiji.manus_handoff.models import ALLOWED_HANDOFF_TASKS, FORBIDDEN_ACTIONS, BlockedActionDecision


def evaluate_manus_action(
    *,
    requested_action: str,
    target_id: str,
    actor: str = "manus",
    audit_path: str | Path | None = None,
) -> BlockedActionDecision:
    """Evaluate and optionally audit a requested Manus action.

    Only narrow local review-assistance tasks are allowed. Unknown actions are
    blocked by default so the initial MVP cannot drift into external execution.
    """

    normalized = _normalize(requested_action)
    matched_forbidden = tuple(action for action in FORBIDDEN_ACTIONS if action in normalized)
    if matched_forbidden:
        decision = BlockedActionDecision(
            requested_action=requested_action,
            target_id=target_id,
            allowed=False,
            decision="blocked",
            machine_readable_reasons=tuple(f"forbidden_action:{action}" for action in matched_forbidden),
            human_readable_explanation=(
                f"Blocked Manus action '{requested_action}' for {target_id}. "
                "The initial MVP never allows Manus to perform purchase, payment, listing, checkout, login, cart, browser automation, scraping, or live API actions."
            ),
        )
        return _with_audit(decision, actor=actor, audit_path=audit_path)

    if normalized not in ALLOWED_HANDOFF_TASKS:
        decision = BlockedActionDecision(
            requested_action=requested_action,
            target_id=target_id,
            allowed=False,
            decision="blocked",
            machine_readable_reasons=("not_in_p8_allowed_task_allowlist",),
            human_readable_explanation=(
                f"Blocked Manus action '{requested_action}' for {target_id} because it is not in the P8 local handoff allowlist."
            ),
        )
        return _with_audit(decision, actor=actor, audit_path=audit_path)

    decision = BlockedActionDecision(
        requested_action=requested_action,
        target_id=target_id,
        allowed=True,
        decision="pass",
        machine_readable_reasons=("p8_local_review_assistance_only",),
        human_readable_explanation=(
            f"Allowed Manus action '{requested_action}' for {target_id} as local review assistance only. Human approval remains required."
        ),
    )
    return _with_audit(decision, actor=actor, audit_path=audit_path)


def _with_audit(decision: BlockedActionDecision, *, actor: str, audit_path: str | Path | None) -> BlockedActionDecision:
    if audit_path is None:
        return decision
    audit_event_id = f"p8-audit:{uuid4()}"
    audited_decision = BlockedActionDecision(
        requested_action=decision.requested_action,
        target_id=decision.target_id,
        allowed=decision.allowed,
        decision=decision.decision,
        machine_readable_reasons=decision.machine_readable_reasons,
        human_readable_explanation=decision.human_readable_explanation,
        requires_human_approval=decision.requires_human_approval,
        audit_event_id=audit_event_id,
    )
    append_audit_event(
        audit_path,
        create_audit_event(
            event_type="manus_action_evaluated" if decision.allowed else "blocked_action",
            actor=actor,
            target_type="manus_handoff",
            target_id=decision.target_id,
            payload=audited_decision.to_dict(),
        ),
    )
    return audited_decision


def _normalize(value: str) -> str:
    return value.strip().lower().replace(" ", "_").replace("-", "_")
