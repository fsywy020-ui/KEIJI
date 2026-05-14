from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from keiji.candidate_scoring import CandidateScoreInput, CandidateScoreValue, CandidateScoringEngine
from keiji.market_monitoring import load_market_observations
from keiji.p3_profit import ProfitEngine, ProfitInput
from keiji.p4_identity import MarketListing, ProductIdentityEngine, SourceOffer
from keiji.review import build_candidate_review_packet, export_review_packets_markdown

ROOT = Path(__file__).resolve().parents[2]


class P4ToP7OfflineFlowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.p4 = ProductIdentityEngine.from_config_path(ROOT / "config/product_identity_rules.v1.yaml")
        cls.p3 = ProfitEngine.from_config_path(ROOT / "config/profit_rules.v1.yaml")
        cls.p6 = CandidateScoringEngine()
        cls.market = tuple(load_market_observations(ROOT / "tests/fixtures/market_observations.v1.json"))

    def _run(self, *, candidate_id: str, source: SourceOffer, listing: MarketListing, sale_price: int | None, market=None, allocated_budget_yen: int = 0):
        identity = self.p4.evaluate(source, listing)
        profit = self.p3.evaluate(ProfitInput(id=f"p3:{candidate_id}", p4_decision=identity.decision.value, p4_confidence_score=identity.confidence_score, p4_requires_human_review=identity.requires_human_review, expected_sale_price_yen=sale_price, purchase_price_yen=source.purchase_price_yen, inbound_shipping_yen=source.domestic_shipping_yen, category="electronics", allocated_budget_yen=allocated_budget_yen))
        observations = self.market if market is None else market
        score = self.p6.score(CandidateScoreInput(candidate_id=candidate_id, source_offer=source, market_listing=listing, identity_decision=identity, profit_estimate=profit, market_observations=observations, allocated_budget_yen=allocated_budget_yen))
        packet = build_candidate_review_packet(candidate_id=candidate_id, source_offer=source, market_listing=listing, identity_decision=identity, profit_estimate=profit, market_observations=observations, candidate_score=score, allocated_budget_yen=allocated_budget_yen)
        return identity, profit, score, packet

    def test_buy_watch_blocked_and_human_review_cases_generate_packets(self) -> None:
        base_source = SourceOffer(id="src-flow-buy", title="SONY Wireless Headphones WH-1000XM4 Black", brand="SONY", model="WH-1000XM4", jan="4548736112100", condition="new", purchase_price_yen=3000)
        base_listing = MarketListing(id="amz-flow-buy", marketplace="amazon_jp", title="ソニー ワイヤレスヘッドホン WH-1000XM4 ブラック", brand="ソニー", model="WH-1000XM4", jan="4548736112100", asin="B08F2B5Y9K", condition="new")
        _, _, buy_score, buy_packet = self._run(candidate_id="flow-buy", source=base_source, listing=base_listing, sale_price=7200)
        self.assertEqual(CandidateScoreValue.BUY_CANDIDATE, buy_score.decision)

        _, _, watch_score, _ = self._run(candidate_id="flow-watch", source=base_source, listing=base_listing, sale_price=4300)
        self.assertEqual(CandidateScoreValue.WATCH_ONLY, watch_score.decision)

        blocked_source = SourceOffer(id="src-flow-block", title="SONY Wireless Headphones WH-1000XM4 Black", brand="SONY", model="WH-1000XM4", jan="4548736112100", condition="new", purchase_price_yen=5001)
        _, _, blocked_score, _ = self._run(candidate_id="flow-block", source=blocked_source, listing=base_listing, sale_price=9000)
        self.assertEqual(CandidateScoreValue.BLOCKED, blocked_score.decision)

        review_listing = MarketListing(id="amz-flow-review", marketplace="amazon_jp", title="ソニー ワイヤレスヘッドホン WH-1000XM4 ホワイト", brand="ソニー", model="WH-1000XM4", jan="4548736112100", asin="B08F2B5Y9K", condition="new")
        _, _, review_score, _ = self._run(candidate_id="flow-review", source=base_source, listing=review_listing, sale_price=7200)
        self.assertEqual(CandidateScoreValue.NEEDS_HUMAN_REVIEW, review_score.decision)

        with tempfile.TemporaryDirectory() as tmp:
            export_review_packets_markdown([buy_packet], Path(tmp) / "p4-p7-review.md")
            report = (Path(tmp) / "p4-p7-review.md").read_text(encoding="utf-8")
            self.assertIn("live external API は実行しません", report)
            self.assertIn("購入してはいけない理由", report)


if __name__ == "__main__":
    unittest.main()
