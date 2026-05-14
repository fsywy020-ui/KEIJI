from __future__ import annotations

from pathlib import Path
import unittest

from keiji.common.config_loader import load_rule_config
from keiji.common.enums import IdentityDecisionValue, P3GateDecisionValue
from keiji.p4_identity.input_models import IdentityDecision, IdentityEvidence, IdentityScores
from keiji.pipeline.p4_to_p3 import evaluate_p3_gate


ROOT = Path(__file__).resolve().parents[3]


def identity(decision: IdentityDecisionValue, confidence: float, review: bool) -> IdentityDecision:
    return IdentityDecision(
        decision=decision,
        confidence_score=confidence,
        requires_human_review=review,
        scores=IdentityScores(identifier_score=1.0, match_score=1.0),
        evidence=(IdentityEvidence("test", "test evidence"),),
    )


class P4ToP3GateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profit_rules = load_rule_config(ROOT / "config/profit_rules.v1.yaml")

    def test_allows_high_confidence_same_identity(self) -> None:
        result = evaluate_p3_gate(identity(IdentityDecisionValue.SAME, 0.95, False), self.profit_rules)
        self.assertEqual(P3GateDecisionValue.ALLOW, result.decision)

    def test_skips_ambiguous_without_human_approval(self) -> None:
        result = evaluate_p3_gate(identity(IdentityDecisionValue.AMBIGUOUS, 0.5, True), self.profit_rules)
        self.assertEqual(P3GateDecisionValue.SKIP, result.decision)

    def test_human_approved_ambiguous_is_review_only(self) -> None:
        result = evaluate_p3_gate(
            identity(IdentityDecisionValue.AMBIGUOUS, 0.5, True),
            self.profit_rules,
            human_approved=True,
        )
        self.assertEqual(P3GateDecisionValue.REVIEW_ONLY, result.decision)

    def test_blocked_identity_is_always_skipped(self) -> None:
        result = evaluate_p3_gate(
            identity(IdentityDecisionValue.BLOCKED, 1.0, True),
            self.profit_rules,
            human_approved=True,
        )
        self.assertEqual(P3GateDecisionValue.SKIP, result.decision)


if __name__ == "__main__":
    unittest.main()
