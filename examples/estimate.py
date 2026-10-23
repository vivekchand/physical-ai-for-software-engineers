#!/usr/bin/env python3
"""Seeded synthetic measurements and a scalar Kalman-style filter."""
import argparse
import json
import math
import random


def estimate(seed=7, measurement_variance=0.25):
    if not math.isfinite(measurement_variance) or measurement_variance <= 0:
        raise ValueError("Measurement variance must be positive and finite")
    rng = random.Random(seed)
    truth, mean, variance, process_variance = 2.0, 0.0, 4.0, 0.01
    samples = []
    for i in range(30):
        observation = truth + rng.gauss(0, math.sqrt(measurement_variance))
        predicted_variance = variance + process_variance
        gain = predicted_variance / (predicted_variance + measurement_variance)
        mean += gain * (observation - mean)
        variance = (1 - gain) * predicted_variance
        samples.append({"step": i + 1, "measurement_m": observation, "estimate_m": mean,
                        "variance_m2": variance, "kalman_gain": gain})
    return {"synthetic": True, "seed": seed, "reference_position_m": truth,
            "measurement_variance_m2": measurement_variance,
            "process_variance_m2": process_variance, "samples": samples}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--measurement-variance", type=float, default=0.25)
    args = parser.parse_args()
    try:
        print(json.dumps(estimate(args.seed, args.measurement_variance), indent=2, allow_nan=False))
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
