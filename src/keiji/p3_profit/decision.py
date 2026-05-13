"""P3 decision policy."""

from __future__ import annotations

from typing import Any

from keiji.p3_profit.capital_guard import CapitalGuardResult
from keiji.p3_profit.roi_calculator import ProfitNumbers


def decide_profit(numbers: ProfitNumbers | None, capital: CapitalGuardResult | None, rules: dict[str, Any], reasons: list[str]) -> str:
    """Return P3 decision string."""

    if numbers is None or capital is None:
        return "skipped"
    if capital.status == "blocked":
        reasons.extend(capital.reasons)
        return "blocked"
    thresholds = rules.get("profit_thresholds", {})
    min_profit = int(thresholds.get("minimum_net_profit_yen", 500))
    min_roi = float(thresholds.get("minimum_roi_percent", 20))
    min_margin = float(thresholds.get("minimum_profit_margin_percent", 8))
    if numbers.net_profit_yen < min_profit:
        reasons.append(f"net_profit_below_minimum:{numbers.net_profit_yen}<{min_profit}")
        return "fail"
    if numbers.roi_percent < min_roi:
        reasons.append(f"roi_below_minimum:{numbers.roi_percent}<{min_roi}")
        return "fail"
    if numbers.profit_margin_percent < min_margin:
        reasons.append(f"margin_below_minimum:{numbers.profit_margin_percent}<{min_margin}")
        return "fail"
    if capital.status == "review":
        reasons.extend(capital.reasons)
        return "review"
    return "pass"
