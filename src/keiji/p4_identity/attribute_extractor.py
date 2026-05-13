"""Structured attribute extraction for P4 product identity.

The extractor is deliberately conservative and local-only. It extracts only
attributes that can be recognized deterministically from manually supplied text
or fixture data; uncertain values are left as ``None`` so the downstream P4 gate
can require review instead of guessing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from keiji.p4_identity.normalizer import normalize_identifier, normalize_text


@dataclass(frozen=True)
class ProductAttributes:
    """Conservative product attributes extracted from a source/listing record."""

    jan: str | None = None
    asin: str | None = None
    model: str | None = None
    capacity: str | None = None
    color: str | None = None
    set_count: int | None = None
    condition: str | None = None

    def variant_dict(self) -> dict[str, str]:
        """Return extracted variant-critical fields for comparison."""

        variants: dict[str, str] = {}
        if self.capacity:
            variants["capacity"] = self.capacity
        if self.color:
            variants["color"] = self.color
        if self.set_count is not None:
            variants["quantity"] = str(self.set_count)
        return variants


_DEFAULT_COLOR_ALIASES: dict[str, tuple[str, ...]] = {
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

_CONDITION_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("junk", ("junk", "ジャンク", "故障", "部品取り", "parts only")),
    ("used", ("used", "中古", "使用済", "開封済", "開封品")),
    ("open_box", ("open box", "opened", "未使用に近い", "箱開封")),
    ("new", ("new", "新品", "未使用", "sealed", "未開封")),
)

_JAN_PATTERN = re.compile(r"(?<!\d)(\d{8}|\d{12}|\d{13})(?!\d)")
_ASIN_PATTERN = re.compile(r"(?<![A-Z0-9])([A-Z0-9]{10})(?![A-Z0-9])", re.IGNORECASE)
_CAPACITY_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*(tb|gb|mb|kg|g|ml|l)\b", re.IGNORECASE)
_SET_COUNT_PATTERN = re.compile(r"(\d+)\s*(個入|本入|枚入|個|本|枚|台|袋|セット|set|pack|packs|pcs|pieces)", re.IGNORECASE)
_MODEL_PATTERN = re.compile(
    r"(?<![A-Z0-9])([A-Z]{1,}[A-Z0-9]*[-_][A-Z0-9][A-Z0-9-_]{1,}|[A-Z]{2,}\d[A-Z0-9]{2,}|\d+[A-Z]{2,}[A-Z0-9]*)(?![A-Z0-9])",
    re.IGNORECASE,
)


def extract_product_attributes(
    *,
    title: str,
    rules: dict[str, Any],
    brand: str | None = None,
    model: str | None = None,
    jan: str | None = None,
    asin: str | None = None,
    condition: str | None = None,
) -> ProductAttributes:
    """Extract JAN/ASIN/model/capacity/color/set-count/condition from local text.

    Explicit structured fields take precedence for identifiers. Title extraction
    fills gaps only; it never overwrites manually supplied JAN/ASIN/model values.
    """

    text = " ".join(part for part in [title, brand, model, jan, asin, condition] if part)
    normalized_text = normalize_text(text, rules) or ""
    explicit_jan = normalize_identifier(jan, rules)
    explicit_asin = normalize_identifier(asin, rules)
    explicit_model = normalize_identifier(model, rules)
    explicit_condition = normalize_text(condition, rules)

    extracted_jan = explicit_jan or _extract_jan(normalized_text)
    extracted_asin = explicit_asin or _extract_asin(normalized_text)
    extracted_model = explicit_model or _extract_model(text, rules)
    extracted_capacity = _extract_capacity(normalized_text)
    extracted_color = _extract_color(normalized_text, rules)
    extracted_set_count = _extract_set_count(normalized_text)
    extracted_condition = _extract_condition(normalized_text) or explicit_condition

    return ProductAttributes(
        jan=extracted_jan,
        asin=extracted_asin,
        model=extracted_model,
        capacity=extracted_capacity,
        color=extracted_color,
        set_count=extracted_set_count,
        condition=extracted_condition,
    )


def _extract_jan(text: str) -> str | None:
    match = _JAN_PATTERN.search(text)
    return match.group(1) if match else None


def _extract_asin(text: str) -> str | None:
    for match in _ASIN_PATTERN.finditer(text.upper()):
        value = match.group(1).upper()
        if value.startswith("B0") or value.startswith("B00"):
            return value.lower()
    return None


def _extract_model(text: str, rules: dict[str, Any]) -> str | None:
    candidates: list[str] = []
    for match in _MODEL_PATTERN.finditer(text):
        candidate = match.group(1).strip(" -_")
        if len(candidate) >= 4 and not candidate.isdigit():
            candidates.append(candidate)
    if not candidates:
        return None
    # Prefer the most specific token with digits and separators, otherwise the longest token.
    candidates.sort(key=lambda item: ("-" in item or "_" in item or " " in item, len(item)), reverse=True)
    return normalize_identifier(candidates[0], rules)


def _extract_capacity(text: str) -> str | None:
    match = _CAPACITY_PATTERN.search(text)
    if not match:
        return None
    amount, unit = match.groups()
    return f"{amount}{unit.lower()}"


def _extract_color(text: str, rules: dict[str, Any]) -> str | None:
    color_aliases = rules.get("variant_aliases", {}).get("colors", _DEFAULT_COLOR_ALIASES)
    for canonical, aliases in color_aliases.items():
        if any(str(alias).lower() in text for alias in aliases):
            return str(canonical).lower()
    for canonical, aliases in _DEFAULT_COLOR_ALIASES.items():
        if any(alias.lower() in text for alias in aliases):
            return canonical
    return None


def _extract_set_count(text: str) -> int | None:
    match = _SET_COUNT_PATTERN.search(text)
    if not match:
        return None
    count = int(match.group(1))
    return count if count > 0 else None


def _extract_condition(text: str) -> str | None:
    for canonical, keywords in _CONDITION_KEYWORDS:
        if any(keyword.lower() in text for keyword in keywords):
            return canonical
    return None
