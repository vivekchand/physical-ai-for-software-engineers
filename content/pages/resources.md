## How to use the references

Read the lesson, attempt its exercise, then consult the primary source for a concept you cannot explain. Source code and installed-version documentation take precedence over a remembered command or an AI-generated explanation.

## PORA: the theoretical spine

[Principles of Robot Autonomy](https://porabook.com/) is by Daniele Gammelli, Joseph Lorenzetti, Katie Luo, Gioele Zardini, and Marco Pavone. The official site provides the book, exercises, and lecture recordings. This project is an independent learning companion; it does not reproduce the book, its figures, or its videos and is not affiliated with its authors or institutions.

| Guide days | PORA material | Focus |
|---|---|---|
| 1–2 | Preface and Software | Integrated autonomy and software components |
| 3–4 | Chapter 1; geometric foundations in chapter 6 | State, motion, coordinates, calibration |
| 5 | Chapters 2 and 4 | Optimization, paths, trajectories, search |
| 6 | Chapter 3 | Feedback, tracking, PID, LQR, MPC |
| 7 | Chapters 5–10 | Sensors, cameras, stereo, classical/learned perception, detection |
| 8 and 14 | Chapters 11–15 | Filtering, localization, SLAM, fusion, tracking |
| 15–16 | Chapters 16–18 | Task modes, sequential decisions, dynamic programming, RL |
| 17–18 | Chapter 19 and Prospects | Imitation, foundation models, emerging directions |

- [Full contents](https://porabook.com/book/).
- [Interactive exercises](https://porabook.com/exercises/).
- [Official exercise repository](https://github.com/StanfordASL/pora-exercises).
- [Lecture catalog](https://porabook.com/lectures/).

### A focused video route

From AA174A, prioritize lectures 1 (kinematics), 3 (tracking), 7 (sensors), and 12–14 (localization/filtering). From AA203, consult 11 (MPC) and 14–15 (learning and imitation). Follow the official catalog for current titles and links. Watch the part that resolves a question, then return to the experiment.

## ROS 2 and navigation

- [Jazzy installation](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html).
- [ROS 2 actions](https://design.ros2.org/articles/actions.html).
- [QoS design](https://design.ros2.org/articles/qos.html), with installed-version docs for exact behavior.
- [REP 103](https://github.com/ros-infrastructure/rep/blob/master/rep-0103.rst) and [REP 105](https://github.com/ros-infrastructure/rep/blob/master/rep-0105.rst).
- [rosbag2](https://github.com/ros2/rosbag2) and [Nav2](https://docs.nav2.org/).

## NVIDIA primary sources

- [Isaac Sim documentation](https://docs.isaacsim.omniverse.nvidia.com/latest/index.html), [requirements](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html), and [cross-product compatibility](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/compatibility.html).
- [Isaac Lab versioned docs](https://isaac-sim.github.io/IsaacLab/v3.0.0/source/isaaclab/quickstart.html).
- [Isaac ROS docs](https://nvidia-isaac-ros.github.io/).
- [Isaac GR00T](https://github.com/NVIDIA/Isaac-GR00T).
- [Cosmos projects](https://github.com/nvidia-cosmos), [Newton](https://github.com/newton-physics/newton), and [Warp](https://github.com/NVIDIA/warp).

## Manipulation, model research, and hardware

- [Franka pick-and-place reference](https://docs.isaacsim.omniverse.nvidia.com/latest/examples/manipulation_franka_pick_place.html) and [NVIDIA manipulator workflow](https://docs.isaacsim.omniverse.nvidia.com/latest/robot_setup_tutorials/tutorial_manipulator_workflow.html).
- [Dream Labs Dream-1](https://dreamlabs.ai/research/dream-1/) and [DreamZero](https://dreamzero0.github.io/).
- [LeRobot](https://huggingface.co/docs/lerobot), including [SmolVLA](https://huggingface.co/docs/lerobot/smolvla) and the [ACT imitation baseline](https://huggingface.co/docs/lerobot/act).
- [openpi](https://github.com/Physical-Intelligence/openpi), [π0.7 research](https://www.pi.website/blog/pi07), and the [Pi API announcement](https://www.pi.website/blog/api-beta).
- [Gemini Robotics](https://deepmind.google/models/gemini-robotics/), with its distinct action and reasoning variants.

- [OpenVLA](https://openvla.github.io/).
- [Physical Intelligence: pi-zero](https://www.pi.website/blog/pi0).

The [model field note](models.md) explains access and compatibility distinctions. The [hardware guide](hardware.md) links to the supplier pages behind each dated price; those are listings rather than independent hardware evaluations.

## Additional course perspective

[Intro to Physical AI and Next Generation Robotics, DuraThink eLearning on Udemy](https://www.udemy.com/course/intro-to-physical-ai-and-next-generation-robotics/) provided an additional perspective during the 23 October 2026 refinement. The 15 accessible lecture transcripts were reviewed for topic coverage: foundations, architecture, NVIDIA tools, learning, cloud demos, and applications. This guide's explanations, examples, trial fixture, and exercises are original; the paid lessons and transcripts are not redistributed.

The practical extensions are [robot learning](robot-learning.md), [cloud Isaac setup](cloud-lab.md), [evaluation and sim-to-real](evaluation.md), and [application economics](applications.md). Use the vendor's installed-version documentation for executable instructions; claims about generalization or business value need task-specific measurements.

### Primary references for these extensions

- [Brev Launchables](https://docs.nvidia.com/brev/concepts/launchables), [instance lifecycle](https://docs.nvidia.com/brev/cli/instance-management), and [Isaac Sim's Brev deployment](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/install_advanced_cloud_setup_brev.html).
- [Isaac Lab 3.0 cloud deployment](https://isaac-sim.github.io/IsaacLab/v3.0.0/source/features/cloud_deployment.html) and [imitation-learning workflows](https://isaac-sim.github.io/IsaacLab/v3.0.0/source/features/imitation-learning/index.html).
- [LeRobot imitation learning](https://huggingface.co/docs/lerobot/il_robots) and [dataset format](https://huggingface.co/docs/lerobot/lerobot-dataset-v3).
- [NVIDIA robotics architecture](https://www.nvidia.com/en-us/industries/robotics/) and [GR00T interfaces/evaluation](https://github.com/NVIDIA/Isaac-GR00T).

## ClawMetry and provenance

[ClawMetry's physical AI page](https://clawmetry.com/physical-ai) describes a proposed integration/partnership track. It informs the observation-boundary discussion on day 20; the course does not claim those robot adapters are shipped.

Vivek Chand started this guide from the perspective of a software engineer entering physical AI while building ClawMetry. Initial drafting and site implementation used AI assistance. Technical corrections and independently reproduced workflows are welcome. The primary sources remain authoritative for their own systems.

## Licensing and attribution

Original text in this repository is **CC BY 4.0**. Original site code and included examples are **MIT**. Attribution: “Physical AI for Software Engineers, Vivek Chand and contributors,” with a link to this guide, its license, and a description of your changes where applicable.

External books, videos, software, models, datasets, and assets retain their own licenses. Linking to them does not relicense them. NVIDIA, ROS, Stanford, and PORA names identify the referenced work; they do not imply endorsement.
