from __future__ import annotations

from pathlib import Path
import unittest

from keiji.candidate_scoring import CandidateScoreInput, CandidateScoreValue, CandidateScoringEngine
from keiji.market_monitoring import load_market_observations
from keiji.p3_profit import ProfitEngine, ProfitInput
from keiji.p4_identity import MarketListing, ProductIdentityEngine, SourceOffer

ROOT = Path(__file__).resolve().parents[3]


class CandidateScoringEngineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.p4 = ProductIdentityEngine.from_config_path(ROOT / "config/product_identity_rules.v1.yaml")
        cls.p3 = ProfitEngine.from_config_path(ROOT / "config/profit_rules.v1.yaml")
        cls.market = tuple(load_market_observations(ROOT / "tests/fixtures/market_observations.v1.json"))
        cls.engine = CandidateScoringEngine()

    def _input(self, *, sale_price: int = 7200, source: SourceOffer | None = None, listing: MarketListing | None = None, market=None) -> CandidateScoreInput:
        source = source or SourceOffer(id="src-score", title="SONY Wireless Headphones WH-1000XM4 Black", brand="SONY", model="WH-1000XM4", jan="4548736112100", condition="new", purchase_price_yen=3000)
        listing = listing or MarketListing(id="amz-score", marketplace="amazon_jp", title="ソニー ワイヤレスヘッドホン WH-1000XM4 ブラック", brand="ソニー", model="WH-1000XM4", jan="4548736112100", asin="B08F2B5Y9K", condition="new")
        identity = self.p4.evaluate(source, listing)
        profit = self.p3.evaluate(ProfitInput(id="p3-score", p4_decision=identity.decision.value, p4_confidence_score=identity.confidence_score, p4_requires_human_review=identity.requires_human_review, expected_sale_price_yen=sale_price, purchase_price_yen=source.purchase_price_yen, inbound_shipping_yen=source.domestic_shipping_yen, category="electronics"))
        return CandidateScoreInput(candidate_id="cand-score", source_offer=source, market_listing=listing, identity_decision=identity, profit_estimate=profit, market_observations=self.market if market is None else market)

    def test_scores_buy_candidate_when_identity_profit_and_market_are_safe(self) -> None:
        score = self.engine.score(self._input())
        self.assertEqual(CandidateScoreValue.BUY_CANDIDATE, score.decision)
        self.assertTrue(score.human_review_required)

    def test_ambiguous_identity_needs_human_review_not_buy(self) -> None:
        source = SourceOffer(id="src-amb", title="SONY Headphone Black", brand="SONY", jan="4548736112100", condition="new", purchase_price_yen=3000)
        listing = MarketListing(id="amz-amb", marketplace="amazon_jp", title="ソニー Headphone ホワイト", brand="ソニー", jan="4548736112100", condition="new")
        score = self.engine.score(self._input(source=source, listing=listing))
        self.assertEqual(CandidateScoreValue.NEEDS_HUMAN_REVIEW, score.decision)

    def test_profit_failure_is_watch_only(self) -> None:
        score = self.engine.score(self._input(sale_price=4300))
        self.assertEqual(CandidateScoreValue.WATCH_ONLY, score.decision)

    def test_per_sku_limit_blocks(self) -> None:
        source = SourceOffer(id="src-block", title="SONY Wireless Headphones WH-1000XM4 Black", brand="SONY", model="WH-1000XM4", jan="4548736112100", condition="new", purchase_price_yen=5001)
        score = self.engine.score(self._input(source=source))
        self.assertEqual(CandidateScoreValue.BLOCKED, score.decision)


if __name__ == "__main__":
    unittest.main()
