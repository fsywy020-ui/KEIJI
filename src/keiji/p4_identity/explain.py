"""Human-readable explanations for P4 identity decisions."""

from __future__ import annotations

from keiji.p4_identity.input_models import IdentityDecision


def explain_identity_decision(decision: IdentityDecision) -> str:
    """Build a concise human-readable explanation for review screens/logs."""

    lines = [
        f"P4 decision: {decision.decision.value}",
        f"Confidence: {decision.confidence_score:.2f}",
        f"Human review required: {str(decision.requires_human_review).lower()}",
    ]
    if decision.block_reason:
        lines.append(f"Block reason: {decision.block_reason}")
    if decision.evidence:
        lines.append("Evidence:")
        for item in decision.evidence:
            lines.append(f"- [{item.severity}] {item.code}: {item.message}")
    return "\n".join(lines)
