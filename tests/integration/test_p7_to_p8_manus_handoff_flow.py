from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from keiji.candidate_scoring import CandidateScoreInput, CandidateScoringEngine
from keiji.io.local_candidates import load_candidates_csv
from keiji.manus_handoff import build_manus_handoff_packet, export_handoff_packets_json, export_handoff_packets_markdown
from keiji.market_monitoring import load_market_observations, matching_market_observations
from keiji.p3_profit import ProfitEngine, ProfitInput
from keiji.p4_identity import ProductIdentityEngine
from keiji.review import build_candidate_review_packet

ROOT = Path(__file__).resolve().parents[2]


class P7ToP8ManusHandoffFlowTest(unittest.TestCase):
    def test_p7_review_packet_exports_p8_handoff_without_secrets_or_execution(self) -> None:
        candidate = load_candidates_csv(ROOT / "data/samples/offline_candidates.example.csv")[0]
        p4 = ProductIdentityEngine.from_config_path(ROOT / "config/product_identity_rules.v1.yaml")
        p3 = ProfitEngine.from_config_path(ROOT / "config/profit_rules.v1.yaml")
        p6 = CandidateScoringEngine()
        market = tuple(load_market_observations(ROOT / "data/samples/market_observations.example.csv"))
        matching_market = matching_market_observations(
            market,
            jan=candidate.market_listing.jan,
            asin=candidate.market_listing.asin,
            model_number=candidate.market_listing.model,
        )
        identity = p4.evaluate(candidate.source_offer, candidate.market_listing)
        profit = p3.evaluate(
            ProfitInput(
                id="p8-profit",
                p4_decision=identity.decision.value,
                p4_confidence_score=identity.confidence_score,
                p4_requires_human_review=identity.requires_human_review,
                expected_sale_price_yen=candidate.expected_sale_price_yen,
                purchase_price_yen=candidate.source_offer.purchase_price_yen,
                inbound_shipping_yen=candidate.source_offer.domestic_shipping_yen,
                category=candidate.category,
                allocated_budget_yen=candidate.allocated_budget_yen,
            )
        )
        score = p6.score(
            CandidateScoreInput(
                candidate_id="candidate-p8-flow",
                source_offer=candidate.source_offer,
                market_listing=candidate.market_listing,
                identity_decision=identity,
                profit_estimate=profit,
                market_observations=matching_market,
                allocated_budget_yen=candidate.allocated_budget_yen,
            )
        )
        review_packet = build_candidate_review_packet(
            candidate_id="candidate-p8-flow",
            source_offer=candidate.source_offer,
            market_listing=candidate.market_listing,
            identity_decision=identity,
            profit_estimate=profit,
            market_observations=matching_market,
            candidate_score=score,
            allocated_budget_yen=candidate.allocated_budget_yen,
        )
        handoff_packet = build_manus_handoff_packet(review_packet)
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            export_handoff_packets_json([handoff_packet], tmp / "handoff.json")
            export_handoff_packets_markdown([handoff_packet], tmp / "handoff.md")
            payload_text = (tmp / "handoff.json").read_text(encoding="utf-8")
            payload = json.loads(payload_text)[0]
            markdown = (tmp / "handoff.md").read_text(encoding="utf-8")
        self.assertTrue(payload["human_approval_required"])
        self.assertTrue(payload["local_file_only"])
        self.assertTrue(payload["external_send_disabled"])
        self.assertTrue(payload["purchase_execution_disabled"])
        self.assertIn("purchase", payload["forbidden_actions"])
        self.assertIn("read_local_handoff_packets", payload["allowed_actions"])
        self.assertIn("not_purchase_permission", payload["recommended_action"])
        self.assertNotIn("password", payload_text.lower())
        self.assertNotIn("api_key", payload_text.lower())
        self.assertNotIn("token", payload_text.lower())
        self.assertIn("Human approval required", markdown)


if __name__ == "__main__":
    unittest.main()
