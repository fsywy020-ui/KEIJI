"""Conservative local attribute extraction for P4 product identity.

The extractor intentionally uses deterministic regexes and local alias tables only.
It never calls external services and treats extracted values as supporting evidence,
not as a replacement for explicit manual fields when those fields are present.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ProductAttributes:
    """Product attributes extracted from local text."""

    jan: str | None = None
    asin: str | None = None
    model: str | None = None
    capacity: str | None = None
    color: str | None = None
    set_count: int | None = None
    condition: str | None = None
    edition: str | None = None
    domestic_or_import: str | None = None
    size: str | None = None
    generation: str | None = None
    included_accessories: str | None = None
    bundle_type: str | None = None
    evidence: dict[str, str] = field(default_factory=dict)

    def variants(self) -> dict[str, str]:
        """Return variant-critical attributes used by variant matching."""

        values: dict[str, str] = {}
        if self.capacity:
            values["capacity"] = self.capacity
        if self.color:
            values["color"] = self.color
        if self.set_count is not None:
            values["set_count"] = str(self.set_count)
        if self.edition:
            values["edition"] = self.edition
        if self.domestic_or_import:
            values["domestic_or_import"] = self.domestic_or_import
        if self.size:
            values["size"] = self.size
        if self.generation:
            values["generation"] = self.generation
        if self.included_accessories:
            values["included_accessories"] = self.included_accessories
        if self.bundle_type:
            values["bundle_type"] = self.bundle_type
        return values


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

_CONDITION_ALIASES: dict[str, tuple[str, ...]] = {
    "new": ("new", "新品", "未使用", "未開封"),
    "sealed": ("未開封", "sealed"),
    "damaged_box": ("箱傷み", "箱潰れ", "外箱傷み"),
    "used": ("used", "中古", "使用済み"),
    "open_box": ("open box", "open_box", "開封済み", "開封品"),
    "junk": ("junk", "ジャンク", "部品取り"),
}


def extract_product_attributes(text: str | None) -> ProductAttributes:
    """Extract JAN/ASIN/model/capacity/color/set-count/condition from local text."""

    normalized = _search_text(text)
    if not normalized:
        return ProductAttributes()

    evidence: dict[str, str] = {}
    jan = _first_match(r"(?<!\d)(\d{13}|\d{12}|\d{8})(?!\d)", normalized, evidence, "jan")
    asin = _first_match(r"\b(b[0-9a-z]{9})\b", normalized, evidence, "asin")
    model = _extract_model(normalized, evidence)
    capacity = _extract_capacity(normalized, evidence)
    set_count = _extract_set_count(normalized, evidence)
    color = _extract_alias(normalized, _COLOR_ALIASES, evidence, "color")
    condition = _extract_alias(normalized, _CONDITION_ALIASES, evidence, "condition")
    edition = _extract_alias(normalized, _EDITION_ALIASES, evidence, "edition")
    domestic_or_import = _extract_alias(normalized, _DOMESTIC_IMPORT_ALIASES, evidence, "domestic_or_import")
    size = _extract_size(normalized, evidence)
    generation = _extract_generation(normalized, evidence)
    included_accessories = _extract_accessories(normalized, evidence)
    bundle_type = _extract_bundle_type(normalized, evidence)
    return ProductAttributes(
        jan=jan,
        asin=asin,
        model=model,
        capacity=capacity,
        color=color,
        set_count=set_count,
        condition=condition,
        edition=edition,
        domestic_or_import=domestic_or_import,
        size=size,
        generation=generation,
        included_accessories=included_accessories,
        bundle_type=bundle_type,
        evidence=evidence,
    )


def _search_text(text: str | None) -> str:
    if text is None:
        return ""
    normalized = unicodedata.normalize("NFKC", str(text)).lower()
    return re.sub(r"\s+", " ", normalized).strip()


def _first_match(pattern: str, text: str, evidence: dict[str, str], key: str) -> str | None:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if not match:
        return None
    value = match.group(1).lower()
    evidence[key] = value
    return value


def _extract_model(text: str, evidence: dict[str, str]) -> str | None:
    labeled = re.search(r"(?:model|型番|品番)\s*[:：]?\s*([a-z0-9][a-z0-9_-]{2,})", text, flags=re.IGNORECASE)
    if labeled:
        value = _normalize_model(labeled.group(1))
        evidence["model"] = value
        return value

    structured = re.search(r"\b([a-z0-9]+-[a-z0-9-]*\d[a-z0-9-]*)\b", text, flags=re.IGNORECASE)
    if structured:
        value = _normalize_model(structured.group(1))
        evidence["model"] = value
        return value
    return None


def _normalize_model(value: str) -> str:
    return re.sub(r"[\s_-]+", "", value.lower())


def _extract_capacity(text: str, evidence: dict[str, str]) -> str | None:
    match = re.search(r"(\d+(?:\.\d+)?)\s*(tb|gb|mb|ml|l|g|kg)\b", text, flags=re.IGNORECASE)
    if not match:
        return None
    amount, unit = match.groups()
    value = f"{amount}{unit.lower()}"
    evidence["capacity"] = value
    return value


def _extract_set_count(text: str, evidence: dict[str, str]) -> int | None:
    match = re.search(r"(\d+)\s*(個入|本入|枚入|個|本|枚|セット|packs|pack|pcs|pieces|piece)", text, flags=re.IGNORECASE)
    if not match:
        return None
    value = int(match.group(1))
    evidence["set_count"] = str(value)
    return value


def _extract_alias(text: str, aliases: dict[str, tuple[str, ...]], evidence: dict[str, str], key: str) -> str | None:
    for canonical, values in aliases.items():
        if any(alias.lower() in text for alias in values):
            evidence[key] = canonical
            return canonical
    return None


def _extract_size(text: str, evidence: dict[str, str]) -> str | None:
    match = re.search(r"\b(xs|s|m|l|xl|xxl)サイズ?\b|サイズ\s*[:：]?\s*(xs|s|m|l|xl|xxl)", text, flags=re.IGNORECASE)
    if not match:
        return None
    value = next(group for group in match.groups() if group).lower()
    evidence["size"] = value
    return value


def _extract_generation(text: str, evidence: dict[str, str]) -> str | None:
    if any(token in text for token in ("新モデル", "最新版", "2024", "2025", "2026")):
        evidence["generation"] = "new_model"
        return "new_model"
    if any(token in text for token in ("旧モデル", "型落ち", "2020", "2021", "2022")):
        evidence["generation"] = "old_model"
        return "old_model"
    return None


def _extract_accessories(text: str, evidence: dict[str, str]) -> str | None:
    if any(token in text for token in ("付属品なし", "本体のみ", "ケーブルなし", "箱なし")):
        evidence["included_accessories"] = "missing"
        return "missing"
    if any(token in text for token in ("付属品あり", "付属品完備", "完品", "箱付き")):
        evidence["included_accessories"] = "included"
        return "included"
    return None


def _extract_bundle_type(text: str, evidence: dict[str, str]) -> str | None:
    if any(token in text for token in ("まとめ売り", "セット売り")):
        evidence["bundle_type"] = "bundle"
        return "bundle"
    if any(token in text for token in ("単品", "1点", "1個")):
        evidence["bundle_type"] = "single"
        return "single"
    return None
