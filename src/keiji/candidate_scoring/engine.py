"""Conservative offline P6 candidate scoring."""

from __future__ import annotations

from keiji.candidate_scoring.models import CandidateScore, CandidateScoreInput, CandidateScoreValue


class CandidateScoringEngine:
    """Score local candidates without purchase execution or external access."""

    def __init__(self, *, initial_budget_yen: int = 50000, max_per_sku_yen: int = 5000) -> None:
        self.initial_budget_yen = initial_budget_yen
        self.max_per_sku_yen = max_per_sku_yen

    def score(self, candidate: CandidateScoreInput) -> CandidateScore:
        reasons: list[str] = ["human_approval_required_for_all_purchase_decisions"]
        purchase_total = candidate.source_offer.purchase_price_yen + candidate.source_offer.domestic_shipping_yen
        identity_score = _clamp(candidate.identity_decision.confidence_score)
        profit_score = _score_profit(candidate.profit_estimate.net_profit_yen)
        roi_score = _score_roi(candidate.profit_estimate.roi_percent)
        primary_observation = _best_observation(candidate.market_observations)
        rank_score = _score_rank(primary_observation.rank if primary_observation else None)
        price_gap_score = _score_price_gap(candidate.profit_estimate.break_even_price_yen, primary_observation.price if primary_observation else None)
        stock_risk_score = _score_stock(primary_observation.stock_status if primary_observation else None)
        seller_competition_score = _score_sellers(primary_observation.seller_count if primary_observation else None)
        condition_risk_score = 1.0 if candidate.source_offer.condition == candidate.market_listing.condition == "new" else 0.3
        policy_risk_score = 1.0

        if candidate.identity_decision.decision.value != "same" or candidate.identity_decision.requires_human_review:
            reasons.append(f"p4_identity_not_safe:{candidate.identity_decision.decision.value}")
        if candidate.profit_estimate.decision != "pass":
            reasons.append(f"p3_profit_not_pass:{candidate.profit_estimate.decision}")
        if not candidate.market_observations:
            reasons.append("p5_market_data_missing")
        if purchase_total > self.max_per_sku_yen:
            policy_risk_score = 0.0
            reasons.append(f"per_sku_limit_exceeded:{purchase_total}>{self.max_per_sku_yen}")
        if candidate.allocated_budget_yen + purchase_total > self.initial_budget_yen:
            policy_risk_score = 0.0
            reasons.append("initial_budget_exceeded")
        if primary_observation and primary_observation.source != "amazon_jp":
            policy_risk_score = min(policy_risk_score, 0.6)
            reasons.append("primary_sales_channel_is_not_amazon")
        if primary_observation and primary_observation.stock_status.lower() in {"unknown", "out_of_stock"}:
            reasons.append(f"stock_status_requires_review:{primary_observation.stock_status}")

        total_score = round(
            identity_score * 0.25
            + profit_score * 0.18
            + roi_score * 0.15
            + rank_score * 0.10
            + price_gap_score * 0.10
            + stock_risk_score * 0.07
            + seller_competition_score * 0.05
            + condition_risk_score * 0.05
            + policy_risk_score * 0.05,
            4,
        )
        decision = self._decide(candidate, total_score, purchase_total, reasons)
        explanation = _explain(decision, reasons)
        return CandidateScore(
            candidate_id=candidate.candidate_id,
            decision=decision,
            total_score=total_score,
            identity_score=round(identity_score, 4),
            profit_score=round(profit_score, 4),
            roi_score=round(roi_score, 4),
            rank_score=round(rank_score, 4),
            price_gap_score=round(price_gap_score, 4),
            stock_risk_score=round(stock_risk_score, 4),
            seller_competition_score=round(seller_competition_score, 4),
            condition_risk_score=round(condition_risk_score, 4),
            policy_risk_score=round(policy_risk_score, 4),
            human_review_required=True,
            reasons=tuple(reasons),
            human_explanation=explanation,
        )

    def _decide(self, candidate: CandidateScoreInput, total_score: float, purchase_total: int, reasons: list[str]) -> CandidateScoreValue:
        if purchase_total > self.max_per_sku_yen or candidate.allocated_budget_yen + purchase_total > self.initial_budget_yen:
            return CandidateScoreValue.BLOCKED
        if candidate.identity_decision.decision.value == "blocked" or candidate.profit_estimate.decision == "blocked":
            return CandidateScoreValue.BLOCKED
        if candidate.identity_decision.decision.value != "same" or candidate.identity_decision.requires_human_review:
            return CandidateScoreValue.NEEDS_HUMAN_REVIEW
        if candidate.profit_estimate.decision != "pass":
            return CandidateScoreValue.WATCH_ONLY
        if not candidate.market_observations:
            return CandidateScoreValue.WATCH_ONLY
        if any("requires_review" in reason for reason in reasons):
            return CandidateScoreValue.NEEDS_HUMAN_REVIEW
        if total_score >= 0.82 and purchase_total <= 4000:
            return CandidateScoreValue.BUY_CANDIDATE
        if total_score >= 0.70:
            return CandidateScoreValue.TEST_BUY_CANDIDATE
        return CandidateScoreValue.WATCH_ONLY


def _best_observation(observations: tuple) -> object | None:
    return observations[0] if observations else None


def _score_profit(net_profit_yen: int) -> float:
    if net_profit_yen <= 0:
        return 0.0
    return _clamp(net_profit_yen / 2000)


def _score_roi(roi_percent: float) -> float:
    return _clamp(roi_percent / 60)


def _score_rank(rank: int | None) -> float:
    if rank is None or rank <= 0:
        return 0.4
    if rank <= 10000:
        return 1.0
    if rank <= 50000:
        return 0.8
    if rank <= 150000:
        return 0.55
    return 0.25


def _score_price_gap(break_even_price_yen: int, market_price_yen: int | None) -> float:
    if not market_price_yen or break_even_price_yen <= 0:
        return 0.4
    return _clamp((market_price_yen - break_even_price_yen) / max(market_price_yen, 1) * 3)


def _score_stock(stock_status: str | None) -> float:
    return {"in_stock": 1.0, "low_stock": 0.7, "unknown": 0.4, "out_of_stock": 0.2}.get((stock_status or "unknown").lower(), 0.4)


def _score_sellers(seller_count: int | None) -> float:
    if seller_count is None:
        return 0.5
    if seller_count <= 3:
        return 1.0
    if seller_count <= 10:
        return 0.7
    if seller_count <= 25:
        return 0.4
    return 0.2


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _explain(decision: CandidateScoreValue, reasons: list[str]) -> str:
    return f"P6 recommendation is {decision.value}. Human approval remains required. Key reasons: {', '.join(reasons)}."
