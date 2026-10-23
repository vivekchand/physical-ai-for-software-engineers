## Understand the experiment before training

Isaac Lab provides environments and workflows for robot learning. An environment defines observations, actions, dynamics, resets, reward, and termination. A training library updates a policy. A simulator or backend advances the world. Inspect these boundaries before changing a network architecture.

**Reviewed baseline:** Isaac Lab 3.0.0 documentation, 23 October 2026. Version 3 introduces unified `train` and `play` entrypoints. Older tutorials using backend-specific `train.py` paths do not describe the same CLI.

## A small reference workflow

Follow the v3.0.0 installation page for a supported machine and backend. This is a GPU/reference exercise, not a command tested by this repository's CPU CI. The project's own environment is separate from Isaac Lab's.

Clone the release with submodules:

```bash
git clone --branch v3.0.0 --recurse-submodules https://github.com/isaac-sim/IsaacLab.git
cd IsaacLab
```

With `uv` installed according to its official instructions, inspect help and tasks:

```bash
uv run isaaclab train --help
uv run isaaclab list_envs
```

The reviewed quickstart uses a small Cartpole task:

```bash
uv run isaaclab train --rl_library rsl_rl --task Isaac-Cartpole \
  --num_envs 16 physics=newton_mjwarp
```

This selects the Newton MJWarp backend, not Isaac Sim's rendering stack. Consult its requirements. Isaac Lab 3 does not require every workflow to start the full Isaac Sim application. Keep simulator, physics, renderer, and task compatibility explicit.

After a checkpoint exists under `logs/`, evaluate a recorded checkpoint:

```bash
uv run isaaclab play --rl_library rsl_rl --task Isaac-Cartpole \
  --checkpoint /ABSOLUTE/PATH/TO/model.pt --num_envs 16 physics=newton_mjwarp
```

Replace the checkpoint path with a real output. Use the same observation/action configuration and physics/backend settings. Add the visualization option from the matching quickstart if supported by your host.

## Read a training run correctly

An iteration can contain many environment steps and optimizer updates. Equal iteration counts need not mean equal experience or compute when environment count, rollout length, or task changes. Record those settings, elapsed time, seed, reward, and operational outcomes. A moving agent in playback proves that a checkpoint executes; it does not establish reliable skill.

Start with [the robot-learning guide](../pages/robot-learning.md) if the distinction between reinforcement learning, demonstrations, and VLA adaptation is unclear. Use the [cloud lab](../pages/cloud-lab.md) if your training host is remote. These are optional extensions to today's small task.

## Today's practice

Save the task configuration, seed, package commit, backend, checkpoint path, reward curve, and evaluation results. Repeat with a different seed or initial condition. Explain which results generalize and which only describe that run.

If compute is unavailable, inspect the environment definition and complete the reward-design exercise from day 15. Mark training and playback unexecuted.

## Checkpoint

<details><summary>Can a checkpoint be replayed with arbitrary observation and action settings?</summary><p>No. Those settings define the policy interface and often its architecture. Changing them can cause shape errors or invalid behavior even if the weights load.</p></details>

## Go deeper

- [Isaac Lab 3.0 quickstart](https://isaac-sim.github.io/IsaacLab/v3.0.0/source/isaaclab/quickstart.html).
- [Isaac Lab 3.0 training configuration](https://isaac-sim.github.io/IsaacLab/v3.0.0/source/how-to/configuring_rl_training.html).
- [Backends and presets](https://isaac-sim.github.io/IsaacLab/v3.0.0/source/concepts/backends_and_presets.html).
