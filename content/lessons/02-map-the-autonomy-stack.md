## Follow the information

For our delivery robot, a useful architecture is:

```text
cameras, lidar, encoders, IMU
             ↓
perception + state estimation
             ↓
task decisions → motion planning → feedback control → actuators
             ↑                                      ↓
             └──────────── changing world ───────────┘
```

Perception interprets measurements: perhaps there is a pallet ahead. Estimation combines information over time: perhaps the robot is at this pose with this uncertainty. Decision-making chooses a task mode: wait, deliver, or recover. Planning proposes a route or motion. Control computes inputs that track that motion.

The boundaries are useful even when a learned model combines several functions. Ask what inputs and outputs remain visible.

## The analogy that helps, and its limit

Think of the stack as interacting services, but remember their rates and deadlines differ. A camera, planner, and motor controller may update at different frequencies. A slow scene update should not prevent a fast controller from using fresh local feedback. Numbers depend on the actual system; avoid copying arbitrary timing thresholds into a product requirement.

Distributed traces tell you which component ran. Robotic traces also need to explain which observation, timestamp, transform, model, and state estimate informed an action. A timestamped event graph is more honest than pretending all messages form one perfectly synchronized sequence.

## Failure belongs somewhere

Suppose the robot fails to reach dock B. The reason might be:

| Symptom | A possible origin | Useful evidence |
|---|---|---|
| No usable route | Planning | Planner status and obstacle map |
| Route looks valid, motion drifts | Control or model mismatch | Reference, estimated state, commands |
| Robot appears in the wrong aisle | Localization | Pose history, uncertainty, sensor residuals |
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
