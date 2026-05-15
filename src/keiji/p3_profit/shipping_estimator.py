"""Local-config shipping and fulfillment assumptions for P3."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from keiji.p3_profit.input_models import ProfitInput


@dataclass(frozen=True)
class ShippingEstimate:
    """Operational shipping assumptions used by the offline P3 estimate."""

    inbound_shipping_yen: int
    packaging_cost_yen: int
    fulfillment_fee_yen: int
    assumptions: tuple[str, ...]


def estimate_shipping(profit_input: ProfitInput, rules: dict[str, Any]) -> ShippingEstimate:
    """Estimate local/manual shipping assumptions without external access.

    This is an operational estimate for purchase-review screening only. It is
    not accounting or tax advice and it does not perform fulfillment actions.
    """

    shipping_rules = rules.get("shipping", {})
    category_overrides = shipping_rules.get("category_overrides") or {}
    category_rules = category_overrides.get(profit_input.category, {})
    amazon_rules = rules.get("marketplace", {}).get("amazon_jp", {})

    packaging_cost = int(
        category_rules.get(
            "packaging_cost_yen",
            shipping_rules.get(
                "default_packaging_cost_yen",
                amazon_rules.get("default_other_cost_yen", 0),
            ),
        )
    )
    fulfillment_fee = int(
        category_rules.get(
            "fulfillment_fee_yen",
            shipping_rules.get(
                "default_fulfillment_fee_yen",
                amazon_rules.get("default_fulfillment_fee_yen", 0),
            ),
        )
    )

    assumption_values = [
        f"source:{shipping_rules.get('source', 'local_or_manual_only')}",
        f"fulfillment_model:{shipping_rules.get('fulfillment_model', 'local_config_default')}",
        f"inbound_shipping:{shipping_rules.get('inbound_shipping_policy', 'input_value')}",
        "no_live_rate_lookup",
    ]
    for assumption in shipping_rules.get("assumptions", ()):  # optional human-readable notes
        assumption_values.append(str(assumption))

    return ShippingEstimate(
        inbound_shipping_yen=profit_input.inbound_shipping_yen,
        packaging_cost_yen=packaging_cost,
        fulfillment_fee_yen=fulfillment_fee,
        assumptions=tuple(assumption_values),
    )
