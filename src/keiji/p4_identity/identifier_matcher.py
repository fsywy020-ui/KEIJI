"""Identifier matching for P4 product identity."""

from __future__ import annotations

from dataclasses import dataclass

from keiji.p4_identity.normalizer import NormalizedProductText


@dataclass(frozen=True)
class IdentifierMatchResult:
    """Identifier comparison result."""

    score: float
    status: str
    code: str
    message: str


def match_identifiers(source: NormalizedProductText, listing: NormalizedProductText) -> IdentifierMatchResult:
    """Compare strong identifiers with conservative conflict handling."""

    source_jans = _identifier_values(source.jan, source.jan_candidates)
    listing_jans = _identifier_values(listing.jan, listing.jan_candidates)
    if source_jans and listing_jans:
        if source_jans & listing_jans:
            return IdentifierMatchResult(1.0, "match", "jan_match", "JAN/EAN/UPC matches exactly or via extracted title candidate.")
        if source.jan and listing.jan:
            return IdentifierMatchResult(0.0, "conflict", "jan_conflict", "JAN/EAN/UPC conflicts.")

    if source.asin and listing.asin:
        if source.asin == listing.asin:
            return IdentifierMatchResult(0.95, "match", "asin_match", "ASIN matches exactly.")
        return IdentifierMatchResult(0.0, "conflict", "asin_conflict", "ASIN conflicts.")

    source_models = _identifier_values(source.model, source.model_candidates)
    listing_models = _identifier_values(listing.model, listing.model_candidates)
    if source_models and listing_models:
        if source_models & listing_models:
            if source.model and listing.model:
                return IdentifierMatchResult(0.85, "match", "model_match", "Model number matches exactly.")
            return IdentifierMatchResult(0.75, "match", "model_candidate_match", "Model number matches via extracted title candidate.")
        if source.model and listing.model:
            return IdentifierMatchResult(0.0, "conflict", "model_conflict", "Model number conflicts.")

    return IdentifierMatchResult(0.0, "missing", "identifier_missing", "Strong identifiers are missing or incomplete.")


def _identifier_values(primary: str | None, candidates: tuple[str, ...]) -> set[str]:
    values = set(candidates)
    if primary:
        values.add(primary)
    return values
