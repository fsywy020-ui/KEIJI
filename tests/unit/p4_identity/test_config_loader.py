from __future__ import annotations

from pathlib import Path
import unittest

from keiji.common.config_loader import load_rule_config


ROOT = Path(__file__).resolve().parents[3]


class ConfigLoaderTest(unittest.TestCase):
    def test_loads_product_identity_rules_without_external_yaml_dependency(self) -> None:
        config = load_rule_config(ROOT / "config/product_identity_rules.v1.yaml")
        self.assertEqual("product_identity_rules.v1", config["version"])
        self.assertEqual("KEIJI", config["project"])
        self.assertEqual(5000, config["budgets"]["max_purchase_amount_per_sku_yen"])
        self.assertIn("互換", config["exclusion_keywords"]["blocked"])

    def test_loads_profit_rules_without_external_yaml_dependency(self) -> None:
        config = load_rule_config(ROOT / "config/profit_rules.v1.yaml")
        self.assertEqual("profit_rules.v1", config["version"])
        self.assertEqual(50000, config["capital"]["initial_purchase_budget_yen"])
        self.assertEqual("amazon_jp", config["marketplace"]["primary"])


if __name__ == "__main__":
    unittest.main()
