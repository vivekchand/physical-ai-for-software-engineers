## Establish a versioned environment

**Documentation reviewed on 23 October 2026:** NVIDIA announced Isaac Sim 6.2 GA on 22 October. Some download pages may still show 6.1. Use the release notes and matching available installation artifact together. The guide does not silently equate a moving `latest` URL with an installed version.

The reviewed ROS bridge documentation recommends Ubuntu 24.04 with ROS 2 Jazzy. Isaac Sim supports particular Linux/Windows configurations and compatible GPUs. Native macOS is not listed as a supported simulator host. A Mac streaming client is a viewer for a remote machine, not the simulator itself.

## Check hardware before downloading

Run `nvidia-smi` on the proposed GPU host. Record GPU model, VRAM, driver, OS, and free storage. Compare them with the current requirements and compatibility checker. The reviewed requirements list 32 GB minimum system RAM and note that GPUs without RT cores, including A100 and H100, are unsupported for Isaac Sim. “A cloud GPU” is not a sufficient specification.

Training workloads and scene complexity can require substantially more resources. Verify the separate requirements for Isaac Lab, GR00T, and any selected backend. Their GPU requirements are not identical.

## First successful run

Using a Mac or a laptop without a suitable GPU? Follow the [cloud Isaac lab](../pages/cloud-lab.md) for a Brev-oriented session plan, host checks, streaming diagnostics, and resource shutdown. It also includes a cube-and-floor physics check before adding the arm. The operating system and GPU requirements apply to the remote host.

Follow the workstation or Linux container procedure linked below for your selected release. Accept applicable vendor licenses yourself. Keep the simulator's Python environment separate from the course site's Python environment.

On a supported Linux workstation installation, launch from its extracted installation directory:

```bash
./isaac-sim.sh
```

Then use the release's Basic Robot tutorial, followed by the [Franka pick-and-place example](https://docs.isaacsim.omniverse.nvidia.com/latest/examples/manipulation_franka_pick_place.html):

1. Open the tutorial's supported robot scene.
2. Start simulation and confirm the scene advances.
3. Pause, reset, and run again.
4. Inspect the startup log for missing assets, extension failures, and GPU errors.

Save the exact version, launch method, scene identifier, and a screenshot showing a running scene. A loaded viewport alone does not demonstrate advancing physics.

## Practice

Produce `environment.md` with a successful launch record or an explicit blocker. On the laptop route, complete the portable motion/control lab and write down what that model cannot validate. Mark the GPU step pending rather than counting it as executed.

**Verification boundary:** this guide's included CPU labs are tested in CI. The NVIDIA workflows are source-reviewed reference exercises; this project does not claim to have run them on your GPU or validated physical hardware.

## Checkpoint

<details><summary>Can an H100 machine that runs model training necessarily run Isaac Sim?</summary><p>No. Workloads have different hardware requirements. Isaac Sim's reviewed requirements exclude GPUs without RT cores. Check the exact product and backend before selecting compute.</p></details>

## Go deeper

- [Isaac Sim 6.2 GA announcement](https://forums.developer.nvidia.com/t/isaac-sim-6-2-general-availability/386512).
- [Requirements](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html), [downloads](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/download.html), and [workstation installation](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/install_workstation.html).
- [Isaac Sim tutorials](https://docs.isaacsim.omniverse.nvidia.com/latest/index.html).
