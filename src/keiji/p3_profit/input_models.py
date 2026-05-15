"""Input/output models for offline P3 profit calculation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ProfitInput:
    """P3 input derived from a P4-approved local candidate."""

    id: str
    p4_decision: str
    p4_confidence_score: float
    p4_requires_human_review: bool
    expected_sale_price_yen: int | None
    purchase_price_yen: int
    inbound_shipping_yen: int = 0
    category: str = "default"
    allocated_budget_yen: int = 0
    quantity: int = 1
    price_uncertainty_percent: float | None = None
    return_risk_level: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProfitInput":
        return cls(
            id=str(data["id"]),
            p4_decision=str(data.get("p4_decision", "same")),
            p4_confidence_score=float(data.get("p4_confidence_score", 1.0)),
            p4_requires_human_review=bool(data.get("p4_requires_human_review", False)),
            expected_sale_price_yen=(
                None if data.get("expected_sale_price_yen") is None else int(data["expected_sale_price_yen"])
            ),
            purchase_price_yen=int(data["purchase_price_yen"]),
            inbound_shipping_yen=int(data.get("inbound_shipping_yen", 0)),
            category=str(data.get("category", "default")),
            allocated_budget_yen=int(data.get("allocated_budget_yen", 0)),
            quantity=int(data.get("quantity", 1)),
            price_uncertainty_percent=(
                None if data.get("price_uncertainty_percent") is None else float(data["price_uncertainty_percent"])
            ),
            return_risk_level=(None if data.get("return_risk_level") is None else str(data["return_risk_level"])),
        )


@dataclass(frozen=True)
class FeeBreakdown:
    """P3 fee estimates in JPY."""

    platform_fee_yen: int
    fulfillment_fee_yen: int
    storage_fee_yen: int
    other_cost_yen: int


@dataclass(frozen=True)
class ShippingEstimateSummary:
    """Shipping assumptions copied into the P3 output contract."""

    inbound_shipping_yen: int
    packaging_cost_yen: int
    fulfillment_fee_yen: int
    assumptions: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class RiskDetail:
    """Structured operational risk adjustment detail."""

    name: str
    penalty_yen: int
    severity: str
    explanation: str


@dataclass(frozen=True)
class ProfitEstimate:
    """Final P3 estimate."""

    decision: str
    net_profit_yen: int
    roi_percent: float
    profit_margin_percent: float
    break_even_price_yen: int
    risk_adjusted_profit_yen: int
    fees: FeeBreakdown
    shipping: ShippingEstimateSummary = field(default_factory=lambda: ShippingEstimateSummary(0, 0, 0, ()))
    risk_details: tuple[RiskDetail, ...] = field(default_factory=tuple)
    reasons: tuple[str, ...] = field(default_factory=tuple)
    requires_human_approval: bool = True
