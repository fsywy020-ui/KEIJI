#!/usr/bin/env python3
"""Record a human review decision for a purchase candidate.

This script updates local review state only. It does not purchase, pay, open a
browser, or call external APIs.
"""

from __future__ import annotations

import argparse

from keiji.approval.workflow import ApprovalWorkflow
from keiji.db.connection import connect
from keiji.db.repositories.approval_repository import ApprovalRepository
from keiji.db.repositories.audit_repository import AuditRepository
from keiji.db.repositories.purchase_candidate_repository import PurchaseCandidateRepository


def main() -> int:
    parser = argparse.ArgumentParser(description="Record human review for a pending candidate")
    parser.add_argument("--db", default="storage/keiji.sqlite3")
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--decision", choices=["approved", "rejected", "needs_more_info"], required=True)
    parser.add_argument("--reviewer", required=True)
    parser.add_argument("--comment", default=None)
    args = parser.parse_args()

    connection = connect(args.db)
    workflow = ApprovalWorkflow(
        approvals=ApprovalRepository(connection),
        candidates=PurchaseCandidateRepository(connection),
        audit=AuditRepository(connection),
    )
    approval_id = workflow.review_purchase_candidate(
        candidate_id=args.candidate_id,
        decision=args.decision,
        reviewer_name=args.reviewer,
        comment=args.comment,
    )
    print(f"approval_id={approval_id} candidate_id={args.candidate_id} decision={args.decision}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
