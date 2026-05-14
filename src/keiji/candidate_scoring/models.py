"""P6 candidate scoring models."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from keiji.market_monitoring.models import MarketObservation
from keiji.p3_profit.input_models import ProfitEstimate
from keiji.p4_identity.input_models import IdentityDecision, MarketListing, SourceOffer


class CandidateScoreValue(StrEnum):
    BUY_CANDIDATE = "BUY_CANDIDATE"
    TEST_BUY_CANDIDATE = "TEST_BUY_CANDIDATE"
    WATCH_ONLY = "WATCH_ONLY"
    BLOCKED = "BLOCKED"
    NEEDS_HUMAN_REVIEW = "NEEDS_HUMAN_REVIEW"


@dataclass(frozen=True)
class CandidateScoreInput:
    candidate_id: str
    source_offer: SourceOffer
    market_listing: MarketListing
    identity_decision: IdentityDecision
    profit_estimate: ProfitEstimate
    market_observations: tuple[MarketObservation, ...] = ()
    allocated_budget_yen: int = 0


@dataclass(frozen=True)
class CandidateScore:
    candidate_id: str
    decision: CandidateScoreValue
    total_score: float
    identity_score: float
    profit_score: float
    roi_score: float
    rank_score: float
    price_gap_score: float
    stock_risk_score: float
    seller_competition_score: float
    condition_risk_score: float
    policy_risk_score: float
    human_review_required: bool
    reasons: tuple[str, ...] = field(default_factory=tuple)
    human_explanation: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "decision": self.decision.value,
            "total_score": self.total_score,
            "identity_score": self.identity_score,
            "profit_score": self.profit_score,
            "roi_score": self.roi_score,
            "rank_score": self.rank_score,
            "price_gap_score": self.price_gap_score,
            "stock_risk_score": self.stock_risk_score,
            "seller_competition_score": self.seller_competition_score,
            "condition_risk_score": self.condition_risk_score,
            "policy_risk_score": self.policy_risk_score,
            "human_review_required": self.human_review_required,
            "reasons": list(self.reasons),
            "human_explanation": self.human_explanation,
        }
