## A model is one component of a deployment

Deployment includes sensors, preprocessing, inference, action conversion, controllers, networking, power, thermals, logging, and recovery. A policy that performs well in a simulator can fail when any of those assumptions change.

Jetson is an edge-compute family. JetPack supplies a hardware-specific software stack. TensorRT can optimize inference for supported models and targets. Triton supports inference-serving workflows. Isaac ROS packages integrate accelerated robot capabilities. Match each tool to the actual bottleneck.

Jetson hardware generations do not share every software combination. Check the selected module, supported JetPack release, ROS distro, CUDA/TensorRT versions, and the specific Isaac ROS package. Do not assume the latest JetPack supports every older device.

## Measure the full path

For one sensor sample, identify:

```text
capture → transfer → preprocessing → inference → action conversion
        → controller acceptance → measured physical response
```

Report source-to-decision age and end-to-end timing as well as model execution time. Inspect latency distributions and long tails under load. CPU/GPU transfers, thermal throttling, and memory pressure can dominate the result.

Batching may improve throughput while increasing delay. A server-style optimization is not automatically suitable for a feedback loop. Evaluate it against the system's actual requirements.

## Before physical trials

### Close the sim-to-real loop

Record mismatches in appearance, camera calibration, contact/friction, actuator response, and observation delay. Change one variable at a time before testing realistic combinations. A digital scene becomes useful for transfer when its relevant behavior is checked against the intended system.

Use the [evaluation test matrix](../pages/evaluation.md#a-small-sim-to-real-test-matrix) to plan those comparisons. Bring measured failures back into the next dataset or simulator revision, then reevaluate a frozen candidate before deployment. Logging and observability support this loop; they do not replace the local controller.

Work with the manufacturer or responsible integrator on one bounded, supervised workflow. Establish robot model and firmware, supported command semantics, local safety ownership, recovery behavior, operating limits, and test conditions. A software stop request is not a safety-rated emergency stop.

The guide teaches concepts and simulation exercises; it does not certify a deployment or provide a complete safety-engineering process.

## Today's practice

Write a deployment budget with a measured or explicitly unknown value for each stage. On a GPU host, profile a supported inference example using its documented tools. Save model revision, precision, input shape, hardware, warm-up method, and latency distribution.

On the laptop route, annotate the mission trace with where each timing measurement would need to originate. Mark unmeasured values unknown instead of inventing performance numbers.

## Checkpoint

<details><summary>Does a 5 ms inference benchmark establish a 5 ms robot response?</summary><p>No. It measures only the benchmarked portion of the path. Sensor age, data movement, scheduling, conversion, control, and physical dynamics add their own behavior and delay.</p></details>

## Go deeper

- [Jetson developer resources](https://developer.nvidia.com/embedded-computing).
- [Isaac ROS getting started](https://nvidia-isaac-ros.github.io/getting_started/index.html).
- [TensorRT documentation](https://docs.nvidia.com/deeplearning/tensorrt/latest/).
- [Triton inference server](https://github.com/triton-inference-server/server).
