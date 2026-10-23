## Follow a claim to its evidence

For our warehouse delivery, distinguish:

| Claim | Evidence to look for |
|---|---|
| A person permitted the delivery | Scoped authorization record |
| The robot accepted the mission | Goal acceptance from its supported interface |
| Progress occurred | Fresh state or task feedback, with known meaning |
| Cancellation was requested | Actor, target, request identifier, and time |
| The request was accepted | Matching acknowledgment |
| The task ended | Terminal task status |
| Physical motion changed | Fresh, suitable motion evidence |

An unknown result is useful information. Disconnection should produce “state unavailable” rather than preserve a stale green indicator. Correlation helps reconstruct events; it does not prove causation by itself.

## Run the portable incident lab

From the repository root:

```bash
python3 examples/mission.py --scenario normal --output normal.jsonl
python3 examples/mission.py --scenario delayed --output delayed.jsonl
python3 examples/mission.py --scenario disconnected --output disconnected.jsonl
python3 examples/mission.py --scenario rejected --output rejected.jsonl
python3 examples/mission.py --scenario duplicate --output duplicate.jsonl
```

These files contain explicitly synthetic events. They are generated fixtures, not ROS data or robot integrations. The delayed scenario includes a cancellation acknowledgment before later motion evidence. The disconnected scenario has no confirmed final motion state. The duplicate scenario repeats a request identifier so a consumer can demonstrate deduplication.

## Where ClawMetry fits

[ClawMetry](https://clawmetry.com/physical-ai) proposes an observation and governance layer for physical AI through manufacturer-supported integrations. Its physical robot work is a development/partnership track. This guide does not imply that a general Isaac, ROS 2, or robot adapter already ships.

The design lesson is useful beyond any product: keep the observer outside the robot's fast control loop, collect evidence with explicit provenance, and route authorized interventions through supported interfaces. A telemetry observer's failure should not become a dependency of the machine's local safety system.

## Today's practice

Write an incident report for each scenario. State the last known task state, last motion measurement, evidence age, and unresolved questions. For duplicate events, preserve raw evidence but avoid double-counting a single request as two distinct actions.

Draft an optional ClawMetry-style event adapter interface. Label it a proposal; no installed ClawMetry import or live product integration is required by these exercises.

## Checkpoint

<details><summary>A cancellation was accepted, then the network disappeared. What should an operator see?</summary><p>The accepted request and the loss of fresh evidence, with physical outcome unconfirmed. The observer cannot infer that the robot stopped from silence or a software acknowledgment alone.</p></details>

## Go deeper

- [ROS 2 action states and cancellation](https://design.ros2.org/articles/actions.html).
- [ClawMetry physical AI vision and current boundaries](https://clawmetry.com/physical-ai).
- [rosbag2](https://github.com/ros2/rosbag2) for captured ROS evidence.
