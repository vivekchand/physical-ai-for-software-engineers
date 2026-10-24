## First learn from demonstrations

Imitation learning uses expert behavior as training information. Behavior cloning learns demonstrated actions from observations. Inverse reinforcement learning attempts to infer a reward from demonstrations. Data quality, coverage, and consistency matter.

For the red-cube task, record observation/state/action sequences for successful grasps, transfers, releases, and recoveries. A model can drift into states absent from those demonstrations. Each action changes the next observation, so independent frame accuracy alone is a poor measure of closed-loop skill.

## VLA, WAM, and a useful baseline

A vision-language-action model (VLA) connects visual/language context and robot inputs to a defined action representation. A world-action model (WAM) couples action prediction with predictions of the world/video. A conventional imitation policy such as ACT supplies a useful baseline without inherently understanding arbitrary task language.

For our task, compare these routes:

| Route | A reference to study | The first question |
|---|---|---|
| Demonstration baseline | LeRobot ACT | Does the training data cover this arm and task? |
| Accessible/open VLA workflows | SmolVLA, OpenVLA, selected openpi checkpoints | What cameras, state, preprocessing, and actions are expected? |
| Larger/generalist VLA | NVIDIA GR00T, Physical Intelligence π family | Which embodiment and checkpoint actually match? |
| WAM | Dream Labs Dream-1, DreamZero research | How are action prediction and world prediction connected? |
| Robotics model family | Gemini Robotics | Is the selected variant a controller/VLA or an embodied reasoner? |

Use the [Models field note](../pages/models.md) for current primary links, access distinctions, and a practical route. This is a map of approaches, not a leaderboard.

## Dream Labs and the arm example

Dream-1 is introduced by Dream Labs as a hosted WAM for manipulation. Its reviewed scope emphasizes bimanual parallel-gripper robots. A single Franka or SO-101 exercise is not automatically a matching embodiment. Consult its published limitations and current platform requirements before choosing an experiment.

The same rule applies to every model: visual similarity to a demo does not establish compatibility.

## Language understanding is one part of execution

For “put the red cube in the tray,” distinguish identifying the intended object from choosing a feasible grasp and executing it. A model's action representation may be joint targets, end-effector deltas, continuous chunks, or a controller-specific latent. Do not assume the same output directly drives every robot's motors.

“Zero-shot” describes what adaptation was omitted in a particular evaluation. It is not a guarantee for arbitrary tasks, instructions, or hardware. Record which objects, layouts, and embodiments the evidence covers. The [learning guide](../pages/robot-learning.md) explains dataset splits and chunk execution; the [evaluation guide](../pages/evaluation.md) supplies a comparison protocol.

## Inspect before running

Read the model card and repository at a pinned revision. Record expected camera views and timestamps, state fields, normalization/history, joint or end-effector actions, coordinate frames, units, chunk duration, control rate, IK/controller requirements, compute, and licenses.

Open source code, open model weights, research descriptions, hosted inference, and commercial support are separate access questions. The π family's openpi checkpoints are not a promise that every newer hosted model is downloadable. A Gemini reasoning endpoint is not automatically a motor controller.

## Practice

Write an observation/action contract for one open-model route and Dream-1. Compare both with your arm task and record mismatches. Then choose one route to study further. On a suitable environment, use the selected project's supplied-data inference example before planning robot execution. The guide does not authenticate services, upload observations, or control remote playground robots.

## Checkpoint

<details><summary>Does an action vector with the right length establish compatibility?</summary><p>No. Units, frames, normalization, action meaning, timing, controller expectations, and embodiment matter. A valid tensor can encode an unsuitable motion.</p></details>

## Go deeper

- [PORA: Imitation Learning](https://porabook.com/book/imitation-learning/).
- [Dream-1 research](https://dreamlabs.ai/research/dream-1/) and [DreamZero](https://dreamzero0.github.io/).
- [LeRobot](https://huggingface.co/docs/lerobot), [OpenVLA](https://openvla.github.io/), and [openpi](https://github.com/Physical-Intelligence/openpi).
- [GR00T](https://github.com/NVIDIA/Isaac-GR00T) and [Gemini Robotics](https://deepmind.google/models/gemini-robotics/).
