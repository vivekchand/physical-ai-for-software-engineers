#!/usr/bin/env python3
"""Geometry and clock arithmetic on invented inputs. No renderer, simulator or robot."""
import argparse
import json
import math


def finite_values(*values):
    if any(type(value) not in (int, float) or not math.isfinite(value) for value in values):
        raise ValueError("Use finite numeric measurements")


def backproject(u, v, depth_m, fx, fy, cx, cy, convention="z"):
    """Undistorted pinhole model; X right, Y down, Z forward, focal lengths in pixels."""
    finite_values(u, v, depth_m, fx, fy, cx, cy)
    if depth_m <= 0 or fx <= 0 or fy <= 0:
        raise ValueError("Depth and focal lengths must be positive")
    if convention not in ("z", "range"):
        raise ValueError("Depth convention must be z or range")
    ray = ((u - cx) / fx, (v - cy) / fy, 1.0)
    scale = depth_m if convention == "z" else depth_m / math.hypot(*ray)
    return tuple(scale * axis for axis in ray)


def analyze_timing(samples, physics_dt_s):
    """Compare source-time motion and wall-time delivery within one episode."""
    finite_values(physics_dt_s)
    if physics_dt_s <= 0 or len(samples) < 2:
        raise ValueError("Use a positive physics timestep and at least two samples")
    for sample in samples:
        if not isinstance(sample, dict) or not all(key in sample for key in ("sim_time_s", "received_monotonic_s", "x_m")):
            raise ValueError("Each sample needs sim_time_s, received_monotonic_s, and x_m")
        finite_values(sample["sim_time_s"], sample["received_monotonic_s"], sample["x_m"])
    for previous, current in zip(samples, samples[1:]):
        if current["sim_time_s"] <= previous["sim_time_s"]:
            raise ValueError("Simulation time must increase within an episode; split resets into a new episode")
        if current["received_monotonic_s"] <= previous["received_monotonic_s"]:
            raise ValueError("Receipt monotonic time must increase")
    first, last = samples[0], samples[-1]
    sim_elapsed = last["sim_time_s"] - first["sim_time_s"]
    wall_elapsed = last["received_monotonic_s"] - first["received_monotonic_s"]
    displacement = last["x_m"] - first["x_m"]
    intervals = len(samples) - 1
    return {
        "simulation_elapsed_s": sim_elapsed, "wall_elapsed_s": wall_elapsed,
        "rtf_over_observed_window": sim_elapsed / wall_elapsed,
        "velocity_per_sim_second_m_s": displacement / sim_elapsed,
        "velocity_per_wall_second_m_s": displacement / wall_elapsed,
        "samples_per_sim_second": intervals / sim_elapsed,
        "samples_per_wall_second": intervals / wall_elapsed,
        "naive_velocity_using_physics_dt_m_s": (samples[1]["x_m"] - first["x_m"]) / physics_dt_s,
        "clock_note": "RTF uses two elapsed intervals, not a subtraction across clock origins. Receipt-window rates can include delivery effects; measure execution RTF at the simulator when possible.",
    }


def run(scenario="normal"):
    if scenario not in ("normal", "reset"):
        raise ValueError("Scenario must be normal or reset")
    # A ray with normalized coordinates (0.75, 0, 1), length 1.25.
    intrinsics = dict(u=620, v=240, fx=400, fy=400, cx=320, cy=240)
    point_z = backproject(depth_m=.8, convention="z", **intrinsics)
    point_range = backproject(depth_m=1.0, convention="range", **intrinsics)
    wrong = backproject(depth_m=1.0, convention="z", **intrinsics)
    samples = [{"sim_time_s": index / 30, "received_monotonic_s": index / 15, "x_m": .25 * index / 30}
               for index in range(7)]
    if scenario == "reset":
        samples[4]["sim_time_s"] = 0.0
    timing = analyze_timing(samples, physics_dt_s=1 / 120)
    return {
        "synthetic": True, "model": "pinhole-and-clock-arithmetic-v1",
        "scope": "Invented measurements; no GPU, camera, simulator, or robot was exercised.",
        "depth": {
            "optical_frame": "X right, Y down, Z forward; undistorted pinhole",
            "point_from_z_m": point_z, "point_from_range_m": point_range,
            "point_from_range_misread_as_z_m": wrong,
            "point_error_when_range_is_misread_m": math.dist(point_z, wrong),
        },
        "timing": timing, "samples": samples,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=("normal", "reset"), default="normal")
    args = parser.parse_args()
    try:
        result = run(args.scenario)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
