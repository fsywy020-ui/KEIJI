"""Human-readable explanations for P3 profit estimates."""

from __future__ import annotations

from keiji.p3_profit.input_models import ProfitEstimate


def explain_profit_estimate(estimate: ProfitEstimate) -> str:
    """Build a concise human-readable P3 explanation."""

    lines = [
        f"P3 decision: {estimate.decision}",
        f"Net profit: {estimate.net_profit_yen} JPY",
        f"ROI: {estimate.roi_percent:.2f}%",
        f"Profit margin: {estimate.profit_margin_percent:.2f}%",
        f"Break-even price: {estimate.break_even_price_yen} JPY",
        "Human approval required: true",
    ]
    if estimate.reasons:
        lines.append("Reasons:")
        lines.extend(f"- {reason}" for reason in estimate.reasons)
    return "\n".join(lines)
