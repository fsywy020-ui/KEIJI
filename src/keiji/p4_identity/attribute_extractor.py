"""Conservative local product attribute extraction for P4 identity checks."""

from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any


@dataclass(frozen=True)
class ProductAttributes:
    """Machine-readable attributes extracted from normalized local product text."""

    jan: str | None = None
    model: str | None = None
    capacity: str | None = None
    color: str | None = None
    set_count: str | None = None
    edition: str | None = None
    domestic_or_import: str | None = None
    condition: str | None = None

    def as_variants(self) -> dict[str, str]:
        """Return attributes that should participate in variant comparison."""

        variants: dict[str, str] = {}
        if self.capacity:
            variants["capacity"] = self.capacity
        if self.color:
            variants["color"] = self.color
        if self.set_count:
            variants["quantity"] = self.set_count
        if self.edition:
            variants["edition"] = self.edition
        if self.domestic_or_import:
            variants["domestic_or_import"] = self.domestic_or_import
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

_DEFAULT_EDITION_ALIASES: dict[str, tuple[str, ...]] = {
    "limited": ("limited", "限定", "初回限定"),
    "standard": ("standard", "通常版", "標準"),
    "oled": ("oled", "有機el"),
    "lite": ("lite", "ライト"),
}

_DEFAULT_DOMESTIC_IMPORT_ALIASES: dict[str, tuple[str, ...]] = {
    "domestic": ("国内", "日本版", "国内正規"),
    "import": ("海外", "輸入", "並行輸入", "import"),
}

_DEFAULT_CONDITION_KEYWORDS: dict[str, tuple[str, ...]] = {
    "new": ("new", "新品", "未使用", "未開封"),
    "used": ("used", "中古"),
    "open_box": ("open box", "openbox", "開封済み", "開封品"),
    "junk": ("junk", "ジャンク", "部品取り"),
}

_DEFAULT_MODEL_PATTERNS: tuple[str, ...] = (
    r"\b[a-z]{1,8}\d[a-z0-9]{2,}\b",
    r"\b[a-z]{1,8}\s+\d[a-z0-9]{2,}\b",
    r"\b[a-z]{1,6}\d{1,5}[a-z]{0,4}\b",
)


_JAN_PATTERN = re.compile(r"(?<!\d)(\d{8}|\d{12,14})(?!\d)")
_CAPACITY_PATTERN = re.compile(r"(?<![a-z0-9])(\d+(?:\.\d+)?)\s*(tb|gb|mb|ml|l|kg|g)(?![a-z])")
_SET_COUNT_PATTERN = re.compile(r"(?<!\d)(\d+)\s*(?:個セット|点セット|本セット|枚セット|セット|個入|本入|枚入|pack|packs|pcs)(?![a-z])")


def extract_product_attributes(
    title: str,
    *,
    explicit_jan: str | None = None,
    explicit_model: str | None = None,
    explicit_condition: str | None = None,
    rules: dict[str, Any] | None = None,
) -> ProductAttributes:
    """Extract JAN/model/capacity/color/set-count/condition from normalized local text.

    Explicit structured fields win for identifiers. For condition, title-derived unsafe
    terms such as used/open-box/junk can override a default-looking ``new`` value.
    Uncertain values are left as ``None`` so later P4 logic can request review
    instead of over-matching.
    """

    rule_block = (rules or {}).get("attribute_extraction", {})
    text = title.lower()
    title_condition = _extract_alias(text, rule_block.get("condition_keywords", _DEFAULT_CONDITION_KEYWORDS))
    return ProductAttributes(
        jan=_first_non_empty(explicit_jan, _extract_jan(text)),
        model=_first_non_empty(explicit_model, _extract_model(text, rule_block)),
        capacity=_extract_capacity(text),
        color=_extract_alias(text, rule_block.get("color_aliases", _DEFAULT_COLOR_ALIASES)),
        set_count=_extract_set_count(text),
        edition=_extract_alias(text, rule_block.get("edition_aliases", _DEFAULT_EDITION_ALIASES)),
        domestic_or_import=_extract_alias(
            text,
            rule_block.get("domestic_import_aliases", _DEFAULT_DOMESTIC_IMPORT_ALIASES),
        ),
        condition=_merge_condition(explicit_condition, title_condition),
    )


def _merge_condition(explicit_condition: str | None, title_condition: str | None) -> str | None:
    """Prefer title-derived unsafe condition over a default-looking explicit new value."""

    explicit = _first_non_empty(explicit_condition)
    title = _first_non_empty(title_condition)
    if title in {"used", "open_box", "junk"} and explicit in {None, "", "new"}:
        return title
    return _first_non_empty(explicit, title)


def _first_non_empty(*values: str | None) -> str | None:
    for value in values:
        if value:
            stripped = str(value).strip()
            if stripped:
                return stripped
    return None


def _extract_jan(text: str) -> str | None:
    for match in _JAN_PATTERN.finditer(text):
        candidate = match.group(1)
        if len(candidate) in {8, 12, 13, 14}:
            return candidate
    return None


def _extract_model(text: str, rule_block: dict[str, Any]) -> str | None:
    patterns = tuple(str(pattern) for pattern in rule_block.get("model_patterns", _DEFAULT_MODEL_PATTERNS))
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            candidate = re.sub(r"\s+", "", match.group(0))
            if _looks_like_model(candidate):
                return candidate
    return None


def _looks_like_model(candidate: str) -> bool:
    if candidate.isdigit():
        return False
    if re.fullmatch(r"\d+(?:tb|gb|mb|ml|l|kg|g)", candidate):
        return False
    return bool(re.search(r"[a-z]", candidate) and re.search(r"\d", candidate))


def _extract_capacity(text: str) -> str | None:
    match = _CAPACITY_PATTERN.search(text)
    if not match:
        return None
    amount, unit = match.groups()
    return f"{_normalize_decimal(amount)}{unit.lower()}"


def _extract_set_count(text: str) -> str | None:
    match = _SET_COUNT_PATTERN.search(text)
    if not match:
        return None
    return match.group(1)


def _extract_alias(text: str, aliases: dict[str, Any]) -> str | None:
    for canonical, values in aliases.items():
        normalized_values = tuple(str(value).lower() for value in values)
        if any(value and value in text for value in normalized_values):
            return str(canonical)
    return None


def _normalize_decimal(value: str) -> str:
    try:
        decimal = Decimal(value)
    except InvalidOperation:
        return value
    if decimal == decimal.to_integral_value():
        return str(int(decimal))
    return format(decimal.normalize(), "f")
