from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from keiji.candidate_scoring import CandidateScoreInput, CandidateScoringEngine
from keiji.manus_handoff import (
    build_manus_handoff_packet,
    export_handoff_packets_csv,
    export_handoff_packets_json,
    export_handoff_packets_markdown,
)
from keiji.market_monitoring import load_market_observations
from keiji.p3_profit import ProfitEngine, ProfitInput
from keiji.p4_identity import MarketListing, ProductIdentityEngine, SourceOffer
from keiji.review import build_candidate_review_packet

ROOT = Path(__file__).resolve().parents[3]


class ManusHandoffPacketTest(unittest.TestCase):
    def test_builds_local_handoff_packet_without_purchase_permission(self) -> None:
        source = SourceOffer(
            id="src-manus-unit",
            title="SONY Wireless Headphones WH-1000XM4 Black",
            brand="SONY",
            model="WH-1000XM4",
            jan="4548736112100",
            condition="new",
            purchase_price_yen=3000,
        )
        listing = MarketListing(
            id="listing-manus-unit",
            marketplace="amazon_jp",
            title="ソニー ワイヤレスヘッドホン WH-1000XM4 ブラック",
            brand="ソニー",
            model="WH-1000XM4",
            jan="4548736112100",
            asin="B08F2B5Y9K",
            condition="new",
        )
        p4 = ProductIdentityEngine.from_config_path(ROOT / "config/product_identity_rules.v1.yaml")
        p3 = ProfitEngine.from_config_path(ROOT / "config/profit_rules.v1.yaml")
        identity = p4.evaluate(source, listing)
        profit = p3.evaluate(
            ProfitInput(
                id="profit-manus-unit",
                p4_decision=identity.decision.value,
                p4_confidence_score=identity.confidence_score,
                p4_requires_human_review=identity.requires_human_review,
                expected_sale_price_yen=7200,
                purchase_price_yen=source.purchase_price_yen,
                category="electronics",
            )
        )
        market = tuple(load_market_observations(ROOT / "tests/fixtures/market_observations.v1.json"))
        score = CandidateScoringEngine().score(
            CandidateScoreInput(
                candidate_id="candidate-manus-unit",
                source_offer=source,
                market_listing=listing,
                identity_decision=identity,
                profit_estimate=profit,
                market_observations=market,
            )
        )
        review_packet = build_candidate_review_packet(
            candidate_id="candidate-manus-unit",
            source_offer=source,
            market_listing=listing,
            identity_decision=identity,
            profit_estimate=profit,
            market_observations=market,
            candidate_score=score,
        )
        handoff_packet = build_manus_handoff_packet(review_packet)
        payload = handoff_packet.to_dict()
        self.assertTrue(payload["human_approval_required"])
        self.assertTrue(payload["external_send_disabled"])
        self.assertTrue(payload["purchase_execution_disabled"])
        self.assertEqual("human_review_candidate_only_not_purchase_permission", payload["recommended_action"])
        self.assertIn("purchase", payload["forbidden_actions"])
        self.assertIn("read_local_handoff_packets", payload["allowed_actions"])
        self.assertNotIn("password", json.dumps(payload).lower())
        self.assertNotIn("api_key", json.dumps(payload).lower())
        self.assertNotIn("token", json.dumps(payload).lower())

    def test_exports_json_csv_and_markdown_locally(self) -> None:
        review_packet = build_candidate_review_packet(
            candidate_id="candidate-export-unit",
            source_offer=SourceOffer(id="src-export", title="Export Test", purchase_price_yen=1000),
            market_listing=MarketListing(id="listing-export", marketplace="amazon_jp", title="Export Test"),
            identity_decision=ProductIdentityEngine.from_config_path(ROOT / "config/product_identity_rules.v1.yaml").evaluate(
                SourceOffer(id="src-export-p4", title="SONY Test Black", brand="SONY", jan="1", purchase_price_yen=1000),
                MarketListing(id="listing-export-p4", marketplace="amazon_jp", title="ソニー Test ブラック", brand="ソニー", jan="1"),
            ),
            profit_estimate=ProfitEngine.from_config_path(ROOT / "config/profit_rules.v1.yaml").evaluate(
                ProfitInput(id="profit-export", p4_decision="same", p4_confidence_score=1.0, p4_requires_human_review=False, expected_sale_price_yen=3000, purchase_price_yen=1000)
            ),
            market_observations=(),
            candidate_score=CandidateScoringEngine().score(
                CandidateScoreInput(
                    candidate_id="candidate-export-unit",
                    source_offer=SourceOffer(id="src-score-export", title="Export Test", purchase_price_yen=1000),
                    market_listing=MarketListing(id="listing-score-export", marketplace="amazon_jp", title="Export Test"),
                    identity_decision=ProductIdentityEngine.from_config_path(ROOT / "config/product_identity_rules.v1.yaml").evaluate(
                        SourceOffer(id="src-score-p4", title="SONY Test Black", brand="SONY", jan="1", purchase_price_yen=1000),
                        MarketListing(id="listing-score-p4", marketplace="amazon_jp", title="ソニー Test ブラック", brand="ソニー", jan="1"),
                    ),
                    profit_estimate=ProfitEngine.from_config_path(ROOT / "config/profit_rules.v1.yaml").evaluate(
                        ProfitInput(id="profit-score-export", p4_decision="same", p4_confidence_score=1.0, p4_requires_human_review=False, expected_sale_price_yen=3000, purchase_price_yen=1000)
                    ),
                )
            ),
        )
        handoff_packet = build_manus_handoff_packet(review_packet)
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            self.assertEqual(1, export_handoff_packets_json([handoff_packet], tmp / "handoff.json"))
            self.assertEqual(1, export_handoff_packets_csv([handoff_packet], tmp / "handoff.csv"))
            self.assertEqual(1, export_handoff_packets_markdown([handoff_packet], tmp / "handoff.md"))
            self.assertIn("purchase_execution_disabled", (tmp / "handoff.json").read_text(encoding="utf-8"))
            self.assertIn("Manusに許可される作業", (tmp / "handoff.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
