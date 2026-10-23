"""Test kinematic correctness and the distinction between gripper command and outcome."""
from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from pick_place import forward, inverse, run


class KinematicsTests(unittest.TestCase):
    def test_inverse_solutions_reach_targets_across_workspace(self):
        for x, y in [(0.28, .12), (.16, .28), (-.20, .10), (0, .45), (.05, 0)]:
            point = forward(*inverse(x, y))
            self.assertAlmostEqual(point[0], x, places=8)
            self.assertAlmostEqual(point[1], y, places=8)

    def test_unreachable_and_nonfinite_targets_are_rejected(self):
        for target in [(.6, .2), (0, 0), (math.nan, .2), (math.inf, 0)]:
            with self.assertRaises(ValueError):
                inverse(*target)

    def test_forward_zero_pose_is_full_extension(self):
        self.assertAlmostEqual(forward(0, 0)[0], .45)
        self.assertAlmostEqual(forward(0, 0)[1], 0)


class PickPlaceTests(unittest.TestCase):
    def test_normal_run_places_cube_and_exposes_joint_and_object_evidence(self):
        result = run()
        self.assertTrue(result["placed"])
        self.assertLess(math.dist(result["cube_position_m"], result["tray_position_m"]), 1e-8)
        states = [event for event in result["events"] if event["event_type"] == "arm_state_observed"]
        self.assertEqual(len(states), 20)
        self.assertTrue(all(len(event["payload"]["joint_position_rad"]) == 2 for event in states))

    def test_close_request_does_not_prove_grasp(self):
        result = run("missed-grasp")
        self.assertFalse(result["placed"])
        self.assertIn("gripper_close_requested", [event["event_type"] for event in result["events"]])
        self.assertEqual(result["cube_position_m"], [.28, .12])

    def test_slip_leaves_cube_away_from_tray(self):
        result = run("slip")
        self.assertFalse(result["placed"])
        self.assertGreater(math.dist(result["cube_position_m"], result["tray_position_m"]), .02)
        self.assertIn("synthetic_attachment_lost", [event["event_type"] for event in result["events"]])

    def test_unreachable_plan_is_rejected_before_gripper_command(self):
        result = run("unreachable")
        self.assertEqual(result["outcome"], "unreachable")
        self.assertFalse(any(event["event_type"] == "gripper_close_requested" for event in result["events"]))

    def test_all_scenarios_declare_their_synthetic_origin(self):
        for scenario in ["normal", "missed-grasp", "slip", "unreachable"]:
            result = run(scenario)
            self.assertTrue(result["synthetic"])
            self.assertTrue(all(event["synthetic"] for event in result["events"]))


if __name__ == "__main__":
    unittest.main()
