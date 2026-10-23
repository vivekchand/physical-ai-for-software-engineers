## ROS 2 is the integration vocabulary

ROS 2 provides communication and tooling for robot software. A node is a logical participant with publishers, subscribers, services, and other interfaces. Multiple nodes can share a process; do not equate node identity with operating-system process identity.

Topics carry streams such as camera images or odometry. Services support request/response interactions. Actions support longer-running goals with feedback, results, and cancellation requests. An action's canceled state is a software task outcome, not a measurement of physical stopping.

## Start on a supported environment

The guide's recommended ROS baseline is Ubuntu 24.04 with ROS 2 Jazzy, aligning with the reviewed Isaac Sim bridge guidance. Follow the official Jazzy installation instructions linked below to configure the package repository and install the desktop tools. A Mac can use a supported remote Linux environment; it does not become an Isaac Sim host merely by running a container.

After installation, open two terminals. In each:

```bash
source /opt/ros/jazzy/setup.bash
```

In terminal A:

```bash
ros2 run demo_nodes_cpp talker
```

In terminal B:

```bash
ros2 run demo_nodes_py listener
```

The listener should display the talker's messages. Inspect the graph in a third sourced terminal:

```bash
ros2 node list
ros2 topic list -t
ros2 topic info /chatter --verbose
ros2 topic echo /chatter --once
```

These commands inspect or run demonstration software. They do not command a robot.

## Read before you connect

Before subscribing to a robot's topic, inspect its type, rate, frame conventions, source timestamp, and QoS. Before calling a service or sending an action, understand authority, side effects, and supported behavior. Discovery alone does not grant permission to control a machine.

## Today's practice

Save a text transcript containing node names, the `/chatter` type, one received sample, and the observed publisher/subscriber counts. Stop the talker and record what the listener does. Distinguish “no new messages” from “the last message means the system is healthy.”

If ROS is not available today, run the portable mission lab and write the same interface inventory. Mark this as a laptop exercise; complete the actual ROS graph later.

## Checkpoint

<details><summary>Should a two-minute navigation task be represented as one blocking service call?</summary><p>A ROS action is often a better fit because it exposes progress and a terminal result, with a cancellation mechanism. The actual robot interface and application requirements determine the design.</p></details>

## Go deeper

- [ROS 2 Jazzy installation](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html).
- [ROS 2 action design](https://design.ros2.org/articles/actions.html).
- [PORA: Robot Autonomy Software](https://porabook.com/book/software/).
