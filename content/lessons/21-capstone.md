## Build a report another engineer can reproduce

Return to your day-1 mission. Your final artifact is a working experiment plus an evidence-based explanation of its behavior. Select the route matching your actual environment.

### Laptop capstone

Run the control and estimation labs. Generate all five mission scenarios. Write an analyzer that reconstructs a task timeline, deduplicates request identifiers for counting, preserves raw events, and marks physical outcomes unknown when measurements are missing.

Use the example schema as a starting contract, not a universal robot standard. Do not claim you integrated ROS or Isaac when you only ran the synthetic fixture.

### ROS + Isaac capstone

Run one supported simulated delivery/navigation workflow. Collect task outcomes, state samples, transforms, clock information, and connection/freshness observations from real simulator interfaces. Use one normal run, one changed obstacle, and one disconnected observer.

Add policy training only if it serves your chosen task. An Isaac Lab Cartpole experiment can be a separate learning artifact; it does not need to be disguised as the warehouse controller.

## Your deliverables

| Artifact | What it should contain |
|---|---|
| `README.md` | Task, route chosen, prerequisites, exact reproduction commands |
| `environment.md` | OS, hardware, tool versions, commits, backend, assets, seeds |
| `architecture.md` | Nodes/components, frames, topics, control ownership, timing assumptions |
| `runs/` | Raw traces or bag references, run IDs, configurations, results |
| `report.md` | Success criteria, failure cases, evidence, unknowns, and limitations |
| `next.md` | The next experiment most likely to challenge your conclusions |

Keep recordings and sensitive data out of public repositories unless you have permission to publish them. The portable synthetic fixtures are safe to share as examples.

## Evaluate yourself honestly

Score each item 0, 1, or 2: absent, partial, or independently reproducible.

1. The task and outcome are measurable.
2. Frames, units, timestamps, and run identity are explicit.
3. State estimates and physical truth are distinguished.
4. Failure cases include a useful unknown state.
5. The experiment reproduces from its instructions.
6. Claims stay within the evidence and environment tested.

A score is a prompt for review, not a professional qualification. Ask another engineer to reproduce one run and identify one claim they cannot verify.

## A book starts with examples that survive scrutiny

If you turn these notes into a book, keep the original Markdown chapters, versioned exercises, primary sources, and correction history together. Add real failure investigations and hardware experience over time. ClawMetry can supply a perspective on observability without making the robotics material depend on one product.

## Checkpoint

<details><summary>What does completing 21 days establish?</summary><p>A foundation and the specific practical work you actually completed. It does not establish general robotics expertise, hardware compatibility, safety certification, or proficiency with every NVIDIA tool. Your reproducible artifacts make the accomplishment concrete.</p></details>

## Continue

- Revisit the [PORA exercises](https://porabook.com/exercises/) and implement one algorithm without a completed notebook.
- Choose one physical platform with a qualified partner and study its supported interfaces.
- Read the guide's “After day 21” field note for a 90-day continuation.
