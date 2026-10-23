## A position is not just three numbers

`(1.0, 0.0, 0.0)` might mean one meter ahead of the robot, one meter along a map axis, or a point in a camera frame. A useful position needs a frame, units, and a time.

For a planar robot, pose usually includes position and heading: `(x, y, theta)`. A full spatial pose includes three-dimensional position and orientation. Rotations are not ordinary independent scalar additions; rotation order and representation matter.

## Transform the meaning

Suppose a camera's origin is at `(0.10, 0.20)` in the arm-base frame and its planar axes align with that frame. A cube at camera coordinates `(0.20, 0.10)` maps to `(0.30, 0.30)`. Rotate the camera axes by 90 degrees while keeping the same translation and the same local point maps to `(0.00, 0.40)`. This is a simplified planar example; real camera optical frames have their own conventions.

More generally:

```text
point_in_arm_base = rotation_base_from_camera × point_in_camera + translation
```

The transform must correspond to the measurement time. Using a current wrist-camera pose with an old image creates a geometrically inconsistent grasp target.

For an arm, inspect the base, links, end-effector, camera, object, and target frames. Names depend on the robot. For the optional mobile example, ROS conventions distinguish `map`, `odom`, and `base_link`: local odometry can drift while localization corrects its relationship to the global map. Follow the actual frame tree.

## Clocks are another coordinate system

Use simulated time consistently within a simulated graph. Keep wall-clock receipt time separately for operations. Use a monotonic clock for local elapsed durations. Never subtract timestamps from different clock domains without an established relationship.

Simulator resets can move simulated time backward. A recorder needs a run or episode identifier so two distinct episodes do not appear to overlap.

## Today's practice

Calculate the cube's arm-base coordinates for camera rotations of 0, 90, and 180 degrees. Then sketch this record:

```json
{"run_id":"trial-01","frame_id":"arm_base","position_m":[0.3,0.3,0.04],
 "source_time_s":12.5,"clock_domain":"simulation","received_at":"2026-10-23T10:00:00Z"}
```

List the missing information you would need to compare it with a different sensor. The JSON is illustrative, not a ROS message schema.

## Checkpoint

<details><summary>Can two correct sensors report different coordinates for the same box?</summary><p>Yes. They may use different frames, measurement times, calibration, or uncertainty. Transform and align the observations before treating the numbers as a disagreement.</p></details>

## Go deeper

- [ROS REP 103: units and coordinate conventions](https://github.com/ros-infrastructure/rep/blob/master/rep-0103.rst).
- [ROS REP 105: coordinate frames](https://github.com/ros-infrastructure/rep/blob/master/rep-0105.rst).
- [PORA: Camera Models and Calibration](https://porabook.com/book/camera-models/).
