"""Check that reporting cannot hide unknowns, interventions or incompatible evidence."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples"))
from evaluate import load_trials, summarize


def trial(**changes):
    return dict(attempt_id="one", policy="baseline", condition="nominal", evidence="synthetic",
                outcome="placed", intervened=False, elapsed_s=30) | changes


class EvaluationTests(unittest.TestCase):
    def test_fixture_exposes_nominal_help_and_held_out_degradation(self):
        report = summarize(load_trials(ROOT / "examples/data/policy_trials.jsonl"))
        self.assertEqual(report["trial_count"], 12)
        groups = {(row["policy"], row["condition"]): row for row in report["groups"]}
        nominal = groups[("candidate-v1", "nominal")]
        shifted = groups[("candidate-v1", "shifted-tray")]
        self.assertEqual(nominal["verified_placements"], 3)
        self.assertEqual(nominal["autonomous_verified"], 2)
        self.assertEqual(nominal["interventions"], 1)
        self.assertEqual(shifted["unconfirmed"], 1)
        self.assertEqual(shifted["autonomous_verified_rate"], 1 / 3)
        self.assertTrue(all(row["evidence"] == "synthetic" for row in report["groups"]))

    def test_unconfirmed_stays_in_denominator_without_becoming_physical_failure(self):
        group = summarize([trial(), trial(attempt_id="two", outcome="unconfirmed")])["groups"][0]
        self.assertEqual(group["verified_placement_rate"], .5)
        self.assertEqual(group["failed"], 0)
        self.assertEqual(group["unconfirmed"], 1)

    def test_intervention_does_not_erase_placement_or_count_as_autonomous(self):
        group = summarize([trial(intervened=True)])["groups"][0]
        self.assertEqual(group["verified_placements"], 1)
        self.assertEqual(group["autonomous_verified"], 0)
        self.assertEqual(group["intervention_rate"], 1)

    def test_throughput_includes_failed_and_reset_time(self):
        group = summarize([trial(), trial(attempt_id="two", outcome="failed", elapsed_s=90)])["groups"][0]
        self.assertEqual(group["elapsed_s"], 120)
        self.assertEqual(group["autonomous_verified_per_hour"], 30)

    def test_conditions_and_evidence_sources_are_never_pooled(self):
        rows = [trial(), trial(attempt_id="two", condition="shifted"),
                trial(attempt_id="three", evidence="hardware")]
        self.assertEqual(len(summarize(rows)["groups"]), 3)

    def test_duplicate_attempts_are_rejected_instead_of_inflating_counts(self):
        with self.assertRaisesRegex(ValueError, "Duplicate attempt_id"):
            summarize([trial(), trial()])

    def test_bad_labels_types_times_and_empty_input_fail_explicitly(self):
        for change in [{"outcome": "accepted"}, {"intervened": "false"}, {"intervened": 0},
                       {"elapsed_s": True}, {"elapsed_s": 0}, {"elapsed_s": -1},
                       {"elapsed_s": float("nan")}, {"elapsed_s": float("inf")},
                       {"evidence": "unknown"}, {"condition": ""}]:
            with self.subTest(change=change), self.assertRaises(ValueError):
                summarize([trial(**change)])
        for rows in [[], [None], [{}]]:
            with self.assertRaises(ValueError):
                summarize(rows)

    def test_cli_default_fixture_works_outside_the_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, str(ROOT / "examples/evaluate.py")],
                                    cwd=directory, capture_output=True, text=True, check=True)
            self.assertEqual(json.loads(result.stdout)["trial_count"], 12)
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_invalid_json_reports_its_line_and_cli_exits_without_a_report(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.jsonl"
            path.write_text(json.dumps(trial()) + "\nnot json\n")
            result = subprocess.run([sys.executable, str(ROOT / "examples/evaluate.py"), "--input", str(path)],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")
            self.assertIn("Line 2: invalid JSON", result.stderr)


if __name__ == "__main__":
    unittest.main()
