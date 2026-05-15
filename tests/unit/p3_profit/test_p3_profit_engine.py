from __future__ import annotations

import json
from pathlib import Path
import unittest

from keiji.common.config_loader import load_rule_config
from keiji.p3_profit import ProfitEngine, ProfitInput
from keiji.p3_profit.capital_guard import evaluate_capital
from keiji.p3_profit.explain import explain_profit_estimate
from keiji.p3_profit.fee_estimator import estimate_fees
from keiji.p3_profit.risk_adjuster import adjust_for_risk
from keiji.p3_profit.shipping_estimator import estimate_shipping


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

    def test_shipping_estimator_uses_local_config_assumptions(self) -> None:
        profit_input = ProfitInput.from_dict({
            "id": "profit-shipping-unit",
            "purchase_price_yen": 3000,
            "inbound_shipping_yen": 250,
            "category": "electronics",
        })

        shipping = estimate_shipping(profit_input, self.rules)

        self.assertEqual(250, shipping.inbound_shipping_yen)
        self.assertEqual(100, shipping.packaging_cost_yen)
        self.assertEqual(450, shipping.fulfillment_fee_yen)
        self.assertIn("source:local_or_manual_only", shipping.assumptions)
        self.assertIn("fulfillment_model:amazon_jp_default", shipping.assumptions)

    def test_engine_preserves_existing_profit_math_with_shipping_module(self) -> None:
        estimate = self.engine.evaluate(ProfitInput.from_dict(self.cases[0]["input"]))

        self.assertEqual("pass", estimate.decision)
        self.assertEqual(2372, estimate.net_profit_yen)
        self.assertEqual(500, estimate.shipping.inbound_shipping_yen)
        self.assertEqual(100, estimate.shipping.packaging_cost_yen)
        self.assertEqual(450, estimate.fees.fulfillment_fee_yen)
        self.assertEqual(100, estimate.fees.other_cost_yen)

    def test_risk_adjuster_uses_structured_configured_penalties(self) -> None:
        profit_input = ProfitInput.from_dict({
            "id": "profit-risk-unit",
            "purchase_price_yen": 4000,
            "inbound_shipping_yen": 300,
            "expected_sale_price_yen": 7000,
            "category": "electronics",
            "allocated_budget_yen": 35200,
            "price_uncertainty_percent": 15,
            "return_risk_level": "high",
        })

        adjustment = adjust_for_risk(
            net_profit_yen=1200,
            total_purchase_cost_yen=4500,
            profit_input=profit_input,
            rules=self.rules,
        )

        self.assertEqual(450, adjustment.total_penalty_yen)
        self.assertEqual(750, adjustment.risk_adjusted_profit_yen)
        self.assertEqual(
            ("price_uncertainty", "return_risk", "budget_concentration"),
            tuple(detail.name for detail in adjustment.details),
        )
        self.assertTrue(all(detail.explanation for detail in adjustment.details))

    def test_engine_exposes_risk_details_without_changing_decision_reasons(self) -> None:
        risky_input = ProfitInput.from_dict({
            "id": "profit-risk-engine",
            "p4_decision": "same",
            "p4_confidence_score": 0.95,
            "p4_requires_human_review": False,
            "expected_sale_price_yen": 7000,
            "purchase_price_yen": 4000,
            "inbound_shipping_yen": 300,
            "category": "electronics",
            "allocated_budget_yen": 35200,
            "price_uncertainty_percent": 15,
            "return_risk_level": "high",
        })

        estimate = self.engine.evaluate(risky_input)

        self.assertEqual("pass", estimate.decision)
        self.assertEqual(450, sum(detail.penalty_yen for detail in estimate.risk_details))
        self.assertEqual(estimate.net_profit_yen - 450, estimate.risk_adjusted_profit_yen)
        self.assertNotIn("risk_penalty_reason_count", estimate.reasons)

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
