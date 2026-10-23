## Plans need correction

An open-loop command says what to do without correcting from the observed result. Feedback control repeatedly compares a reference with a measurement or state estimate and adjusts the input.

A proportional controller reacts to current error. An integral term accumulates error over time. A derivative term responds to how error changes. PID is a family of useful controllers, not a guarantee of stability for every plant or tuning.

LQR provides a model-based way to trade state error against control effort for a linear system with a quadratic cost. MPC repeatedly solves a finite-horizon optimization problem and applies its first control action before replanning. Constraints and computational deadlines matter.

## Try the loop

This browser lab models a one-dimensional point mass with damping, limited acceleration, a proportional position term, and a velocity-damping term. It is deliberately simpler than a robot controller. Increase the gain, then add measurement delay. Watch overshoot and recovery after a disturbance.

<div class="lab-panel" data-control-lab>
<div class="lab-controls"><label>Position gain: <output data-gain-label>2.0</output><input type="range" name="gain" min="0.5" max="8" step="0.5" value="2" aria-label="Position gain"></label><label>Measurement delay: <output data-delay-label>0 ms</output><input type="range" name="delay" min="0" max="12" step="1" value="0" aria-label="Measurement delay"></label></div>
<svg viewBox="0 0 600 300" role="img" aria-label="Simulated position response over eight seconds, with an adaptive vertical scale and a target at one meter"><rect x="40" y="20" width="515" height="230" fill="#f5f7fa"/><path data-target-line d="M40 95H555" stroke="#77916c" stroke-dasharray="5 5"/><path d="M40 25V250H555" fill="none" stroke="#a1aab5"/><rect x="248" y="20" width="32" height="230" fill="#ebbc8b" opacity=".22"/><polyline data-response fill="none" stroke="#244bdd" stroke-width="2.5"/><text x="44" y="283" font-size="11" fill="#626974">0 s</text><text x="526" y="283" font-size="11" fill="#626974">8 s</text><text data-target-label x="440" y="85" font-size="11" fill="#52694b">target: 1 m</text></svg>
<p class="lab-metrics" data-metrics aria-live="polite"></p>
</div>

The vertical scale adapts to show the full response. Compare the numerical overshoot as well as the curve. The disturbance applies during 3.25–3.75 seconds. The acceleration command is clipped to a fixed range. The velocity feedback remains current while the position measurement is delayed. These assumptions explain the graph; it is not a benchmark of PID, MPC, or Isaac.

## Today's practice

Run `python3 examples/control.py --gain 2 --delay-steps 0`, then repeat with a higher gain and delayed feedback. The included Python model matches the browser equations.

Record final error, peak overshoot, and the parameters. Look at the full response: a small final error can hide large intermediate deviations. Explain why saturation means a larger gain cannot produce unlimited acceleration.

## Checkpoint

<details><summary>Why can a correct feedback algorithm fail with delayed measurements?</summary><p>Its input describes an earlier state. A correction can arrive after the physical system has changed, producing oscillation or poor tracking. Stability depends on the complete plant, controller, timing, and constraints.</p></details>

## Go deeper

- [PORA: Closed-Loop Control and Trajectory Tracking](https://porabook.com/book/closed-loop-control/).
- [Lecture catalog](https://porabook.com/lectures/): AA174A trajectory tracking; AA203 introduction to MPC.
