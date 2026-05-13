"""Local Amazon listing models for adapter interfaces."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AmazonListingSnapshot:
    """Amazon listing data snapshot used by P4/P3 without live calls."""

    asin: str
    title: str
    brand: str | None
    model: str | None
    jan: str | None
    marketplace: str = "amazon_jp"
    buybox_price_yen: int | None = None
    category: str = "default"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AmazonListingSnapshot":
        return cls(
            asin=str(data["asin"]),
            title=str(data["title"]),
            brand=None if data.get("brand") is None else str(data["brand"]),
            model=None if data.get("model") is None else str(data["model"]),
            jan=None if data.get("jan") is None else str(data["jan"]),
            marketplace=str(data.get("marketplace", "amazon_jp")),
            buybox_price_yen=None if data.get("buybox_price_yen") is None else int(data["buybox_price_yen"]),
            category=str(data.get("category", "default")),
        )
