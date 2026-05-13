"""P4 identity score aggregation helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class IdentityScoreWeights:
    """Configurable component weights for final P4 match score."""

    identifier: float = 0.35
    brand: float = 0.15
    title: float = 0.20
    variant: float = 0.20
    condition: float = 0.10

    @classmethod
    def from_rules(cls, rules: dict[str, Any]) -> "IdentityScoreWeights":
        defaults = cls()
        configured = rules.get("scoring", {}).get("weights", {})
        return cls(
            identifier=float(configured.get("identifier", defaults.identifier)),
            brand=float(configured.get("brand", defaults.brand)),
            title=float(configured.get("title", defaults.title)),
            variant=float(configured.get("variant", defaults.variant)),
            condition=float(configured.get("condition", defaults.condition)),
        )


def calculate_identity_match_score(
    *,
    identifier_score: float,
    brand_score: float,
    title_score: float,
    variant_score: float,
    condition_score: float,
    rules: dict[str, Any] | None = None,
) -> float:
    """Calculate the weighted P4 match score from component scores."""

    weights = IdentityScoreWeights.from_rules(rules or {})
    weighted_sum = (
        identifier_score * weights.identifier
        + brand_score * weights.brand
        + title_score * weights.title
        + variant_score * weights.variant
        + condition_score * weights.condition
    )
    weight_total = weights.identifier + weights.brand + weights.title + weights.variant + weights.condition
    if weight_total <= 0:
        return 0.0
    return round(weighted_sum / weight_total, 4)
