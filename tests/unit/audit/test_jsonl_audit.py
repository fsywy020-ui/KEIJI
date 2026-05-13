from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from keiji.audit.jsonl import append_audit_event, create_audit_event


class JsonlAuditTest(unittest.TestCase):
    def test_append_audit_event_writes_json_line(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "audit.jsonl"
            event = create_audit_event(
                event_type="p4_decision",
                actor="system",
                target_type="identity",
                target_id="identity-1",
                payload={"decision": "same"},
            )
            append_audit_event(path, event)
            lines = path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(1, len(lines))
            data = json.loads(lines[0])
            self.assertEqual("p4_decision", data["event_type"])
            self.assertEqual("same", data["payload"]["decision"])


if __name__ == "__main__":
    unittest.main()
