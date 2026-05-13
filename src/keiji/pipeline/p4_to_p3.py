"""P4-to-P3 gate logic.

This module does not implement P3 profit calculation. It only decides whether a
P4 identity result may be handed to P3 according to the offline rule config.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from keiji.common.enums import IdentityDecisionValue, P3GateDecisionValue
from keiji.p4_identity.input_models import IdentityDecision


@dataclass(frozen=True)
class P3GateResult:
    """Result of evaluating whether P3 may run."""

    decision: P3GateDecisionValue
    reason: str


def evaluate_p3_gate(
    identity_decision: IdentityDecision,
    profit_rules: dict[str, Any],
    *,
    human_approved: bool = False,
) -> P3GateResult:
    """Evaluate the documented P4-to-P3 gate without running P3."""

    gate_rules = profit_rules.get("p4_gate", {})
    if identity_decision.decision in {
        IdentityDecisionValue.DIFFERENT,
        IdentityDecisionValue.BLOCKED,
    }:
        return P3GateResult(P3GateDecisionValue.SKIP, f"P4 decision is {identity_decision.decision.value}.")

    if identity_decision.decision == IdentityDecisionValue.AMBIGUOUS:
        if human_approved and gate_rules.get("human_approved_override", {}).get("allowed", False):
            return P3GateResult(P3GateDecisionValue.REVIEW_ONLY, "Human-approved ambiguous identity may run P3 in review-only mode.")
        return P3GateResult(P3GateDecisionValue.SKIP, "P4 decision is ambiguous and lacks human approval.")

    for allow_rule in gate_rules.get("allow_p3_when", []):
        if allow_rule.get("decision") != identity_decision.decision.value:
            continue
        min_confidence = float(allow_rule.get("min_confidence", 1.0))
        requires_review = bool(allow_rule.get("requires_human_review", False))
        if (
            identity_decision.confidence_score >= min_confidence
            and identity_decision.requires_human_review is requires_review
        ):
            return P3GateResult(P3GateDecisionValue.ALLOW, "P4 identity passed configured P3 gate.")

    if human_approved and gate_rules.get("human_approved_override", {}).get("allowed", False):
        return P3GateResult(P3GateDecisionValue.REVIEW_ONLY, "Human approval allows P3 review-only mode.")

    return P3GateResult(P3GateDecisionValue.SKIP, "P4 identity did not satisfy configured P3 gate.")
