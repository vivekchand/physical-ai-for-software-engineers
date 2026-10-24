## Start with joints and the gripper

For the arm task, model joint positions `q`, joint velocities, gripper state, and relevant object state. A state collects the quantities your model needs to predict future behavior given inputs. A richer model includes actuator lag, loads, contact, and uncertainty.

Kinematics describes geometric relationships. Dynamics describes how forces, torques, inertia, and contacts affect motion. Finding joint angles for a cube position does not establish a feasible grasp or a safe path.

## Forward and inverse kinematics

For a two-link planar arm, forward kinematics maps shoulder/elbow angles to the endpoint:

```python
from math import cos, sin

def endpoint(q1, q2, l1=0.25, l2=0.20):
    return (l1*cos(q1) + l2*cos(q1 + q2),
            l1*sin(q1) + l2*sin(q1 + q2))
```

Inverse kinematics (IK) goes the other way: find a joint configuration for a desired endpoint pose. There can be multiple solutions, no solution, or a solution unsuitable because of limits or collision. The portable lab solves one elbow branch with unconstrained joints and no orientation target.

Real manipulators add spatial rotations, more joints, self-collision, actuator limits, singularities, and contact dynamics. Near a singular configuration, some requested endpoint motions may demand unfavorable joint motion or become unavailable. The toy's workspace diagram does not represent a full Franka model.

## Run a complete toy sequence

```bash
python3 examples/pick_place.py --scenario normal
python3 examples/pick_place.py --scenario unreachable
```

Read the joint positions, endpoint positions, and placement result. The script uses a declared attachment rule, not grasp physics. Joint interpolation between valid endpoints is not guaranteed collision-free. See the [arm field note](../pages/manipulation.md) for assumptions and interactive IK.

## Dynamics changes the story

The same endpoint trajectory can produce different joint torques when the cube is heavier or friction changes. A closed gripper can lose the object. Reducing an integration timestep can improve numerical accuracy for a model; it cannot correct missing contact or actuator behavior.

The optional mobile comparison is a unicycle model. It is useful for understanding nonholonomic motion, but the arm's joint/configuration model is our main example.

## Practice

Compute the endpoint at zero joint angles, solve IK for the pickup and tray positions, and compare by applying forward kinematics again. Then try a target farther than the sum of the link lengths. Save a table of targets, joint solutions, and rejection reasons. Write down three effects the toy does not simulate.

## Checkpoint

<details><summary>Does an IK solution prove the arm can grasp the cube?</summary><p>No. It establishes a solution under the chosen geometric model. Orientation, joint limits, collision, reachability along the path, gripper contact, and execution still need evaluation.</p></details>

## Go deeper

- [PORA: Modeling Robot Dynamics](https://porabook.com/book/modeling-robot-dynamics/).
- [NVIDIA manipulator workflow](https://docs.isaacsim.omniverse.nvidia.com/latest/robot_setup_tutorials/tutorial_manipulator_workflow.html).
