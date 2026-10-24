## What you are learning

A robot is a program whose outputs change its future inputs. Reaching for a cube changes the next camera image. Closing a gripper changes contact with the object. Your code operates inside that loop.

Imagine a backend accepting a job and reporting that a worker received it. A pick-and-place arm adds another question: did the cube actually end up in the tray? An accepted command, a controller's estimate, and an independently observed outcome are different pieces of evidence.

## The software instincts to keep

Keep modular interfaces, reproducible tests, version control, observability, and explicit ownership. They matter here too. Extend them with three habits:

- **State has uncertainty.** A reported position can be wrong even when the message is valid.
- **Timing changes behavior.** A correct observation delivered late can be useless for a decision.
- **Actions have physical persistence.** A robot has velocity and momentum while your application is waiting.

Automation can work in a carefully arranged environment. Autonomy involves choosing actions as circumstances change. Physical AI adds learned perception, reasoning, or action policies to embodied systems. These categories overlap; none automatically implies general intelligence or reliable operation everywhere.

## Three ways to move the same cube

| System | How it chooses an action | What happens when the cube moves? |
|---|---|---|
| Fixed sequence | Recorded coordinates | The grasp can miss |
| Perception, planning, and feedback | Updated object pose and an explicit controller | It can replan within its modeled limits |
| Learned policy | A trained observation-to-action mapping | It may adapt within its learned coverage; test it |

Classical robotics includes sensing, feedback, optimization, and adaptation. Physical AI is broader than VLAs. ROS 2 can connect any of these approaches; using it does not determine whether behavior is scripted or learned.

## One running example

Throughout this guide, a tabletop arm puts a red cube in a tray. It must locate the cube, transform the pose into the arm's frame, reach a grasp, close the gripper, lift, transfer, release, and verify placement. A person can request an interruption. We will keep asking what each subsystem actually knows.

Start with a transparent scripted baseline. Later, examine how a demonstration policy, VLA, or world-action model could replace part of it. The [pick-and-place field note](../pages/manipulation.md) includes a browser IK experiment and a runnable Python lab. Mobile robots remain a secondary example for localization and navigation.

You can learn the core ideas on a laptop. GPU exercises later use manufacturer-supported environments. A small mathematical model, a photorealistic simulation, and a physical robot are three different kinds of evidence.

## Practice

Write a one-page mission specification:

1. What counts as a successful placement? Define a tray region, release condition, and stability check.
2. What can the robot sense? What remains unknown?
3. Which failures should be recoverable, and which require an operator?
4. Who can authorize the task, and who owns the machine's local control?

Save it as `mission.md`. Revisit it on lesson 21. Work through the exercise at your own pace; the short reading is only the beginning.

Add one changed-cube-position scenario and predict how each approach above could fail. The optional [applications guide](../pages/applications.md) helps turn the mission into a useful pilot.

## Checkpoint

<details><summary>The API returns “accepted.” Has the robot completed the task?</summary><p>No. Acceptance is evidence about the request interface. Completion needs task-result evidence, and physical claims need suitable state measurements. The exact evidence depends on the robot and workflow.</p></details>

## Go deeper

- [PORA: Preface](https://porabook.com/book/preface/) for the integrated view of autonomy.
- [PORA: Robot Autonomy Software](https://porabook.com/book/software/) for the systems perspective.

These are optional deeper readings. The explanations and tabletop exercises here are original, independent educational material.
