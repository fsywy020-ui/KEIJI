from __future__ import annotations

from pathlib import Path
import unittest

from keiji.common.config_loader import load_rule_config
from keiji.integrations.access_policy import ExternalAccessRequest, evaluate_external_access_request


ROOT = Path(__file__).resolve().parents[3]


class ExternalAccessPolicyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.policy = load_rule_config(ROOT / "config/external_access_policy.v1.yaml")

    def test_rejects_missing_approval_fields(self) -> None:
        decision = evaluate_external_access_request(
            ExternalAccessRequest(
                api_name="amazon_api",
                purpose="listing lookup",
                endpoint_or_operation="get_listing_by_asin",
                data_fields_requested=("asin", "title"),
            ),
            self.policy,
        )
        self.assertFalse(decision.allowed)
        self.assertIn("missing_required_approval_field:reviewer_name", decision.reasons)
        self.assertIn("missing_required_approval_field:approval_timestamp", decision.reasons)

    def test_allows_complete_approved_request_for_allowlisted_api(self) -> None:
        decision = evaluate_external_access_request(
            ExternalAccessRequest(
                api_name="amazon_api",
                purpose="listing lookup",
                endpoint_or_operation="get_listing_by_asin",
                data_fields_requested=("asin", "title"),
                reviewer_name="human-reviewer",
                approval_timestamp="2026-05-13T00:00:00Z",
                no_order_execution_confirmation=True,
            ),
            self.policy,
        )
        self.assertTrue(decision.allowed)
        self.assertEqual((), decision.reasons)

    def test_rejects_unlisted_api(self) -> None:
        decision = evaluate_external_access_request(
            ExternalAccessRequest(
                api_name="unknown_api",
                purpose="listing lookup",
                endpoint_or_operation="lookup",
                data_fields_requested=("title",),
                reviewer_name="human-reviewer",
                approval_timestamp="2026-05-13T00:00:00Z",
                no_order_execution_confirmation=True,
            ),
            self.policy,
        )
        self.assertFalse(decision.allowed)
        self.assertIn("api_not_in_allowlist:unknown_api", decision.reasons)


if __name__ == "__main__":
    unittest.main()
