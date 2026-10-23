#!/usr/bin/env python3
"""Two-link planar kinematics and a synthetic grasp rule. No contact physics or VLA."""
import argparse
import json
import math
from pathlib import Path

LINKS = (0.25, 0.20)
SCENARIOS = ("normal", "missed-grasp", "slip", "unreachable")


def forward(q1, q2, links=LINKS):
    l1, l2 = links
    return (l1 * math.cos(q1) + l2 * math.cos(q1 + q2),
            l1 * math.sin(q1) + l2 * math.sin(q1 + q2))


def inverse(x, y, links=LINKS):
    """One elbow branch, unconstrained joints, no orientation target/collision check."""
    l1, l2 = links
    if not all(math.isfinite(value) for value in (x, y, l1, l2)) or min(l1, l2) <= 0:
        raise ValueError("Use finite coordinates and positive finite link lengths")
    cosine = (x*x + y*y - l1*l1 - l2*l2) / (2*l1*l2)
    if not -1 - 1e-10 <= cosine <= 1 + 1e-10:
        raise ValueError("Target is outside the two-link workspace")
    q2 = math.acos(max(-1.0, min(1.0, cosine)))
    q1 = math.atan2(y, x) - math.atan2(l2 * math.sin(q2), l1 + l2 * math.cos(q2))
    return q1, q2


def run(scenario="normal", run_id="planar-arm-example"):
    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {scenario}")
    cube, tray = (0.28, 0.12), (0.16, 0.28)
    grasp_target = (0.32, 0.12) if scenario == "missed-grasp" else cube
    if scenario == "unreachable":
        tray = (0.60, 0.20)
    trace = []

    def emit(kind, **payload):
        trace.append({"event_id": f"{run_id}:{len(trace):03}", "run_id": run_id,
                      "synthetic": True, "frame_id": "arm_base", "event_type": kind,
                      "payload": payload})

    emit("task_authorized", instruction="place the red cube in the tray")
    # Reject this toy plan before motion if either endpoint is unreachable.
    try:
        pick_q, place_q = inverse(*grasp_target), inverse(*tray)
    except ValueError as exc:
        emit("plan_rejected", reason=str(exc))
        return {"model": "planar-kinematic-grasp-rule-v1", "synthetic": True,
                "scenario": scenario, "placed": False, "outcome": "unreachable",
                "cube_position_m": list(cube), "tray_position_m": list(tray), "events": trace}
    emit("grasp_pose_reached", joint_position_rad=list(pick_q), end_effector_xy_m=list(forward(*pick_q)))
    emit("gripper_close_requested")
    attached = math.dist(grasp_target, cube) <= 0.015
    emit("attachment_rule_evaluated", attached=attached, criterion="distance <= 0.015 m; not contact physics")
    for step in range(1, 21):
        t = step / 20
        joints = tuple(a + t*(b-a) for a, b in zip(pick_q, place_q))
        eef = forward(*joints)
        if scenario == "slip" and step == 10:
            attached = False
            emit("synthetic_attachment_lost", step=step)
        if attached:
            cube = eef
        emit("arm_state_observed", step=step, joint_position_rad=list(joints),
             end_effector_xy_m=list(eef), cube_position_m=list(cube), attached=attached)
    emit("gripper_open_requested")
    placed = attached and math.dist(cube, tray) <= 0.02
    attached = False
    emit("placement_rule_evaluated", placed=placed, criterion="attached until release and within 0.02 m of tray center")
    return {"model": "planar-kinematic-grasp-rule-v1", "synthetic": True,
            "scenario": scenario, "placed": placed, "outcome": "placed" if placed else "not-placed",
            "cube_position_m": list(cube), "tray_position_m": list(tray), "events": trace}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=SCENARIOS, default="normal")
    parser.add_argument("--output", type=Path, help="Write a new JSON file; never overwrite an existing file")
    args = parser.parse_args()
    text = json.dumps(run(args.scenario), indent=2, allow_nan=False) + "\n"
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
