from __future__ import annotations

import json
from pathlib import Path
import unittest

from keiji.p3_profit import ProfitEngine, ProfitInput
from keiji.p3_profit.capital_guard import evaluate_capital
from keiji.p3_profit.explain import explain_profit_estimate
from keiji.p3_profit.fee_estimator import estimate_fees
from keiji.common.config_loader import load_rule_config


ROOT = Path(__file__).resolve().parents[3]


class P3ProfitEngineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rules = load_rule_config(ROOT / "config/profit_rules.v1.yaml")
        cls.engine = ProfitEngine(cls.rules)
        cls.cases = json.loads((ROOT / "tests/fixtures/p3/profit_cases.v1.json").read_text(encoding="utf-8"))

    def test_fixture_cases_match_expected_decisions(self) -> None:
        for case in self.cases:
            with self.subTest(case=case["id"]):
                estimate = self.engine.evaluate(ProfitInput.from_dict(case["input"]))
                self.assertEqual(case["expected_decision"], estimate.decision)
                self.assertTrue(estimate.requires_human_approval)

    def test_fee_estimator_uses_category_rate(self) -> None:
        fees = estimate_fees(10000, "electronics", self.rules)
        self.assertEqual(800, fees.platform_fee_yen)
        self.assertEqual(450, fees.fulfillment_fee_yen)

    def test_capital_guard_blocks_over_sku_limit(self) -> None:
        result = evaluate_capital(purchase_amount_yen=5001, allocated_budget_yen=0, rules=self.rules)
        self.assertEqual("blocked", result.status)
        self.assertIn("per_sku_limit_exceeded", result.reasons[0])

    def test_profit_explanation_includes_human_approval(self) -> None:
        estimate = self.engine.evaluate(ProfitInput.from_dict(self.cases[0]["input"]))
        explanation = explain_profit_estimate(estimate)
        self.assertIn("P3 decision:", explanation)
        self.assertIn("Human approval required: true", explanation)


if __name__ == "__main__":
    unittest.main()
