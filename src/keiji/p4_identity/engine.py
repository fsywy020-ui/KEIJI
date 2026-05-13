"""Offline P4 Product Identity Engine."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from keiji.common.config_loader import load_rule_config
from keiji.p4_identity.brand_matcher import match_brands
from keiji.p4_identity.condition_matcher import match_condition
from keiji.p4_identity.decision import decide_identity
from keiji.p4_identity.identifier_matcher import match_identifiers
from keiji.p4_identity.input_models import IdentityDecision, MarketListing, SourceOffer
from keiji.p4_identity.normalizer import normalize_product_text
from keiji.p4_identity.title_matcher import match_titles
from keiji.p4_identity.variant_matcher import match_variants


class ProductIdentityEngine:
    """Deterministic, offline product identity engine for the initial MVP."""

    def __init__(self, rules: dict[str, Any]) -> None:
        self.rules = rules

    @classmethod
    def from_config_path(cls, config_path: str | Path) -> "ProductIdentityEngine":
        return cls(load_rule_config(config_path))

    def evaluate(self, source_offer: SourceOffer, market_listing: MarketListing) -> IdentityDecision:
        source = normalize_product_text(
            title=source_offer.title,
            brand=source_offer.brand,
            model=source_offer.model,
            jan=source_offer.jan,
            asin=source_offer.asin,
            condition=source_offer.condition,
            rules=self.rules,
        )
        listing = normalize_product_text(
            title=market_listing.title,
            brand=market_listing.brand,
            model=market_listing.model,
            jan=market_listing.jan,
            asin=market_listing.asin,
            condition=market_listing.condition,
            rules=self.rules,
        )
        identifier_result = match_identifiers(source, listing)
        title_result = match_titles(source.title, listing.title)
        brand_result = match_brands(source.brand, listing.brand)
        variant_result = match_variants(source, listing)
        condition_result = match_condition(source.condition, listing.condition, self.rules)
        return decide_identity(
            source=source,
            listing=listing,
            source_purchase_price_yen=source_offer.purchase_price_yen,
            source_domestic_shipping_yen=source_offer.domestic_shipping_yen,
            identifier_result=identifier_result,
            title_result=title_result,
            brand_result=brand_result,
            variant_result=variant_result,
            condition_result=condition_result,
            rules=self.rules,
        )
