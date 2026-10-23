| Term | Working definition |
|---|---|
| Action | In ROS, a long-running goal interface with feedback and a result; elsewhere, a policy output or control choice. State which meaning you intend. |
| Actuator | A mechanism that converts a command into physical effect, such as motor torque. |
| Belief | A probability distribution representing uncertainty about state. |
| Calibration | Estimating the relationship between measurements and the geometry or quantities they represent. |
| Closed loop | Using observations of the result to adjust subsequent inputs. |
| Configuration space | A representation of robot configurations, such as joint angles, used for reasoning about motion and collision. |
| Control policy | A rule for choosing an input from state, observations, time, or history. |
| Covariance | A representation of variance and correlated uncertainty under a statistical model. |
| Digital twin | A digital representation tied to a specific real system; usefulness depends on what is modeled and validated. |
| Domain randomization | Varying environment or system parameters to broaden training/evaluation conditions. |
| Dynamics | How forces, torques, inertia, and other physical effects determine motion over time. |
| Embodiment | The robot's physical form and relevant sensing/action capabilities. |
| End effector | The part of a manipulator that interacts with an object, such as a gripper. |
| Episode | One bounded run of a learning environment or task. |
| Frame | A coordinate reference used to give geometric quantities meaning. |
| Ground truth | A reference treated as truth for a specific evaluation, with its own measurement limits. |
| IMU | Inertial measurement unit, commonly reporting acceleration and angular motion. |
| Inverse kinematics (IK) | Finding joint configurations for a requested endpoint pose under a chosen robot model. |
| Forward kinematics | Computing endpoint/link poses from joint configurations. |
| Leader / follower | A teaching device moved by a person and the robot following it; one pair is usually one working manipulator. |
| Bimanual | Using two working arms, often requiring coordination and inter-arm collision handling. |
| Inference | Computing outputs from a trained model. |
| Isaac Lab | NVIDIA's robot-learning environment and workflow framework. |
| Isaac ROS | NVIDIA's accelerated robot software packages and workflows integrated with ROS. |
| Isaac Sim | NVIDIA's robot/sensor simulation application and platform. |
| JetPack | NVIDIA's supported software stack for particular Jetson hardware. |
| Kinematics | Geometric relationships between robot configuration and motion. |
| Latency | Time between defined endpoints; a number is incomplete without those endpoints and a clock basis. |
| Localization | Estimating robot pose relative to a reference/map. |
| LQR | Linear quadratic regulator, a model-based optimal-control formulation for linear systems and quadratic costs. |
| MPC | Model predictive control: repeatedly optimize a future horizon and apply the next action. |
| Node | A ROS software participant; it need not have a dedicated operating-system process. |
| Odometry | Estimating motion over time from onboard measurements; commonly subject to accumulated drift. |
| Open loop | Applying inputs without correcting from observed execution results. |
| OpenUSD | A system and scene-description ecosystem for composing assets and worlds. |
| PID | Proportional, integral, and derivative feedback terms. |
| Pose | Position and orientation, relative to a frame and time. |
| QoS | Communication policies governing delivery behavior and matching requirements. |
| Reward | A numerical learning/optimization signal; it is not automatically task success. |
| ROS 2 | Middleware, tools, and conventions for robot software integration. |
| Sim-to-real gap | Differences between a simulation and physical deployment relevant to performance. |
| SLAM | Simultaneous localization and mapping: estimating trajectory and map together. |
| State | Quantities sufficient for a model to predict evolution given inputs under its assumptions. |
| Task cancellation | A software task transition/request; it does not alone establish physical stopping. |
| TF / tf2 | ROS tools and conventions for tracking coordinate transforms over time. |
| Trajectory | Motion specified with time, often including state and input references. |
| VLA | Vision-language-action model connecting multimodal inputs to a defined action representation. |
| World model | A learned predictive representation of how aspects of the world develop. |
| World-action model (WAM) | A policy architecture coupling action prediction with predictive world/video representations. |

Use the daily lessons and their primary sources for assumptions, derivations, and product-specific definitions. These brief definitions are a starting vocabulary.
