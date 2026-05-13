from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from keiji.io.candidate_validation import validate_candidate_csv, validate_candidate_json


ROOT = Path(__file__).resolve().parents[2]


class CandidateValidationTest(unittest.TestCase):
    def test_sample_csv_is_valid(self) -> None:
        result = validate_candidate_csv(ROOT / "data/samples/offline_candidates.example.csv")
        self.assertTrue(result.ok, result.format_text())

    def test_fixture_json_is_valid(self) -> None:
        result = validate_candidate_json(ROOT / "tests/fixtures/offline_candidates.v1.json")
        self.assertTrue(result.ok, result.format_text())

    def test_missing_required_column_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "bad.csv"
            path.write_text("source_id\nabc\n", encoding="utf-8")
            result = validate_candidate_csv(path)
            self.assertFalse(result.ok)
            self.assertIn("missing required column", result.format_text())


if __name__ == "__main__":
    unittest.main()
