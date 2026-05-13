"""Fake Amazon adapter for offline tests and fixture-driven development."""

from __future__ import annotations

from collections.abc import Iterable

from keiji.integrations.amazon.models import AmazonListingSnapshot


class FakeAmazonListingAdapter:
    """In-memory Amazon adapter that never performs network calls."""

    def __init__(self, snapshots: Iterable[AmazonListingSnapshot]) -> None:
        self._by_asin = {snapshot.asin: snapshot for snapshot in snapshots}

    def get_listing_by_asin(self, asin: str) -> AmazonListingSnapshot | None:
        return self._by_asin.get(asin)
