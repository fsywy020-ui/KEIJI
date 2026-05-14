"""Local-only policy constants for P8 Manus handoff preparation.

These values define what may be included in local handoff packets. They do not
connect to Manus, browsers, stores, payment services, or external APIs.
"""

from __future__ import annotations

FORBIDDEN_ACTIONS: tuple[str, ...] = (
    "login",
    "cart_operation",
    "checkout",
    "purchase",
    "payment",
    "listing_execution",
    "automatic_purchase",
    "automatic_bidding",
    "browser_automation",
    "scraping",
    "live_external_api_access",
    "auth_info_storage",
    "browser_state_collection",
    "external_operation_without_human_approval",
)

ALLOWED_ACTIONS: tuple[str, ...] = (
    "organize_product_page_information_for_human_review",
    "summarize_price_shipping_stock_model_and_jan_for_human_review",
    "generate_human_visible_checklists",
    "organize_pre_purchase_confirmation_items",
    "read_local_handoff_packets",
    "create_local_reports_only",
)

HUMAN_APPROVAL_REQUIRED_ACTIONS: tuple[str, ...] = (
    "any_purchase_decision",
    "any_payment_or_checkout_related_decision",
    "any_external_site_operation",
    "any_manus_assisted_purchase_adjacent_workflow",
    "any_exception_to_offline_first_policy",
)

FORBIDDEN_PACKET_FIELD_LABELS: tuple[str, ...] = (
    "auth_secret_values",
    "payment_secret_values",
    "browser_state_values",
    "personal_data_values",
    "auto_execution_values",
)

HUMAN_CHECKLIST_ITEMS: tuple[str, ...] = (
    "P4 result is same/acceptable; ambiguous or blocked means do not buy.",
    "P3 net profit, ROI, margin, and break-even price are visible and acceptable.",
    "P5 market data is present and matches real identifiers; missing data means review/watch only.",
    "P6 BUY_CANDIDATE means human-review candidate, not purchase permission.",
    "Total source-side cost is at or below the 5,000 JPY per-SKU cap.",
    "Initial 50,000 JPY purchasing budget impact is understood.",
    "The product is not in a prohibited or high-risk category.",
    "If the item is used, required secondhand-goods operation records are understood.",
    "Only allowed non-secret information is included in the Manus handoff packet.",
    "Manus is explicitly forbidden from purchase, payment, cart, checkout, login, automation, scraping, and live API actions.",
)
