import json
import tempfile
import unittest
from pathlib import Path

from keiji.manus_handoff import evaluate_manus_action


class ManusHandoffBlockedActionsTest(unittest.TestCase):
    def test_forbidden_manus_action_is_blocked_and_audited(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            audit_path = Path(tmp_dir) / "p8_audit.jsonl"

            decision = evaluate_manus_action(
                requested_action="checkout",
                target_id="candidate-1",
                audit_path=audit_path,
            )

            self.assertFalse(decision.allowed)
            self.assertEqual(decision.decision, "blocked")
            self.assertIn("forbidden_action:checkout", decision.machine_readable_reasons)
            self.assertIsNotNone(decision.audit_event_id)
            event = json.loads(audit_path.read_text(encoding="utf-8").strip())
            self.assertEqual(event["event_type"], "blocked_action")
            self.assertEqual(event["payload"]["requested_action"], "checkout")
            self.assertFalse(event["payload"]["allowed"])

    def test_allowed_local_review_task_passes_but_still_requires_human_approval(self):
        decision = evaluate_manus_action(requested_action="summarize_local_review_packet", target_id="candidate-1")

        self.assertTrue(decision.allowed)
        self.assertEqual(decision.decision, "pass")
        self.assertTrue(decision.requires_human_approval)
        self.assertEqual(decision.machine_readable_reasons, ("p8_local_review_assistance_only",))

    def test_unknown_action_is_blocked_by_default(self):
        decision = evaluate_manus_action(requested_action="open supplier page", target_id="candidate-1")

        self.assertFalse(decision.allowed)
        self.assertEqual(decision.decision, "blocked")
        self.assertEqual(decision.machine_readable_reasons, ("not_in_p8_allowed_task_allowlist",))
