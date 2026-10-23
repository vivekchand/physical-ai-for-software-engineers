## Connect two working systems

First prove the ROS talker/listener works. Separately prove Isaac Sim runs a scene. Now connect them. This ordering narrows the failure surface when discovery or message delivery breaks.

The ROS bridge connects supported simulator interfaces with ROS. Your external nodes still require their own compatible ROS environment. Custom message bindings must match the simulator's documented Python/runtime requirements; sourcing an arbitrary workspace is not a universal fix.

## A supported route

Use the reviewed Ubuntu 24.04/Jazzy combination or another explicitly documented configuration. Follow the selected release's ROS installation page to launch the simulator with the correct bridge settings. On Windows and other combinations, follow that platform's instructions rather than copying Linux environment overrides.

Use an official ROS 2 robot tutorial scene. Begin by publishing state from the simulator, without adding a new control path.

In a sourced external ROS terminal:

```bash
source /opt/ros/jazzy/setup.bash
ros2 node list
ros2 topic list -t
ros2 topic info /clock --verbose
ros2 topic echo /clock --once
```

Discover the actual odometry topic. If it is `/odom` with type `nav_msgs/msg/Odometry`:

```bash
ros2 topic info /odom --verbose
ros2 topic echo /odom --once
python3 examples/ros2_observer.py --topic /odom
```

The included observer subscribes to odometry and prints local JSONL. It records message state and its source frame/time; it does not send movement commands. It requires ROS 2 and a matching message publisher, so it is not exercised by the portable CI tests.

## Debug in layers

If nothing appears, check whether simulation is playing and the bridge started. Then inspect ROS domain, middleware, discovery/network settings, topic names, and QoS. Restart components deliberately after changing middleware settings. Keep a record of which adjustment changed the result.

## Today's practice

Record a short state trace. Pause the simulator and verify the source clock and samples behave as expected. Disconnect your observer and confirm that the simulator continues under its own control. Save the graph, message type, clock domain, and the observer's limits.

The laptop alternative is the portable mission trace. It exercises evidence analysis but does not prove this bridge works.

## Checkpoint

<details><summary>Does the simulator's bundled ROS support mean external nodes need no ROS installation?</summary><p>No. The simulator can include libraries for its bridge, while external nodes need a compatible ROS environment. Custom interfaces add further runtime/build requirements.</p></details>

## Go deeper

- [Isaac Sim ROS 2 installation and bridge setup](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/install_ros.html).
- [ROS 2 action design](https://design.ros2.org/articles/actions.html).
