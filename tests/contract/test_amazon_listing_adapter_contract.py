from __future__ import annotations

import unittest

from keiji.integrations.amazon import AmazonListingSnapshot, FakeAmazonListingAdapter


class AmazonListingAdapterContractTest(unittest.TestCase):
    def test_adapter_contract_returns_snapshot_or_none(self) -> None:
        snapshot = AmazonListingSnapshot(
            asin="B000CONTRACT",
            title="Contract Listing",
            brand="ContractBrand",
            model="CONTRACT-1",
            jan="4900000000001",
            marketplace="amazon_jp",
            buybox_price_yen=4980,
            category="electronics",
        )
        adapter = FakeAmazonListingAdapter([snapshot])
        found = adapter.get_listing_by_asin("B000CONTRACT")
        missing = adapter.get_listing_by_asin("B000NONE")
        self.assertIsInstance(found, AmazonListingSnapshot)
        self.assertEqual("B000CONTRACT", found.asin)
        self.assertIsNone(missing)

    def test_snapshot_from_dict_requires_core_fields(self) -> None:
        snapshot = AmazonListingSnapshot.from_dict(
            {
                "asin": "B000DICT",
                "title": "Dict Listing",
                "brand": "DictBrand",
                "model": "D-1",
                "jan": "4900000000002",
                "buybox_price_yen": "5980",
                "category": "electronics",
            }
        )
        self.assertEqual(5980, snapshot.buybox_price_yen)
        self.assertEqual("amazon_jp", snapshot.marketplace)


if __name__ == "__main__":
    unittest.main()
