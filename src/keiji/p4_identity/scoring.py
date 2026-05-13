"""P4 score composition helpers."""

from __future__ import annotations

from typing import Any


def calculate_match_score(
    *,
    identifier_score: float,
    brand_score: float,
    title_score: float,
    variant_score: float,
    condition_score: float,
    rules: dict[str, Any] | None = None,
) -> float:
    """Combine component scores using configured P4 weights."""

    weights = (rules or {}).get("scoring", {}).get("weights", {})
    identifier_weight = float(weights.get("identifier", 0.35))
    brand_weight = float(weights.get("brand", 0.15))
    title_weight = float(weights.get("title", 0.20))
    variant_weight = float(weights.get("variant", 0.20))
    condition_weight = float(weights.get("condition", 0.10))
    return round(
        (identifier_score * identifier_weight)
        + (brand_score * brand_weight)
        + (title_score * title_weight)
        + (variant_score * variant_weight)
        + (condition_score * condition_weight),
        4,
    )
