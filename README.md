# Physical AI for Software Engineers

**Your code. The real world.**

An original, open 21-day field guide for software engineers entering robotics and
physical AI. Connect theory from primary references such as PORA to practical
ROS 2 and NVIDIA Isaac workflows, small runnable labs, and a reproducible capstone.

**[Read the guide](https://vivekchand.github.io/physical-ai-for-software-engineers/)** ·
**[Choose your setup](https://vivekchand.github.io/physical-ai-for-software-engineers/setup/)** ·
**[NVIDIA map](https://vivekchand.github.io/physical-ai-for-software-engineers/nvidia/)** ·
**[Reading edition](https://vivekchand.github.io/physical-ai-for-software-engineers/book/)**

## What you can finish with

- A working mental model of perception, estimation, planning, control, and learning.
- Three portable experiments covering feedback, noisy measurements, and mission evidence.
- Source-reviewed ROS 2, Isaac Sim, and Isaac Lab reference exercises.
- An environment manifest, failure investigations, and a reproducible project report.
- Original Markdown chapters that can evolve into a longer book.

Plan 60–120 minutes most days, with a longer final project. This is a starting path;
expertise grows through implementation, evaluation, and supervised hardware work.
You can read the core and run the included toy labs without an NVIDIA GPU.
The complete GPU route requires compatible hardware and additional setup time.

## The 21-day path

### Week 1: understand the robot

| Day | Lesson |
|---|---|
| 01 | [Your code meets the real world](content/lessons/01-a-new-mental-model.md) |
| 02 | [Read the autonomy stack](content/lessons/02-map-the-autonomy-stack.md) |
| 03 | [Frames, time, and units](content/lessons/03-frames-time-and-units.md) |
| 04 | [Model a moving robot](content/lessons/04-motion-and-dynamics.md) |
| 05 | [Find a path. Make it feasible.](content/lessons/05-planning-and-trajectories.md) |
| 06 | [Close the feedback loop](content/lessons/06-feedback-control.md) |
| 07 | [See through a robot's sensors](content/lessons/07-perception.md) |

### Week 2: build the system

| Day | Lesson |
|---|---|
| 08 | [Estimate what you cannot measure](content/lessons/08-state-estimation.md) |
| 09 | [Speak ROS 2](content/lessons/09-ros2-first-nodes.md) |
| 10 | [Make the messages mean something](content/lessons/10-ros2-reliability.md) |
| 11 | [Find your way around NVIDIA](content/lessons/11-nvidia-map.md) |
| 12 | [Get Isaac Sim running](content/lessons/12-isaac-sim-setup.md) |
| 13 | [Bridge the simulated robot to ROS 2](content/lessons/13-isaac-sim-ros2.md) |
| 14 | [Navigate, localize, and reconstruct](content/lessons/14-navigation-and-mapping.md) |

### Week 3: learn, deploy, observe

| Day | Lesson |
|---|---|
| 15 | [Choose actions over time](content/lessons/15-decisions-and-rewards.md) |
| 16 | [Train and inspect an Isaac Lab policy](content/lessons/16-isaac-lab.md) |
| 17 | [Learn from demonstrations](content/lessons/17-imitation-and-groot.md) |
| 18 | [Build better data and test worlds](content/lessons/18-synthetic-data-and-cosmos.md) |
| 19 | [Bring a policy toward deployment](content/lessons/19-deployment-and-jetson.md) |
| 20 | [Make behavior inspectable](content/lessons/20-observability-and-intervention.md) |
| 21 | [Build it. Break it. Explain it.](content/lessons/21-capstone.md) |

## Run the portable labs

Python 3.10+; no third-party packages:

```bash
git clone https://github.com/vivekchand/physical-ai-for-software-engineers.git
cd physical-ai-for-software-engineers
python3 examples/control.py --gain 2 --delay-steps 0
python3 examples/estimate.py --seed 7
python3 examples/mission.py --scenario delayed
python3 -m unittest discover -s tests -v
```

On Windows, use `py -3` if that is your launcher. The optional
`examples/ros2_observer.py` needs a separately installed/sourced ROS 2 environment.
It subscribes to odometry and does not send movement commands.

## NVIDIA and ROS version policy

Documentation reviewed **23 October 2026**: Isaac Sim 6.2 GA announcement,
Isaac Lab v3.0.0, Isaac ROS release-5.0 docs, GR00T N1.7, and the recommended
Ubuntu 24.04/ROS 2 Jazzy bridge route. These are dated references, not a claim
that every product combination has been executed or is mutually compatible.
Use the vendor's explicit compatibility matrices and pin the actual artifacts.

See [Setup](content/pages/setup.md), [NVIDIA map](content/pages/nvidia.md), and
[verification scope](VERIFICATION.md). GPU, ROS transport, Jetson, and physical
hardware workflows are not validated by the portable CPU CI tests.

## Website development

The site is generated from Markdown with one small Python dependency. No Node
package installation, frontend framework, backend, or external runtime JavaScript.
Node is used only for the optional/CI JavaScript syntax check.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/build.py
python scripts/check_site.py
python -m http.server 8000 --directory dist
```

Open `http://localhost:8000`. To mirror GitHub Pages' project path:

```bash
python scripts/build.py --base-path /physical-ai-for-software-engineers
python scripts/check_site.py --base-path /physical-ai-for-software-engineers
```

GitHub Actions validates the project and deploys `dist/` to GitHub Pages on main.
The repository's Pages source must be **GitHub Actions**. When forking, update
the repository/site URLs and workflow base path. The generator also creates a
printable reading edition and downloadable `book.md` manuscript.

Progress uses local browser storage. Search uses a generated local index.
There are no accounts or analytics scripts. GitHub's hosting infrastructure may
process ordinary access logs under its own policies.

## Sources, independence, and ClawMetry

[Principles of Robot Autonomy](https://porabook.com/) is by Daniele Gammelli,
Joseph Lorenzetti, Katie Luo, Gioele Zardini, and Marco Pavone. We link to the
original book, notebooks, and lectures; we do not reproduce its text or figures.
This project is independent of PORA, Stanford, NVIDIA, and ROS.

Vivek Chand started the guide while exploring physical AI for
[ClawMetry](https://clawmetry.com/physical-ai). ClawMetry appears in relevant
observability discussions, with proposed robot integrations clearly identified.
No product integration is required to use the course. Initial drafting and site
implementation used AI assistance; technical corrections are welcome.

## License and contributions

- **Original text:** [CC BY 4.0](LICENSE-CONTENT).
- **Original site code, SVGs, scripts, examples:** [MIT](LICENSE).
- **External work:** its respective owners' licenses.

For attribution, use “Physical AI for Software Engineers, Vivek Chand and
contributors,” link to this repository and the license, and note adaptations.

Read [CONTRIBUTING.md](CONTRIBUTING.md) to improve a lesson, report a technical
correction, or share a reproduced workflow.
