## A map, not a shopping list

Start with one task. Choose tools that answer a concrete engineering question. This page covers the robotics and physical-AI stack relevant to this guide, rather than every NVIDIA product.

### Simulate and describe

| Tool | What it is for | Your first useful artifact |
|---|---|---|
| Isaac Sim | Robot/sensor simulation and integration workflows | A repeatable scene with recorded state |
| OpenUSD | Describing and composing scenes/assets | A versioned asset with known units and joints |
| Omniverse / Kit | The scene/application platform underlying Isaac Sim | An understood extension and asset environment |
| PhysX / Newton | Physics backends with distinct integrations | An explicit backend and tested contact/motion behavior |
| Warp | Accelerated simulation/computation building blocks | A profiled computation serving a specific need |
| Replicator / SimReady assets | Synthetic data and structured scene assets | Small labeled data with generation provenance |

Begin with [Isaac Sim's documentation](https://docs.isaacsim.omniverse.nvidia.com/latest/index.html), [Newton](https://github.com/newton-physics/newton), and [Warp](https://github.com/NVIDIA/warp). Backend choice is a model assumption. Identical task names do not imply identical trajectories across backends.

### Integrate robot capabilities

| Tool or capability | Where it helps | What to inspect first |
|---|---|---|
| Isaac ROS | Accelerated ROS perception and robot workflows | Supported releases, hardware, input types, latency |
| Visual SLAM / cuVSLAM | Visual motion/state estimation | Sensor calibration, synchronization, tracking status |
| nvblox | Geometric reconstruction and mapping integrations | Pose quality, depth meaning, representation |
| cuMotion / cuRobo ecosystem | Motion generation and planning integrations | Robot model, joint limits, collision geometry |
| FoundationPose / detection / stereo packages | Pose, recognition, and depth capabilities | Model assets, licenses, interfaces, supported GPU |
| ROS 2 buffer acceleration | Efficient data movement | Release-specific buffer contracts and conversions |

[Isaac ROS docs](https://nvidia-isaac-ros.github.io/) are the entry point. The reviewed release-5 documentation includes migration from NITROS to `rosidl::Buffer`. Follow the selected release; older tutorials can be useful conceptually while using obsolete commands.

### Learn and create data

| Tool | Role | A good first experiment |
|---|---|---|
| Isaac Lab | Environments, training, evaluation, robot-learning workflows | A small task with saved config and checkpoint |
| Isaac Lab Mimic / teleoperation workflows | Demonstrations and imitation-data workflows | Inspect one episode's observation/action contract |
| Isaac GR00T | Generalist VLA model and adaptation workflows | Read the model interface; run supplied-data inference if resources permit |
| Cosmos | World-model, generation, and reasoning projects | Analyze how an output could support a test scenario |

Use [Isaac Lab](https://isaac-sim.github.io/IsaacLab/), [GR00T](https://github.com/NVIDIA/Isaac-GR00T), and [Cosmos](https://github.com/nvidia-cosmos). Model code, weights, datasets, and assets can have different licenses. The guide's open license does not change theirs.

### Deploy and operate

| Tool | Role | When to add it |
|---|---|---|
| Jetson / JetPack | Edge hardware and its supported software stack | When the sensor-to-action path needs edge execution |
| TensorRT | Inference optimization on supported targets | After a correct baseline and representative latency measurement |
| Triton | Inference serving | When serving requirements justify it |
| OSMO | Workflow orchestration across compute resources | When training/data/evaluation jobs exceed a simple local workflow |
| Brev | Provisioning reproducible GPU development environments | When you need a compatible remote host rather than a local workstation |

Start with [Jetson resources](https://developer.nvidia.com/embedded-computing), [TensorRT docs](https://docs.nvidia.com/deeplearning/tensorrt/latest/), and [OSMO](https://github.com/NVIDIA/OSMO). A pipeline can include all of these and still fail because the camera is miscalibrated. Keep task correctness visible.

## Follow one artifact through the stack

Our arm produces episodes → a training job produces a checkpoint → evaluation produces a report → deployment runs a selected version. NVIDIA's [three-computer overview](https://www.nvidia.com/en-us/industries/robotics/) separates training, simulation, and robot-side execution. These roles can share a machine for small experiments.

Read the [learning guide](robot-learning.md) for methods and dataset contracts, the [cloud lab](cloud-lab.md) for Brev setup, and the [evaluation guide](evaluation.md) for the test gate between a checkpoint and deployment.

## The reviewed version snapshot

Reviewed **23 October 2026**:

- Isaac Sim **6.2 GA**: [announcement](https://forums.developer.nvidia.com/t/isaac-sim-6-2-general-availability/386512), [release notes](https://docs.isaacsim.omniverse.nvidia.com/latest/overview/release_notes.html). A download listing reviewed at the same time still showed 6.1, so verify artifact availability.
- Isaac Lab **v3.0.0**: [release](https://github.com/isaac-sim/IsaacLab/releases/tag/v3.0.0), [versioned quickstart](https://isaac-sim.github.io/IsaacLab/v3.0.0/source/isaaclab/quickstart.html). Unified training CLI replaces older library-specific scripts.
- Isaac ROS **release-5.0**: [getting started](https://nvidia-isaac-ros.github.io/getting_started/index.html). Verify explicit pairings with your simulator/platform.
- GR00T **N1.7**: [repository](https://github.com/NVIDIA/Isaac-GR00T). Pin the model revision and read its current platform instructions.

This is a dated review, not an automatically refreshed feed. Moving documentation may change after publication. Contributors should update the source, date, compatibility notes, and affected exercises together.

## What to install first

For this guide: Python labs → ROS 2 basics → Isaac Sim → simulator-to-ROS observation → one navigation/perception workflow. Add Isaac Lab, GR00T, Cosmos, and edge deployment as the relevant lessons require. The core lessons does not require training a large foundation model.
