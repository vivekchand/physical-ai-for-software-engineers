## Demonstrations supply another kind of supervision

Imitation learning uses expert behavior as training information. Behavior cloning learns to predict demonstrated actions from observations. Inverse reinforcement learning attempts to infer a reward from demonstrations. The quality, coverage, and consistency of the demonstrations matter.

A policy can drift into states missing from its training data. Small action errors change future observations, so imitation is not simply independent classification over a fixed test set. Recovery behavior and operator corrections deserve their own evaluation.

## Where a VLA model fits

A vision-language-action model takes visual and language information, often with robot state, and produces actions in a defined representation. The output might be joint targets, end-effector deltas, or a sequence of actions. A natural-language instruction alone does not specify the controller interface.

NVIDIA's reviewed GR00T repository describes N1.7 as a generalist VLA model with an embodiment-specific adaptation workflow. Treat “generalist” as a model's scope of intended capability, not evidence it can control your robot without matching interfaces and evaluation. OpenVLA and Physical Intelligence's pi-zero work are other primary research examples to compare.

## Inspect before downloading weights

Read the model card and repository at a pinned commit. Record:

1. Expected images, state fields, normalization, and history.
2. Action dimensions, units, coordinate frame, representation, and rate.
3. Supported embodiment configuration and controller assumptions.
4. Inference and fine-tuning hardware requirements separately.
5. Model, code, and dataset licenses, including any gated access.

Never feed a model output directly into unfamiliar hardware just because the tensor dimensions match.

## Today's practice

Create a model-interface table for GR00T using its current documentation. Compare it with the actual interface of your simulated robot. Identify at least three adaptations or validations that would be required.

Optional GPU extension: follow the repository's inference example using its supplied demonstration data, pinned model revision, and required environment. Log preprocessing, inference duration, action shape, and model version. Do not describe this as robot deployment. Large-model setup is optional in the 21-day core.

## Checkpoint

<details><summary>Does an action vector with the right length establish compatibility?</summary><p>No. Units, frames, normalization, action meaning, timing, controller expectations, and embodiment matter. A valid tensor can encode the wrong motion.</p></details>

## Go deeper

- [PORA: Imitation Learning](https://porabook.com/book/imitation-learning/).
- [NVIDIA Isaac GR00T repository](https://github.com/NVIDIA/Isaac-GR00T).
- [OpenVLA research](https://openvla.github.io/).
- [Physical Intelligence: pi-zero](https://www.pi.website/blog/pi0).
