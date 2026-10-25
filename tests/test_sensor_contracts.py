"""Check depth reconstruction and timing failures independently of Isaac APIs."""
import json
import math
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples"))
from sensor_contracts import analyze_timing, backproject, run


class SensorContractTests(unittest.TestCase):
    def test_consistent_z_and_range_reconstruct_the_same_off_axis_point(self):
        args = dict(u=620, v=240, fx=400, fy=400, cx=320, cy=240)
        from_z = backproject(depth_m=.8, convention="z", **args)
        from_range = backproject(depth_m=1.0, convention="range", **args)
        for actual, expected in zip(from_z, (.6, 0, .8)):
            self.assertAlmostEqual(actual, expected)
        self.assertLess(math.dist(from_z, from_range), 1e-12)
        self.assertAlmostEqual(400 * from_z[0] / from_z[2] + 320, 620)

    def test_center_pixel_agrees_but_off_axis_misinterpretation_has_error(self):
        for convention in ("z", "range"):
            self.assertEqual(backproject(320, 240, 2, 400, 400, 320, 240, convention), (0, 0, 2))
        result = run()
        self.assertAlmostEqual(result["depth"]["point_error_when_range_is_misread_m"], .25)
        self.assertTrue(result["synthetic"])

    def test_invalid_depth_intrinsics_conventions_and_nonfinite_values_are_rejected(self):
        args = dict(u=620, v=240, depth_m=.8, fx=400, fy=400, cx=320, cy=240)
        for changes in ({"depth_m": 0}, {"fx": 0}, {"fy": -1}, {"u": math.inf},
                        {"depth_m": math.nan}, {"depth_m": True}, {"convention": "unknown"}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                backproject(**(args | changes))

    def test_sample_rate_and_rtf_do_not_change_source_time_velocity(self):
        timing = run()["timing"]
        self.assertAlmostEqual(timing["rtf_over_observed_window"], .5)
        self.assertAlmostEqual(timing["velocity_per_sim_second_m_s"], .25)
        self.assertAlmostEqual(timing["velocity_per_wall_second_m_s"], .125)
        self.assertAlmostEqual(timing["samples_per_sim_second"], 30)
        self.assertAlmostEqual(timing["samples_per_wall_second"], 15)
        self.assertAlmostEqual(timing["naive_velocity_using_physics_dt_m_s"], 1)

    def test_absolute_clock_offsets_do_not_change_elapsed_interval_results(self):
        original = run()
        shifted = [sample | {"sim_time_s": sample["sim_time_s"] + 10,
                             "received_monotonic_s": sample["received_monotonic_s"] + 1000}
                   for sample in original["samples"]]
        result = analyze_timing(shifted, 1 / 120)
        for key in ("rtf_over_observed_window", "velocity_per_sim_second_m_s", "velocity_per_wall_second_m_s"):
            self.assertAlmostEqual(result[key], original["timing"][key])

    def test_resets_duplicate_time_and_bad_receipt_order_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "split resets"):
            run("reset")
        for key in ("sim_time_s", "received_monotonic_s"):
            samples = [dict(sim_time_s=0, received_monotonic_s=0, x_m=0),
                       dict(sim_time_s=1, received_monotonic_s=1, x_m=.25)]
            samples[1][key] = 0
            with self.subTest(key=key), self.assertRaises(ValueError):
                analyze_timing(samples, 1 / 120)

    def test_missing_samples_and_bad_timestep_fail_explicitly(self):
        for samples, dt in [([], 1 / 120), ([{}], 1 / 120), ([{}, {}], 1 / 120),
                            (run()["samples"], 0), (run()["samples"], math.nan)]:
            with self.assertRaises(ValueError):
                analyze_timing(samples, dt)

    def test_cli_emits_fixture_or_explains_the_intentional_reset_failure(self):
        command = [sys.executable, str(ROOT / "examples/sensor_contracts.py")]
        normal = subprocess.run(command, capture_output=True, text=True, check=True)
        self.assertTrue(json.loads(normal.stdout)["synthetic"])
        reset = subprocess.run(command + ["--scenario", "reset"], capture_output=True, text=True)
        self.assertNotEqual(reset.returncode, 0)
        self.assertEqual(reset.stdout, "")
        self.assertIn("split resets", reset.stderr)


if __name__ == "__main__":
    unittest.main()
