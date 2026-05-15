"""Config-driven risk adjustment for offline P3 profit estimates."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from keiji.p3_profit.input_models import ProfitInput, RiskDetail


@dataclass(frozen=True)
class RiskAdjustment:
    """Risk-adjusted profit and structured details."""

    risk_adjusted_profit_yen: int
    total_penalty_yen: int
    details: tuple[RiskDetail, ...]


def adjust_for_risk(
    *,
    net_profit_yen: int,
    total_purchase_cost_yen: int,
    profit_input: ProfitInput,
    rules: dict[str, Any],
) -> RiskAdjustment:
    """Apply local-config operational risk penalties.

    The adjustment is a conservative screening aid for human purchase review.
    It is not tax, accounting, or financial advice and it never performs any
    purchase, payment, listing, or external lookup.
    """

    risk_rules = rules.get("risk_adjustment", {})
    details: list[RiskDetail] = []

    price_detail = _price_uncertainty_detail(profit_input, risk_rules)
    if price_detail is not None:
        details.append(price_detail)

    return_detail = _return_risk_detail(profit_input, risk_rules)
    if return_detail is not None:
        details.append(return_detail)

    budget_detail = _budget_concentration_detail(
        total_purchase_cost_yen=total_purchase_cost_yen,
        allocated_budget_yen=profit_input.allocated_budget_yen,
        rules=rules,
        risk_rules=risk_rules,
    )
    if budget_detail is not None:
        details.append(budget_detail)

    total_penalty = sum(detail.penalty_yen for detail in details)
    return RiskAdjustment(
        risk_adjusted_profit_yen=net_profit_yen - total_penalty,
        total_penalty_yen=total_penalty,
        details=tuple(details),
    )


def _price_uncertainty_detail(profit_input: ProfitInput, risk_rules: dict[str, Any]) -> RiskDetail | None:
    price_rules = risk_rules.get("price_uncertainty", {})
    uncertainty = profit_input.price_uncertainty_percent
    if uncertainty is None:
        uncertainty = price_rules.get("default_percent")
    if uncertainty is None:
        return None

    threshold = float(price_rules.get("review_at_or_above_percent", 10))
    uncertainty_float = float(uncertainty)
    if uncertainty_float < threshold:
        return None

    penalty = int(price_rules.get("penalty_yen", 0))
    return RiskDetail(
        name="price_uncertainty",
        penalty_yen=penalty,
        severity=str(price_rules.get("severity", "review")),
        explanation=(
            f"Expected sale price uncertainty is {uncertainty_float:g}% "
            f"against the configured {threshold:g}% review threshold."
        ),
    )


def _return_risk_detail(profit_input: ProfitInput, risk_rules: dict[str, Any]) -> RiskDetail | None:
    return_rules = risk_rules.get("return_risk", {})
    risk_level = profit_input.return_risk_level or str(return_rules.get("default_level", "low"))
    level_rules = return_rules.get("levels", {}).get(risk_level, {})
    penalty = int(level_rules.get("penalty_yen", 0))
    if penalty <= 0:
        return None
    return RiskDetail(
        name="return_risk",
        penalty_yen=penalty,
        severity=str(level_rules.get("severity", "review")),
        explanation=f"Return risk level '{risk_level}' uses the configured {penalty} JPY operational buffer.",
    )


def _budget_concentration_detail(
    *,
    total_purchase_cost_yen: int,
    allocated_budget_yen: int,
    rules: dict[str, Any],
    risk_rules: dict[str, Any],
) -> RiskDetail | None:
    budget_rules = risk_rules.get("budget_concentration", {})
    total_budget = int(rules.get("capital", {}).get("initial_purchase_budget_yen", 50000))
    if total_budget <= 0:
        return RiskDetail(
            name="budget_concentration",
            penalty_yen=int(budget_rules.get("penalty_yen", 0)),
            severity=str(budget_rules.get("severity", "review")),
            explanation="Configured total budget is zero or negative, so budget concentration requires review.",
        )

    utilization = ((allocated_budget_yen + total_purchase_cost_yen) / total_budget) * 100
    threshold = float(budget_rules.get("review_at_or_above_percent", 80))
    if utilization < threshold:
        return None

    penalty = int(budget_rules.get("penalty_yen", 0))
    return RiskDetail(
        name="budget_concentration",
        penalty_yen=penalty,
        severity=str(budget_rules.get("severity", "review")),
        explanation=(
            f"Candidate would use {utilization:.1f}% of the configured initial budget, "
            f"at or above the {threshold:g}% review threshold."
        ),
    )
