"""Check the educational claims made by portable labs, not vendor integrations."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from control import simulate
from estimate import estimate
from mission import events, SCENARIOS

ROOT = Path(__file__).resolve().parents[1]


class ControlTests(unittest.TestCase):
    def test_stable_baseline_tracks_target_with_bounded_commands(self):
        result = simulate()
        self.assertLess(abs(result["final_error_m"]), 0.04)
        self.assertEqual(len(result["samples"]), 160)
        self.assertTrue(all(abs(sample["command_m_s2"]) <= 2 for sample in result["samples"]))
        self.assertEqual(result["samples"][-1]["time_s"], 8)

    def test_delay_changes_response_and_overshoot(self):
        timely, delayed = simulate(6, 0), simulate(6, 8)
        self.assertGreater(delayed["peak_overshoot_m"], timely["peak_overshoot_m"])

    def test_invalid_parameters_fail_explicitly(self):
        for gain, delay in [(float("nan"), 0), (-1, 0), (1, -1)]:
            with self.assertRaises(ValueError):
                simulate(gain, delay)


class EstimatorTests(unittest.TestCase):
    def test_seed_is_reproducible_and_updates_reduce_initial_uncertainty(self):
        result = estimate()
        self.assertEqual(result, estimate())
        self.assertGreater(result["samples"][0]["variance_m2"], result["samples"][-1]["variance_m2"])
        self.assertLess(abs(result["samples"][-1]["estimate_m"] - 2), 0.5)

    def test_noisier_measurement_model_reduces_first_gain(self):
        self.assertLess(estimate(measurement_variance=4)["samples"][0]["kalman_gain"],
                        estimate(measurement_variance=.25)["samples"][0]["kalman_gain"])


class MissionTests(unittest.TestCase):
    def test_every_scenario_declares_synthetic_identity_and_order(self):
        for scenario in SCENARIOS:
            trace = events(scenario, run_id="test-run")
            self.assertTrue(all(event["synthetic"] and event["run_id"] == "test-run" for event in trace))
            self.assertEqual(len({event["event_id"] for event in trace}), len(trace))
            times = [event["source_time_s"] for event in trace]
            self.assertEqual(times, sorted(times))

    def test_cancel_acceptance_precedes_nonzero_motion_evidence(self):
        trace = events("delayed")
        accepted = next(event["source_time_s"] for event in trace if event["event_type"] == "cancel_accepted")
        self.assertTrue(any(event["event_type"] == "motion_observed" and
                            event["source_time_s"] > accepted and event["payload"]["speed_m_s"] > 0 for event in trace))

    def test_disconnection_leaves_outcome_unconfirmed(self):
        trace = events("disconnected")
        self.assertEqual(trace[-1]["event_type"], "observer_disconnected")
        self.assertFalse(any(event["event_type"] in ("goal_canceled", "goal_succeeded") for event in trace))

    def test_rejected_and_duplicate_requests_remain_visible(self):
        self.assertIn("cancel_rejected", [event["event_type"] for event in events("rejected")])
        requests = [event for event in events("duplicate") if event["event_type"] == "cancel_requested"]
        self.assertEqual(len(requests), 2)
        self.assertEqual(len({event["payload"]["request_id"] for event in requests}), 1)

    def test_cli_writes_valid_jsonl_without_overwriting_existing_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "trace.jsonl"
            cmd = [sys.executable, str(ROOT/"examples/mission.py"), "--scenario", "delayed", "--output", str(path)]
            subprocess.run(cmd, check=True, capture_output=True)
            before = path.read_text()
            self.assertTrue(all(json.loads(line)["synthetic"] for line in before.splitlines()))
            again = subprocess.run(cmd, capture_output=True)
            self.assertNotEqual(again.returncode, 0)
            self.assertEqual(before, path.read_text())


if __name__ == "__main__":
    unittest.main()
