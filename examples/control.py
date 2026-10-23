#!/usr/bin/env python3
"""A bounded toy control loop. No robotics framework or hardware connection."""
import argparse
import json
import math


def simulate(gain=2.0, delay_steps=0):
    if not math.isfinite(gain) or gain <= 0 or not 0 <= delay_steps <= 100:
        raise ValueError("Use a positive finite gain and delay steps between 0 and 100")
    dt, target, x, velocity = 0.05, 1.0, 0.0, 0.0
    history, samples = [x], []
    for i in range(160):
        measured = history[max(0, len(history) - 1 - delay_steps)]
        command = max(-2.0, min(2.0, gain * (target - measured) - 0.8 * velocity))
        disturbance = -1.5 if 65 <= i < 75 else 0.0
        velocity += (command - 0.2 * velocity + disturbance) * dt
        x += velocity * dt
        history.append(x)
        samples.append({"time_s": round((i + 1) * dt, 4), "position_m": x,
                        "velocity_m_s": velocity, "command_m_s2": command})
    return {"synthetic": True, "model": "damped-point-mass-v1", "dt_s": dt,
            "gain": gain, "delay_steps": delay_steps, "target_m": target,
            "final_error_m": target - x, "peak_overshoot_m": max(0.0, max(history) - target),
            "samples": samples}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gain", type=float, default=2.0)
    parser.add_argument("--delay-steps", type=int, default=0)
    args = parser.parse_args()
    try:
        print(json.dumps(simulate(args.gain, args.delay_steps), indent=2, allow_nan=False))
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
