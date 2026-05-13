from __future__ import annotations

from pathlib import Path
import unittest

from keiji.common.enums import IdentityDecisionValue
from keiji.common.config_loader import load_rule_config
from keiji.p4_identity import MarketListing, ProductIdentityEngine, SourceOffer
from keiji.p4_identity.condition_matcher import match_condition
from keiji.p4_identity.explain import explain_identity_decision
from keiji.p4_identity.normalizer import normalize_product_text
from keiji.p4_identity.title_matcher import match_titles, tokenize_title
from keiji.p4_identity.variant_matcher import extract_variants, match_variants


ROOT = Path(__file__).resolve().parents[3]


class VariantConditionTitleExplainTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rules = load_rule_config(ROOT / "config/product_identity_rules.v1.yaml")
        cls.engine = ProductIdentityEngine(cls.rules)

    def test_extracts_color_and_capacity_variants(self) -> None:
        variants = extract_variants("sony wh 1000xm4 black 256gb")
        self.assertEqual("black", variants["color"])
        self.assertEqual("256gb", variants["capacity"])

    def test_variant_conflict_for_color_forces_ambiguous(self) -> None:
        source = SourceOffer(
            id="src-variant",
            title="SONY WH-1000XM4 Black",
            brand="SONY",
            model="WH-1000XM4",
            jan="4548736112100",
            condition="new",
            purchase_price_yen=3000,
        )
        listing = MarketListing(
            id="amz-variant",
            marketplace="amazon_jp",
            title="ソニー WH-1000XM4 ホワイト",
            brand="ソニー",
            model="WH-1000XM4",
            jan="4548736112100",
            condition="new",
        )
        decision = self.engine.evaluate(source, listing)
        self.assertEqual(IdentityDecisionValue.AMBIGUOUS, decision.decision)
        self.assertTrue(decision.requires_human_review)
        self.assertIn("variant_conflict", [item.code for item in decision.evidence])

    def test_condition_policy_reads_blocked_pair_from_config(self) -> None:
        result = match_condition("used", "new", self.rules)
        self.assertEqual("blocked", result.status)
        self.assertEqual("condition_blocked", result.evidence_code)

    def test_condition_block_for_used_to_new_in_engine(self) -> None:
        decision = self.engine.evaluate(
            SourceOffer(
                id="src-condition",
                title="Nintendo Switch OLED White",
                brand="Nintendo",
                model="HEG-S-KAAAA",
                jan="4902370548495",
                condition="used",
                purchase_price_yen=4000,
            ),
            MarketListing(
                id="amz-condition",
                marketplace="amazon_jp",
                title="Nintendo Switch OLED White",
                brand="任天堂",
                model="HEG-S-KAAAA",
                jan="4902370548495",
                condition="new",
            ),
        )
        self.assertEqual(IdentityDecisionValue.BLOCKED, decision.decision)
        self.assertEqual("condition_blocked", decision.block_reason)

    def test_title_tokenizer_handles_mixed_alpha_numeric(self) -> None:
        tokens = tokenize_title("Sony WH-1000XM4 Black")
        self.assertIn("sony", tokens)
        self.assertIn("wh", tokens)
        self.assertIn("1000", tokens)
        self.assertIn("xm4", tokens)

    def test_title_match_reports_shared_tokens(self) -> None:
        result = match_titles("sony headphones black", "sony wireless headphones black")
        self.assertGreater(result.score, 0.5)
        self.assertIn("sony", result.shared_tokens)

    def test_explain_identity_decision_contains_evidence(self) -> None:
        source = normalize_product_text(title="SONY Black", brand="SONY", model="M1", jan="1", condition="new", rules=self.rules)
        listing = normalize_product_text(title="ソニー ブラック", brand="ソニー", model="M1", jan="1", condition="new", rules=self.rules)
        variant = match_variants(source, listing)
        self.assertIn(variant.status, {"match", "not_detected"})
        decision = self.engine.evaluate(
            SourceOffer(id="src-explain", title="SONY Black", brand="SONY", model="M1", jan="1", purchase_price_yen=1000),
            MarketListing(id="amz-explain", marketplace="amazon_jp", title="ソニー ブラック", brand="ソニー", model="M1", jan="1"),
        )
        explanation = explain_identity_decision(decision)
        self.assertIn("P4 decision:", explanation)
        self.assertIn("Evidence:", explanation)


if __name__ == "__main__":
    unittest.main()
