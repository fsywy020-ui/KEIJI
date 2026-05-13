"""Normalization helpers for P4 matching."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Any

from keiji.p4_identity.attribute_extractor import ProductAttributes, extract_product_attributes


@dataclass(frozen=True)
class NormalizedProductText:
    """Normalized text fields used by matchers."""

    title: str
    brand: str | None
    model: str | None
    jan: str | None
    asin: str | None
    condition: str
    extracted: ProductAttributes


def normalize_product_text(
    *,
    title: str,
    condition: str,
    rules: dict[str, Any],
    brand: str | None = None,
    model: str | None = None,
    jan: str | None = None,
    asin: str | None = None,
) -> NormalizedProductText:
    """Normalize product fields according to versioned P4 rules."""

    extracted = extract_product_attributes(title)
    return NormalizedProductText(
        title=normalize_text(title, rules),
        brand=normalize_brand(brand, rules),
        model=normalize_identifier(model, rules) or extracted.model,
        jan=normalize_identifier(jan, rules) or extracted.jan,
        asin=normalize_identifier(asin, rules) or extracted.asin,
        condition=normalize_text(condition, rules),
        extracted=extracted,
    )


def normalize_brand(value: str | None, rules: dict[str, Any]) -> str | None:
    normalized = normalize_text(value, rules)
    if normalized is None:
        return None
    aliases = rules.get("normalization", {}).get("brand_aliases", {})
    for canonical, values in aliases.items():
        alias_values = {normalize_text(str(item), rules) for item in values}
        alias_values.add(normalize_text(str(canonical), rules))
        if normalized in alias_values:
            return normalize_text(str(canonical), rules)
    return normalized


def normalize_identifier(value: str | None, rules: dict[str, Any]) -> str | None:
    normalized = normalize_text(value, rules)
    if normalized is None:
        return None
    return re.sub(r"\s+", "", normalized)


def normalize_text(value: str | None, rules: dict[str, Any]) -> str | None:
    if value is None:
        return None
    normalization = rules.get("normalization", {})
    text = str(value).strip()
    if normalization.get("unicode_normalization"):
        text = unicodedata.normalize(str(normalization["unicode_normalization"]), text)
    if normalization.get("lowercase"):
        text = text.lower()
    for symbol in normalization.get("remove_symbols", []):
        text = text.replace(str(symbol), " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text or None
