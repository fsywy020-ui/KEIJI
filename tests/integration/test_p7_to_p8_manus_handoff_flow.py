import json
import tempfile
import unittest
from pathlib import Path

from keiji.candidate_scoring import CandidateScoreInput, CandidateScoringEngine
from keiji.io.local_candidates import load_candidates_csv
from keiji.manus_handoff import build_manus_handoff_packet, evaluate_manus_action, export_manus_handoff_packets_json
from keiji.p3_profit import ProfitEngine, ProfitInput
from keiji.p4_identity import ProductIdentityEngine
from keiji.review import build_candidate_review_packet


class P7ToP8ManusHandoffFlowTest(unittest.TestCase):
    def test_p7_review_packet_can_be_wrapped_as_p8_handoff_contract(self):
        candidate = tuple(load_candidates_csv("data/samples/offline_candidates.example.csv"))[0]
        p4_engine = ProductIdentityEngine.from_config_path("config/product_identity_rules.v1.yaml")
        identity = p4_engine.evaluate(candidate.source_offer, candidate.market_listing)
        profit = ProfitEngine.from_config_path("config/profit_rules.v1.yaml").evaluate(
            ProfitInput(
                id="integration-profit-1",
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
        score = CandidateScoringEngine().score(
            CandidateScoreInput(
                candidate_id="integration-candidate-1",
                source_offer=candidate.source_offer,
                market_listing=candidate.market_listing,
                identity_decision=identity,
                profit_estimate=profit,
                market_observations=(),
                allocated_budget_yen=candidate.allocated_budget_yen,
            )
        )
        review_packet = build_candidate_review_packet(
            candidate_id="integration-candidate-1",
            source_offer=candidate.source_offer,
            market_listing=candidate.market_listing,
            identity_decision=identity,
            profit_estimate=profit,
            market_observations=(),
            candidate_score=score,
            allocated_budget_yen=candidate.allocated_budget_yen,
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            handoff = build_manus_handoff_packet(review_packet)
            output_path = tmp_path / "p8_manus_handoff_packets.json"
            export_manus_handoff_packets_json([handoff], output_path)
            blocked = evaluate_manus_action(
                requested_action="place_order",
                target_id=handoff.candidate_id,
                audit_path=tmp_path / "audit.jsonl",
            )

            exported = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(exported[0]["candidate_id"], "integration-candidate-1")
            self.assertEqual(exported[0]["source_review_packet"]["candidate_id"], "integration-candidate-1")
            self.assertTrue(exported[0]["safety_flags"]["live_external_api_disabled"])
            self.assertFalse(blocked.allowed)
            self.assertIn("forbidden_action:place_order", blocked.machine_readable_reasons)
