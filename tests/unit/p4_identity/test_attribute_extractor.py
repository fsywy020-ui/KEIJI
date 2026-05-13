from __future__ import annotations

import unittest
from pathlib import Path

from keiji.common.enums import IdentityDecisionValue
from keiji.common.config_loader import load_rule_config
from keiji.p4_identity import MarketListing, ProductIdentityEngine, SourceOffer
from keiji.p4_identity.attribute_extractor import extract_product_attributes


ROOT = Path(__file__).resolve().parents[3]


class AttributeExtractorTest(unittest.TestCase):
    def test_extracts_required_p4_attributes_from_title(self) -> None:
        attrs = extract_product_attributes("sony wh-1000xm4 black 256gb 2個セット 新品 jan 4548736112100")
        self.assertEqual(("4548736112100",), attrs.jan_candidates)
        self.assertIn("1000xm4", attrs.model_candidates)
        self.assertEqual("256gb", attrs.capacity)
        self.assertEqual("black", attrs.color)
        self.assertEqual(2, attrs.set_count)
        self.assertEqual("new", attrs.condition)

    def test_extracts_upc_candidate(self) -> None:
        attrs = extract_product_attributes("sample upc 012345678905")
        self.assertEqual(("012345678905",), attrs.jan_candidates)

    def test_title_extracted_jan_can_allow_same_identity_without_explicit_jan_field(self) -> None:
        rules = load_rule_config(ROOT / "config/product_identity_rules.v1.yaml")
        engine = ProductIdentityEngine(rules)
        decision = engine.evaluate(
            SourceOffer(
                id="src-title-jan",
                title="SONY WH-1000XM4 Black JAN 4548736112100",
                brand="SONY",
                condition="new",
                purchase_price_yen=3000,
            ),
            MarketListing(
                id="amz-title-jan",
                marketplace="amazon_jp",
                title="ソニー WH-1000XM4 ブラック 4548736112100",
                brand="ソニー",
                condition="new",
            ),
        )
        self.assertEqual(IdentityDecisionValue.SAME, decision.decision)
        self.assertFalse(decision.requires_human_review)
        self.assertIn("jan_match", [item.code for item in decision.evidence])

    def test_set_count_conflict_requires_human_review(self) -> None:
        rules = load_rule_config(ROOT / "config/product_identity_rules.v1.yaml")
        engine = ProductIdentityEngine(rules)
        decision = engine.evaluate(
            SourceOffer(
                id="src-set",
                title="Panasonic Filter ABC123 2個セット",
                brand="Panasonic",
                model="ABC123",
                condition="new",
                purchase_price_yen=1200,
            ),
            MarketListing(
                id="amz-set",
                marketplace="amazon_jp",
                title="パナソニック Filter ABC123 1個セット",
                brand="パナソニック",
                model="ABC123",
                condition="new",
            ),
        )
        self.assertEqual(IdentityDecisionValue.AMBIGUOUS, decision.decision)
        self.assertTrue(decision.requires_human_review)
        self.assertIn("variant_conflict", [item.code for item in decision.evidence])


if __name__ == "__main__":
    unittest.main()
