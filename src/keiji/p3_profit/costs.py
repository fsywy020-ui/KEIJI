"""P3 cost aggregation helpers.

These helpers keep purchase price, shipping, marketplace fees, fulfillment fees,
storage fees, and conservative buffer/reserve costs explicit for auditability.
"""

from __future__ import annotations

from dataclasses import dataclass

from keiji.p3_profit.input_models import FeeBreakdown


@dataclass(frozen=True)
class CostBreakdown:
    """Auditable P3 cost components in JPY."""

    purchase_price_yen: int
    inbound_shipping_yen: int
    platform_fee_yen: int
    fulfillment_fee_yen: int
    storage_fee_yen: int
    buffer_cost_yen: int

    @property
    def total_purchase_cost_yen(self) -> int:
        """Cash needed before marketplace fees."""

        return self.purchase_price_yen + self.inbound_shipping_yen

    @property
    def total_cost_yen(self) -> int:
        """Total conservative cost basis for break-even and net profit."""

        return (
            self.total_purchase_cost_yen
            + self.platform_fee_yen
            + self.fulfillment_fee_yen
            + self.storage_fee_yen
            + self.buffer_cost_yen
        )


def build_cost_breakdown(*, purchase_price_yen: int, inbound_shipping_yen: int, fees: FeeBreakdown) -> CostBreakdown:
    """Build a cost breakdown from local/manual purchase inputs and fee estimates."""

    return CostBreakdown(
        purchase_price_yen=purchase_price_yen,
        inbound_shipping_yen=inbound_shipping_yen,
        platform_fee_yen=fees.platform_fee_yen,
        fulfillment_fee_yen=fees.fulfillment_fee_yen,
        storage_fee_yen=fees.storage_fee_yen,
        buffer_cost_yen=fees.other_cost_yen,
    )
