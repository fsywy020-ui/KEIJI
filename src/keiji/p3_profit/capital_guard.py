"""Capital guardrails for P3."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CapitalGuardResult:
    """Capital policy evaluation."""

    status: str
    reasons: tuple[str, ...]


def evaluate_capital(
    *,
    purchase_amount_yen: int,
    allocated_budget_yen: int,
    rules: dict[str, Any],
) -> CapitalGuardResult:
    """Enforce per-SKU and total budget constraints."""

    capital = rules.get("capital", {})
    max_sku = int(capital.get("max_purchase_amount_per_sku_yen", 5000))
    total_budget = int(capital.get("initial_purchase_budget_yen", 50000))
    review_at = int(capital.get("review_purchase_amount_at_or_above_yen", 4500))
    review_utilization = float(capital.get("review_budget_utilization_at_or_above_percent", 80))

    reasons: list[str] = []
    if purchase_amount_yen > max_sku:
        return CapitalGuardResult("blocked", (f"per_sku_limit_exceeded:{purchase_amount_yen}>{max_sku}",))
    if allocated_budget_yen + purchase_amount_yen > total_budget:
        return CapitalGuardResult("blocked", (f"total_budget_exceeded:{allocated_budget_yen + purchase_amount_yen}>{total_budget}",))
    if purchase_amount_yen >= review_at:
        reasons.append(f"purchase_amount_near_sku_limit:{purchase_amount_yen}")
    utilization = ((allocated_budget_yen + purchase_amount_yen) / total_budget) * 100 if total_budget else 100
    if utilization >= review_utilization:
        reasons.append(f"budget_utilization_high:{utilization:.1f}%")
    return CapitalGuardResult("review" if reasons else "pass", tuple(reasons))
