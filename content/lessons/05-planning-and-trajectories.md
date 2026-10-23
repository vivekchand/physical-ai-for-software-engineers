## Where, when, and whether it is possible

A path describes a geometric route. A trajectory specifies how the robot should move over time. A controller attempts to execute it. Treating these as one operation makes failures harder to understand.

For our arm, a path moves through joint configurations toward a grasp or tray pose. A feasible trajectory must also respect joint limits, velocity, acceleration, actuator constraints, and the cube carried after grasp. Nearby people or moving objects add time-dependent constraints.

## Three families to recognize

**Graph search:** represent reachable locations and connections as a graph. A* uses accumulated cost plus a heuristic to prioritize exploration. Optimality depends on the graph, cost model, and heuristic assumptions. A coarse grid can miss a passage or distort clearance.

**Sampling:** methods such as RRT grow a structure through sampled configurations; PRM constructs a roadmap. These approaches help explore large configuration spaces. Collision checking and termination criteria remain important costs.

**Trajectory optimization:** choose a sequence of states and inputs to reduce an objective while satisfying constraints. The objective might trade travel time, energy, and smoothness. Local solutions, initialization, and model accuracy matter.

Configuration space includes the robot's joint configuration and geometry. Checking only the gripper tip can miss an elbow hitting the table. After grasp, include the carried cube in the relevant collision geometry. The optional mobile comparison similarly needs the robot's footprint, not just a point.

## Failure is information

“No plan found before timeout” is different from proving that no feasible route exists. “Plan invalidated” is different from controller failure. Record the goal, map version, planner configuration, constraints, result status, and computation time.

Repeated planning can be a reasonable response to a changing obstacle. Diagnose whether the updates produce progress before calling the system stuck.

## Today's practice

Run the A* notebook linked below. Add an obstacle across a corridor, then open a narrow passage. Change the grid resolution. Explain whether a failure comes from the environment, the discretization, or the search budget.

Then sketch approach, grasp, lift, transfer, place, and retreat phases for the arm. Identify when object attachment changes the collision model. Describe why interpolating between two valid joint configurations does not establish that every intermediate configuration is valid.

## Checkpoint

<details><summary>The planner found a collision-free path. Can the robot necessarily follow it?</summary><p>No. The path may not satisfy kinematic or dynamic constraints, timing may be unsuitable, and execution depends on sensing and control. “Collision-free” also depends on the modeled robot and obstacles.</p></details>

## Go deeper

- [PORA: Motion Planning](https://porabook.com/book/motion-planning/).
- [PORA: Open-Loop Control and Trajectory Optimization](https://porabook.com/book/open-loop-control/).
- [PORA exercises](https://porabook.com/exercises/): A*, RRT, and PRM.
