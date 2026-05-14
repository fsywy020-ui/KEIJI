from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from keiji.manus_handoff import FORBIDDEN_MANUS_ACTIONS, record_blocked_action


class BlockedActionsAuditTest(unittest.TestCase):
    def test_audit_payload_keeps_generated_audit_event_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            audit_path = Path(tmpdir) / "p8_blocked_actions_audit.jsonl"
            decision = record_blocked_action(
                action="checkout",
                requested_by="unit_test",
                target_id="candidate-1",
                audit_path=audit_path,
            )

            self.assertIsNotNone(decision.audit_event_id)
            lines = audit_path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(1, len(lines))
            event = json.loads(lines[0])
            payload = event["payload"]
            self.assertEqual(decision.audit_event_id, payload["audit_event_id"])
            self.assertIsNotNone(payload["audit_event_id"])
            self.assertEqual("blocked", payload["decision"])
            self.assertFalse(payload["allowed"])

    def test_all_forbidden_manus_actions_are_blocked(self) -> None:
        for action in FORBIDDEN_MANUS_ACTIONS:
            with self.subTest(action=action):
                decision = record_blocked_action(action=action)
                self.assertEqual("blocked", decision.decision)
                self.assertFalse(decision.allowed)
                self.assertIn(action, decision.reason_code)


if __name__ == "__main__":
    unittest.main()
