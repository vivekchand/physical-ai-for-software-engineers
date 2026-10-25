## Define the result before running the robot

For our task, success means the cube is inside the specified tray region, released, and stable for the chosen observation window. Record the region, tolerance, window, measurement source, and timeout. Select values for the experiment rather than treating this guide as a hardware specification.

The last arm waypoint, a closed gripper, and a high training reward are useful intermediate signals. The operational result needs object evidence. Preserve **unconfirmed** when the observation path cannot determine the outcome.

## Make comparisons answer one question

Freeze the task definition, scene/asset revision, initial-condition list, observation/action interfaces, timeout, and intervention rules. Compare a scripted baseline with a candidate policy under the same condition distribution. Where possible, pair trials by scenario and seed, and alternate execution order to reduce session effects.

Keep training, validation, and held-out test conditions separate. Changing the policy after inspecting test failures turns those cases into development data; use a new held-out set for the next final comparison. Three trials are enough to debug a report, not enough to establish deployment reliability.

## Count every attempt

| Measurement | Definition for this guide's lab |
|---|---|
| Attempts | Every declared trial, including failures and unconfirmed outcomes |
| Verified placement rate | Verified placements / attempts, including placements with human help |
| Autonomous verified rate | Verified placements with no intervention / attempts |
| Intervention rate | Attempts with any human intervention / attempts |
| Unconfirmed outcomes | Attempts whose placement outcome could not be established |
| Autonomous verified throughput | Autonomous verified placements / total elapsed trial hours |

For throughput, elapsed time includes approach, failed attempts, recovery, and reset. A success-only average hides the cost of failure. Any unrecorded downtime must be added before using this as shift-level throughput.

An unconfirmed result is not automatically a physical failure. Keeping it in the denominator makes the reported rate a rate of **verified** outcomes. Show the raw counts so the reader can see why verification was unavailable. Similarly, a placement after operator help can be physically successful while failing the autonomous criterion.

## Run the laptop evaluation lab

From the cloned repository:

```bash
python3 examples/evaluate.py
python3 examples/evaluate.py --input examples/data/policy_trials.jsonl
```

The script reads 12 deliberately invented trial records and prints a grouped JSON report. It does not run a policy, simulator, or robot. Every provided trial declares `evidence: "synthetic"`. Download the [script]({{base}}/examples/evaluate.py) and [trial fixture]({{base}}/examples/data/policy_trials.jsonl) together if working outside a clone.

If both downloaded files are in the same folder, run `python3 evaluate.py --input policy_trials.jsonl` from that folder.

Expected counts:

| Policy | Condition | Verified placements | Autonomous verified | Unconfirmed | Interventions |
|---|---|---|---|---|---|
| baseline-v1 | nominal | 2 / 3 | 2 / 3 | 0 | 0 |
| candidate-v1 | nominal | 3 / 3 | 2 / 3 | 0 | 1 |
| baseline-v1 | shifted-tray | 2 / 3 | 2 / 3 | 0 | 0 |
| candidate-v1 | shifted-tray | 1 / 3 | 1 / 3 | 1 | 0 |

The candidate looks attractive on nominal placement and speed. The intervention count and shifted-tray condition change that interpretation. The report separates conditions and evidence sources rather than pooling them into a flattering headline.

Try changing a fixture copy: turn an unconfirmed outcome into a failed observation, add an intervention to a successful trial, then duplicate an attempt ID. Predict the metric changes and the validation error. Save `evaluation-report.md` explaining which conclusion survives these changes. These labels are synthetic teaching data, not measured baseline/model performance.

## A small sim-to-real test matrix

| Variation | What might change | Evidence to compare |
|---|---|---|
| Lighting and occlusion | Cube detection and pose uncertainty | Image, detection/pose, source timestamp |
| Camera moved slightly | Extrinsics and reachable grasp estimate | Calibration revision, transforms, target pose |
| Friction or object mass | Slip and grasp stability | Contact/object motion, gripper state |
| Observation delay | Action based on an earlier scene | Capture time, inference time, execution time |
| Gripper wear or backlash | Actual motion differs from the model | Command, encoder state, object result |
| Observer disconnect | Missing outcome evidence | Last fresh sample, connection status, unconfirmed count |

First isolate one variable, then test combinations that resemble the intended environment. Record the ranges and why you chose them. Randomized training ranges and held-out evaluation cases serve different purposes.

## Validate a digital twin

A digital twin represents a particular physical system for a stated purpose. A detailed 3D scene alone does not establish that relationship. For grasp testing, inspect dimensions, mass/inertia, joint limits, actuator response, collisions, materials/contact, camera calibration, and timing. A visually simple model can answer a narrow question better than an attractive scene with incorrect contacts.

[Isaac Sim](https://developer.nvidia.com/isaac/sim/) supports importing robot descriptions and composing simulation scenes. URDF describes robot links/joints and related properties; OpenUSD supports composable scene representation. Importing one into the other is an engineering step that needs validation, especially across [asset-pipeline changes](https://docs.isaacsim.omniverse.nvidia.com/latest/migration_guides/isaac_sim_6_0/urdf_mjcf_importer_exporter_pipeline.html).

World-model video can suggest a scenario or augment appearance. Verify task labels, temporal alignment, and geometry after generation. Use measured or simulator state for claims about contact, distances, and placement where appropriate; realistic video does not certify those quantities.

## Transfer in stages

For GPU experiments, the [scene-building workshop](isaac-foundations.md) adds diagnostics for GPU selection, collision geometry, camera depth, and clock interpretation. Exposure/noise/blur tests on synthetic images measure robustness to those selected changes. They do not define a guaranteed mathematical lower bound on real-world error.

Record an evidence ladder in your report: mathematical fixture → supported simulator trial → held-out simulation conditions → bounded, supervised hardware trials with the responsible operator. At each step, name the assumptions the previous step could not test.

Use [GR00T's open-loop and closed-loop evaluation examples](https://github.com/NVIDIA/Isaac-GR00T#evaluation) and [Isaac Lab's sim-to-real resources](https://isaac-sim.github.io/IsaacLab/v3.0.0/source/features/imitation-learning/index.html) for project-specific workflows. Their benchmark scores describe their tested conditions and do not replace your evaluation.

<details><summary>One hundred simulated trials all succeed. Can you report 100% real-world reliability?</summary><p>No. Report the observed simulated counts and conditions. Finite samples leave uncertainty, and transfer introduces sensing, contact, actuator, and timing differences that simulation results alone do not measure.</p></details>
