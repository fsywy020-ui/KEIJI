"""ROI and profit calculation helpers."""

from __future__ import annotations

from dataclasses import dataclass

from keiji.p3_profit.costs import build_cost_breakdown
from keiji.p3_profit.input_models import FeeBreakdown


@dataclass(frozen=True)
class ProfitNumbers:
    """Calculated profit numbers."""

    total_purchase_cost_yen: int
    total_cost_yen: int
    net_profit_yen: int
    roi_percent: float
    profit_margin_percent: float
    break_even_price_yen: int


def calculate_profit_numbers(
    *,
    expected_sale_price_yen: int,
    purchase_price_yen: int,
    inbound_shipping_yen: int,
    fees: FeeBreakdown,
) -> ProfitNumbers:
    """Calculate deterministic offline profit metrics."""

    costs = build_cost_breakdown(
        purchase_price_yen=purchase_price_yen,
        inbound_shipping_yen=inbound_shipping_yen,
        fees=fees,
    )
    purchase_cost = costs.total_purchase_cost_yen
    total_cost = costs.total_cost_yen
    net_profit = expected_sale_price_yen - total_cost
    roi = 0.0 if purchase_cost == 0 else round((net_profit / purchase_cost) * 100, 2)
    margin = 0.0 if expected_sale_price_yen == 0 else round((net_profit / expected_sale_price_yen) * 100, 2)
    return ProfitNumbers(
        total_purchase_cost_yen=purchase_cost,
        total_cost_yen=total_cost,
        net_profit_yen=net_profit,
        roi_percent=roi,
        profit_margin_percent=margin,
        break_even_price_yen=total_cost,
    )
