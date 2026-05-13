"""ROI and profit calculation helpers."""

from __future__ import annotations

from dataclasses import dataclass

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
    quantity: int = 1,
) -> ProfitNumbers:
    """Calculate deterministic offline profit metrics."""

    safe_quantity = max(1, quantity)
    purchase_cost = (purchase_price_yen * safe_quantity) + inbound_shipping_yen
    gross_sale_price = expected_sale_price_yen * safe_quantity
    total_cost = purchase_cost + fees.platform_fee_yen + fees.fulfillment_fee_yen + fees.storage_fee_yen + fees.other_cost_yen
    net_profit = gross_sale_price - total_cost
    roi = 0.0 if purchase_cost == 0 else round((net_profit / purchase_cost) * 100, 2)
    margin = 0.0 if gross_sale_price == 0 else round((net_profit / gross_sale_price) * 100, 2)
    return ProfitNumbers(
        total_purchase_cost_yen=purchase_cost,
        total_cost_yen=total_cost,
        net_profit_yen=net_profit,
        roi_percent=roi,
        profit_margin_percent=margin,
        break_even_price_yen=total_cost,
    )
