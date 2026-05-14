"""Build P8 Manus handoff packets from P7 local review packets."""

from __future__ import annotations

from uuid import uuid4

from keiji.manus_handoff.models import ManusHandoffPacket
from keiji.review import CandidateReviewPacket


PURPOSE = "pre_purchase_human_assistance_only"


def build_manus_handoff_packet(review_packet: CandidateReviewPacket) -> ManusHandoffPacket:
    """Build a local-only Manus handoff packet.

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
        "Manus may summarize the local packet but must not log in, add to cart, checkout, pay, purchase, list, scrape, or use live APIs.",
        "A human must perform and record any approval before any external purchase-side action occurs outside KEIJI.",
    )
    return ManusHandoffPacket(
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
            "This P8 packet is only a Manus handoff safety contract for human-led pre-purchase review. "
            "It cannot approve, purchase, pay, list, log in, add to cart, checkout, scrape, automate a browser, or call live external APIs."
        ),
    )
