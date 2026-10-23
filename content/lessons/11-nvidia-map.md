## Choose by the problem you are solving

The NVIDIA robotics ecosystem spans simulation, training, perception, inference, deployment, and workflow infrastructure. You do not need every component to begin. For the pick-and-place mission, start with simulation and a ROS graph. Add training only when the task requires a learned policy.

| Need | Relevant tool | First question |
|---|---|---|
| Simulate a robot and its sensors | Isaac Sim | Does the model reproduce the behavior I need to test? |
| Train or evaluate policies in environments | Isaac Lab | What are observations, actions, reward, and termination? |
| Accelerated robot software in ROS | Isaac ROS | Which package, hardware, ROS release, and data formats match? |
| Explore generalist learned actions | Isaac GR00T | What embodiment and action representation are supported? |
| Generate or reason about visual world scenarios | Cosmos | Does the generated scenario preserve relevant physical facts? |
| Deploy inference near sensors | Jetson and JetPack | What are the supported hardware/software versions and latency budget? |

Isaac ROS includes capabilities such as visual SLAM, reconstruction with nvblox, perception, and motion-generation integrations. Package support and data paths evolve. For example, the reviewed release-5 documentation includes migration from NITROS to `rosidl::Buffer`; old zero-copy examples need release-specific checking.

OpenUSD describes composable scene assets. Omniverse/Kit supports the application and scene ecosystem used by Isaac Sim. Replicator supports synthetic-data workflows. PhysX, Newton, and Warp concern physics simulation or accelerated computation, with different integrations and requirements. They are not interchangeable product names.

TensorRT and Triton concern inference optimization and serving. OSMO orchestrates workflows across compute resources. They solve problems you may meet after a small local experiment works.

## Training, simulation, and deployment computers

[NVIDIA's three-computer framing](https://www.nvidia.com/en-us/industries/robotics/) separates training, simulation, and execution near the robot. Treat these as workload roles; a small experiment may share a workstation, while larger jobs use separate machines.

For our arm: training consumes episodes and emits checkpoints; simulation produces observations and tests actions; deployment runs a chosen policy with local control. Move versioned artifacts between those roles. A remote GPU desktop or Brev launchable supplies compute/setup, rather than a new learning algorithm.

## A practical ordering

1. Establish a ROS graph and a robot interface contract.
2. Make one Isaac Sim scene run reproducibly.
3. Bridge state into ROS and inspect it.
4. Add the specific perception or navigation capability you need.
5. Evaluate whether policy learning or foundation models address an actual gap.

## Today's practice

Draw a dependency map for your mission. Label each component “needed now,” “optional later,” or “not used.” Write one sentence explaining every inclusion. Read the dedicated NVIDIA field note for the dated compatibility snapshot.

## Checkpoint

<details><summary>Do you need Isaac Lab to observe a robot in Isaac Sim through ROS 2?</summary><p>No. Isaac Lab addresses learning and environment workflows. A simulator-to-ROS observation experiment can begin without training a policy.</p></details>

## Go deeper

- [Isaac Sim documentation](https://docs.isaacsim.omniverse.nvidia.com/latest/index.html).
- [Isaac ROS](https://nvidia-isaac-ros.github.io/).
- [Isaac Lab](https://isaac-sim.github.io/IsaacLab/).
- [NVIDIA GR00T](https://github.com/NVIDIA/Isaac-GR00T).
- [NVIDIA Cosmos](https://github.com/nvidia-cosmos) and [OSMO](https://github.com/NVIDIA/OSMO).
