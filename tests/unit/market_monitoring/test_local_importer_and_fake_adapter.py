from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from keiji.market_monitoring import FakeMarketAdapter, LiveMarketAccessDisabledError, load_market_observations

ROOT = Path(__file__).resolve().parents[3]


class MarketMonitoringTest(unittest.TestCase):
    def test_loads_json_fixture_and_fake_adapter_searches_locally(self) -> None:
        observations = load_market_observations(ROOT / "tests/fixtures/market_observations.v1.json")
        self.assertEqual(1, len(observations))
        adapter = FakeMarketAdapter.from_observations(observations)
        matches = adapter.search(jan="4548736112100")
        self.assertEqual(1, len(matches))
        self.assertEqual("amazon_jp", matches[0].source)

    def test_loads_csv_and_rejects_live_access(self) -> None:
        observations = load_market_observations(ROOT / "data/samples/market_observations.example.csv")
        self.assertGreaterEqual(len(observations), 1)
        with self.assertRaises(LiveMarketAccessDisabledError):
            FakeMarketAdapter.from_observations(observations).fetch_live(query="anything")


if __name__ == "__main__":
    unittest.main()
