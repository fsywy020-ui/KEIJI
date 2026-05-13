"""Amazon adapter protocol.

No live Amazon API implementation is provided in the initial MVP. Implementors
must be explicitly approved before adding network behavior.
"""

from __future__ import annotations

from typing import Protocol

from keiji.integrations.amazon.models import AmazonListingSnapshot


class AmazonListingAdapter(Protocol):
    """Interface for approved Amazon listing lookup adapters."""

    def get_listing_by_asin(self, asin: str) -> AmazonListingSnapshot | None:
        """Return a listing snapshot for an ASIN, or None when unavailable."""
