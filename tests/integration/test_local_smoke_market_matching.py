from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class LocalSmokeMarketMatchingTest(unittest.TestCase):
    def test_smoke_does_not_attach_market_data_when_identifiers_are_blank(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            candidate_path = tmp / "candidates.json"
            market_path = tmp / "market.json"
            out_dir = tmp / "smoke"
            candidate_path.write_text(
                json.dumps(
                    [
                        {
                            "source_offer": {
                                "id": "src-blank-market-match",
                                "title": "Generic Product Without Identifiers",
                                "brand": "Generic",
                                "condition": "new",
                                "purchase_price_yen": 1000,
                                "domestic_shipping_yen": 0,
                            },
                            "market_listing": {
                                "id": "listing-blank-market-match",
                                "marketplace": "amazon_jp",
                                "title": "Generic Product Without Identifiers",
                                "brand": "Generic",
                                "condition": "new",
                            },
                            "expected_sale_price_yen": 3000,
                            "category": "default",
                            "allocated_budget_yen": 0,
                        },
                        {
                            "source_offer": {
                                "id": "src-jan-market-match",
                                "title": "SONY Wireless Headphones WH-1000XM4 Black",
                                "brand": "SONY",
                                "model": "WH-1000XM4",
                                "jan": "1234567890123",
                                "condition": "new",
                                "purchase_price_yen": 3000,
                                "domestic_shipping_yen": 0,
                            },
                            "market_listing": {
                                "id": "listing-jan-market-match",
                                "marketplace": "amazon_jp",
                                "title": "ソニー ワイヤレスヘッドホン WH-1000XM4 ブラック",
                                "brand": "ソニー",
                                "model": "WH-1000XM4",
                                "jan": "1234567890123",
                                "asin": "B012345678",
                                "condition": "new",
                            },
                            "expected_sale_price_yen": 7200,
                            "category": "electronics",
                            "allocated_budget_yen": 0,
                        },
                    ],
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            market_path.write_text(
                json.dumps(
                    [
                        {
                            "source": "amazon_jp",
                            "observed_at": "2026-05-14T00:00:00+00:00",
                            "product_title": "Unrelated market row with blank identifiers",
                            "price": 9999,
                            "stock_status": "in_stock",
                            "condition": "new",
                        },
                        {
                            "source": "amazon_jp",
                            "observed_at": "2026-05-14T00:00:00+00:00",
                            "product_title": "Matching JAN market row",
                            "jan": "1234567890123",
                            "asin": "B012345678",
                            "model_number": "WH-1000XM4",
                            "price": 7200,
                            "rank": 8000,
                            "category": "electronics",
                            "stock_status": "in_stock",
                            "seller_count": 3,
                            "condition": "new",
                        },
                    ],
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/local_smoke.py"),
                    "--input",
                    str(candidate_path),
                    "--market-input",
                    str(market_path),
                    "--out-dir",
                    str(out_dir),
                ],
                check=True,
                text=True,
                capture_output=True,
                env={"PYTHONPATH": str(ROOT / "src")},
            )
            self.assertIn("smoke_ok=true", completed.stdout)
            packets = json.loads((out_dir / "p7_review_packets.json").read_text(encoding="utf-8"))
            blank_packet, jan_packet = packets
            self.assertEqual([], blank_packet["p5_market_data"])
            self.assertIn("p5_market_data_missing", blank_packet["p6_score"]["reasons"])
            self.assertEqual("Matching JAN market row", jan_packet["p5_market_data"][0]["product_title"])
            self.assertNotIn("Unrelated market row with blank identifiers", json.dumps(jan_packet, ensure_ascii=False))


if __name__ == "__main__":
    unittest.main()
