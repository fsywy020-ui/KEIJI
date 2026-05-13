from __future__ import annotations

from pathlib import Path
import unittest

from keiji.common.config_loader import load_rule_config
from keiji.common.enums import IdentityDecisionValue
from keiji.p4_identity import MarketListing, ProductIdentityEngine, SourceOffer
from keiji.p4_identity.attribute_extractor import extract_product_attributes
from keiji.p4_identity.scorer import calculate_identity_match_score
from keiji.p4_identity.variant_matcher import extract_variants


ROOT = Path(__file__).resolve().parents[3]


class AttributeExtractorAndScoringTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rules = load_rule_config(ROOT / "config/product_identity_rules.v1.yaml")
        cls.engine = ProductIdentityEngine(cls.rules)

    def test_extracts_identifier_variant_set_count_and_condition_from_title(self) -> None:
        attributes = extract_product_attributes(
            title="SONY WH-1000XM4 ブラック JAN 4548736112100 2個セット 新品",
            rules=self.rules,
        )
        self.assertEqual("4548736112100", attributes.jan)
        self.assertEqual("wh1000xm4", attributes.model)
        self.assertEqual("black", attributes.color)
        self.assertEqual(2, attributes.set_count)
        self.assertEqual("new", attributes.condition)

    def test_variant_extraction_includes_set_count(self) -> None:
        variants = extract_variants("Nintendo Switch ソフト 3本セット")
        self.assertEqual("3", variants["quantity"])

    def test_scoring_uses_configured_weights(self) -> None:
        score = calculate_identity_match_score(
            identifier_score=1.0,
            brand_score=1.0,
            title_score=0.5,
            variant_score=1.0,
            condition_score=1.0,
            rules={"scoring": {"weights": {"identifier": 1, "brand": 1, "title": 2, "variant": 1, "condition": 1}}},
        )
        self.assertEqual(0.8333, score)

    def test_engine_uses_title_extracted_jan_when_structured_jan_is_missing(self) -> None:
        decision = self.engine.evaluate(
            SourceOffer(
                id="src-title-jan",
                title="SONY WH-1000XM4 ブラック 4548736112100",
                brand="SONY",
                condition="new",
                purchase_price_yen=3000,
            ),
            MarketListing(
                id="amz-title-jan",
                marketplace="amazon_jp",
                title="ソニー WH-1000XM4 ブラック",
                brand="ソニー",
                jan="4548736112100",
                condition="new",
            ),
        )
        self.assertEqual(IdentityDecisionValue.SAME, decision.decision)
        self.assertFalse(decision.requires_human_review)

    def test_engine_blocks_used_title_even_if_default_condition_is_new(self) -> None:
        decision = self.engine.evaluate(
            SourceOffer(
                id="src-used-title",
                title="中古 Nintendo Switch OLED HEG-S-KAAAA ホワイト 4902370548495",
                brand="Nintendo",
                purchase_price_yen=4000,
            ),
            MarketListing(
                id="amz-new-listing",
                marketplace="amazon_jp",
                title="Nintendo Switch OLED HEG-S-KAAAA ホワイト",
                brand="任天堂",
                jan="4902370548495",
                condition="new",
            ),
        )
        self.assertEqual(IdentityDecisionValue.BLOCKED, decision.decision)
        self.assertEqual("condition_blocked", decision.block_reason)


if __name__ == "__main__":
    unittest.main()
