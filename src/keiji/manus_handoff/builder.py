"""Build local P8 Manus handoff packets from P7 review packets."""

from __future__ import annotations

from typing import Any

from keiji.manus_handoff.models import ManusHandoffPacket
from keiji.manus_handoff.policy import HUMAN_CHECKLIST_ITEMS
from keiji.review.packet import CandidateReviewPacket


def build_manus_handoff_packet(review_packet: CandidateReviewPacket, *, p7_review_status: str = "pending_human_approval") -> ManusHandoffPacket:
    """Create a local Manus handoff packet from a P7 human review packet."""

    data = review_packet.to_dict()
    market_summary = _market_summary(data.get("p5_market_data", []))
    return ManusHandoffPacket(
        candidate_id=str(data["candidate_id"]),
        product_name=str(data["product_name"]),
        jan=data.get("jan"),
        asin=data.get("asin"),
        model_number=data.get("model_number"),
        source_url_or_reference=_source_reference(data),
        sales_url_or_reference=_sales_reference(data),
        p4_identity_result=dict(data["p4_identity_result"]),
        p3_profit_result=dict(data["p3_profit_result"]),
        p5_market_data_summary=market_summary,
        p6_score=dict(data["p6_score"]),
        p7_review_status=p7_review_status,
        recommended_action=_recommended_action(data),
        human_check_items=_combined_checklist(data),
        per_sku_limit_ok=bool(data["per_sku_limit_ok"]),
        initial_budget_impact_yen=int(data["initial_budget_impact_yen"]),
        initial_budget_remaining_after_candidate_yen=int(data["initial_budget_remaining_after_candidate_yen"]),
    )


def _market_summary(market_data: list[dict[str, Any]]) -> dict[str, Any]:
    if not market_data:
        return {
            "status": "missing",
            "observation_count": 0,
            "human_explanation": "No matching local P5 market observations were attached; keep this candidate in review/watch mode.",
        }
    first = market_data[0]
    return {
        "status": "present",
        "observation_count": len(market_data),
        "primary_source": first.get("source"),
        "primary_observed_at": first.get("observed_at"),
        "primary_price_yen": first.get("price"),
        "primary_shipping_fee_yen": first.get("shipping_fee"),
        "primary_rank": first.get("rank"),
        "primary_stock_status": first.get("stock_status"),
        "primary_seller_count": first.get("seller_count"),
        "primary_reference": first.get("url_or_reference"),
    }


def _source_reference(data: dict[str, Any]) -> str:
    # Source-side URL is intentionally optional for the initial local MVP.
    # Do not infer or create executable checkout links.
    return "local/manual-source-reference-unavailable"


def _sales_reference(data: dict[str, Any]) -> str:
    for observation in data.get("p5_market_data", []):
        reference = observation.get("url_or_reference")
        if reference:
            return str(reference)
    asin = data.get("asin")
    if asin:
        return f"asin:{asin}"
    return "local/sales-reference-unavailable"


def _recommended_action(data: dict[str, Any]) -> str:
    recommendation = str(data.get("recommendation", "NEEDS_HUMAN_REVIEW"))
    if recommendation == "BUY_CANDIDATE":
        return "human_review_candidate_only_not_purchase_permission"
    if recommendation == "TEST_BUY_CANDIDATE":
        return "human_review_test_candidate_only_not_purchase_permission"
    if recommendation in {"BLOCKED", "WATCH_ONLY", "NEEDS_HUMAN_REVIEW"}:
        return recommendation.lower()
    return "needs_human_review"


def _combined_checklist(data: dict[str, Any]) -> tuple[str, ...]:
    merged: list[str] = []
    for item in (*data.get("human_check_items", []), *HUMAN_CHECKLIST_ITEMS):
        text = str(item).strip()
        if text and text not in merged:
            merged.append(text)
    return tuple(merged)
