"""P4 persistence repository."""

from __future__ import annotations

import json
import sqlite3
from uuid import uuid4

from keiji.p4_identity.input_models import IdentityDecision, MarketListing, SourceOffer


class P4Repository:
    """Persist source offers, listings, P4 runs, and identity decisions."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def save_source_offer(self, offer: SourceOffer) -> str:
        self.connection.execute(
            """
            INSERT OR REPLACE INTO source_offers
            (id, title, brand, model, jan, asin, condition, purchase_price_yen, domestic_shipping_yen)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                offer.id,
                offer.title,
                offer.brand,
                offer.model,
                offer.jan,
                offer.asin,
                offer.condition,
                offer.purchase_price_yen,
                offer.domestic_shipping_yen,
            ),
        )
        self.connection.commit()
        return offer.id

    def save_market_listing(self, listing: MarketListing) -> str:
        self.connection.execute(
            """
            INSERT OR REPLACE INTO market_listings
            (id, marketplace, title, brand, model, jan, asin, condition)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                listing.id,
                listing.marketplace,
                listing.title,
                listing.brand,
                listing.model,
                listing.jan,
                listing.asin,
                listing.condition,
            ),
        )
        self.connection.commit()
        return listing.id

    def create_run(self, *, rules_version: str, source_offer_id: str, market_listing_id: str) -> str:
        run_id = str(uuid4())
        self.connection.execute(
            """
            INSERT INTO p4_identity_runs (id, rules_version, source_offer_id, market_listing_id, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (run_id, rules_version, source_offer_id, market_listing_id, "completed"),
        )
        self.connection.commit()
        return run_id

    def save_decision(
        self,
        *,
        p4_run_id: str,
        source_offer_id: str,
        market_listing_id: str,
        decision: IdentityDecision,
    ) -> str:
        decision_id = str(uuid4())
        payload = decision.to_dict()
        self.connection.execute(
            """
            INSERT INTO product_identity_decisions
            (id, p4_run_id, source_offer_id, market_listing_id, decision, confidence_score,
             match_score, identifier_score, title_score, brand_score, variant_score, condition_score,
             block_reason, explanation_json, requires_human_review)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                decision_id,
                p4_run_id,
                source_offer_id,
                market_listing_id,
                decision.decision.value,
                decision.confidence_score,
                decision.scores.match_score,
                decision.scores.identifier_score,
                decision.scores.title_score,
                decision.scores.brand_score,
                decision.scores.variant_score,
                decision.scores.condition_score,
                decision.block_reason,
                json.dumps(payload, ensure_ascii=False, sort_keys=True),
                int(decision.requires_human_review),
            ),
        )
        self.connection.commit()
        return decision_id

    def get_decision(self, decision_id: str) -> sqlite3.Row:
        row = self.connection.execute("SELECT * FROM product_identity_decisions WHERE id = ?", (decision_id,)).fetchone()
        if row is None:
            raise KeyError(decision_id)
        return row
