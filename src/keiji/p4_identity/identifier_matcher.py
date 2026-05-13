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

    if source.jan and listing.jan:
        if source.jan == listing.jan:
            return IdentifierMatchResult(1.0, "match", "jan_match", "JAN/EAN/UPC matches exactly.")
        return IdentifierMatchResult(0.0, "conflict", "jan_conflict", "JAN/EAN/UPC conflicts.")

    if source.asin and listing.asin:
        if source.asin == listing.asin:
            return IdentifierMatchResult(0.95, "match", "asin_match", "ASIN matches exactly.")
        return IdentifierMatchResult(0.0, "conflict", "asin_conflict", "ASIN conflicts.")

    if source.model and listing.model:
        if source.model == listing.model:
            return IdentifierMatchResult(0.85, "match", "model_match", "Model number matches exactly.")
        return IdentifierMatchResult(0.0, "conflict", "model_conflict", "Model number conflicts.")

    return IdentifierMatchResult(0.0, "missing", "identifier_missing", "Strong identifiers are missing or incomplete.")
