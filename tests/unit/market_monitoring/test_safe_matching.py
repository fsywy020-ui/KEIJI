from __future__ import annotations

import unittest

from keiji.market_monitoring import FakeMarketAdapter, matching_market_observations
from keiji.market_monitoring.matching import identifiers_match
from keiji.market_monitoring.models import MarketObservation


class SafeMarketObservationMatchingTest(unittest.TestCase):
    def test_blank_identifiers_never_match_each_other(self) -> None:
        self.assertFalse(identifiers_match(None, None))
        self.assertFalse(identifiers_match("", ""))
        self.assertFalse(identifiers_match("   ", "   "))
        observation = MarketObservation(source="local", observed_at="2026-05-14T00:00:00+00:00", product_title="Different product")
        self.assertEqual((), matching_market_observations([observation], jan=None, asin="", model_number="  "))

    def test_jan_matches_only_when_both_sides_have_same_real_value(self) -> None:
        matching = MarketObservation(source="amazon_jp", observed_at="2026-05-14T00:00:00+00:00", product_title="Matching JAN", jan="1234567890123")
        blank = MarketObservation(source="amazon_jp", observed_at="2026-05-14T00:00:00+00:00", product_title="Blank JAN")
        self.assertEqual((matching,), matching_market_observations([blank, matching], jan="1234567890123"))
        self.assertEqual((), matching_market_observations([matching], jan="9999999999999"))

    def test_asin_and_model_number_match_only_on_real_values(self) -> None:
        asin_match = MarketObservation(source="amazon_jp", observed_at="2026-05-14T00:00:00+00:00", product_title="ASIN match", asin="B012345678")
        model_match = MarketObservation(source="amazon_jp", observed_at="2026-05-14T00:00:00+00:00", product_title="Model match", model_number="WH-1000XM4")
        self.assertEqual((asin_match,), matching_market_observations([asin_match, model_match], asin="B012345678"))
        self.assertEqual((model_match,), matching_market_observations([asin_match, model_match], model_number="WH-1000XM4"))

    def test_fake_adapter_uses_same_safe_matching_guard(self) -> None:
        observation = MarketObservation(source="amazon_jp", observed_at="2026-05-14T00:00:00+00:00", product_title="Blank identifiers")
        adapter = FakeMarketAdapter.from_observations([observation])
        self.assertEqual([], adapter.search(jan=None, asin="", model_number=" "))


if __name__ == "__main__":
    unittest.main()
