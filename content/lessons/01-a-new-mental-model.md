## What you are learning

A robot is a program whose outputs change its future inputs. Driving forward changes the next camera image. Reaching for a box changes the geometry of the scene. Your code operates inside that loop.

Imagine a delivery service. A backend can accept a request, enqueue a job, and report that the worker received it. A delivery robot adds another question: did the physical delivery happen? An accepted command, a controller's estimate, and an independently observed outcome are different pieces of evidence.

## The software instincts to keep

Keep modular interfaces, reproducible tests, version control, observability, and explicit ownership. They matter here too. Extend them with three habits:

- **State has uncertainty.** A reported position can be wrong even when the message is valid.
- **Timing changes behavior.** A correct observation delivered late can be useless for a decision.
- **Actions have physical persistence.** A robot has velocity and momentum while your application is waiting.

Automation can work in a carefully arranged environment. Autonomy involves choosing actions as circumstances change. Physical AI adds learned perception, reasoning, or action policies to embodied systems. These categories overlap; none automatically implies general intelligence or reliable operation everywhere.

## One running example

Throughout this guide, our robot moves a box from pickup A to dock B in a simulated warehouse. It must find the box, estimate where it is, choose a route, follow it, and report what happened. A person can request a cancellation. We will keep asking what each subsystem actually knows.

You can learn the core ideas on a laptop. GPU exercises later use manufacturer-supported environments. A small mathematical model, a photorealistic simulation, and a physical robot are three different kinds of evidence.

## Today's practice

Write a one-page mission specification:

1. What counts as a successful delivery? Specify a measurable outcome.
2. What can the robot sense? What remains unknown?
3. Which failures should be recoverable, and which require an operator?
4. Who can authorize the task, and who owns the machine's local control?

Save it as `mission.md`. Revisit it on day 21. Plan about 60 minutes including the exercise; the short reading is only the beginning.

## Checkpoint

<details><summary>The API returns “accepted.” Has the robot completed the task?</summary><p>No. Acceptance is evidence about the request interface. Completion needs task-result evidence, and physical claims need suitable state measurements. The exact evidence depends on the robot and workflow.</p></details>

## Go deeper

- [PORA: Preface](https://porabook.com/book/preface/) for the integrated view of autonomy.
- [PORA: Robot Autonomy Software](https://porabook.com/book/software/) for the systems perspective.

These are optional deeper readings. The explanations and warehouse exercises here are original, independent educational material.
