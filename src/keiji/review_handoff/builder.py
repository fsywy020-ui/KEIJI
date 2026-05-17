"""Build P8 Codex review-assist packets from P7 local review packets."""

from __future__ import annotations

from uuid import uuid4

from keiji.review_handoff.models import ReviewHandoffPacket
from keiji.review import CandidateReviewPacket


PURPOSE = "codex_local_review_assistance_only"


def build_review_handoff_packet(review_packet: CandidateReviewPacket) -> ReviewHandoffPacket:
    """Build a local-only Codex review-assist packet.

    The returned packet is a safety contract. It may be copied into a human-led
    review flow, but it does not send data externally or perform actions.
    """

    review_dict = review_packet.to_dict()
    reasons = (
        "p8_contract_requires_human_approval",
        "purchase_execution_disabled",
        "payment_execution_disabled",
        "browser_automation_disabled",
        "scraping_disabled",
        "live_external_api_disabled",
    )
    checklist = tuple(review_dict.get("human_check_items", ())) + (
        "Codex may summarize and challenge the local packet but must not log in, add to cart, checkout, pay, purchase, list, scrape, automate a browser, or use live APIs.",
        "A human must perform and record any approval before any external purchase-side action occurs outside KEIJI.",
    )
    return ReviewHandoffPacket(
        handoff_id=f"p8-handoff:{uuid4()}",
        candidate_id=review_packet.candidate_id,
        purpose=PURPOSE,
        source_review_packet=review_dict,
        human_checklist=checklist,
        safety_flags={
            "manual_copy_only": True,
            "human_approval_required": True,
            "purchase_execution_disabled": True,
            "payment_execution_disabled": True,
            "listing_execution_disabled": True,
            "checkout_disabled": True,
            "login_disabled": True,
            "cart_operation_disabled": True,
            "browser_automation_disabled": True,
            "scraping_disabled": True,
            "live_external_api_disabled": True,
        },
        machine_readable_reasons=reasons,
        human_readable_explanation=(
            "This P8 packet is only a Codex review-assist safety contract for human-led review. "
            "It cannot approve, purchase, pay, list, log in, add to cart, checkout, scrape, automate a browser, or call live external APIs."
        ),
    )
