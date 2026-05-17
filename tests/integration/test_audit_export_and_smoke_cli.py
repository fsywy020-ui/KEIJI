from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest

from keiji.db.connection import connect, initialize_schema
from keiji.io.audit_export import export_audit_json, export_audit_markdown
from keiji.io.local_candidates import load_candidates_json
from keiji.pipeline.offline_runner import OfflinePipelineRunner


ROOT = Path(__file__).resolve().parents[2]


class AuditExportAndSmokeCliTest(unittest.TestCase):
    def test_audit_export_and_smoke_cli(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "keiji.sqlite3"
            audit_json = Path(tmpdir) / "audit.json"
            audit_md = Path(tmpdir) / "audit.md"
            connection = connect(db_path)
            initialize_schema(connection)
            runner = OfflinePipelineRunner(
                connection=connection,
                product_identity_rules_path=str(ROOT / "config/product_identity_rules.v1.yaml"),
                profit_rules_path=str(ROOT / "config/profit_rules.v1.yaml"),
            )
            runner.run_one(load_candidates_json(ROOT / "tests/fixtures/offline_candidates.v1.json")[0])
            json_count = export_audit_json(connection, audit_json)
            md_count = export_audit_markdown(connection, audit_md)
            self.assertGreaterEqual(json_count, 2)
            self.assertEqual(json_count, md_count)
            self.assertIn("p4_decision", audit_json.read_text(encoding="utf-8"))
            audit_markdown = audit_md.read_text(encoding="utf-8")
            self.assertIn("KEIJI Audit Log", audit_markdown)
            self.assertIn("購入実行や購入承認ではありません", audit_markdown)
            connection.close()

            smoke_dir = Path(tmpdir) / "smoke"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/local_smoke.py"),
                    "--input",
                    str(ROOT / "data/samples/offline_candidates.example.csv"),
                    "--out-dir",
                    str(smoke_dir),
                ],
                check=True,
                text=True,
                capture_output=True,
                env={"PYTHONPATH": str(ROOT / "src")},
            )
            self.assertIn("smoke_ok=true", completed.stdout)
            self.assertTrue((smoke_dir / "pending_review.html").exists())
            self.assertTrue((smoke_dir / "audit_log.json").exists())
            audit_payload = json.loads((smoke_dir / "audit_log.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(len(audit_payload), 2)

    def test_smoke_cli_resets_p8_blocked_actions_audit_for_same_out_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            smoke_dir = Path(tmpdir) / "smoke"
            command = [
                sys.executable,
                str(ROOT / "scripts/local_smoke.py"),
                "--input",
                str(ROOT / "data/samples/offline_candidates.example.csv"),
                "--out-dir",
                str(smoke_dir),
            ]
            env = {"PYTHONPATH": str(ROOT / "src")}

            first = subprocess.run(command, check=True, text=True, capture_output=True, env=env)
            self.assertIn("smoke_ok=true", first.stdout)
            audit_path = smoke_dir / "p8_blocked_actions_audit.jsonl"
            first_events = [json.loads(line) for line in audit_path.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(first_events), 1)
            first_audit_event_id = first_events[0]["payload"]["audit_event_id"]
            self.assertIsNotNone(first_audit_event_id)

            second = subprocess.run(command, check=True, text=True, capture_output=True, env=env)
            self.assertIn("smoke_ok=true", second.stdout)
            second_events = [json.loads(line) for line in audit_path.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(second_events), 1)
            self.assertIsNotNone(second_events[0]["payload"]["audit_event_id"])
            self.assertNotEqual(second_events[0]["payload"]["audit_event_id"], first_audit_event_id)


if __name__ == "__main__":
    unittest.main()
