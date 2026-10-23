## Start with the behavior you need

Our arm must put a cube into a tray, with fresh observations and a verified result. A learned policy is one way to choose its actions. First make a scripted baseline work; then identify a variation it handles poorly. This gives learning a measurable purpose.

| Approach | What you supply | What changes during learning | First arm experiment |
|---|---|---|---|
| Scripted planning and feedback | Geometry, task states, constraints, controllers | No learned policy is required | Move a known cube, then change its position |
| Behavior cloning | Demonstration observations paired with actions | A policy predicts demonstrated actions | Compare imitation on familiar and held-out placements |
| Reinforcement learning | Environment, observations/actions, reward, termination | A policy improves its expected return through interaction | Test whether reward favors moving the cube or just the gripper |
| VLA adaptation | A pretrained checkpoint, matching demonstrations, language, embodiment configuration | Selected model parameters adapt to the task | Test a compatible checkpoint with new layouts and instructions |
| World-model-assisted learning | A model of possible developments plus a learning/planning procedure | The world model, policy, or both, depending on the method | Check whether predicted outcomes agree with an independent evaluator |

These approaches can be combined. Real-robot learning also exists; simulation is a useful tool whose necessity depends on the method and experiment. A camera-guided planner can adapt without a VLA. A VLA can fail on an unfamiliar cube pose.

## Two objectives, one operational test

Behavior cloning asks: **given this observation, what action did the demonstrator take?** A simple continuous-action objective minimizes prediction error. An action target that is delayed, in the wrong frame, or normalized incorrectly teaches the wrong behavior even if loss decreases.

Reinforcement learning asks: **which actions lead to greater accumulated reward?** A reward for reaching the tray can favor an empty gripper. A reward for holding the cube can favor never releasing it. Keep the operational success rule independent of reward.

For both methods, evaluate a full episode: the robot acts, the world changes, and the next observation depends on the previous action. Predicting actions on a fixed recording is an **open-loop check**. Executing a policy in an environment is a **closed-loop trial**. Passing the first helps diagnose an interface; it does not establish the second.

Use [LeRobot's imitation workflow](https://huggingface.co/docs/lerobot/il_robots) for the record/train/evaluate lifecycle and [Isaac Lab's versioned imitation-learning overview](https://isaac-sim.github.io/IsaacLab/v3.0.0/source/features/imitation-learning/index.html) for its demonstration-generation routes. These projects have their own dependencies and supported hardware.

## A demonstration is an episode, not a photograph

An episode records a task from initial condition through outcome and reset. Write the contract before collecting data:

| Field | An example contract for our experiment |
|---|---|
| Identity | Episode, recording session, operator, task, robot, and calibration revision |
| Observations | Named camera views, capture timestamps, joint state, gripper state |
| Instruction | The task text actually available to the policy |
| Actions | Joint targets or end-effector deltas, units, frame, gripper encoding |
| Timing | Observation/action alignment, nominal rate, gaps, action horizon |
| Outcome | Placement evidence, failure reason, interventions, unknown measurements |
| Provenance | Real, simulated, or synthetic fixture; license and publication permission |

An image's delivery time is not its capture time. A logged joint position is not necessarily the action requested at that instant. Check alignment on a short episode before recording hundreds.

LeRobot datasets associate video with state/action information and episode metadata. Check the selected consumer's exact schema. For example, the reviewed GR00T N1.7 workflow uses a LeRobot-v2-style format with additional modality metadata; a current LeRobot-v3 dataset may require conversion. See [LeRobot's dataset documentation](https://huggingface.co/docs/lerobot/lerobot-dataset-v3) and [GR00T's data preparation](https://github.com/NVIDIA/Isaac-GR00T#data-format).

## Split the data before choosing a model

Adjacent video frames share almost the same scene. Randomly putting frames from one episode into both training and testing can produce reassuring scores without measuring a new trial.

Start by splitting entire episodes. When the question is generalization to a new session, object, camera setup, or layout, keep that entire group out of training. Document exactly what is held out. Fit normalization using the training split and retain it with the checkpoint. Select settings on validation data; reserve the test split for a frozen comparison.

Example design: train on several cube positions and two recording sessions; validate on a third session; test on a fourth session with a shifted tray. This tests session/layout change. It does not establish generalization to new grippers, materials, or embodiments.

## From a VLA output to a motor command

An illustrative integration is:

```text
camera + robot state + instruction
                ↓
       policy preprocessing
                ↓
      VLA action prediction
                ↓
denormalization + frame/unit conversion
                ↓
  supported controller / IK interface
                ↓
    local feedback and actuators
```

Some models predict continuous action chunks; others use tokens or latent representations. The selected checkpoint and controller determine the meaning. Do not assume every VLA predicts torque, balances a humanoid, or accepts arbitrary cameras. Speech may need a separate transcription step when the model expects text.

Suppose an illustrative policy predicts 20 actions at 10 Hz: that is a two-second prediction horizon. Executing only the first two actions before reobserving gives a different feedback pattern from executing all 20. Those numbers describe this example, not a recommended robot rate. Define what happens when an observation is stale, a chunk expires, or an interruption arrives.

The [GR00T repository](https://github.com/NVIDIA/Isaac-GR00T) documents its controller connection and embodiment-specific action interfaces. The [model guide](models.md) compares those requirements with Dream Labs and other VLA/WAM routes.

## Practice: produce a learning plan

Save `learning-plan.md` with a baseline, one target variation, the observation/action contract, dataset split groups, learning method, compute plan, and a fixed evaluation rule. Include one reason a larger model might not help.

On a laptop, run the [evaluation lab](evaluation.md#run-the-laptop-evaluation-lab). On a suitable training machine, follow a pinned project's supplied-data example before recording a new robot. Save dataset and checkpoint revisions, preprocessing, configuration, and evaluation results together.

<details><summary>A policy has lower action-prediction error. Is it better at pick-and-place?</summary><p>Not necessarily. It may fit familiar recordings while drifting during execution. Compare closed-loop outcomes under fixed conditions and preserve intervention and unknown-result counts.</p></details>
