# Verification scope

## Automated

The repository's GitHub Actions workflow runs:

- Behavioral tests for the portable control, estimation, mission, manipulation, evaluation, and sensor-contract examples.
- JavaScript syntax validation.
- The static build under the GitHub Pages project base path.
- Local destination/fragment validation across generated pages.
- Coverage checks for all 21 lessons, source links, checkpoints, and search entries.

The tests verify bounded commands and baseline tracking, delay effects, seeded
filter behavior, synthetic event identity, cancellation versus motion evidence,
unconfirmed disconnects, duplicate requests, and preservation of existing output.
The manipulation tests also check forward/inverse kinematic agreement, unreachable
targets, missed grasps, slips, and the distinction between a close request and placement.
Evaluation tests keep unknown outcomes and intervention counts distinct. Sensor-contract
tests verify pinhole depth/range reconstruction, source/wall-time differences, sample-rate
mismatch, and reset rejection on invented inputs. These checks do not execute Isaac Sim.

The hardware table is generated from `data/hardware.json`. It records dated supplier
listings and package scope, not purchase/stock guarantees or independent hardware tests.
Dream Labs and other model introductions are based on primary sources; no vendor API
authentication, paid inference, observation uploads, or playground robot actions are tested.

## Source-reviewed reference exercises

The ROS 2 and NVIDIA instructions link to official documentation. The initial
review date is 23 October 2026. Product references include Isaac Sim 6.2 GA,
Isaac Lab v3.0.0, Isaac ROS release-5.0 docs, and GR00T N1.7. Individual compatibility
and artifact availability must be checked for the user's environment.

These source reviews are not execution evidence for GPU training, ROS middleware,
Isaac bridges, Jetson deployment, or physical robot behavior. Contributors can add
reproduction reports with exact hardware, versions, commands, logs, and limitations.

The scene-building workshop adds primary-source checks dated 25 October 2026 for
GPU selection, USD, physics, current camera APIs, and clock interpretation. The complete
outline and selected transcripts of a second Udemy course informed topic selection;
the sources page records the exact review scope. No paid course material is redistributed.

## Reproduction report template

```text
Date:
Guide commit:
Lesson:
Route (CPU / ROS / GPU / hardware):
OS and hardware:
Drivers and product versions:
Physics backend and renderer:
Exact commands:
Expected result:
Observed result:
Evidence artifacts:
Unexecuted steps:
Known limitations:
```

Never publish credentials, proprietary scenes, personal data, or recordings without
permission. A successful simulation or software acknowledgment does not certify a
physical machine or establish a safety-rated intervention.
