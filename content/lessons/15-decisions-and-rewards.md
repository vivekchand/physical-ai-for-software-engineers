## Choose a behavior, then execute it

The manipulation mission can be expressed as task modes: observing, approaching, grasping, lifting, transferring, releasing, verifying, and recovering. A finite state machine makes those modes and allowed transitions explicit. It is easy to inspect when the number of modes and interactions stays manageable.

As tasks grow, hand-written transitions can become difficult to maintain. Sequential decision-making asks which action to choose when its consequences extend into the future. Dynamic programming relates the value of a current decision to values of subsequent states. Stochastic formulations account for uncertain outcomes.

## Reward is an engineering choice

Reinforcement learning learns behavior from interaction and numerical reward. A policy maps observations or state information to actions. A value estimate describes expected future return under the relevant assumptions. Exploration gathers information, but can be expensive or unacceptable on real machines.

For the arm, “reward for reaching the tray” can encourage moving an empty gripper. “Reward for closing the gripper” may not ensure the cube is held. A termination rule can also create shortcuts: ending an episode early might avoid accumulated penalties.

Keep at least three measurements separate:

- The training reward the algorithm optimizes.
- The operational success criterion from lesson 1.
- Constraint violations, interventions, and adverse outcomes.

Partial observations complicate matters further. An instantaneous camera frame may not reveal velocity or what is hidden behind an obstacle. History or a maintained belief can matter for decisions.

## Practice

Write a state machine for pick-and-place and interruption. Include an explicit unknown/outcome-not-confirmed condition rather than forcing every task into success or failure.

Then propose a reward with three terms and invent a behavior that exploits it. Explain what held-out evaluation would reveal the problem. Use the Markovian Drone or Cartpole notebook in PORA if you want a runnable decision-learning example before the GPU workflow.

## Checkpoint

<details><summary>If average training reward rises, is the pick-and-place system improving?</summary><p>Possibly, but not necessarily. The reward may be misaligned with completion, the evaluation distribution may be too narrow, or failures may be hidden by averages. Check task outcomes and constraints on separate trials.</p></details>

## Go deeper

- [PORA: Finite State Machines](https://porabook.com/book/finite-state-machines/).
- [PORA: Sequential Decision Making](https://porabook.com/book/decision-making/).
- [PORA: Reinforcement Learning](https://porabook.com/book/reinforcement-learning/).
