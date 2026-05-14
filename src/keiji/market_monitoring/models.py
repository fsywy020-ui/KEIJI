"""P5 market monitoring input models.

All records are local observations loaded from CSV/JSON fixtures or manually
prepared files. They are not fetched from live APIs in the initial MVP.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class MarketObservation:
    """One local market observation used by P5/P6."""

    source: str
    observed_at: str
    product_title: str
    jan: str | None = None
    asin: str | None = None
    model_number: str | None = None
    price: int | None = None
    shipping_fee: int = 0
    rank: int | None = None
    category: str = "default"
    stock_status: str = "unknown"
    seller_count: int | None = None
    condition: str = "new"
    url_or_reference: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MarketObservation":
        return cls(
            source=str(data.get("source", "local")),
            observed_at=_observed_at(data.get("observed_at")),
            product_title=str(data["product_title"]),
            jan=_optional_str(data.get("jan")),
            asin=_optional_str(data.get("asin")),
            model_number=_optional_str(data.get("model_number")),
            price=_optional_int(data.get("price")),
            shipping_fee=int(data.get("shipping_fee") or 0),
            rank=_optional_int(data.get("rank")),
            category=str(data.get("category", "default")),
            stock_status=str(data.get("stock_status", "unknown")),
            seller_count=_optional_int(data.get("seller_count")),
            condition=str(data.get("condition", "new")),
            url_or_reference=_optional_str(data.get("url_or_reference")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "observed_at": self.observed_at,
            "product_title": self.product_title,
            "jan": self.jan,
            "asin": self.asin,
            "model_number": self.model_number,
            "price": self.price,
            "shipping_fee": self.shipping_fee,
            "rank": self.rank,
            "category": self.category,
            "stock_status": self.stock_status,
            "seller_count": self.seller_count,
            "condition": self.condition,
            "url_or_reference": self.url_or_reference,
        }


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _optional_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    return int(value)


def _observed_at(value: Any) -> str:
    if value in (None, ""):
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return str(value)
