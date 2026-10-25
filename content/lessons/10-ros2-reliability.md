## Delivery is only one contract

A message can be delivered successfully and still be unsuitable for a decision. It might be old, expressed in an unexpected frame, or derived from an invalid transform. ROS integration requires semantic and timing contracts alongside transport.

QoS policies describe matters such as reliability, history, depth, and durability. Compatible publisher/subscriber settings are required for communication. A subscriber that sees nothing may have a QoS mismatch rather than a network outage.

For some sensor streams, receiving fresh samples is more useful than receiving every historical sample. For other data, loss has a different cost. Choose from the actual workflow, and inspect the offered settings before overriding them.

## Inspect a simulated graph

Use these only with your isolated simulator or recording environment after the relevant nodes exist:

```bash
ros2 topic info /joint_states --verbose
ros2 topic hz /joint_states
ros2 run tf2_ros tf2_echo base_link ee_link
ros2 topic echo /clock --once
```

Topic and frame names vary. Replace them using the graph you discovered. The arm may use different base/end-effector frame names; discover them before running the command. A mobile graph may additionally provide `map` and `odom`. The CLI rate is an observed receiving rate, not a complete proof of publisher performance.

## Separate three rates

Physics stepping, sensor production, and message receipt can have different rates. A velocity estimate needs the interval between the source samples, rather than the physics timestep or a typed-in ROS rate.

Real-time factor is elapsed simulation time divided by elapsed wall time. At RTF 0.5, 0.25 m per simulated second appears as 0.125 m per wall second. This does not by itself mean the simulated dynamics or ROS timestamps are wrong. Measure which clock the complaint refers to. The [laptop contract lab](../pages/isaac-foundations.md#8-run-the-laptop-contract-lab) also shows how a slower sensor stream can yield a fourfold velocity error when divided by the physics timestep.

## Record an experiment

```bash
ros2 bag record -o mission_run /joint_states /tf /tf_static /clock
```

After stopping the recording with Ctrl+C, inspect it:

```bash
ros2 bag info mission_run
```

Replay in a separate, isolated test graph. Do not replay recorded command traffic onto a physical robot.

```bash
ros2 bag play mission_run --clock
```

Configure consumers to use simulated time where appropriate. Avoid running two independent clock publishers in the same replay graph. Recordings only contain what was captured; they do not reconstruct missing sensor measurements or hidden internal state.

## Practice

Capture 30 seconds of a simulated topic. Save the bag metadata, ROS distro, topic types, QoS observations, frame tree, and run identifier. Pause or reset the simulator and inspect the clock behavior. Document what needs to restart for replay.

On the laptop route, use the timestamped JSONL mission trace. It teaches evidence handling but is not a substitute for a ROS bag or DDS behavior.

## Checkpoint

<details><summary>If two events arrive in order, did they necessarily occur in that order?</summary><p>No. Transport, buffering, and different clocks can change apparent order. Preserve source and receipt times, clock domains, sequence identifiers, and causal relationships where available.</p></details>

## Go deeper

- [ROS 2 QoS design](https://design.ros2.org/articles/qos.html).
- [rosbag2 source and usage](https://github.com/ros2/rosbag2).
- [ROS frame conventions](https://github.com/ros-infrastructure/rep/blob/master/rep-0105.rst).
