"""Human approval workflow.

This module changes review state only. It only records review state and never performs external actions.
"""

from __future__ import annotations

from keiji.db.repositories.approval_repository import ApprovalRepository
from keiji.db.repositories.audit_repository import AuditRepository
from keiji.db.repositories.purchase_candidate_repository import PurchaseCandidateRepository


class ApprovalWorkflow:
    """Coordinate human approval records, candidate status, and audit logs."""

    def __init__(
        self,
        *,
        approvals: ApprovalRepository,
        candidates: PurchaseCandidateRepository,
        audit: AuditRepository,
    ) -> None:
        self.approvals = approvals
        self.candidates = candidates
        self.audit = audit

    def review_purchase_candidate(
        self,
        *,
        candidate_id: str,
        decision: str,
        reviewer_name: str,
        comment: str | None = None,
    ) -> str:
        approval_id = self.approvals.record(
            target_type="purchase",
            target_id=candidate_id,
            decision=decision,
            reviewer_name=reviewer_name,
            comment=comment,
        )
        status = {
            "approved": "approved",
            "rejected": "rejected",
            "needs_more_info": "pending_review",
        }[decision]
        self.candidates.update_status(candidate_id=candidate_id, status=status)
        self.audit.record(
            event_type="human_approval",
            actor=f"human:{reviewer_name.strip()}",
            target_type="purchase",
            target_id=candidate_id,
            payload={"approval_id": approval_id, "decision": decision, "comment": comment},
        )
        return approval_id
