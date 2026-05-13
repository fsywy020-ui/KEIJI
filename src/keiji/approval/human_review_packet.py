"""Human review packet builders.

These helpers create review payloads only. They do not approve, purchase, pay,
open browsers, or call external APIs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class HumanReviewPacket:
    """Review packet presented to a human operator."""

    target_type: str
    target_id: str
    summary: str
    reasons: tuple[str, ...]
    requires_human_approval: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_type": self.target_type,
            "target_id": self.target_id,
            "summary": self.summary,
            "reasons": list(self.reasons),
            "requires_human_approval": self.requires_human_approval,
        }


def build_review_packet(*, target_type: str, target_id: str, summary: str, reasons: tuple[str, ...]) -> HumanReviewPacket:
    """Build a human review packet for P4/P3/approval workflows."""

    return HumanReviewPacket(
        target_type=target_type,
        target_id=target_id,
        summary=summary,
        reasons=reasons,
        requires_human_approval=True,
    )
