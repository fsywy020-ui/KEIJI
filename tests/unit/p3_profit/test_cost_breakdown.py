from __future__ import annotations

import unittest

from keiji.p3_profit.costs import build_cost_breakdown
from keiji.p3_profit.input_models import FeeBreakdown
from keiji.p3_profit.roi_calculator import calculate_profit_numbers


class CostBreakdownTest(unittest.TestCase):
    def test_cost_breakdown_keeps_buffer_cost_auditable(self) -> None:
        fees = FeeBreakdown(platform_fee_yen=800, fulfillment_fee_yen=450, storage_fee_yen=0, other_cost_yen=100)
        costs = build_cost_breakdown(purchase_price_yen=3000, inbound_shipping_yen=500, fees=fees)
        self.assertEqual(3500, costs.total_purchase_cost_yen)
        self.assertEqual(4850, costs.total_cost_yen)
        self.assertEqual(100, costs.buffer_cost_yen)

    def test_roi_calculator_uses_total_cost_including_buffer(self) -> None:
        fees = FeeBreakdown(platform_fee_yen=800, fulfillment_fee_yen=450, storage_fee_yen=0, other_cost_yen=100)
        numbers = calculate_profit_numbers(
            expected_sale_price_yen=7000,
            purchase_price_yen=3000,
            inbound_shipping_yen=500,
            fees=fees,
        )
        self.assertEqual(4850, numbers.break_even_price_yen)
        self.assertEqual(2150, numbers.net_profit_yen)


if __name__ == "__main__":
    unittest.main()
