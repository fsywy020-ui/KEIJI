"""Brand matching for P4 product identity."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BrandMatchResult:
    """Conservative brand comparison result."""

    score: float
    status: str
    evidence_code: str
    message: str


def match_brands(source_brand: str | None, listing_brand: str | None) -> BrandMatchResult:
    """Compare normalized brands without allowing brand-only identity success."""

    if source_brand and listing_brand:
        if source_brand == listing_brand:
            return BrandMatchResult(1.0, "match", "brand_match", "Brand matches after normalization.")
        return BrandMatchResult(0.0, "conflict", "brand_conflict", "Brand conflicts after normalization.")
    return BrandMatchResult(0.0, "missing", "brand_missing", "Brand is missing on one or both sides.")
