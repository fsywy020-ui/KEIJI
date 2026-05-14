from __future__ import annotations

import ast
import json
from pathlib import Path
import unittest

from keiji.manus_handoff.models import ManusHandoffPacket

ROOT = Path(__file__).resolve().parents[2]
SCAN_DIRS = (ROOT / "src", ROOT / "scripts")
FORBIDDEN_IMPORT_ROOTS = {"requests", "httpx", "aiohttp", "selenium", "playwright", "scrapy", "bs4"}
FORBIDDEN_CALL_NAMES = {
    "login",
    "add_to_cart",
    "checkout",
    "place_order",
    "execute_payment",
    "purchase",
    "create_listing",
    "browser_automation",
    "scrape",
}
SECRET_WORDS = ("password", "api_key", "token", "cookie", "session")


class BlockedActionsAuditTest(unittest.TestCase):
    def test_no_forbidden_external_action_imports_or_calls_in_executable_code(self) -> None:
        violations: list[str] = []
        for directory in SCAN_DIRS:
            for path in directory.rglob("*.py"):
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            root = alias.name.split(".")[0]
                            if root in FORBIDDEN_IMPORT_ROOTS:
                                violations.append(f"{path}: forbidden import {alias.name}")
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        root = node.module.split(".")[0]
                        if root in FORBIDDEN_IMPORT_ROOTS:
                            violations.append(f"{path}: forbidden import {node.module}")
                    elif isinstance(node, ast.Call):
                        name = _call_name(node.func)
                        if name in FORBIDDEN_CALL_NAMES:
                            violations.append(f"{path}: forbidden executable call {name}")
        self.assertEqual([], violations)

    def test_manus_handoff_packet_contains_no_secret_or_execution_fields(self) -> None:
        packet = ManusHandoffPacket(
            candidate_id="audit-candidate",
            product_name="Audit Product",
            jan=None,
            asin=None,
            model_number=None,
            source_url_or_reference="local/source",
            sales_url_or_reference="local/sales",
            p4_identity_result={"decision": "ambiguous"},
            p3_profit_result={"decision": "review"},
            p5_market_data_summary={"status": "missing"},
            p6_score={"decision": "WATCH_ONLY", "reasons": ["p5_market_data_missing"]},
            p7_review_status="pending_human_approval",
            recommended_action="watch_only",
            human_check_items=("BUY_CANDIDATE is not purchase permission.",),
            per_sku_limit_ok=True,
            initial_budget_impact_yen=1000,
            initial_budget_remaining_after_candidate_yen=49000,
        )
        payload_text = json.dumps(packet.to_dict(), ensure_ascii=False).lower()
        for word in SECRET_WORDS:
            self.assertNotIn(word, payload_text)
        self.assertNotIn("execute_purchase", payload_text)
        self.assertIn("purchase", packet.forbidden_actions)

    def test_buy_candidate_is_not_purchase_permission(self) -> None:
        packet = ManusHandoffPacket(
            candidate_id="buy-wording",
            product_name="Buy wording",
            jan="1234567890123",
            asin="B012345678",
            model_number="MODEL1",
            source_url_or_reference="local/source",
            sales_url_or_reference="local/sales",
            p4_identity_result={"decision": "same"},
            p3_profit_result={"decision": "pass"},
            p5_market_data_summary={"status": "present"},
            p6_score={"decision": "BUY_CANDIDATE"},
            p7_review_status="pending_human_approval",
            recommended_action="human_review_candidate_only_not_purchase_permission",
            human_check_items=("BUY_CANDIDATE is not purchase permission.",),
            per_sku_limit_ok=True,
            initial_budget_impact_yen=1000,
            initial_budget_remaining_after_candidate_yen=49000,
        )
        self.assertTrue(packet.human_approval_required)
        self.assertIn("not_purchase_permission", packet.recommended_action)
        self.assertIn("purchase", packet.forbidden_actions)


def _call_name(func: ast.expr) -> str:
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return ""


if __name__ == "__main__":
    unittest.main()
