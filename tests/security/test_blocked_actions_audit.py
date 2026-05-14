import json
import tempfile
import unittest
from pathlib import Path

from keiji.manus_handoff import FORBIDDEN_ACTIONS, evaluate_manus_action


class BlockedActionsAuditSecurityTest(unittest.TestCase):
    def test_all_forbidden_actions_create_blocked_audit_records(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            audit_path = Path(tmp_dir) / "blocked_actions.jsonl"

            for action in FORBIDDEN_ACTIONS:
                decision = evaluate_manus_action(
                    requested_action=action,
                    target_id="candidate-security",
                    actor="manus:test",
                    audit_path=audit_path,
                )
                self.assertFalse(decision.allowed)
                self.assertEqual(decision.decision, "blocked")
                self.assertTrue(any(reason.startswith("forbidden_action:") for reason in decision.machine_readable_reasons))

            events = [json.loads(line) for line in audit_path.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(events), len(FORBIDDEN_ACTIONS))
            self.assertEqual({event["event_type"] for event in events}, {"blocked_action"})
            self.assertTrue(all(event["payload"]["requires_human_approval"] is True for event in events))
