from __future__ import annotations

import csv
from pathlib import Path
import tempfile
import unittest

from keiji.db.connection import connect, initialize_schema
from keiji.io.local_candidates import load_candidates_json
from keiji.io.review_export import export_pending_review_csv
from keiji.pipeline.offline_runner import OfflinePipelineRunner


ROOT = Path(__file__).resolve().parents[2]


class OfflineBatchRunnerTest(unittest.TestCase):
    def test_offline_json_batch_creates_review_export(self) -> None:
        connection = connect()
        initialize_schema(connection)
        candidates = load_candidates_json(ROOT / "tests/fixtures/offline_candidates.v1.json")
        runner = OfflinePipelineRunner(
            connection=connection,
            product_identity_rules_path=str(ROOT / "config/product_identity_rules.v1.yaml"),
            profit_rules_path=str(ROOT / "config/profit_rules.v1.yaml"),
        )
        result = runner.run_one(candidates[0])
        self.assertEqual("same", result.p4_decision)
        self.assertEqual("pass", result.p3_decision)
        self.assertIsNotNone(result.purchase_candidate_id)
        with tempfile.TemporaryDirectory() as tmpdir:
            out = Path(tmpdir) / "review.csv"
            count = export_pending_review_csv(connection, out)
            self.assertEqual(1, count)
            with out.open(encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(1, len(rows))
            self.assertEqual("pending_review", rows[0]["status"])
            self.assertEqual("1", rows[0]["requires_human_approval"])
        connection.close()


if __name__ == "__main__":
    unittest.main()
