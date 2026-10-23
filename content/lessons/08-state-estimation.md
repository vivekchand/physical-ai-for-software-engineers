## A robot maintains a belief

The delivery robot cannot read its exact physical state from one perfect sensor. Wheel odometry drifts. Images can be ambiguous. Measurements arrive at different rates. State estimation combines a model and observations to maintain a useful belief about the state.

A basic filtering cycle has two steps:

1. **Predict:** use the previous belief and motion model to predict the next state and uncertainty.
2. **Correct:** compare the new measurement with what the model predicted and update the belief.

For a scalar Kalman-style update, the gain depends on predicted variance and measurement variance. A measurement modeled as noisy receives less weight. That reasoning is useful even before deriving the matrix equations.

## Which approximation are you using?

The Kalman filter is exact under linear-Gaussian assumptions. The extended Kalman filter linearizes nonlinear models locally. The unscented Kalman filter uses selected sample points to propagate an approximation. Particle filters maintain weighted state samples and can represent multiple distinct hypotheses.

A Gaussian-shaped belief around one pose is not a good description when the robot might be in either of two identical aisles. The representation itself affects what uncertainty the system can express.

Localization estimates pose relative to a map. SLAM estimates the robot trajectory and map together. Sensor fusion combines information across sources; tracking estimates the changing state of other objects. Correlated sensors do not provide independent evidence merely because they arrive on different topics.

## Read the uncertainty carefully

An estimator's covariance describes uncertainty under its assumptions. It can be overconfident when the model, noise, or data associations are wrong. Compare reported uncertainty with actual error on held-out trials when ground truth is available.

## Today's practice

Run `python3 examples/estimate.py`. Repeat with `--measurement-variance 4`. The script uses seeded synthetic measurements of a fixed position and a scalar filter. Inspect the estimate and variance as new observations arrive.

Then run PORA's Kalman filter notebook and change measurement noise. Describe which uncertainty grows during prediction and why a correction can reduce it. Explain why the toy script is not a complete localization system.

## Checkpoint

<details><summary>A dashboard shows low covariance. Does that prove a precise physical position?</summary><p>No. It shows the estimator's reported uncertainty under its model. Calibration errors, incorrect data association, or violated noise assumptions can make the estimate wrong and overconfident.</p></details>

## Go deeper

- [PORA: Localization and Filtering](https://porabook.com/book/localization-filtering/) and [Approximate Filters](https://porabook.com/book/approximate-filters/).
- [PORA: Robot Localization](https://porabook.com/book/robot-localization/), [SLAM](https://porabook.com/book/slam/), and [Sensor Fusion](https://porabook.com/book/sensor-fusion/).
