"""P8 Manus handoff safety helpers.

The package only records local safety decisions. It does not perform purchase,
payment, listing, checkout, login, cart, browser automation, scraping, or live
external API actions.
"""

from keiji.manus_handoff.blocked_actions import (
    FORBIDDEN_MANUS_ACTIONS,
    BlockedActionDecision,
    record_blocked_action,
)

__all__ = ["FORBIDDEN_MANUS_ACTIONS", "BlockedActionDecision", "record_blocked_action"]
