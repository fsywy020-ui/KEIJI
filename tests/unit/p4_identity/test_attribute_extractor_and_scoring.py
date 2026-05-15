from __future__ import annotations

from pathlib import Path
import unittest

from keiji.common.config_loader import load_rule_config
from keiji.common.enums import IdentityDecisionValue
from keiji.p4_identity import MarketListing, ProductIdentityEngine, SourceOffer
from keiji.p4_identity.attribute_extractor import extract_product_attributes
from keiji.p4_identity.brand_matcher import match_brands
from keiji.p4_identity.scoring import calculate_match_score
from keiji.p4_identity.variant_matcher import extract_variants


ROOT = Path(__file__).resolve().parents[3]


class AttributeExtractorAndScoringTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rules = load_rule_config(ROOT / "config/product_identity_rules.v1.yaml")
        cls.engine = ProductIdentityEngine(cls.rules)

    def test_extracts_jan_model_capacity_color_set_count_and_condition(self) -> None:
        attrs = extract_product_attributes(
            "新品 SONY WH-1000XM4 ブラック 128GB 2個セット JAN:4548736112100 ASIN B08F2B5Y9K"
        )
        self.assertEqual("4548736112100", attrs.jan)
        self.assertEqual("b08f2b5y9k", attrs.asin)
        self.assertEqual("wh1000xm4", attrs.model)
        self.assertEqual("128gb", attrs.capacity)
        self.assertEqual("black", attrs.color)
        self.assertEqual(2, attrs.set_count)
        self.assertEqual("new", attrs.condition)

    def test_variant_extraction_uses_set_count_key(self) -> None:
        variants = extract_variants("ホワイト 3個入 通常版 国内正規")
        self.assertEqual("white", variants["color"])
        self.assertEqual("3", variants["set_count"])
        self.assertEqual("standard", variants["edition"])
        self.assertEqual("domestic", variants["domestic_or_import"])

    def test_extracts_edge_case_variant_notation(self) -> None:
        attrs = extract_product_attributes("日本正規品 ネイビー 2箱セット サイズ フリー 0.5 L")
        self.assertEqual("domestic", attrs.domestic_or_import)
        self.assertEqual("navy", attrs.color)
        self.assertEqual(2, attrs.set_count)
        self.assertEqual("free", attrs.size)
        self.assertEqual("500ml", attrs.capacity)

    def test_normalizes_storage_capacity_units(self) -> None:
        attrs = extract_product_attributes("Portable SSD 1 TB")
        self.assertEqual("1000gb", attrs.capacity)

    def test_missing_explicit_jan_and_model_can_be_extracted_for_same_decision(self) -> None:
        decision = self.engine.evaluate(
            SourceOffer(
                id="src-extracted-id",
                title="新品 SONY WH-1000XM4 ブラック JAN 4548736112100",
                brand="SONY",
                condition="new",
                purchase_price_yen=3000,
            ),
            MarketListing(
                id="amz-extracted-id",
                marketplace="amazon_jp",
                title="ソニー WH-1000XM4 ブラック JAN:4548736112100",
                brand="ソニー",
                condition="new",
            ),
        )
        self.assertEqual(IdentityDecisionValue.SAME, decision.decision)
        self.assertGreaterEqual(decision.scores.identifier_score, 1.0)

    def test_brand_conflict_forces_human_review_even_when_identifier_matches(self) -> None:
        decision = self.engine.evaluate(
            SourceOffer(
                id="src-brand-conflict",
                title="SONY WH-1000XM4 Black",
                brand="SONY",
                model="WH-1000XM4",
                jan="4548736112100",
                condition="new",
                purchase_price_yen=3000,
            ),
            MarketListing(
                id="amz-brand-conflict",
                marketplace="amazon_jp",
                title="Generic WH-1000XM4 Black",
                brand="Generic",
                model="WH-1000XM4",
                jan="4548736112100",
                condition="new",
            ),
        )
        self.assertEqual(IdentityDecisionValue.AMBIGUOUS, decision.decision)
        self.assertTrue(decision.requires_human_review)
        self.assertIn("brand_conflict", [item.code for item in decision.evidence])

    def test_brand_matcher_and_configured_score_weights(self) -> None:
        self.assertEqual("match", match_brands("sony", "sony").status)
        self.assertEqual("conflict", match_brands("sony", "generic").status)
        score = calculate_match_score(
            identifier_score=1.0,
            brand_score=1.0,
            title_score=0.5,
            variant_score=1.0,
            condition_score=1.0,
            rules=self.rules,
        )
        self.assertEqual(0.9, score)


if __name__ == "__main__":
    unittest.main()
