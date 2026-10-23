## Name the capability before adding a package

Navigation coordinates a goal, localization, a representation of obstacles, planning, and execution. SLAM estimates motion and a map. Reconstruction creates a geometric representation. None alone means the robot can reliably complete a delivery.

Nav2 supplies ROS 2 navigation components. Isaac ROS offers accelerated capabilities that can participate in a larger graph. Visual SLAM estimates motion from visual inputs under its assumptions. nvblox reconstructs geometry from supported observations and pose information, with integrations relevant to navigation. A reconstructed scene is not automatically a correct traversability map.

## One practical experiment

Start with the official navigation example matching your Isaac Sim release. Use its supported robot and scene before changing sensors or combining third-party launch files.

1. Inspect the graph and frame tree while the robot is stationary.
2. Establish which node supplies global pose, local odometry, and obstacle information.
3. Submit a goal using the example's supported UI or action interface in simulation.
4. Record the goal status, path updates, state estimates, and terminal result.
5. Change one obstacle and repeat, preserving the run identifiers.

Then choose **one** accelerated perception or mapping tutorial from Isaac ROS, such as visual SLAM or nvblox. Follow its own quickstart, input requirements, release tag, and supported GPU setup. Preserve the baseline run for comparison.

## What to measure

Compare successful completion rate, pose error when reference truth exists, input age, processing latency, and resource use. A faster individual node can leave end-to-end performance unchanged if another component dominates. Speed is also of little value if frames or calibration are wrong.

Record dependency versions and conversions between CPU/GPU buffers. The release-5 documentation's buffer migration is a reminder to use the package's own release instructions rather than assume historical NITROS commands still apply.

## Today's practice

Create two mission reports: the unchanged navigation example and one deliberate perturbation. Explain whether the robot replanned, recovered, aborted, or failed to report an outcome. If you only have the laptop track, inspect the portable mission scenarios and label the graph-level/GPU steps pending.

## Checkpoint

<details><summary>Does a visually detailed 3D reconstruction establish a usable navigation solution?</summary><p>No. Localization, collision representation, traversability, planning, controls, and timing must work together. Evaluate the complete mission and each interface's assumptions.</p></details>

## Go deeper

- [Nav2 documentation](https://docs.nav2.org/).
- [Isaac ROS visual SLAM](https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_visual_slam/index.html).
- [Isaac ROS nvblox](https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_nvblox/index.html).
- [PORA: Robot Localization](https://porabook.com/book/robot-localization/).
