"""Variant extraction and matching for P4 product identity."""

from __future__ import annotations

from dataclasses import dataclass

from keiji.p4_identity.attribute_extractor import extract_product_attributes
from keiji.p4_identity.normalizer import NormalizedProductText


@dataclass(frozen=True)
class VariantMatchResult:
    """Variant comparison result."""

    score: float
    status: str
    evidence_code: str
    message: str
    source_variants: dict[str, str]
    listing_variants: dict[str, str]


_COLOR_ALIASES: dict[str, tuple[str, ...]] = {
    "black": ("black", "ブラック", "黒"),
    "white": ("white", "ホワイト", "白"),
    "red": ("red", "レッド", "赤"),
    "blue": ("blue", "ブルー", "青"),
    "green": ("green", "グリーン", "緑"),
    "yellow": ("yellow", "イエロー", "黄色"),
    "pink": ("pink", "ピンク"),
    "gray": ("gray", "grey", "グレー", "灰"),
    "silver": ("silver", "シルバー", "銀"),
}

_EDITION_ALIASES: dict[str, tuple[str, ...]] = {
    "limited": ("limited", "限定", "初回限定"),
    "standard": ("standard", "通常版", "標準"),
    "oled": ("oled", "有機el"),
    "lite": ("lite", "ライト"),
}

_DOMESTIC_IMPORT_ALIASES: dict[str, tuple[str, ...]] = {
    "domestic": ("国内", "日本版", "国内正規"),
    "import": ("海外", "輸入", "並行輸入", "import"),
}


def extract_variants(text: str) -> dict[str, str]:
    """Extract conservative variant attributes from normalized text."""

    variants: dict[str, str] = {}
    lower_text = text.lower()
    for canonical, aliases in _COLOR_ALIASES.items():
        if any(alias.lower() in lower_text for alias in aliases):
            variants["color"] = canonical
            break
    for canonical, aliases in _EDITION_ALIASES.items():
        if any(alias.lower() in lower_text for alias in aliases):
            variants["edition"] = canonical
            break
    for canonical, aliases in _DOMESTIC_IMPORT_ALIASES.items():
        if any(alias.lower() in lower_text for alias in aliases):
            variants["domestic_or_import"] = canonical
            break

    extracted = extract_product_attributes(title=text, rules={})
    variants.update(extracted.variant_dict())

    return variants


def match_variants(source: NormalizedProductText, listing: NormalizedProductText) -> VariantMatchResult:
    """Compare extracted variants and flag conflicts conservatively."""

    source_variants = extract_variants(source.title)
    listing_variants = extract_variants(listing.title)
    compared_keys = set(source_variants) | set(listing_variants)
    conflicts = [
        key
        for key in compared_keys
        if key in source_variants and key in listing_variants and source_variants[key] != listing_variants[key]
    ]
    if conflicts:
        return VariantMatchResult(
            score=0.0,
            status="conflict",
            evidence_code="variant_conflict",
            message=f"Variant conflict detected: {', '.join(sorted(conflicts))}.",
            source_variants=source_variants,
            listing_variants=listing_variants,
        )

    missing = [key for key in compared_keys if key not in source_variants or key not in listing_variants]
    if missing:
        return VariantMatchResult(
            score=0.5,
            status="missing",
            evidence_code="variant_missing",
            message=f"Variant information is missing on one side: {', '.join(sorted(missing))}.",
            source_variants=source_variants,
            listing_variants=listing_variants,
        )

    if compared_keys:
        return VariantMatchResult(
            score=1.0,
            status="match",
            evidence_code="variant_match",
            message="Extracted variant attributes match.",
            source_variants=source_variants,
            listing_variants=listing_variants,
        )

    return VariantMatchResult(
        score=1.0,
        status="not_detected",
        evidence_code="variant_not_detected",
        message="No variant-specific attributes were detected.",
        source_variants=source_variants,
        listing_variants=listing_variants,
    )
