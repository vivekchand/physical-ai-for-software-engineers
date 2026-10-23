## Pick a route before installing anything

The core reading and included Python labs run without a GPU. The ROS exercises need a supported ROS environment. Isaac Sim and GPU-training exercises require additional hardware and matching software. Completing a reading alternative does not mean you have completed the corresponding integration.

| Your machine | Start here | Add later |
|---|---|---|
| Mac, including Apple Silicon | Browser guide and Python labs | Supported remote Ubuntu + compatible NVIDIA GPU host |
| Linux laptop without NVIDIA GPU | Python labs; ROS 2 on a supported distro | Compatible GPU workstation or remote host |
| Windows laptop | Python labs; supported ROS options | Follow Isaac's Windows-specific workflow or use a remote Linux host |
| Compatible NVIDIA workstation | Core + ROS + Isaac workflows | More demanding scenes, training, and deployment targets |

## The laptop track

Install Git and Python 3.10 or newer. Clone the guide:

```bash
git clone https://github.com/vivekchand/physical-ai-for-software-engineers.git
cd physical-ai-for-software-engineers
python3 examples/control.py
python3 examples/estimate.py
python3 examples/mission.py --scenario delayed
python3 examples/pick_place.py --scenario normal
```

On Windows, use `py -3` in place of `python3` if that is your Python launcher. These examples use only the Python standard library. They write to stdout unless you explicitly request an output file.

The course website itself is static. You do not need to install the website generator to run the labs or read the Markdown lessons on GitHub. Start with the [pick-and-place task](manipulation.md). When you want physical equipment, the [hardware guide](hardware.md) compares dated package prices and one-arm versus bimanual setups. The [model guide](models.md) introduces Dream Labs and other VLA/WAM routes.

## The GPU track

**Documentation snapshot: 23 October 2026.** This is a reviewed starting point, not a guarantee every combination works. Check each product's current requirements before buying hardware or reserving compute.

| Layer | Reviewed baseline | What to record |
|---|---|---|
| OS and ROS | Ubuntu 24.04 + ROS 2 Jazzy recommended by Isaac bridge docs | OS release, ROS distro, middleware |
| Isaac Sim | 6.2 GA announced 22 Oct 2026 | Exact available artifact, release, driver, GPU |
| Isaac Lab | v3.0.0 release verified on GitHub | Commit, backend, task, observation/action presets |
| Isaac ROS | release-5.0 documentation | Its explicit compatibility matrix and package versions |
| GR00T | N1.7 described by the reviewed repository | Model revision, embodiment config, platform-specific requirements |

Use the [cross-product matrix](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/compatibility.html), plus the selected Isaac ROS release's compatibility guidance. Do not infer a supported pairing solely from matching “latest” labels.

The reviewed Isaac Sim x86 requirements list 32 GB RAM, an RTX 4080/16 GB VRAM minimum class, and supported Linux/Windows configurations. Larger workloads need more. Isaac Sim excludes GPUs without RT cores, including A100/H100. Training/model workloads have their own rules. Run the [compatibility checker](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html) on the intended simulator host.

## Keep a small environment manifest

```text
run_id:
review_date:
host_os:
gpu_model_and_vram:
driver:
ros_distro_and_rmw:
isaac_sim_version:
isaac_ros_version:
isaac_lab_commit:
physics_and_renderer:
task_and_asset_versions:
seed:
executed_steps:
unexecuted_steps_and_reasons:
```

Never put tokens, passwords, or cloud credentials in the manifest. Cloud instances accrue costs while running; use the provider's usage controls and shut down resources you no longer need.

## Verification scope

This repository checks its static site and portable lab behavior in CI. ROS/Isaac/Jetson instructions are source-reviewed reference workflows. GPU training, native ROS transport behavior, hardware compatibility, and physical safety are not established by that CI.

The project does not install NVIDIA software, accept vendor licenses, purchase compute, or connect to a real robot on your behalf.
