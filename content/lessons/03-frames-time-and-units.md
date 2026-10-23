## A position is not just three numbers

`(1.0, 0.0, 0.0)` might mean one meter ahead of the robot, one meter along a map axis, or a point in a camera frame. A useful position needs a frame, units, and a time.

For a planar robot, pose usually includes position and heading: `(x, y, theta)`. A full spatial pose includes three-dimensional position and orientation. Rotations are not ordinary independent scalar additions; rotation order and representation matter.

## Transform the meaning

Suppose the robot is at map position `(2, 3)` facing along the map's positive x-axis. A box one meter forward in the robot frame is at `(3, 3)` in the map. Rotate the robot by 90 degrees and the same local point becomes `(2, 4)`.

More generally:

```text
point_in_map = rotation_map_from_robot × point_in_robot + translation
```

The transform must correspond to the measurement time. Using a current robot pose with an old camera image creates a geometrically inconsistent result.

ROS conventions distinguish frames such as `map`, `odom`, and `base_link`. In a common arrangement, `odom` provides locally continuous motion but can drift, while global localization corrections affect the relationship to `map`. Follow the specific robot's frame tree and published conventions.

## Clocks are another coordinate system

Use simulated time consistently within a simulated graph. Keep wall-clock receipt time separately for operations. Use a monotonic clock for local elapsed durations. Never subtract timestamps from different clock domains without an established relationship.

Simulator resets can move simulated time backward. A recorder needs a run or episode identifier so two distinct episodes do not appear to overlap.

## Today's practice

Calculate the box position for headings of 0, 90, and 180 degrees. Then sketch this record:

```json
{"run_id":"trial-01","frame_id":"map","position_m":[3,3,0],
 "source_time_s":12.5,"clock_domain":"simulation","received_at":"2026-10-23T10:00:00Z"}
```

List the missing information you would need to compare it with a different sensor. The JSON is illustrative, not a ROS message schema.

## Checkpoint

<details><summary>Can two correct sensors report different coordinates for the same box?</summary><p>Yes. They may use different frames, measurement times, calibration, or uncertainty. Transform and align the observations before treating the numbers as a disagreement.</p></details>

## Go deeper

- [ROS REP 103: units and coordinate conventions](https://github.com/ros-infrastructure/rep/blob/master/rep-0103.rst).
- [ROS REP 105: coordinate frames](https://github.com/ros-infrastructure/rep/blob/master/rep-0105.rst).
- [PORA: Camera Models and Calibration](https://porabook.com/book/camera-models/).
