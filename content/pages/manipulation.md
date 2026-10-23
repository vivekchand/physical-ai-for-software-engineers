## Our running task: the red cube goes in the tray

A tabletop arm observes a red cube, reaches it, closes a parallel gripper, lifts, transfers, places, releases, and checks the outcome. Start in simulation. The learning objective is to connect each physical step to its geometry, software interface, and evidence.

For the GPU route, use NVIDIA's [Franka pick-and-place example](https://docs.isaacsim.omniverse.nvidia.com/latest/examples/manipulation_franka_pick_place.html) and [manipulator workflow](https://docs.isaacsim.omniverse.nvidia.com/latest/robot_setup_tutorials/tutorial_manipulator_workflow.html) for your installed release. The portable route below uses a deliberately small two-link model. It is not a Franka simulator.

## Why an arm is a useful first example

The same task touches perception, transforms, inverse kinematics, collision checking, feedback, contact, demonstrations, and VLA policies. “The gripper closed” is visibly different from “the cube was grasped.” You can study the whole chain on a tabletop.

Autonomous driving remains an important robotics application. Its sensing, estimation, and control principles still transfer. This guide uses manipulation as its primary task because it connects directly to arm policies and accessible experiments; mobile navigation remains an optional comparison.

## Move a target through the workspace

Forward kinematics maps joint angles to gripper position. Inverse kinematics finds joint angles for a requested position. In this **planar toy**, the links are 0.25 m and 0.20 m long. Joint angles are unconstrained and the gripper's orientation is not controlled. The reachable radius is between 0.05 m and 0.45 m.

<div class="lab-panel" data-arm-lab>
<div class="lab-controls"><label>Target x: <output data-arm-x-label>0.28 m</output><input type="range" name="arm-x" min="-0.45" max="0.45" step="0.01" value="0.28" aria-label="Arm target x"></label><label>Target y: <output data-arm-y-label>0.12 m</output><input type="range" name="arm-y" min="-0.1" max="0.5" step="0.01" value="0.12" aria-label="Arm target y"></label></div>
<svg viewBox="0 0 480 500" role="img" aria-label="Two-link planar arm reaching a target, with its geometric workspace shown"><circle cx="240" cy="260" r="202.5" fill="#f2f5fa" stroke="#c9d4e2" stroke-dasharray="4 5"/><circle cx="240" cy="260" r="22.5" fill="#e3e6ec"/><path d="M20 260H460M240 25V315" stroke="#c5cbd3" stroke-width="1"/><g data-arm-links><line data-arm-upper x1="240" y1="260" x2="300" y2="170" stroke="#244bdd" stroke-width="13" stroke-linecap="round"/><line data-arm-fore x1="300" y1="170" x2="366" y2="206" stroke="#557ec1" stroke-width="11" stroke-linecap="round"/><circle data-arm-elbow cx="300" cy="170" r="8" fill="#111d30"/><circle data-arm-eef cx="366" cy="206" r="8" fill="#477841"/></g><circle cx="240" cy="260" r="10" fill="#111d30"/><circle data-arm-target cx="366" cy="206" r="13" fill="none" stroke="#d86346" stroke-width="2"/><text x="250" y="287" font-size="11" fill="#626974">arm_base / meters</text><text x="28" y="490" font-size="11" fill="#626974">Position-only IK · no collision, limits, or contact model</text></svg>
<p class="lab-metrics" data-arm-status aria-live="polite">Enable JavaScript for the interactive solver, or run the Python lab below.</p>
</div>

A reachable endpoint does not establish a collision-free or dynamically feasible path. A real arm also has joint limits, actuator limits, self-collision, orientation constraints, singularities, and contacts. This toy deliberately leaves those out.

## Run the pick-and-place lab

From your clone of this repository, using Python 3.10+:

```bash
python3 examples/pick_place.py --scenario normal
python3 examples/pick_place.py --scenario missed-grasp
python3 examples/pick_place.py --scenario slip
python3 examples/pick_place.py --scenario unreachable
```

Each command prints JSON with joint positions, gripper requests, object positions, and a task outcome. Event order is a synthetic sequence, not a measured latency trace. `--output trial.json` saves a new file without overwriting existing evidence.

The script solves IK for grasp/place endpoints and interpolates joint angles. An explicit distance rule attaches the cube; it follows the gripper while attached. A slip leaves it at the previous toy position. There is no vertical lift, gravity, friction, motor dynamics, image inference, or learned policy. An object frozen after a slip is a fixture behavior, not a physical prediction.

Expected results:

| Scenario | What you should find |
|---|---|
| normal | Cube reaches the tray under the toy attachment rule |
| missed-grasp | Gripper-close request exists, but the cube remains at pickup |
| slip | Attachment is lost and placement does not succeed |
| unreachable | Planning rejects the endpoint before gripper/motion events |

## Advance to the Isaac Sim task

1. Reproduce the official Franka example on a compatible host and record the scene and versions.
2. Identify the controller, joint state, end-effector frame, camera frame, cube pose, and target region.
3. Capture approach, grasp, lift, transfer, release, and verification as separate phases.
4. Shift the cube or tray and repeat with a new run ID.
5. Add an unreachable target or missed-grasp condition under the example's supported simulation controls.
6. Compare controller-reported completion with simulator object state. Simulator ground truth remains distinct from a camera estimate.

These steps are a source-reviewed exercise; this project's CPU tests do not run Isaac Sim or validate hardware. Use the official workflow's interfaces rather than inventing a generic robot command.

## Add a learned policy only after the baseline

Keep the task and outcome definition fixed. Compare a scripted baseline, a demonstration-trained policy, and a VLA/WAM candidate using the same test conditions. Read the Models field note for Dream-1, SmolVLA, OpenVLA, the π family, GR00T, and Gemini Robotics.

Do not assume the guide's single-arm Franka task matches a bimanual model's input/action contract. Decide explicitly whether a model is compatible, needs adaptation, or belongs in a separate bimanual experiment.

## Evidence and ClawMetry

Record task authorization, policy/model version, action timestamps, command acknowledgments, joint state, and relevant object/grasp evidence. ClawMetry's proposed physical-AI observation role is to make those relationships inspectable through supported integrations. This example does not claim a shipped robot adapter.

## Your artifact

Publish a short report comparing all four portable scenarios, then add a separately labeled Isaac report if you execute it. Explain why “move completed,” “gripper closed,” and “cube placed” are different claims.
