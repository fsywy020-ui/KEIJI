"""Money helpers for yen-denominated MVP rules."""

from __future__ import annotations


def total_purchase_amount_yen(purchase_price_yen: int, domestic_shipping_yen: int = 0) -> int:
    """Return total purchase-side amount in JPY.

    The initial MVP uses integer yen amounts only. Negative values are rejected
    because they would hide budget and approval violations.
    """

    if purchase_price_yen < 0 or domestic_shipping_yen < 0:
        raise ValueError("yen amounts must be non-negative")
    return purchase_price_yen + domestic_shipping_yen
