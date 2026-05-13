"""Validation for local candidate CSV/JSON inputs."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REQUIRED_CSV_COLUMNS = (
    "source_id",
    "source_title",
    "source_condition",
    "purchase_price_yen",
    "domestic_shipping_yen",
    "listing_id",
    "marketplace",
    "listing_title",
    "listing_condition",
    "expected_sale_price_yen",
    "category",
)


@dataclass(frozen=True)
class ValidationIssue:
    """One input validation issue."""

    severity: str
    location: str
    message: str


@dataclass(frozen=True)
class ValidationResult:
    """Validation result for a local candidate input file."""

    issues: tuple[ValidationIssue, ...]

    @property
    def ok(self) -> bool:
        return not any(issue.severity == "error" for issue in self.issues)

    def format_text(self) -> str:
        if not self.issues:
            return "OK: no validation issues"
        return "\n".join(f"{issue.severity.upper()} {issue.location}: {issue.message}" for issue in self.issues)


def validate_candidate_file(path: str | Path) -> ValidationResult:
    """Validate a local candidate JSON or CSV file."""

    input_path = Path(path)
    if input_path.suffix.lower() == ".json":
        return validate_candidate_json(input_path)
    return validate_candidate_csv(input_path)


def validate_candidate_csv(path: str | Path) -> ValidationResult:
    """Validate flat CSV candidate input before offline batch execution."""

    issues: list[ValidationIssue] = []
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = tuple(reader.fieldnames or ())
        for column in REQUIRED_CSV_COLUMNS:
            if column not in fieldnames:
                issues.append(ValidationIssue("error", "header", f"missing required column: {column}"))
        for index, row in enumerate(reader, start=2):
            _validate_row(row, f"row {index}", issues)
    return ValidationResult(tuple(issues))


def validate_candidate_json(path: str | Path) -> ValidationResult:
    """Validate JSON candidate input before offline batch execution."""

    issues: list[ValidationIssue] = []
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        return ValidationResult((ValidationIssue("error", "json", "top-level value must be an array"),))
    for index, item in enumerate(data):
        location = f"item {index}"
        if not isinstance(item, dict):
            issues.append(ValidationIssue("error", location, "candidate must be an object"))
            continue
        source = item.get("source_offer")
        listing = item.get("market_listing")
        if not isinstance(source, dict):
            issues.append(ValidationIssue("error", location, "source_offer object is required"))
            continue
        if not isinstance(listing, dict):
            issues.append(ValidationIssue("error", location, "market_listing object is required"))
            continue
        row = {
            "source_id": source.get("id"),
            "source_title": source.get("title"),
            "source_condition": source.get("condition"),
            "purchase_price_yen": source.get("purchase_price_yen"),
            "domestic_shipping_yen": source.get("domestic_shipping_yen", 0),
            "listing_id": listing.get("id"),
            "marketplace": listing.get("marketplace", "amazon_jp"),
            "listing_title": listing.get("title"),
            "listing_condition": listing.get("condition"),
            "expected_sale_price_yen": item.get("expected_sale_price_yen"),
            "category": item.get("category", "default"),
        }
        _validate_row(row, location, issues)
    return ValidationResult(tuple(issues))


def _validate_row(row: dict[str, Any], location: str, issues: list[ValidationIssue]) -> None:
    for column in REQUIRED_CSV_COLUMNS:
        if row.get(column) in {None, ""}:
            issues.append(ValidationIssue("error", location, f"{column} is required"))
    for column in ("purchase_price_yen", "domestic_shipping_yen", "expected_sale_price_yen"):
        value = row.get(column)
        if value in {None, ""}:
            continue
        try:
            numeric_value = int(value)
        except (TypeError, ValueError):
            issues.append(ValidationIssue("error", location, f"{column} must be an integer yen amount"))
            continue
        if numeric_value < 0:
            issues.append(ValidationIssue("error", location, f"{column} must be non-negative"))
    purchase = _safe_int(row.get("purchase_price_yen"))
    shipping = _safe_int(row.get("domestic_shipping_yen"))
    if purchase is not None and shipping is not None and purchase + shipping > 5000:
        issues.append(ValidationIssue("warning", location, "source-side total exceeds 5,000 JPY SKU cap"))
    source_jan = str(row.get("source_jan") or "").strip()
    listing_jan = str(row.get("listing_jan") or "").strip()
    if not source_jan and not listing_jan:
        issues.append(ValidationIssue("warning", location, "JAN missing on both source and listing"))


def _safe_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
