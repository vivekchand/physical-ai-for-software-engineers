## Start with a small state

Model the delivery robot with position, heading, and velocity. A state collects the quantities needed by your model to predict future behavior given inputs. A richer model might include wheel speeds, actuator lag, or battery-dependent limits.

Kinematics describes how motion is geometrically possible. Dynamics describes how forces, torques, and inertia produce motion. A geometric route may be impossible to execute at the requested speed.

## The unicycle model

A useful planar approximation has forward velocity `v` and turn rate `omega`:

```python
from math import cos, sin

def step(x, y, theta, v, omega, dt):
    return (x + v * cos(theta) * dt,
            y + v * sin(theta) * dt,
            theta + omega * dt)
```

This is an Euler integration step. It approximates continuous motion over a small time interval. It does not model wheel slip, collision, actuator saturation, or full rigid-body dynamics. Reducing `dt` can improve integration accuracy for this model; it cannot fix a wrong physical model.

A differential-drive robot cannot instantly slide sideways while preserving its heading. That constraint affects planning. Similarly, a robot carrying a heavy load may have a different braking response from an unloaded one.

## Learn to ask about assumptions

For every simulator, ask which dynamics are modeled, which parameters were identified, which contacts are approximated, and whether the timestep changes results. A convincing animation alone answers none of these questions.

For a simple constant-deceleration model, braking distance is `v² / (2a)`, with speed `v` and deceleration magnitude `a`. A reaction delay adds approximately `v × delay`. Real stopping behavior also depends on friction, controllers, loads, and other conditions. Use the formula for intuition, not a certified stopping-distance claim.

## Today's practice

Put the `step` function in a small script. Simulate five seconds of straight motion, then turning. Compare results for timesteps of 0.1 and 0.01 seconds. Save the trajectory as rows of time, x, y, and heading.

Write down three physical effects the model cannot reproduce. Those limitations should accompany every graph you publish from it.

## Checkpoint

<details><summary>Does a more detailed rendering make the motion model more accurate?</summary><p>No. Appearance, sensor realism, dynamics, and contact fidelity are different properties. Validate the properties relevant to the experiment.</p></details>

## Go deeper

- [PORA: Modeling Robot Dynamics](https://porabook.com/book/modeling-robot-dynamics/).
- [PORA notebooks](https://porabook.com/exercises/): nonholonomic wheeled robot dynamics and numerical integration.
