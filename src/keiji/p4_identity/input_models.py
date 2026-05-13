"""Input and output models for the P4 Product Identity Engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from keiji.common.enums import IdentityDecisionValue


@dataclass(frozen=True)
class SourceOffer:
    """Purchase-side offer captured from manual input, CSV, or fixture data."""

    id: str
    title: str
    purchase_price_yen: int
    domestic_shipping_yen: int = 0
    brand: str | None = None
    model: str | None = None
    jan: str | None = None
    asin: str | None = None
    condition: str = "new"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SourceOffer":
        return cls(
            id=str(data["id"]),
            title=str(data["title"]),
            brand=_optional_str(data.get("brand")),
            model=_optional_str(data.get("model")),
            jan=_optional_str(data.get("jan")),
            asin=_optional_str(data.get("asin")),
            condition=str(data.get("condition", "new")),
            purchase_price_yen=int(data["purchase_price_yen"]),
            domestic_shipping_yen=int(data.get("domestic_shipping_yen", 0)),
        )


@dataclass(frozen=True)
class MarketListing:
    """Amazon-side listing candidate stored locally for offline P4 matching."""

    id: str
    marketplace: str
    title: str
    brand: str | None = None
    model: str | None = None
    jan: str | None = None
    asin: str | None = None
    condition: str = "new"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MarketListing":
        return cls(
            id=str(data["id"]),
            marketplace=str(data.get("marketplace", "amazon_jp")),
            title=str(data["title"]),
            brand=_optional_str(data.get("brand")),
            model=_optional_str(data.get("model")),
            jan=_optional_str(data.get("jan")),
            asin=_optional_str(data.get("asin")),
            condition=str(data.get("condition", "new")),
        )


@dataclass(frozen=True)
class IdentityScores:
    """Component scores used to explain a P4 decision."""

    identifier_score: float = 0.0
    brand_score: float = 0.0
    title_score: float = 0.0
    variant_score: float = 0.0
    condition_score: float = 0.0
    match_score: float = 0.0


@dataclass(frozen=True)
class IdentityEvidence:
    """Single machine-readable evidence item."""

    code: str
    message: str
    severity: str = "info"


@dataclass(frozen=True)
class IdentityDecision:
    """Final P4 product identity decision."""

    decision: IdentityDecisionValue
    confidence_score: float
    requires_human_review: bool
    scores: IdentityScores
    evidence: tuple[IdentityEvidence, ...] = field(default_factory=tuple)
    block_reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision.value,
            "confidence_score": self.confidence_score,
            "requires_human_review": self.requires_human_review,
            "scores": {
                "identifier_score": self.scores.identifier_score,
                "brand_score": self.scores.brand_score,
                "title_score": self.scores.title_score,
                "variant_score": self.scores.variant_score,
                "condition_score": self.scores.condition_score,
                "match_score": self.scores.match_score,
            },
            "evidence": [e.__dict__ for e in self.evidence],
            "block_reason": self.block_reason,
        }


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip()
    return normalized or None
