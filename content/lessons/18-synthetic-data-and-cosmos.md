## Data is part of the system

A perception model trained on clean, centered boxes may fail when lighting changes or an object is partially hidden. A learned controller can exploit simulator artifacts. More samples only help when they broaden useful coverage or improve the learning signal.

Domain randomization changes aspects of an environment: textures, illumination, object placement, friction, mass, sensor noise, or delay. Choose ranges based on plausible deployment conditions and measured uncertainty. Arbitrary randomization can waste compute or teach irrelevant behavior.

## Three tools, three jobs

**Replicator** supports synthetic-data generation in the simulation ecosystem. Scene state can supply labels such as instance identity or geometry. Check that the selected annotator and output meaning match your downstream task.

**World models**, including NVIDIA Cosmos-related projects, can generate or reason about possible visual developments and scenarios. Generated video can broaden ideas or datasets, but a plausible frame is not a validated physical trajectory or collision-free plan.

**Evaluation design** determines which scenarios are held out, what constitutes success, and how failures are measured. It is your responsibility even when the training data and simulator come from a vendor.

## A practical dataset experiment

Use the synthetic-data tutorial for your installed Isaac Sim release. Begin with one box and one camera. Generate a small baseline set, then vary lighting and camera position while keeping a separate held-out condition.

Inspect a few samples manually. Are labels aligned? Is depth in the expected units? Does occlusion affect ground truth as expected? Save the generation configuration and seed, along with asset and tool versions.

If you cannot run GPU generation, design the experiment using an explicit scene specification and a failure taxonomy. Label it a design artifact rather than a generated dataset.

## Today's practice

Write a test matrix for low lighting, reflective packaging, partial occlusion, changed friction, and delayed observations. For each condition, name the subsystem being tested and the measurement that would expose a failure.

Optional extension: inspect a Cosmos project's model card and example output. List what it can suggest and what still needs validation in a simulator or physical environment.

## Checkpoint

<details><summary>Does photorealistic synthetic data eliminate the sim-to-real gap?</summary><p>No. Appearance is only one source of mismatch. Dynamics, contacts, sensing, timing, calibration, data coverage, and operator behavior can differ.</p></details>

## Go deeper

- [Isaac Sim synthetic data and tutorials](https://docs.isaacsim.omniverse.nvidia.com/latest/index.html).
- [NVIDIA Cosmos projects](https://github.com/nvidia-cosmos).
- [PORA: Prospects](https://porabook.com/book/prospects/).
