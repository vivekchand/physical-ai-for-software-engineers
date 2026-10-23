## Learn the interface before the model name

**Primary sources reviewed 23 October 2026.** This is an introduction to model families and access patterns, not a performance ranking. Availability, licenses, supported robots, and model revisions can change.

For our arm task, imagine the instruction “put the red cube in the tray.” A useful policy must turn observations and state into an action representation the robot can execute. The controller, kinematic limits, scene, and task evaluation still matter.

## Four related ideas

| Family | What it does | What to avoid assuming |
|---|---|---|
| Demonstration policy, such as ACT | Learns actions from expert examples | Every imitation policy understands arbitrary language |
| Vision-language-action model (VLA) | Uses visual/language context and robot inputs to produce actions | A tensor output matches your arm's units, frames, or controller |
| World-action model (WAM) | Couples action prediction with a predictive world/video representation | Predicted video proves physical feasibility |
| World or embodied-reasoning model | Predicts developments or reasons about scenes and tasks | Its output is automatically an executable motor command |

Boundaries vary by architecture. Inspect the actual observation/action contract and training objective instead of relying only on the acronym.

## A useful starting set

| Project | Why read it | First practical step |
|---|---|---|
| [LeRobot ACT](https://huggingface.co/docs/lerobot/act) | An accessible demonstration-policy baseline, not inherently a language-conditioned VLA | Inspect a task dataset and action chunks before training |
| [SmolVLA](https://huggingface.co/docs/lerobot/smolvla) | A VLA route in the LeRobot ecosystem | Read camera/state preprocessing and checkpoint requirements |
| [OpenVLA](https://openvla.github.io/) | A reference for visual-language representations producing robot actions | Inspect the selected checkpoint's embodiment and action conventions |
| [Physical Intelligence π family](https://www.pi.website/blog/pi07) | VLA research connecting generalist learning and manipulation | Separate openpi checkpoints from newer hosted API models |
| [NVIDIA GR00T](https://github.com/NVIDIA/Isaac-GR00T) | Generalist VLA adaptation and deployment workflows | Choose an embodiment configuration and pin the model revision |
| [Dream Labs Dream-1](https://dreamlabs.ai/research/dream-1/) | A hosted WAM route for manipulation | Read the scope and interface, then choose a suitable simulation/recorded-data experiment |
| [DreamZero](https://dreamzero0.github.io/) | Research on jointly predicted video and actions | Study its inference/evaluation setup; distinguish it from Dream-1's service |
| [Gemini Robotics](https://deepmind.google/models/gemini-robotics/) | VLA, on-device, and embodied-reasoning variants | Identify which variant is available and whether it acts or reasons |

## Start with Dream Labs

[Dream Labs](https://dreamlabs.ai/) describes Dream-1 as a world-action model available through its platform. Its research introduction focuses on bimanual robots with parallel grippers and discusses end-effector outputs, inverse kinematics, and limitations. The main single-arm exercise here is not automatically compatible.

1. Read the [Dream-1 research introduction](https://dreamlabs.ai/research/dream-1/), especially the interface and limitations.
2. Inspect the [getting-started entry point](https://platform.dreamlabs.ai/setup-api) and current [platform docs](https://platform.dreamlabs.ai/docs/). Access may require an account; this guide has not authenticated or executed the API.
3. Inventory required cameras, state fields, action conventions, and controller/IK requirements for the chosen embodiment.
4. Use the [Playground](https://dreamlabs.ai/playground/) to distinguish simulation from real-robot sessions. Viewing a demo is not your own deployment evidence. This guide does not submit prompts or control those robots.
5. Before an API experiment, check current access, charges, licenses, data handling, and the supported environment. Keep keys out of notebooks and public repos.

## Physical Intelligence: research, open checkpoints, and hosted models

[openpi](https://github.com/Physical-Intelligence/openpi) supplies an open implementation and selected checkpoints in the π family. The [π0.7 research post](https://www.pi.website/blog/pi07) and [October 2026 API announcement](https://www.pi.website/blog/api-beta) describe newer work and hosted access. A paper or service announcement does not imply that the same weights are downloadable under the openpi license.

## Gemini: choose the variant

The reviewed [Gemini Robotics page](https://deepmind.google/models/gemini-robotics/) distinguishes Robotics 2 (VLA), Robotics ER 2 (embodied reasoning), and On-Device 2 (local VLA). Read the current model card and access instructions. An ER result can help plan a grasp without being a drop-in arm controller. Do not promise unrestricted API access or open weights for every variant.

## A practical route for a software engineer

1. Run the guide's scripted pick-and-place fixture and define what success means.
2. Inspect one LeRobot dataset and a demonstration baseline such as ACT.
3. Study SmolVLA or an available openpi/OpenVLA checkpoint with a matching documented setup.
4. Compare one hosted or larger-model route only when you can match its contract and resources.
5. Keep the same held-out scenes, object placements, and outcome rubric across comparisons.

You do not need to install or train every model in the 21-day core. Choose one reproducible path. [LeRobot's policy catalog](https://huggingface.co/docs/lerobot) provides further families as your needs grow.

## Write an observation/action contract

Before calling a model, fill in:

```text
model/checkpoint and revision:
embodiment / number of arms / joint names:
camera names, order, resolution, and timestamps:
state fields, units, normalization, and history:
output (joint targets / end-effector deltas / action chunk):
action frame and rotation convention:
control rate, chunk duration, and latency handling:
controller and IK solver:
expiry and stale-action handling:
grasp and placement evidence:
access, licenses, data handling, and compute:
```

Keep the observation, returned action, executed command, and measured outcome separate. Long action chunks create a timing question: which actions remain valid when a new image or cancellation arrives? Design expiry and supported interruption behavior deliberately.

## Compare evidence, not demo reels

Vary cube position, distractors, instruction wording, lighting, tray location, and an out-of-workspace target. Report completion, grasp failure, slip, latency distribution, interventions, and unknown outcomes. Use the same trial budget and disclose whether a robot/task appeared in adaptation data.

Claims about unseen robots or zero-shot behavior are claims under a particular evaluation setup. A vendor's successful video does not establish performance for your hardware or task.
