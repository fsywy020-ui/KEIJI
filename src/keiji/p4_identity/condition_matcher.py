"""Condition policy matching for P4 product identity."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ConditionMatchResult:
    """Condition policy decision used by P4."""

    score: float
    status: str
    evidence_code: str
    message: str


def match_condition(source_condition: str, listing_condition: str, rules: dict[str, Any]) -> ConditionMatchResult:
    """Match source/listing conditions using the configured policy matrix."""

    policy = rules.get("condition_policy", {})
    source = source_condition.lower()
    listing = listing_condition.lower()
    if _pair_in_policy(source, listing, policy.get("allowed_same_condition_pairs", [])):
        return ConditionMatchResult(1.0, "match", "condition_match", "Condition pair is allowed by policy.")
    if _pair_in_policy(source, listing, policy.get("review_condition_pairs", [])):
        return ConditionMatchResult(0.5, "review", "condition_review", "Condition pair requires human review by policy.")
    if _pair_in_policy(source, listing, policy.get("blocked_pairs", [])):
        return ConditionMatchResult(0.0, "blocked", "condition_blocked", "Condition pair is blocked by policy.")
    if source == listing:
        return ConditionMatchResult(0.5, "review", "condition_unknown_pair", "Condition pair is not explicitly configured.")
    return ConditionMatchResult(0.0, "blocked", "condition_mismatch", "Condition pair is incompatible or unknown.")


def _pair_in_policy(source: str, listing: str, pairs: list[dict[str, Any]]) -> bool:
    return any(str(pair.get("source", "")).lower() == source and str(pair.get("marketplace", "")).lower() == listing for pair in pairs)
