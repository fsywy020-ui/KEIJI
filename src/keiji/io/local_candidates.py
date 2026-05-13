"""Local JSON/CSV candidate import for offline operation."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from keiji.pipeline.offline_runner import OfflineCandidateInput


def load_candidates_json(path: str | Path) -> list[OfflineCandidateInput]:
    """Load offline candidates from a JSON array file."""

    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("candidate JSON must be an array")
    return [OfflineCandidateInput.from_dict(item) for item in data]


def load_candidates_csv(path: str | Path) -> list[OfflineCandidateInput]:
    """Load offline candidates from a flat CSV file.

    Expected column prefixes are `source_` and `listing_` for the two P4 sides.
    """

    with Path(path).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return [OfflineCandidateInput.from_dict(_row_to_candidate_dict(row)) for row in rows]


def _row_to_candidate_dict(row: dict[str, str]) -> dict[str, Any]:
    source = {
        "id": row["source_id"],
        "title": row["source_title"],
        "brand": row.get("source_brand") or None,
        "model": row.get("source_model") or None,
        "jan": row.get("source_jan") or None,
        "asin": row.get("source_asin") or None,
        "condition": row.get("source_condition") or "new",
        "purchase_price_yen": int(row["purchase_price_yen"]),
        "domestic_shipping_yen": int(row.get("domestic_shipping_yen") or 0),
    }
    listing = {
        "id": row["listing_id"],
        "marketplace": row.get("marketplace") or "amazon_jp",
        "title": row["listing_title"],
        "brand": row.get("listing_brand") or None,
        "model": row.get("listing_model") or None,
        "jan": row.get("listing_jan") or None,
        "asin": row.get("listing_asin") or None,
        "condition": row.get("listing_condition") or "new",
    }
    return {
        "source_offer": source,
        "market_listing": listing,
        "expected_sale_price_yen": int(row["expected_sale_price_yen"]) if row.get("expected_sale_price_yen") else None,
        "category": row.get("category") or "default",
        "allocated_budget_yen": int(row.get("allocated_budget_yen") or 0),
    }
