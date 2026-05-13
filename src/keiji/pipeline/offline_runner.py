"""Offline orchestration for P4 -> P3 -> persistence -> review candidates.

The runner is intentionally local-only. It never calls external APIs, opens a
browser, purchases, pays, checks out, or logs in to any service.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Any

from keiji.common.config_loader import load_rule_config
from keiji.db.repositories.audit_repository import AuditRepository
from keiji.db.repositories.p3_repository import P3Repository
from keiji.db.repositories.p4_repository import P4Repository
from keiji.db.repositories.purchase_candidate_repository import PurchaseCandidateRepository
from keiji.p3_profit import ProfitEngine, ProfitInput
from keiji.p4_identity import MarketListing, ProductIdentityEngine, SourceOffer


@dataclass(frozen=True)
class OfflineCandidateInput:
    """Single local candidate input for the offline pipeline."""

    source_offer: SourceOffer
    market_listing: MarketListing
    expected_sale_price_yen: int | None
    category: str = "default"
    allocated_budget_yen: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "OfflineCandidateInput":
        return cls(
            source_offer=SourceOffer.from_dict(data["source_offer"]),
            market_listing=MarketListing.from_dict(data["market_listing"]),
            expected_sale_price_yen=(
                None if data.get("expected_sale_price_yen") is None else int(data["expected_sale_price_yen"])
            ),
            category=str(data.get("category", "default")),
            allocated_budget_yen=int(data.get("allocated_budget_yen", 0)),
        )


@dataclass(frozen=True)
class OfflineRunResult:
    """Persisted IDs and decisions for one offline candidate run."""

    identity_decision_id: str
    p3_run_id: str
    profit_estimate_id: str
    purchase_candidate_id: str | None
    p4_decision: str
    p3_decision: str


class OfflinePipelineRunner:
    """Run local candidates through P4, P3, audit, and candidate creation."""

    def __init__(
        self,
        *,
        connection: sqlite3.Connection,
        product_identity_rules_path: str,
        profit_rules_path: str,
    ) -> None:
        self.connection = connection
        self.p4_rules = load_rule_config(product_identity_rules_path)
        self.p3_rules = load_rule_config(profit_rules_path)
        self.p4_engine = ProductIdentityEngine(self.p4_rules)
        self.p3_engine = ProfitEngine(self.p3_rules)
        self.audit = AuditRepository(connection)
        self.p4_repo = P4Repository(connection)
        self.p3_repo = P3Repository(connection)
        self.candidates = PurchaseCandidateRepository(connection)

    def run_one(self, candidate: OfflineCandidateInput) -> OfflineRunResult:
        """Run one local candidate through the safe offline flow."""

        self.p4_repo.save_source_offer(candidate.source_offer)
        self.p4_repo.save_market_listing(candidate.market_listing)
        p4_decision = self.p4_engine.evaluate(candidate.source_offer, candidate.market_listing)
        p4_run_id = self.p4_repo.create_run(
            rules_version=str(self.p4_rules["version"]),
            source_offer_id=candidate.source_offer.id,
            market_listing_id=candidate.market_listing.id,
        )
        identity_decision_id = self.p4_repo.save_decision(
            p4_run_id=p4_run_id,
            source_offer_id=candidate.source_offer.id,
            market_listing_id=candidate.market_listing.id,
            decision=p4_decision,
        )
        self.audit.record(
            event_type="p4_decision",
            actor="system",
            target_type="identity",
            target_id=identity_decision_id,
            payload=p4_decision.to_dict(),
        )

        profit_input = ProfitInput(
            id=f"profit:{identity_decision_id}",
            p4_decision=p4_decision.decision.value,
            p4_confidence_score=p4_decision.confidence_score,
            p4_requires_human_review=p4_decision.requires_human_review,
            expected_sale_price_yen=candidate.expected_sale_price_yen,
            purchase_price_yen=candidate.source_offer.purchase_price_yen,
            inbound_shipping_yen=candidate.source_offer.domestic_shipping_yen,
            category=candidate.category,
            allocated_budget_yen=candidate.allocated_budget_yen,
        )
        p3_estimate = self.p3_engine.evaluate(profit_input)
        p3_run_id = self.p3_repo.create_run(
            rules_version=str(self.p3_rules["version"]),
            identity_decision_id=identity_decision_id,
            status="skipped" if p3_estimate.decision == "skipped" else "completed",
            skip_reason=";".join(p3_estimate.reasons) if p3_estimate.decision == "skipped" else None,
        )
        profit_estimate_id = self.p3_repo.save_estimate(
            p3_run_id=p3_run_id,
            identity_decision_id=identity_decision_id,
            profit_input=profit_input,
            estimate=p3_estimate,
        )
        self.audit.record(
            event_type="p3_decision",
            actor="system",
            target_type="profit",
            target_id=profit_estimate_id,
            payload={"decision": p3_estimate.decision, "reasons": list(p3_estimate.reasons)},
        )
        purchase_candidate_id = self.candidates.create_from_estimate_if_allowed(
            profit_estimate_id=profit_estimate_id
        )
        if purchase_candidate_id:
            self.audit.record(
                event_type="purchase_candidate_created",
                actor="system",
                target_type="purchase",
                target_id=purchase_candidate_id,
                payload={"status": "pending_review", "requires_human_approval": True},
            )
        return OfflineRunResult(
            identity_decision_id=identity_decision_id,
            p3_run_id=p3_run_id,
            profit_estimate_id=profit_estimate_id,
            purchase_candidate_id=purchase_candidate_id,
            p4_decision=p4_decision.decision.value,
            p3_decision=p3_estimate.decision,
        )
