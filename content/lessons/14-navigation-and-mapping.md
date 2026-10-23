## Make one pick-and-place workflow work

Our main task is an arm moving a cube into a tray. A feasible grasp configuration, a collision-aware path, a tracked trajectory, and a verified placement are separate achievements. Keep them visible as you integrate the system.

Start with the official [Franka pick-and-place example](https://docs.isaacsim.omniverse.nvidia.com/latest/examples/manipulation_franka_pick_place.html) for your installed Isaac Sim release. Use its supported scene, controller, and assets before substituting a learned policy or another arm.

## Inspect the phases

1. Establish the arm-base, end-effector, camera, cube, and target frames.
2. Record joint state and the controller's reference or reported status where exposed.
3. Separate approach, grasp, lift, transfer, place, release, and retreat.
4. Compare a gripper-close request with suitable attachment/contact evidence.
5. Verify the cube's final state in the tray after release, separately from controller completion.

Simulator object state can be a reference for an experiment. It is different from what a camera-based estimator could know. Label both sources.

## Change one thing

Move the cube, shift the tray, add a supported obstacle, or choose a target beyond the workspace. Preserve an unchanged baseline and a separate run ID for every variation. Explain whether failure arose in perception, transforms, IK, planning, grasp, execution, or observation.

For an extended integration, use the official [manipulator workflow](https://docs.isaacsim.omniverse.nvidia.com/latest/robot_setup_tutorials/tutorial_manipulator_workflow.html). Check the robot description, joint limits, collision geometry, and supported motion-generation interfaces. Match the exact release and package compatibility before adding Isaac ROS or cuMotion.

## From one arm to two

A second arm introduces shared workspace, synchronized actions, handovers, and inter-arm collisions. Establish the single-arm outcome first, then add a bimanual extension such as one gripper holding a container while the other sorts objects. The Models field note explains why some WAM/VLA interfaces expect two arms. The Hardware field note distinguishes two working arms from a leader/follower pair.

## Optional mobile comparison

Localization and navigation remain useful for a mobile manipulator or delivery robot. Nav2 coordinates navigation; visual SLAM estimates motion/map information; nvblox supports reconstruction/mapping workflows. They do not replace the arm's grasp and execution logic. Explore these as a separate route when mobility is part of your task.

## Today's practice

On a compatible GPU host, produce a baseline and one perturbed Franka run with scene version, frames, task phases, object outcome, and failure evidence. Otherwise run all four scenarios in `examples/pick_place.py` and explain the kinematic fixture's missing contact/dynamics. Mark GPU integration pending when it has not been executed.

## Checkpoint

<details><summary>The arm reached its final joint target. Did pick-and-place succeed?</summary><p>Not necessarily. The cube may have been missed, slipped, or remained attached at the wrong place. Check the object state and release/placement criterion independently of arm motion completion.</p></details>

## Go deeper

- [NVIDIA Franka example](https://docs.isaacsim.omniverse.nvidia.com/latest/examples/manipulation_franka_pick_place.html).
- [Manipulator workflow](https://docs.isaacsim.omniverse.nvidia.com/latest/robot_setup_tutorials/tutorial_manipulator_workflow.html).
- [Nav2](https://docs.nav2.org/) and [Isaac ROS](https://nvidia-isaac-ros.github.io/) for the optional mobility route.
