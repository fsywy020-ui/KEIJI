import json
import tempfile
import unittest
from pathlib import Path

from keiji.candidate_scoring import CandidateScoreInput, CandidateScoringEngine
from keiji.io.local_candidates import load_candidates_csv
from keiji.review_handoff import build_review_handoff_packet, evaluate_review_assist_action, export_review_handoff_packets_json, export_review_handoff_packets_markdown
from keiji.p3_profit import ProfitEngine, ProfitInput
from keiji.p4_identity import ProductIdentityEngine
from keiji.review import build_candidate_review_packet


class P7ToP8ReviewHandoffFlowTest(unittest.TestCase):
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
            handoff = build_review_handoff_packet(review_packet)
            output_path = tmp_path / "p8_review_handoff_packets.json"
            markdown_path = tmp_path / "p8_review_handoff_packets.md"
            export_review_handoff_packets_json([handoff], output_path)
            export_review_handoff_packets_markdown([handoff], markdown_path)
            blocked = evaluate_review_assist_action(
                requested_action="place_order",
                target_id=handoff.candidate_id,
                audit_path=tmp_path / "audit.jsonl",
            )

            exported = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(exported[0]["candidate_id"], "integration-candidate-1")
            self.assertEqual(exported[0]["source_review_packet"]["candidate_id"], "integration-candidate-1")
            self.assertTrue(exported[0]["safety_flags"]["live_external_api_disabled"])
            markdown = markdown_path.read_text(encoding="utf-8")
            self.assertIn("購入許可ではありません", markdown)
            self.assertIn("P3 Snapshot for Human Review", markdown)
            self.assertIn("Risk details", markdown)
            self.assertIn("KEIJI外の別判断として承認記録が必要", markdown)
            self.assertIn("CodexやKEIJIは実行しません", markdown)
            self.assertFalse(blocked.allowed)
            self.assertIn("forbidden_action:place_order", blocked.machine_readable_reasons)
