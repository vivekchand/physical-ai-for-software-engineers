## Follow the information

For our pick-and-place arm, a useful architecture is:

```text
cameras, joint encoders, gripper/contact signals
             ↓
perception + state estimation
             ↓
task decisions → motion planning → feedback control → actuators
             ↑                                      ↓
             └──────────── changing world ───────────┘
```

Perception interprets measurements: the red cube appears at this image location. Estimation combines information into object and arm state with uncertainty. Decision-making chooses a phase: approach, grasp, lift, transfer, release, or recover. Planning proposes collision-aware arm motion. Control computes inputs that track it.

The boundaries are useful even when a learned model combines several functions. Ask what inputs and outputs remain visible.

## The analogy that helps, and its limit

Think of the stack as interacting services, but remember their rates and deadlines differ. A camera, planner, and motor controller may update at different frequencies. A slow scene update should not prevent a fast controller from using fresh local feedback. Numbers depend on the actual system; avoid copying arbitrary timing thresholds into a product requirement.

Distributed traces tell you which component ran. Robotic traces also need to explain which observation, timestamp, transform, model, and state estimate informed an action. A timestamped event graph is more honest than pretending all messages form one perfectly synchronized sequence.

## Failure belongs somewhere

Suppose the cube never reaches the tray. The reason might be:

| Symptom | A possible origin | Useful evidence |
|---|---|---|
| No feasible grasp configuration | IK or planning | Target pose, joint limits, collision geometry |
| Arm motion drifts | Control or model mismatch | Reference, estimated joints, commands |
| Gripper closes on empty space | Perception or transforms | Object pose, camera calibration, source time |
| Cube falls during transfer | Grasp/contact or execution | Gripper state, object motion, contact evidence |
| Nothing changes in the dashboard | Observation path | Heartbeats, freshness, connection status |

These are hypotheses, not diagnoses. Several components can contribute to one failure.

## Today's practice

Draw this stack for your mission. For every arrow, write a message type, a timestamp requirement, and what happens when updates stop. Mark which signals are measured, estimated, requested, or merely reported by software.

Then describe a failure that could look like a planner bug but originate in stale sensor data.

## Checkpoint

<details><summary>If perception is healthy, is navigation necessarily healthy?</summary><p>No. Perception can produce plausible detections while localization, planning, transforms, or control are failing. Health is a property of the integrated workflow as well as its components.</p></details>

## Go deeper

- [PORA: Software](https://porabook.com/book/software/).
- [PORA: Prospects](https://porabook.com/book/prospects/) for modular and learned systems.
