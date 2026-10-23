## Choose a useful task you can measure

An arm, a cube, and a tray teach a useful pattern: identify an object, manipulate it under constraints, and verify the result. Extend that pattern before jumping to a general-purpose humanoid.

| Application to investigate | What carries over | What the cube exercise leaves out |
|---|---|---|
| Sorting packaged parts into bins | Object pose, grasp, placement, recovery | Many shapes, clutter, packaging damage, sustained throughput |
| Machine tending | Approach, grasp, handoff, verification | Machine state, fixtures, interlocks, tooling, cycle coordination |
| Kitting an order | Task selection, semantic labels, tray regions | Inventory errors, ambiguous parts, order completeness |
| Handling deformable objects | Observation/action learning and evaluation | Shape changes, uncertain contact, material behavior |
| Mobile manipulation | Arm task plus localization and navigation | Reachability from the base, moving scenes, shared workspaces |

These are directions for study, not claims that a particular product solves them. Start with a bounded task and a baseline that already has a measured result.

## Write the operating envelope

For a parts-sorting pilot, specify supported parts, presentation, lighting, clutter, tray location, allowable damage, cycle-time target, replenishment, and recovery ownership. Name what happens outside that envelope. A person requesting a task in natural language does not make an unsupported object or grasp valid.

Use a fixed fixture or classical vision/planning when it meets the requirements. Consider a learned policy when variation or demonstration data makes it useful. Compare engineering effort and outcomes under the same conditions. A VLA can add language-conditioned behavior, but its integration and evaluation still cost time.

## Measure useful work over a complete shift

Start with three quantities:

```text
verified throughput = accepted completed units / elapsed operating hours
intervention load = operator minutes spent helping / elapsed operating hours
cost per accepted unit = total attributable operating cost / accepted completed units
```

Define accepted quality independently of whether the robot completed its motion. Include downtime, failed attempts, resets, replenishment, and rework. Track autonomous units separately from units completed with help. Keep shift-level figures separate from the short trial throughput in the [evaluation lab](evaluation.md).

Count costs for the same period and scope: equipment allocation, integration amortization, labor, support, compute, consumables, maintenance, and rejected units. Avoid counting an operator's intervention time twice if it is already included in paid attendance. Time saved is not automatically money saved; it might instead increase capacity or improve ergonomics.

## Work a deliberately hypothetical example

Imagine a pilot produces **900 accepted units from 1,000 attempts** in an eight-hour shift. All numbers below are invented to demonstrate the calculation, not equipment prices, market rates, or an ROI forecast.

| Cost attributed to the shift | Hypothetical USD |
|---|---:|
| Attending labor: 8 hours × $25 | 200 |
| Separate specialist support: 2 hours × $30 | 60 |
| Equipment and integration allocation | 50 |
| Compute, energy, consumables, and rework | 40 |
| Total | 350 |

The cost is `$350 / 900 ≈ $0.389` per accepted unit. Throughput is `900 / 8 = 112.5` accepted units/hour. If a comparable manual workflow costs $150 to produce those same 900 accepted units, the robot has not yet demonstrated an operating-cost advantage in this example.

The next experiment might reduce attendance, intervention, rework, or changeover effort. Recalculate using measured values. Keep implementation cost and assumptions visible; a success-rate improvement alone is not an ROI calculation. If an investment never produces positive net savings, a simple payback period is not defined.

## A one-page pilot decision

Save `pilot-decision.md` containing the task/envelope, baseline, accepted-quality rule, condition-level results, operator load, full-shift throughput, costs with assumptions, and a go/revise/stop decision. Write the observation that would change your mind.

Use the [learning pipeline](robot-learning.md) to justify the chosen method and the [NVIDIA map](nvidia.md) to justify each tool. [NVIDIA's robotics overview](https://www.nvidia.com/en-us/industries/robotics/) describes its training/simulation/deployment roles; your pilot measurements establish whether that architecture helps your task.

<details><summary>The new policy raises placement rate. Has the pilot proved economic value?</summary><p>Not by itself. Measure quality, elapsed throughput, intervention and maintenance load, and total comparable costs. A higher placement rate can coexist with lower throughput or greater operator effort.</p></details>
