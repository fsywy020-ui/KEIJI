"""P7 candidate review packet builder.

Packets are local human-review artifacts only. They never execute purchase,
payment, listing, checkout, login, browser automation, scraping, or live APIs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from keiji.candidate_scoring.models import CandidateScore
from keiji.market_monitoring.models import MarketObservation
from keiji.p3_profit.input_models import ProfitEstimate
from keiji.p4_identity.input_models import IdentityDecision, MarketListing, SourceOffer


@dataclass(frozen=True)
class CandidateReviewPacket:
    candidate_id: str
    product_name: str
    jan: str | None
    asin: str | None
    model_number: str | None
    p4_identity_result: dict[str, Any]
    p3_profit_result: dict[str, Any]
    p5_market_data: list[dict[str, Any]]
    p6_score: dict[str, Any]
    recommendation: str
    do_not_purchase_reasons: tuple[str, ...]
    human_check_items: tuple[str, ...]
    initial_budget_impact_yen: int
    initial_budget_remaining_after_candidate_yen: int
    per_sku_limit_ok: bool
    external_send_disabled: bool = True
    purchase_execution_disabled: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "product_name": self.product_name,
            "jan": self.jan,
            "asin": self.asin,
            "model_number": self.model_number,
            "p4_identity_result": self.p4_identity_result,
            "p3_profit_result": self.p3_profit_result,
            "p5_market_data": self.p5_market_data,
            "p6_score": self.p6_score,
            "recommendation": self.recommendation,
            "do_not_purchase_reasons": list(self.do_not_purchase_reasons),
            "human_check_items": list(self.human_check_items),
            "initial_budget_impact_yen": self.initial_budget_impact_yen,
            "initial_budget_remaining_after_candidate_yen": self.initial_budget_remaining_after_candidate_yen,
            "per_sku_limit_ok": self.per_sku_limit_ok,
            "external_send_disabled": self.external_send_disabled,
            "purchase_execution_disabled": self.purchase_execution_disabled,
        }


def build_candidate_review_packet(
    *,
    candidate_id: str,
    source_offer: SourceOffer,
    market_listing: MarketListing,
    identity_decision: IdentityDecision,
    profit_estimate: ProfitEstimate,
    market_observations: tuple[MarketObservation, ...],
    candidate_score: CandidateScore,
    allocated_budget_yen: int = 0,
    initial_budget_yen: int = 50000,
    max_per_sku_yen: int = 5000,
) -> CandidateReviewPacket:
    purchase_total = source_offer.purchase_price_yen + source_offer.domestic_shipping_yen
    do_not_purchase = _do_not_purchase_reasons(identity_decision, profit_estimate, candidate_score, purchase_total, max_per_sku_yen)
    checklist = (
        "JAN/ASIN/型番が同一商品を指しているか目視確認する",
        "容量・色・セット数・edition・国内正規品/並行輸入品・付属品差を確認する",
        "新品/中古/未開封/箱傷みなど状態差を確認する",
        "Amazon想定販売価格、手数料、ランキング、出品者数を確認する",
        "50,000 JPY初期枠と1SKU 5,000 JPY上限を確認する",
        "購入・決済・出品はこのレポートから実行しない",
    )
    return CandidateReviewPacket(
        candidate_id=candidate_id,
        product_name=source_offer.title,
        jan=source_offer.jan or market_listing.jan,
        asin=source_offer.asin or market_listing.asin,
        model_number=source_offer.model or market_listing.model,
        p4_identity_result=identity_decision.to_dict(),
        p3_profit_result={
            "decision": profit_estimate.decision,
            "net_profit_yen": profit_estimate.net_profit_yen,
            "roi_percent": profit_estimate.roi_percent,
            "profit_margin_percent": profit_estimate.profit_margin_percent,
            "break_even_price_yen": profit_estimate.break_even_price_yen,
            "risk_adjusted_profit_yen": profit_estimate.risk_adjusted_profit_yen,
            "reasons": list(profit_estimate.reasons),
            "requires_human_approval": profit_estimate.requires_human_approval,
        },
        p5_market_data=[observation.to_dict() for observation in market_observations],
        p6_score=candidate_score.to_dict(),
        recommendation=candidate_score.decision.value,
        do_not_purchase_reasons=do_not_purchase,
        human_check_items=checklist,
        initial_budget_impact_yen=purchase_total,
        initial_budget_remaining_after_candidate_yen=initial_budget_yen - allocated_budget_yen - purchase_total,
        per_sku_limit_ok=purchase_total <= max_per_sku_yen,
    )


def _do_not_purchase_reasons(
    identity_decision: IdentityDecision,
    profit_estimate: ProfitEstimate,
    candidate_score: CandidateScore,
    purchase_total: int,
    max_per_sku_yen: int,
) -> tuple[str, ...]:
    reasons: list[str] = ["human_approval_not_recorded"]
    if identity_decision.decision.value != "same" or identity_decision.requires_human_review:
        reasons.append(f"identity_not_safe:{identity_decision.decision.value}")
    if profit_estimate.decision != "pass":
        reasons.append(f"profit_not_pass:{profit_estimate.decision}")
    if candidate_score.decision.value in {"BLOCKED", "WATCH_ONLY", "NEEDS_HUMAN_REVIEW"}:
        reasons.append(f"score_recommendation_not_buy:{candidate_score.decision.value}")
    if purchase_total > max_per_sku_yen:
        reasons.append(f"per_sku_limit_exceeded:{purchase_total}>{max_per_sku_yen}")
    reasons.extend(reason for reason in candidate_score.reasons if reason != "human_approval_required_for_all_purchase_decisions")
    return tuple(dict.fromkeys(reasons))
