import unittest

from keiji.candidate_scoring import CandidateScore, CandidateScoreValue
from keiji.common.enums import IdentityDecisionValue
from keiji.manus_handoff import FORBIDDEN_ACTIONS, build_manus_handoff_packet
from keiji.p3_profit.input_models import FeeBreakdown, ProfitEstimate
from keiji.p4_identity.input_models import IdentityDecision, IdentityScores, MarketListing, SourceOffer
from keiji.review import build_candidate_review_packet


def _review_packet():
    source = SourceOffer(
        id="source-1",
        title="Safe Local Test Item",
        brand="Example",
        model="EX-1",
        jan="4900000000000",
        condition="new",
        purchase_price_yen=3000,
        domestic_shipping_yen=500,
    )
    listing = MarketListing(
        id="listing-1",
        marketplace="amazon_jp",
        title="Safe Local Test Item",
        brand="Example",
        model="EX-1",
        jan="4900000000000",
        asin="B000TEST00",
        condition="new",
    )
    identity = IdentityDecision(
        decision=IdentityDecisionValue.SAME,
        confidence_score=0.96,
        requires_human_review=False,
        scores=IdentityScores(
            identifier_score=1.0,
            brand_score=1.0,
            title_score=0.9,
            variant_score=1.0,
            condition_score=1.0,
            match_score=0.96,
        ),
    )
    profit = ProfitEstimate(
        decision="pass",
        net_profit_yen=1000,
        roi_percent=28.5,
        profit_margin_percent=12.5,
        break_even_price_yen=4000,
        risk_adjusted_profit_yen=850,
        fees=FeeBreakdown(platform_fee_yen=500, fulfillment_fee_yen=400, storage_fee_yen=50, other_cost_yen=0),
        reasons=("profit_thresholds_passed",),
    )
    score = CandidateScore(
        candidate_id="candidate-1",
        decision=CandidateScoreValue.TEST_BUY_CANDIDATE,
        total_score=0.75,
        identity_score=0.96,
        profit_score=0.7,
        roi_score=0.6,
        rank_score=0.5,
        price_gap_score=0.7,
        stock_risk_score=0.4,
        seller_competition_score=0.5,
        condition_risk_score=1.0,
        policy_risk_score=1.0,
        human_review_required=True,
        reasons=("human_approval_required_for_all_purchase_decisions",),
    )
    return build_candidate_review_packet(
        candidate_id="candidate-1",
        source_offer=source,
        market_listing=listing,
        identity_decision=identity,
        profit_estimate=profit,
        market_observations=(),
        candidate_score=score,
        allocated_budget_yen=0,
    )


class ManusHandoffBuilderTest(unittest.TestCase):
    def test_build_manus_handoff_packet_is_local_safety_contract(self):
        packet = build_manus_handoff_packet(_review_packet())
        data = packet.to_dict()

        self.assertEqual(data["purpose"], "pre_purchase_human_assistance_only")
        self.assertEqual(data["candidate_id"], "candidate-1")
        self.assertTrue(data["safety_flags"]["human_approval_required"])
        self.assertTrue(data["safety_flags"]["purchase_execution_disabled"])
        self.assertTrue(data["safety_flags"]["payment_execution_disabled"])
        self.assertTrue(data["safety_flags"]["browser_automation_disabled"])
        self.assertIn("execute_payment", data["forbidden_actions"])
        self.assertTrue(set(FORBIDDEN_ACTIONS).issubset(set(data["forbidden_actions"])))
        self.assertIn("p8_contract_requires_human_approval", data["machine_readable_reasons"])
        self.assertIn("must not log in", " ".join(data["human_checklist"]))
