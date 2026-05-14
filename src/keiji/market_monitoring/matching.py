"""Safe local matching for P5 market observations.

Identifier matching is intentionally conservative: blank values never match
blank values. A market observation may be attached only when both sides have a
real JAN, ASIN, or model number value and those real values are equal.
"""

from __future__ import annotations

from keiji.market_monitoring.models import MarketObservation


def has_identifier_value(value: str | None) -> bool:
    """Return whether an identifier contains a non-blank value."""

    return bool(str(value).strip()) if value is not None else False


def identifiers_match(left: str | None, right: str | None) -> bool:
    """Return True only when both identifiers are present and equal after trimming."""

    if not has_identifier_value(left) or not has_identifier_value(right):
        return False
    return str(left).strip() == str(right).strip()


def observation_matches_identifiers(
    observation: MarketObservation,
    *,
    jan: str | None = None,
    asin: str | None = None,
    model_number: str | None = None,
) -> bool:
    """Match an observation against supplied candidate identifiers safely."""

    return (
        identifiers_match(jan, observation.jan)
        or identifiers_match(asin, observation.asin)
        or identifiers_match(model_number, observation.model_number)
    )


def matching_market_observations(
    observations: tuple[MarketObservation, ...] | list[MarketObservation],
    *,
    jan: str | None = None,
    asin: str | None = None,
    model_number: str | None = None,
) -> tuple[MarketObservation, ...]:
    """Return observations that match at least one real supplied identifier."""

    if not any(has_identifier_value(value) for value in (jan, asin, model_number)):
        return ()
    return tuple(
        observation
        for observation in observations
        if observation_matches_identifiers(observation, jan=jan, asin=asin, model_number=model_number)
    )
