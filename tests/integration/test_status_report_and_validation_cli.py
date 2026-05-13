from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest

from keiji.db.connection import connect, initialize_schema
from keiji.io.local_candidates import load_candidates_json
from keiji.io.status_report import export_status_json, export_status_markdown
from keiji.pipeline.offline_runner import OfflinePipelineRunner


ROOT = Path(__file__).resolve().parents[2]


class StatusReportAndValidationCliTest(unittest.TestCase):
    def test_validation_cli_and_status_report(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/validate_candidates.py"),
                "--input",
                str(ROOT / "data/samples/offline_candidates.example.csv"),
            ],
            check=True,
            text=True,
            capture_output=True,
            env={"PYTHONPATH": str(ROOT / "src")},
        )
        self.assertIn("OK", completed.stdout)

        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "keiji.sqlite3"
            json_path = Path(tmpdir) / "status.json"
            md_path = Path(tmpdir) / "status.md"
            connection = connect(db_path)
            initialize_schema(connection)
            runner = OfflinePipelineRunner(
                connection=connection,
                product_identity_rules_path=str(ROOT / "config/product_identity_rules.v1.yaml"),
                profit_rules_path=str(ROOT / "config/profit_rules.v1.yaml"),
            )
            runner.run_one(load_candidates_json(ROOT / "tests/fixtures/offline_candidates.v1.json")[0])
            export_status_json(connection, json_path)
            export_status_markdown(connection, md_path)
            summary = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(1, summary["counts"]["purchase_candidates"])
            self.assertIn("pending_review", summary["candidate_statuses"])
            self.assertIn("KEIJI Local Status", md_path.read_text(encoding="utf-8"))
            connection.close()


if __name__ == "__main__":
    unittest.main()
