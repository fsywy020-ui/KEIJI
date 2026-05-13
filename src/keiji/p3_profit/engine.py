"""Offline P3 Profit Calculation Engine."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from keiji.common.config_loader import load_rule_config
from keiji.p3_profit.capital_guard import evaluate_capital
from keiji.p3_profit.decision import decide_profit
from keiji.p3_profit.fee_estimator import estimate_fees
from keiji.p3_profit.input_models import FeeBreakdown, ProfitEstimate, ProfitInput
from keiji.p3_profit.roi_calculator import calculate_profit_numbers


class ProfitEngine:
    """Deterministic offline profit engine that never purchases or pays."""

    def __init__(self, rules: dict[str, Any]) -> None:
        self.rules = rules

    @classmethod
    def from_config_path(cls, config_path: str | Path) -> "ProfitEngine":
        return cls(load_rule_config(config_path))

    def evaluate(self, profit_input: ProfitInput) -> ProfitEstimate:
        reasons: list[str] = []
        if profit_input.p4_decision != "same" or profit_input.p4_requires_human_review:
            reasons.append(f"p4_gate_not_allowed:{profit_input.p4_decision}")
            return _empty_estimate("skipped", reasons)
        if profit_input.expected_sale_price_yen is None:
            reasons.append("expected_sale_price_missing")
            return _empty_estimate("review", reasons)

        fees = estimate_fees(profit_input.expected_sale_price_yen, profit_input.category, self.rules)
        numbers = calculate_profit_numbers(
            expected_sale_price_yen=profit_input.expected_sale_price_yen,
            purchase_price_yen=profit_input.purchase_price_yen,
            inbound_shipping_yen=profit_input.inbound_shipping_yen,
            fees=fees,
        )
        capital = evaluate_capital(
            purchase_amount_yen=numbers.total_purchase_cost_yen,
            allocated_budget_yen=profit_input.allocated_budget_yen,
            rules=self.rules,
        )
        decision = decide_profit(numbers, capital, self.rules, reasons)
        risk_adjusted_profit = _risk_adjusted_profit(numbers.net_profit_yen, reasons)
        return ProfitEstimate(
            decision=decision,
            net_profit_yen=numbers.net_profit_yen,
            roi_percent=numbers.roi_percent,
            profit_margin_percent=numbers.profit_margin_percent,
            break_even_price_yen=numbers.break_even_price_yen,
            risk_adjusted_profit_yen=risk_adjusted_profit,
            fees=fees,
            reasons=tuple(reasons),
            requires_human_approval=True,
        )


def _empty_estimate(decision: str, reasons: list[str]) -> ProfitEstimate:
    return ProfitEstimate(
        decision=decision,
        net_profit_yen=0,
        roi_percent=0.0,
        profit_margin_percent=0.0,
        break_even_price_yen=0,
        risk_adjusted_profit_yen=0,
        fees=FeeBreakdown(0, 0, 0, 0),
        reasons=tuple(reasons),
        requires_human_approval=True,
    )


def _risk_adjusted_profit(net_profit_yen: int, reasons: list[str]) -> int:
    penalty = 100 * len(reasons)
    return net_profit_yen - penalty
