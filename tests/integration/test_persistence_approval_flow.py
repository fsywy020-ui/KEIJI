from __future__ import annotations

import json
from pathlib import Path
import unittest

from keiji.approval.workflow import ApprovalWorkflow
from keiji.common.config_loader import load_rule_config
from keiji.db.connection import connect, initialize_schema
from keiji.db.repositories.approval_repository import ApprovalRepository
from keiji.db.repositories.audit_repository import AuditRepository
from keiji.db.repositories.p3_repository import P3Repository
from keiji.db.repositories.p4_repository import P4Repository
from keiji.db.repositories.purchase_candidate_repository import PurchaseCandidateRepository
from keiji.p3_profit import ProfitEngine, ProfitInput
from keiji.p4_identity import MarketListing, ProductIdentityEngine, SourceOffer


ROOT = Path(__file__).resolve().parents[2]


class PersistenceApprovalFlowTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = connect()
        initialize_schema(self.connection)
        self.audit = AuditRepository(self.connection)
        self.p4_repo = P4Repository(self.connection)
        self.p3_repo = P3Repository(self.connection)
        self.candidates = PurchaseCandidateRepository(self.connection)
        self.approvals = ApprovalRepository(self.connection)
        self.workflow = ApprovalWorkflow(approvals=self.approvals, candidates=self.candidates, audit=self.audit)
        self.p4_rules = load_rule_config(ROOT / "config/product_identity_rules.v1.yaml")
        self.p3_rules = load_rule_config(ROOT / "config/profit_rules.v1.yaml")

    def tearDown(self) -> None:
        self.connection.close()

    def test_p4_p3_candidate_approval_audit_flow(self) -> None:
        p4_case = json.loads((ROOT / "tests/fixtures/p4/identity_cases.v1.json").read_text(encoding="utf-8"))[0]
        source = SourceOffer.from_dict(p4_case["source_offer"])
        listing = MarketListing.from_dict(p4_case["market_listing"])
        decision = ProductIdentityEngine(self.p4_rules).evaluate(source, listing)

        self.p4_repo.save_source_offer(source)
        self.p4_repo.save_market_listing(listing)
        p4_run_id = self.p4_repo.create_run(
            rules_version=self.p4_rules["version"],
            source_offer_id=source.id,
            market_listing_id=listing.id,
        )
        identity_decision_id = self.p4_repo.save_decision(
            p4_run_id=p4_run_id,
            source_offer_id=source.id,
            market_listing_id=listing.id,
            decision=decision,
        )
        self.audit.record(
            event_type="p4_decision",
            actor="system",
            target_type="identity",
            target_id=identity_decision_id,
            payload=decision.to_dict(),
        )

        profit_input = ProfitInput.from_dict(
            {
                "id": "integration-profit",
                "p4_decision": decision.decision.value,
                "p4_confidence_score": decision.confidence_score,
                "p4_requires_human_review": decision.requires_human_review,
                "expected_sale_price_yen": 6980,
                "purchase_price_yen": source.purchase_price_yen,
                "inbound_shipping_yen": source.domestic_shipping_yen,
                "category": "electronics",
                "allocated_budget_yen": 0,
            }
        )
        estimate = ProfitEngine(self.p3_rules).evaluate(profit_input)
        p3_run_id = self.p3_repo.create_run(
            rules_version=self.p3_rules["version"],
            identity_decision_id=identity_decision_id,
            status="completed",
        )
        estimate_id = self.p3_repo.save_estimate(
            p3_run_id=p3_run_id,
            identity_decision_id=identity_decision_id,
            profit_input=profit_input,
            estimate=estimate,
        )
        self.audit.record(
            event_type="p3_decision",
            actor="system",
            target_type="profit",
            target_id=estimate_id,
            payload={"decision": estimate.decision, "net_profit_yen": estimate.net_profit_yen},
        )

        candidate_id = self.candidates.create_from_estimate_if_allowed(profit_estimate_id=estimate_id)
        self.assertIsNotNone(candidate_id)
        assert candidate_id is not None
        candidate = self.candidates.get(candidate_id)
        self.assertEqual("pending_review", candidate["status"])
        self.assertFalse(self.candidates.is_executable(candidate_id))

        with self.assertRaises(ValueError):
            self.workflow.review_purchase_candidate(candidate_id=candidate_id, decision="approved", reviewer_name="")

        approval_id = self.workflow.review_purchase_candidate(
            candidate_id=candidate_id,
            decision="approved",
            reviewer_name="human-reviewer",
            comment="manual approval for test",
        )
        self.assertTrue(approval_id)
        self.assertTrue(self.candidates.is_executable(candidate_id))
        events = self.audit.list_events()
        self.assertEqual(3, len(events))
        self.assertEqual("human_approval", events[-1]["event_type"])


if __name__ == "__main__":
    unittest.main()
