from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest

from keiji.manus_handoff import FORBIDDEN_MANUS_ACTIONS

ROOT = Path(__file__).resolve().parents[2]


class LocalSmokeP8AuditResetTest(unittest.TestCase):
    def test_smoke_re_run_resets_p8_blocked_actions_audit_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            out_dir = Path(tmpdir) / "smoke"
            out_dir.mkdir(parents=True, exist_ok=True)
            audit_path = out_dir / "p8_blocked_actions_audit.jsonl"
            audit_path.write_text('{"payload":{"audit_event_id":"old-event"}}\n', encoding="utf-8")

            command = [
                sys.executable,
                str(ROOT / "scripts/local_smoke.py"),
                "--input",
                str(ROOT / "data/samples/offline_candidates.example.csv"),
                "--out-dir",
                str(out_dir),
            ]
            env = {"PYTHONPATH": str(ROOT / "src")}
            first = subprocess.run(command, check=True, text=True, capture_output=True, env=env)
            first_lines = audit_path.read_text(encoding="utf-8").splitlines()
            second = subprocess.run(command, check=True, text=True, capture_output=True, env=env)
            second_lines = audit_path.read_text(encoding="utf-8").splitlines()

            self.assertIn("smoke_ok=true", first.stdout)
            self.assertIn("smoke_ok=true", second.stdout)
            self.assertEqual(len(FORBIDDEN_MANUS_ACTIONS), len(first_lines))
            self.assertEqual(len(FORBIDDEN_MANUS_ACTIONS), len(second_lines))
            self.assertNotIn("old-event", "\n".join(second_lines))
            for line in second_lines:
                payload = json.loads(line)["payload"]
                self.assertIsNotNone(payload["audit_event_id"])

    def test_smoke_start_removes_stale_p8_audit_even_when_validation_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            out_dir = tmp / "smoke"
            out_dir.mkdir(parents=True, exist_ok=True)
            audit_path = out_dir / "p8_blocked_actions_audit.jsonl"
            audit_path.write_text('{"payload":{"audit_event_id":"stale-before-validation"}}\n', encoding="utf-8")
            invalid_input = tmp / "invalid.csv"
            invalid_input.write_text("not_a_required_header\nvalue\n", encoding="utf-8")

            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/local_smoke.py"),
                    "--input",
                    str(invalid_input),
                    "--out-dir",
                    str(out_dir),
                ],
                check=False,
                text=True,
                capture_output=True,
                env={"PYTHONPATH": str(ROOT / "src")},
            )

            self.assertNotEqual(0, completed.returncode)
            self.assertFalse(audit_path.exists())


if __name__ == "__main__":
    unittest.main()
