"""Hard rejection rules for P4 product identity."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from keiji.common.money import total_purchase_amount_yen
from keiji.p4_identity.input_models import IdentityEvidence
from keiji.p4_identity.normalizer import NormalizedProductText


@dataclass(frozen=True)
class ExclusionResult:
    """Result of applying immediate block rules."""

    blocked: bool
    evidence: tuple[IdentityEvidence, ...]
    block_reason: str | None = None


def evaluate_exclusions(
    *,
    source: NormalizedProductText,
    listing: NormalizedProductText,
    source_purchase_price_yen: int,
    source_domestic_shipping_yen: int,
    rules: dict[str, Any],
) -> ExclusionResult:
    """Evaluate hard rejection conditions before normal identity scoring."""

    keyword_evidence = _blocked_keyword_evidence(source, listing, rules)
    if keyword_evidence:
        return ExclusionResult(True, keyword_evidence, keyword_evidence[0].code)

    max_sku_amount = int(rules.get("budgets", {}).get("max_purchase_amount_per_sku_yen", 5000))
    purchase_total = total_purchase_amount_yen(source_purchase_price_yen, source_domestic_shipping_yen)
    if purchase_total > max_sku_amount:
        evidence = (
            IdentityEvidence(
                "per_sku_limit_exceeded",
                f"Purchase amount {purchase_total} JPY exceeds per-SKU limit {max_sku_amount} JPY.",
                "error",
            ),
        )
        return ExclusionResult(True, evidence, "per_sku_limit_exceeded")

    return ExclusionResult(False, ())


def _blocked_keyword_evidence(
    source: NormalizedProductText, listing: NormalizedProductText, rules: dict[str, Any]
) -> tuple[IdentityEvidence, ...]:
    text = " ".join(part for part in [source.title, listing.title] if part)
    evidence = []
    for keyword in rules.get("exclusion_keywords", {}).get("blocked", []):
        keyword_text = str(keyword).lower()
        if keyword_text and keyword_text in text:
            evidence.append(IdentityEvidence("blocked_keyword", f"Blocked keyword detected: {keyword}", "error"))
    return tuple(evidence)
