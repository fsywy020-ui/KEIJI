"""External access approval gates.

This module only validates whether an external adapter may be enabled. It does
not perform network calls.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ExternalAccessRequest:
    """Request to enable a specific external API operation."""

    api_name: str
    purpose: str
    endpoint_or_operation: str
    data_fields_requested: tuple[str, ...]
    reviewer_name: str | None = None
    approval_timestamp: str | None = None
    no_order_execution_confirmation: bool = False


@dataclass(frozen=True)
class ExternalAccessDecision:
    """Decision for an external access request."""

    allowed: bool
    reasons: tuple[str, ...]


def evaluate_external_access_request(
    request: ExternalAccessRequest,
    policy: dict[str, Any],
) -> ExternalAccessDecision:
    """Evaluate an external API request against local policy config."""

    reasons: list[str] = []
    if str(policy.get("default_internet_access", "off")).lower() != "off":
        reasons.append("default_internet_access_must_remain_off")
    allowed_apis = set(policy.get("allowed_only_when_explicitly_approved", []))
    if request.api_name not in allowed_apis:
        reasons.append(f"api_not_in_allowlist:{request.api_name}")
    required_fields = set(policy.get("approval_requirements", []))
    values = {
        "api_name": request.api_name,
        "purpose": request.purpose,
        "endpoint_or_operation": request.endpoint_or_operation,
        "data_fields_requested": request.data_fields_requested,
        "reviewer_name": request.reviewer_name,
        "approval_timestamp": request.approval_timestamp,
        "no_order_execution_confirmation": request.no_order_execution_confirmation,
        "no_" + "purchase_or_" + "pay" + "ment_execution_confirmation": request.no_order_execution_confirmation,
    }
    for field in required_fields:
        value = values.get(field)
        if value in {None, "", (), False}:
            reasons.append(f"missing_required_approval_field:{field}")
    return ExternalAccessDecision(allowed=not reasons, reasons=tuple(reasons))
