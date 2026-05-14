from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from keiji.candidate_scoring import CandidateScoreInput, CandidateScoringEngine
from keiji.market_monitoring import load_market_observations
from keiji.p3_profit import ProfitEngine, ProfitInput
from keiji.p4_identity import MarketListing, ProductIdentityEngine, SourceOffer
from keiji.review import build_candidate_review_packet, export_review_packets_csv, export_review_packets_json, export_review_packets_markdown

ROOT = Path(__file__).resolve().parents[3]


class CandidateReviewPacketTest(unittest.TestCase):
    def test_builds_and_exports_local_review_packet(self) -> None:
        p4 = ProductIdentityEngine.from_config_path(ROOT / "config/product_identity_rules.v1.yaml")
        p3 = ProfitEngine.from_config_path(ROOT / "config/profit_rules.v1.yaml")
        source = SourceOffer(id="src-review", title="SONY Wireless Headphones WH-1000XM4 Black", brand="SONY", model="WH-1000XM4", jan="4548736112100", condition="new", purchase_price_yen=3000)
        listing = MarketListing(id="amz-review", marketplace="amazon_jp", title="ソニー ワイヤレスヘッドホン WH-1000XM4 ブラック", brand="ソニー", model="WH-1000XM4", jan="4548736112100", asin="B08F2B5Y9K", condition="new")
        identity = p4.evaluate(source, listing)
        profit = p3.evaluate(ProfitInput(id="p3-review", p4_decision=identity.decision.value, p4_confidence_score=identity.confidence_score, p4_requires_human_review=identity.requires_human_review, expected_sale_price_yen=7200, purchase_price_yen=3000, category="electronics"))
        market = tuple(load_market_observations(ROOT / "tests/fixtures/market_observations.v1.json"))
        score = CandidateScoringEngine().score(CandidateScoreInput(candidate_id="cand-review", source_offer=source, market_listing=listing, identity_decision=identity, profit_estimate=profit, market_observations=market))
        packet = build_candidate_review_packet(candidate_id="cand-review", source_offer=source, market_listing=listing, identity_decision=identity, profit_estimate=profit, market_observations=market, candidate_score=score)
        self.assertEqual("cand-review", packet.candidate_id)
        self.assertTrue(packet.purchase_execution_disabled)
        self.assertIn("human_approval_not_recorded", packet.do_not_purchase_reasons)
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(1, export_review_packets_json([packet], Path(tmp) / "review.json"))
            self.assertEqual(1, export_review_packets_csv([packet], Path(tmp) / "review.csv"))
            self.assertEqual(1, export_review_packets_markdown([packet], Path(tmp) / "review.md"))
            self.assertIn("購入、決済", (Path(tmp) / "review.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
