## Run three small experiments anywhere

Clone the repository first using the Setup page. These examples require Python 3.10+ and no third-party packages. They are simplified educational models and synthetic events, not hardware drivers.

## Lab 1: feedback, delay, and saturation

```bash
python3 examples/control.py --gain 2 --delay-steps 0
python3 examples/control.py --gain 6 --delay-steps 8
```

The model integrates a damped point mass over eight seconds. A fixed disturbance occurs partway through the run. Position feedback can be delayed, velocity feedback is current, and commands are clipped to a bounded range. Output is JSON containing parameters, final error, overshoot, and samples.

Predict how increasing gain changes the response, then compare your prediction with the data. Use day 6's browser experiment to visualize the same equations. Do not generalize these gains to an actual robot.

## Lab 2: noisy measurements and a scalar belief

```bash
python3 examples/estimate.py --seed 7
python3 examples/estimate.py --seed 7 --measurement-variance 4
```

The script generates seeded noisy measurements of a fixed position. It uses a scalar predict/correct filter with configurable modeled noise. Output contains measurements, estimates, variance, and the synthetic reference position.

Explain which values are known to the simulator and which are available to the estimator. Check whether reported confidence is sensible across repeated trials. The model deliberately omits nonlinear robot geometry and real sensor data.

## Lab 3: reconstruct a mission honestly

```bash
python3 examples/mission.py --scenario normal
python3 examples/mission.py --scenario delayed
python3 examples/mission.py --scenario disconnected
python3 examples/mission.py --scenario rejected
python3 examples/mission.py --scenario duplicate
```

Every event is marked `synthetic: true`. Files use a named simulation clock and unique run identity. These are deterministic fixtures for learning evidence handling; they do not claim to emulate a manufacturer's robot controller.

Write an analyzer that answers: was the goal accepted? Was cancellation requested, accepted, or rejected? What was the last reported task state? What do the latest motion measurements support? Is a result unknown?

Preserve raw duplicated events while deduplicating request counts by identifier. Do not invent missing motion state after a disconnect.

## Optional: observe actual ROS odometry

After completing ROS and simulator setup, discover an odometry topic of type `nav_msgs/msg/Odometry`:

```bash
source /opt/ros/jazzy/setup.bash
python3 examples/ros2_observer.py --topic /odom
```

This optional observer emits JSONL and sends no robot commands. Source frames/timestamps and receipt timestamps remain separate. Its subscription uses sensor-data QoS; inspect compatibility with your actual publisher. It does not validate the robot's estimate against physical truth.

The CPU tests do not execute this ROS adapter or GPU workflows. Follow days 9–14 for integration evidence.

## Keep your results

Use a new run folder for each configuration. Save the exact command, tool versions, raw output, and a paragraph stating what the result proves. Include what it does not tell you when the distinction matters.
