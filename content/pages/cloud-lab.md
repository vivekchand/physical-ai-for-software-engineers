## Use your laptop as the client

You can read, edit code, and view a remote desktop on a Mac or modest laptop while the simulator runs elsewhere:

```text
your laptop: editor + terminal + stream viewer
                         ↕
remote host: GPU + driver + simulator/training environment
```

The remote GPU host must meet the workload's requirements. A browser stream does not move simulation onto the laptop. Start with a scene or small task; postpone foundation-model fine-tuning until the basic workflow runs.

**Documentation reviewed: 23 October 2026.** This is a source-reviewed procedure. This repository's CI has not provisioned a cloud GPU or executed these NVIDIA workflows.

## Choose the workload before the instance

| Session goal | Check before reserving compute | Evidence to bring home |
|---|---|---|
| View and simulate the arm | Isaac Sim GPU, RT cores, driver, OS, RAM, storage, streaming support | Scene, advancing simulation state, logs |
| Train a small Isaac Lab task | Exact Lab release, backend, task and renderer requirements | Configuration, checkpoint, evaluation |
| Run a VLA on supplied data | Model VRAM, framework versions, checkpoint and input contract | Predicted actions with model/data revisions |

Isaac Sim's reviewed requirements include supported Ubuntu and Windows 11 workstation configurations; its container is Linux-only. Native macOS is not listed as a simulator host. GPUs without RT cores, such as A100/H100, are excluded for Isaac Sim even though other model-training workloads may support them. Check the [requirements](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html) and [cross-product matrix](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/compatibility.html).

## A Brev session, step by step

1. **Prepare locally.** Choose lesson 12's scene or lesson 16's small task. Write the exact release/backend and the question the session should answer. Downloading assets and first startup can consume much of a short session.
2. **Inspect the launch configuration.** Follow the official [Isaac Sim Brev deployment guide](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/install_advanced_cloud_setup_brev.html) or [Isaac Lab cloud guide](https://isaac-sim.github.io/IsaacLab/v3.0.0/source/features/cloud_deployment.html). Record the image tag/digest, source revision, selected hardware, disk, and viewer method. An older launchable can be a valid older environment; use its matching docs.
3. **Set a session budget.** Read the provider's current quote and storage terms. Record the latest time you intend to stop. Provision the instance yourself after checking the configuration and applicable terms.
4. **Connect with the documented client.** Use the deployment's provided terminal/desktop/streaming instructions. A viewer hostname or port from one tutorial is not universal. Keep the viewer and development services accessible through the supported authenticated connection.
5. **Verify inside the host.** Record the GPU/driver, OS, and available workspace storage. Compare them with your manifest before troubleshooting Python.
6. **Run one small experiment.** Complete the simulation check below or the version-matched training example. Save logs when it fails; increasing instance size will not repair an incompatible API.
7. **Export and close.** Copy your scene, configuration, logs, checkpoint, and report to storage you control. Stop the intended instance and verify its state in the provider console. Check separately for retained storage and other billable resources.

[Brev Launchables](https://docs.nvidia.com/brev/concepts/launchables) package hardware/software/code configuration. A launchable helps reproduce setup; it is not evidence that the selected scene or policy works.

On an Ubuntu host, these inspection commands are read-only:

```bash
nvidia-smi
cat /etc/os-release
df -h .
```

With the Brev CLI already installed and authenticated, inspect instances and stop the one you used:

```bash
brev list
brev stop YOUR_INSTANCE_NAME
```

Replace the placeholder after inspecting the list. Follow [Brev's lifecycle documentation](https://docs.nvidia.com/brev/cli/instance-management) for workspace persistence. Stopping, deleting, closing a browser, and ending a training process are different actions. Export needed files before deleting resources.

## First simulation check: a cube and a floor

Before adding a robot, use the installed release's scene/physics tutorials to make a ground collider and a small rigid cube above it. Record scene units, gravity, cube mass, initial pose, and time step. Then:

1. Start physics and confirm the cube's measured height changes with simulation time.
2. Confirm it contacts the floor, settles, and resets to the recorded initial pose.
3. Remove the floor collider in a separate scene copy. Predict the result, then observe it.
4. Restore the baseline. Save the scene and a short state/log record.

A visible mesh is not automatically a collider or a dynamic rigid body. A rendering of a warehouse establishes appearance; this experiment checks a small part of the configured physics. The next step is the supported Franka workflow on lesson 14, followed by the [evaluation guide](evaluation.md).

## When the screen stays blank

| Symptom | Investigate first |
|---|---|
| Desktop works; simulator does not start | GPU/driver support, application logs, selected artifact |
| Simulator runs; stream is blank | Documented streaming client, connection path, renderer |
| Scene loads; nothing falls | Play/pause state, rigid-body settings, gravity, simulated time |
| Missing robots or materials | Asset paths, cache, download completion, outbound asset access |
| Training stops out of memory | Task size, cameras, environment count, backend requirements |

## Your session artifact

Save `cloud-session.md`: goal, provider/configuration, environment versions, start/stop times, estimated and actual charges, execution evidence, exported files, and any remaining resources. A local alternative is to prepare this plan and run the portable labs. Label remote execution as pending until it happens.
