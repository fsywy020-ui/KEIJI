from __future__ import annotations

import json
from pathlib import Path
import unittest

from keiji.common.enums import IdentityDecisionValue
from keiji.p4_identity import MarketListing, ProductIdentityEngine, SourceOffer


ROOT = Path(__file__).resolve().parents[3]


class P4MinimalIdentityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = ProductIdentityEngine.from_config_path(ROOT / "config/product_identity_rules.v1.yaml")
        cls.cases = json.loads((ROOT / "tests/fixtures/p4/identity_cases.v1.json").read_text(encoding="utf-8"))

    def test_fixture_cases_match_expected_decisions(self) -> None:
        for case in self.cases:
            with self.subTest(case=case["id"]):
                source = SourceOffer.from_dict(case["source_offer"])
                listing = MarketListing.from_dict(case["market_listing"])
                decision = self.engine.evaluate(source, listing)
                self.assertEqual(IdentityDecisionValue(case["expected_decision"]), decision.decision)
                self.assertTrue(decision.evidence, "P4 decisions must include evidence")

    def test_same_case_does_not_require_human_review(self) -> None:
        case = self.cases[0]
        decision = self.engine.evaluate(
            SourceOffer.from_dict(case["source_offer"]),
            MarketListing.from_dict(case["market_listing"]),
        )
        self.assertEqual(IdentityDecisionValue.SAME, decision.decision)
        self.assertFalse(decision.requires_human_review)
        self.assertGreaterEqual(decision.confidence_score, 0.90)

    def test_ambiguous_case_requires_human_review(self) -> None:
        case = next(item for item in self.cases if item["id"] == "P4-201")
        decision = self.engine.evaluate(
            SourceOffer.from_dict(case["source_offer"]),
            MarketListing.from_dict(case["market_listing"]),
        )
        self.assertEqual(IdentityDecisionValue.AMBIGUOUS, decision.decision)
        self.assertTrue(decision.requires_human_review)

    def test_blocked_keyword_has_block_reason(self) -> None:
        case = next(item for item in self.cases if item["id"] == "P4-301")
        decision = self.engine.evaluate(
            SourceOffer.from_dict(case["source_offer"]),
            MarketListing.from_dict(case["market_listing"]),
        )
        self.assertEqual(IdentityDecisionValue.BLOCKED, decision.decision)
        self.assertEqual("blocked_keyword", decision.block_reason)


if __name__ == "__main__":
    unittest.main()
