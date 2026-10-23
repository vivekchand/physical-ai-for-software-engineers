#!/usr/bin/env python3
"""Synthetic mission traces for learning evidence handling; no robot integration."""
import argparse
import json
from pathlib import Path
import uuid

SCENARIOS = ("normal", "delayed", "disconnected", "rejected", "duplicate")


def events(scenario="normal", run_id=None):
    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {scenario}")
    run_id = run_id or str(uuid.uuid4())
    sequence = [
        (0.0, "authorization_recorded", {"actor": "demo-operator", "scope": "deliver-box-A-to-B"}),
        (0.1, "goal_accepted", {"goal_id": "goal-001"}),
        (1.0, "motion_observed", {"frame_id": "map", "position_m": [0.2, 0.0], "speed_m_s": 0.4}),
    ]
    cancel = (2.0, "cancel_requested", {"request_id": "cancel-001", "goal_id": "goal-001", "actor": "demo-operator"})
    if scenario == "normal":
        sequence += [(5.0, "goal_succeeded", {"goal_id": "goal-001"}),
                     (5.1, "motion_observed", {"frame_id": "map", "position_m": [1.0, 0.0], "speed_m_s": 0.0})]
    else:
        sequence.append(cancel)
        if scenario == "duplicate":
            sequence.append(cancel)
        if scenario == "rejected":
            sequence += [(2.1, "cancel_rejected", {"request_id": "cancel-001", "reason": "synthetic-policy-denial"}),
                         (5.0, "goal_succeeded", {"goal_id": "goal-001"}),
                         (5.1, "motion_observed", {"frame_id": "map", "position_m": [1.0, 0.0], "speed_m_s": 0.0})]
        else:
            sequence += [(2.1, "cancel_accepted", {"request_id": "cancel-001"})]
            if scenario == "disconnected":
                sequence += [(2.2, "observer_disconnected", {"reason": "synthetic-network-loss"})]
            else:
                sequence += [(2.2, "motion_observed", {"frame_id": "map", "position_m": [0.6, 0.0], "speed_m_s": 0.3}),
                             (2.5, "goal_canceled", {"goal_id": "goal-001"}),
                             (3.0, "motion_observed", {"frame_id": "map", "position_m": [0.7, 0.0], "speed_m_s": 0.0})]
    result = []
    for i, (time_s, kind, payload) in enumerate(sequence):
        result.append({"schema_version": 1, "synthetic": True, "run_id": run_id,
                       "event_id": f"{run_id}:{i:03}", "robot_id": "synthetic-delivery-robot",
                       "source_time_s": time_s, "clock_domain": "simulation",
                       "source": "educational-fixture", "event_type": kind, "payload": payload})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=SCENARIOS, default="normal")
    parser.add_argument("--run-id", help="Optional explicit run identity; otherwise a new UUID")
    parser.add_argument("--output", type=Path, help="Write a new file; existing files are preserved")
    args = parser.parse_args()
    text = "".join(json.dumps(event, allow_nan=False) + "\n" for event in events(args.scenario, args.run_id))
    if args.output:
        try:
            with args.output.open("x") as handle:
                handle.write(text)
        except OSError as exc:
            parser.error(str(exc))
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
