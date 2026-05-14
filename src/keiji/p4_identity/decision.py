"""Decision logic for the P4 Product Identity Engine."""

from __future__ import annotations

from typing import Any

from keiji.common.enums import IdentityDecisionValue
from keiji.p4_identity.brand_matcher import BrandMatchResult
from keiji.p4_identity.condition_matcher import ConditionMatchResult
from keiji.p4_identity.identifier_matcher import IdentifierMatchResult
from keiji.p4_identity.exclusion_rules import evaluate_exclusions
from keiji.p4_identity.input_models import IdentityDecision, IdentityEvidence, IdentityScores
from keiji.p4_identity.title_matcher import TitleMatchResult
from keiji.p4_identity.variant_matcher import VariantMatchResult
from keiji.p4_identity.normalizer import NormalizedProductText
from keiji.p4_identity.scoring import calculate_match_score


def decide_identity(
    *,
    source: NormalizedProductText,
    listing: NormalizedProductText,
    source_purchase_price_yen: int,
    source_domestic_shipping_yen: int,
    identifier_result: IdentifierMatchResult,
    title_result: TitleMatchResult,
    brand_result: BrandMatchResult,
    variant_result: VariantMatchResult,
    condition_result: ConditionMatchResult,
    rules: dict[str, Any],
) -> IdentityDecision:
    """Create the final conservative P4 identity decision."""

    exclusion_result = evaluate_exclusions(
        source=source,
        listing=listing,
        source_purchase_price_yen=source_purchase_price_yen,
        source_domestic_shipping_yen=source_domestic_shipping_yen,
        rules=rules,
    )
    if exclusion_result.blocked:
        return _decision(
            IdentityDecisionValue.BLOCKED,
            confidence=1.0,
            review=True,
            identifier_score=identifier_result.score,
            brand_score=brand_result.score,
            title_score=title_result.score,
            variant_score=variant_result.score,
            condition_score=condition_result.score,
            evidence=exclusion_result.evidence,
            block_reason=exclusion_result.block_reason,
            rules=rules,
        )

    if condition_result.status == "blocked":
        evidence = (IdentityEvidence(condition_result.evidence_code, condition_result.message, "error"),)
        return _decision(
            IdentityDecisionValue.BLOCKED,
            confidence=1.0,
            review=True,
            identifier_score=identifier_result.score,
            title_score=title_result.score,
            variant_score=variant_result.score,
            condition_score=condition_result.score,
            evidence=evidence,
            block_reason=condition_result.evidence_code,
            rules=rules,
        )

    if identifier_result.status == "conflict":
        return _decision(
            IdentityDecisionValue.DIFFERENT,
            confidence=1.0,
            review=False,
            identifier_score=0.0,
            title_score=title_result.score,
            variant_score=variant_result.score,
            condition_score=condition_result.score,
            evidence=(IdentityEvidence(identifier_result.code, identifier_result.message, "error"),),
            rules=rules,
        )

    if source.model and listing.model and source.model != listing.model:
        return _decision(
            IdentityDecisionValue.AMBIGUOUS,
            confidence=0.7,
            review=True,
            identifier_score=identifier_result.score,
            brand_score=brand_result.score,
            title_score=title_result.score,
            variant_score=variant_result.score,
            condition_score=condition_result.score,
            evidence=(IdentityEvidence("model_conflict", "Model number differs even though a stronger identifier may match; human verification is required.", "warning"),),
            rules=rules,
        )

    if variant_result.status == "conflict":
        return _decision(
            IdentityDecisionValue.AMBIGUOUS,
            confidence=0.7,
            review=True,
            identifier_score=identifier_result.score,
            title_score=title_result.score,
            variant_score=variant_result.score,
            condition_score=condition_result.score,
            evidence=(IdentityEvidence(variant_result.evidence_code, variant_result.message, "warning"),),
            rules=rules,
        )

    if identifier_result.status == "missing":
        return _decision(
            IdentityDecisionValue.AMBIGUOUS,
            confidence=0.5,
            review=True,
            identifier_score=0.0,
            title_score=title_result.score,
            variant_score=variant_result.score,
            condition_score=condition_result.score,
            evidence=(IdentityEvidence(identifier_result.code, identifier_result.message, "warning"),),
            rules=rules,
        )

    if brand_result.status == "conflict":
        return _decision(
            IdentityDecisionValue.AMBIGUOUS,
            confidence=0.75,
            review=True,
            identifier_score=identifier_result.score,
            brand_score=brand_result.score,
            title_score=title_result.score,
            variant_score=variant_result.score,
            condition_score=condition_result.score,
            evidence=(IdentityEvidence(brand_result.evidence_code, brand_result.message, "warning"),),
            rules=rules,
        )

    brand_score = brand_result.score
    model_bonus = 0.05 if source.model and source.model == listing.model else 0.0
    confidence = min(1.0, identifier_result.score + model_bonus)
    evidence: list[IdentityEvidence] = [
        IdentityEvidence(identifier_result.code, identifier_result.message, "info"),
        IdentityEvidence(brand_result.evidence_code, brand_result.message, "info" if brand_result.status == "match" else "warning"),
    ]

    if variant_result.status == "missing":
        confidence = min(confidence, 0.85)
        evidence.append(IdentityEvidence(variant_result.evidence_code, variant_result.message, "warning"))
    elif variant_result.status == "match":
        evidence.append(IdentityEvidence(variant_result.evidence_code, variant_result.message, "info"))

    if condition_result.status == "review":
        confidence = min(confidence, 0.85)
        evidence.append(IdentityEvidence(condition_result.evidence_code, condition_result.message, "warning"))

    same_threshold = float(rules.get("scoring", {}).get("thresholds", {}).get("same_min_confidence", 0.9))
    review = confidence < same_threshold
    if review:
        evidence.append(IdentityEvidence("confidence_below_same_threshold", "Identity evidence is below the same-product threshold.", "warning"))
        return _decision(
            IdentityDecisionValue.AMBIGUOUS,
            confidence=confidence,
            review=True,
            identifier_score=identifier_result.score,
            brand_score=brand_score,
            title_score=title_result.score,
            variant_score=variant_result.score,
            condition_score=condition_result.score,
            evidence=tuple(evidence),
            rules=rules,
        )

    return _decision(
        IdentityDecisionValue.SAME,
        confidence=confidence,
        review=False,
        identifier_score=identifier_result.score,
        brand_score=brand_score,
        title_score=title_result.score,
        variant_score=variant_result.score,
        condition_score=condition_result.score,
        evidence=tuple(evidence),
        rules=rules,
    )


def _decision(
    decision: IdentityDecisionValue,
    *,
    confidence: float,
    review: bool,
    identifier_score: float,
    brand_score: float = 0.0,
    title_score: float = 0.0,
    variant_score: float = 1.0,
    condition_score: float = 1.0,
    evidence: tuple[IdentityEvidence, ...],
    block_reason: str | None = None,
    rules: dict[str, Any] | None = None,
) -> IdentityDecision:
    match_score = calculate_match_score(
        identifier_score=identifier_score,
        brand_score=brand_score,
        title_score=title_score,
        variant_score=variant_score,
        condition_score=condition_score,
        rules=rules,
    )
    return IdentityDecision(
        decision=decision,
        confidence_score=round(confidence, 4),
        requires_human_review=review,
        scores=IdentityScores(
            identifier_score=identifier_score,
            brand_score=brand_score,
            title_score=title_score,
            variant_score=variant_score,
            condition_score=condition_score,
            match_score=match_score,
        ),
        evidence=evidence,
        block_reason=block_reason,
    )
