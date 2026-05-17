from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import tempfile
import unittest

from keiji.db.connection import connect, initialize_schema
from keiji.io.local_candidates import load_candidates_json
from keiji.io.review_report import export_pending_review_html, export_pending_review_markdown
from keiji.pipeline.offline_runner import OfflinePipelineRunner


ROOT = Path(__file__).resolve().parents[2]


class ReviewReportsAndCliTest(unittest.TestCase):
    def test_reports_and_review_cli(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "keiji.sqlite3"
            html_path = Path(tmpdir) / "review.html"
            md_path = Path(tmpdir) / "review.md"
            connection = connect(db_path)
            initialize_schema(connection)
            runner = OfflinePipelineRunner(
                connection=connection,
                product_identity_rules_path=str(ROOT / "config/product_identity_rules.v1.yaml"),
                profit_rules_path=str(ROOT / "config/profit_rules.v1.yaml"),
            )
            candidate = load_candidates_json(ROOT / "tests/fixtures/offline_candidates.v1.json")[0]
            result = runner.run_one(candidate)
            self.assertIsNotNone(result.purchase_candidate_id)
            html_count = export_pending_review_html(connection, html_path)
            md_count = export_pending_review_markdown(connection, md_path)
            self.assertEqual(1, html_count)
            self.assertEqual(1, md_count)
            html_report = html_path.read_text(encoding="utf-8")
            md_report = md_path.read_text(encoding="utf-8")
            self.assertIn("KEIJI Pending Review", html_report)
            self.assertIn("Human approval required", html_report)
            self.assertIn("Candidate", md_report)
            self.assertIn("Human approval required", md_report)
            self.assertIn("P4 additional identity review", md_report)
            self.assertIn("P3 Profit Estimate (Operational Estimate Only)", md_report)
            self.assertIn("Forbidden actions", md_report)
            self.assertIn("Reason: (none)", md_report)
            self.assertNotIn("human_review `0`", md_report)
            connection.close()

            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/review_candidate.py"),
                    "--db",
                    str(db_path),
                    "--candidate-id",
                    str(result.purchase_candidate_id),
                    "--decision",
                    "needs_more_info",
                    "--reviewer",
                    "human-reviewer",
                    "--comment",
                    "need more visual confirmation",
                ],
                check=True,
                text=True,
                capture_output=True,
                env={"PYTHONPATH": str(ROOT / "src")},
            )
            self.assertIn("approval_id=", completed.stdout)


if __name__ == "__main__":
    unittest.main()
