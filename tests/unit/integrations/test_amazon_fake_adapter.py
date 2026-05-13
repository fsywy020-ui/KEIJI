from __future__ import annotations

import unittest

from keiji.integrations.amazon import AmazonListingSnapshot, FakeAmazonListingAdapter


class AmazonFakeAdapterTest(unittest.TestCase):
    def test_fake_adapter_returns_local_snapshot_without_network(self) -> None:
        snapshot = AmazonListingSnapshot(
            asin="B000TEST",
            title="Local fixture listing",
            brand="FixtureBrand",
            model="MODEL-1",
            jan="4900000000000",
            buybox_price_yen=6980,
            category="electronics",
        )
        adapter = FakeAmazonListingAdapter([snapshot])
        self.assertEqual(snapshot, adapter.get_listing_by_asin("B000TEST"))
        self.assertIsNone(adapter.get_listing_by_asin("B000MISS"))


if __name__ == "__main__":
    unittest.main()
