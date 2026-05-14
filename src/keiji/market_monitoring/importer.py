"""Local CSV/JSON importer for P5 market monitoring."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from keiji.market_monitoring.models import MarketObservation


def load_market_observations(path: str | Path) -> list[MarketObservation]:
    """Load local market observations from a CSV or JSON file."""

    input_path = Path(path)
    suffix = input_path.suffix.lower()
    if suffix == ".csv":
        with input_path.open(newline="", encoding="utf-8") as handle:
            return [MarketObservation.from_dict(row) for row in csv.DictReader(handle)]
    if suffix == ".json":
        payload = json.loads(input_path.read_text(encoding="utf-8"))
        records = payload if isinstance(payload, list) else payload.get("observations", [])
        return [MarketObservation.from_dict(item) for item in records]
    raise ValueError(f"Unsupported market observation format: {input_path.suffix}")
