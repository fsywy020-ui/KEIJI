"""Shared enums for deterministic KEIJI decisions."""

from __future__ import annotations

from enum import StrEnum


class IdentityDecisionValue(StrEnum):
    """P4 product identity decision values."""

    SAME = "same"
    DIFFERENT = "different"
    AMBIGUOUS = "ambiguous"
    BLOCKED = "blocked"


class P3GateDecisionValue(StrEnum):
    """P4-to-P3 gate decision values."""

    ALLOW = "allow"
    REVIEW_ONLY = "review_only"
    SKIP = "skip"
