"""Conservative local attribute extraction for P4 product identity.

The extractor is intentionally deterministic and offline-only. It extracts only
attributes that can be inferred from manually supplied/local title text and does
not call external services.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ProductAttributes:
    """Machine-readable attributes extracted from local product text."""

    jan_candidates: tuple[str, ...] = field(default_factory=tuple)
    model_candidates: tuple[str, ...] = field(default_factory=tuple)
    capacity: str | None = None
    color: str | None = None
    set_count: int | None = None
    condition: str | None = None
    edition: str | None = None
    domestic_or_import: str | None = None

    def variant_dict(self) -> dict[str, str]:
        """Return variant-critical attributes as comparable string values."""

        variants: dict[str, str] = {}
        for key in ("capacity", "color", "condition", "edition", "domestic_or_import"):
            value = getattr(self, key)
            if value is not None:
                variants[key] = str(value)
        if self.set_count is not None:
            variants["set_count"] = str(self.set_count)
        return variants


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
    "new": ("new", "新品", "未使用"),
    "used": ("used", "中古"),
    "open_box": ("open box", "open_box", "開封済み"),
    "junk": ("junk", "ジャンク", "部品取り"),
}

_MODEL_STOPWORDS = {
    "amazon",
    "sony",
    "nintendo",
    "panasonic",
    "black",
    "white",
    "red",
    "blue",
    "green",
    "yellow",
    "pink",
    "gray",
    "grey",
    "silver",
    "pack",
    "pcs",
}


def extract_product_attributes(text: str) -> ProductAttributes:
    """Extract JAN, model, capacity, color, set count, and condition from text.

    The implementation favors precision over recall. Ambiguous or unsupported
    attributes are omitted so downstream P4 decisions can request human review
    instead of over-asserting identity.
    """

    lower_text = text.lower()
    return ProductAttributes(
        jan_candidates=_extract_jan_candidates(lower_text),
        model_candidates=_extract_model_candidates(lower_text),
        capacity=_first_capacity(lower_text),
        color=_first_alias_match(lower_text, _COLOR_ALIASES),
        set_count=_first_set_count(lower_text),
        condition=_first_alias_match(lower_text, _CONDITION_ALIASES),
        edition=_first_alias_match(lower_text, _EDITION_ALIASES),
        domestic_or_import=_first_alias_match(lower_text, _DOMESTIC_IMPORT_ALIASES),
    )


def _extract_jan_candidates(text: str) -> tuple[str, ...]:
    candidates = re.findall(r"(?<!\d)(?:\d{13}|\d{12}|\d{8})(?!\d)", text)
    return tuple(dict.fromkeys(candidates))


def _extract_model_candidates(text: str) -> tuple[str, ...]:
    normalized = re.sub(r"[^a-z0-9]+", " ", text.lower())
    tokens = normalized.split()
    candidates: list[str] = []
    for token in tokens:
        if token in _MODEL_STOPWORDS or token.isdigit() or len(token) < 3:
            continue
        if any(char.isalpha() for char in token) and any(char.isdigit() for char in token):
            candidates.append(token)
    # Capture common split forms such as "wh 1000xm4" as "wh1000xm4".
    for left, right in zip(tokens, tokens[1:]):
        combined = f"{left}{right}"
        if (
            len(combined) >= 4
            and left not in _MODEL_STOPWORDS
            and right not in _MODEL_STOPWORDS
            and any(char.isalpha() for char in combined)
            and any(char.isdigit() for char in combined)
        ):
            candidates.append(combined)
    return tuple(dict.fromkeys(candidates))


def _first_capacity(text: str) -> str | None:
    match = re.search(r"(\d+(?:\.\d+)?)\s*(tb|gb|mb|ml|l|g|kg)", text)
    if not match:
        return None
    amount, unit = match.groups()
    return f"{amount}{unit}"


def _first_set_count(text: str) -> int | None:
    patterns = (
        r"(\d+)\s*(?:個|本|枚)\s*(?:セット|組|入り|入)",
        r"(\d+)\s*(?:pack|packs|pcs|pieces|set|sets)",
        r"(?:x|×)\s*(\d+)(?!\d)",
    )
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))
    return None


def _first_alias_match(text: str, aliases_by_canonical: dict[str, tuple[str, ...]]) -> str | None:
    for canonical, aliases in aliases_by_canonical.items():
        if any(alias.lower() in text for alias in aliases):
            return canonical
    return None
