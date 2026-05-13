"""Amazon fee estimation for offline P3."""

from __future__ import annotations

from typing import Any

from keiji.p3_profit.input_models import FeeBreakdown


def estimate_fees(expected_sale_price_yen: int, category: str, rules: dict[str, Any], *, quantity: int = 1) -> FeeBreakdown:
    """Estimate fees using local configured Amazon JP defaults."""

    safe_quantity = max(1, quantity)
    amazon = rules.get("marketplace", {}).get("amazon_jp", {})
    category_rates = amazon.get("category_fee_rates", {})
    rate = float(category_rates.get(category, category_rates.get("default", amazon.get("default_referral_fee_rate", 0.10))))
    return FeeBreakdown(
        platform_fee_yen=round(expected_sale_price_yen * safe_quantity * rate),
        fulfillment_fee_yen=int(amazon.get("default_fulfillment_fee_yen", 0)) * safe_quantity,
        storage_fee_yen=int(amazon.get("default_storage_fee_yen", 0)) * safe_quantity,
        other_cost_yen=int(amazon.get("default_other_cost_yen", 0)) * safe_quantity,
    )
