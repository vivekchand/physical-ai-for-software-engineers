## Build confidence in small stages

Before asking an arm to grasp a cube, make the simulator's contracts visible. This optional workshop sits alongside lessons 3–7 and 12–14. It keeps the arm as the running example while developing the scene, physics, and debugging skills needed to change it.

**Source review: 25 October 2026.** These are reference exercises for a compatible Isaac Sim installation. The included laptop lab checks geometry and timing arithmetic; this repository has not executed the GPU procedures or validated a physical robot.

| Stage | Build or inspect | Evidence to save |
|---|---|---|
| Host | Supported GPU, renderer, exact software artifact | Compatibility result and renderer's active-device log |
| Scene | Bench, cube, open tray, camera | Stage, units, dimensions, asset revisions |
| Contact | Falling cube and tray colliders | Pose trace, collision debug view, reset result |
| Joint | One anchored link on a driven hinge | Named joint, limits, units, command/state comparison |
| Arm | Supported Franka asset and controller | Joint names, frames, baseline task result |
| Observation | Camera and joint state at explicit rates | Frame/time contracts and separate simulation/wall intervals |
| Data | Small annotated image set | Class mapping, aligned overlays, generation configuration |

## 1. Prove which GPU the renderer uses

`nvidia-smi` establishes useful GPU/driver information. It does not establish which Vulkan device Kit selected. Likewise, an OpenGL renderer check answers a different question from the RTX rendering path.

On a configured Linux host, inspect:

```bash
nvidia-smi
free -h
df -h .
```

If the supported Vulkan diagnostic utility is already available, inspect its device summary with `vulkaninfo --summary`. Follow NVIDIA's setup instructions for the utility rather than installing unrelated graphics packages to repair a working driver.

Then inspect the running application's log. Find its GPU table and active-device indication, match the device name/identity to the intended RTX GPU, and retain the surrounding renderer errors if startup fails. Application GPU indices need not match `nvidia-smi` indices. Enumeration establishes availability; the application log establishes selection. See [Kit's Linux troubleshooting](https://docs.omniverse.nvidia.com/kit/docs/kit-manual/latest/guide/linux_troubleshooting.html).

Repeat the relevant checks inside the container when using one. A healthy host does not prove the container has matching device access and graphics libraries. Use the release's documented selection mechanism if necessary; verify the resulting log after restarting.

**Current requirements matter.** The reviewed [Isaac Sim requirements](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html) list a 16 GB minimum VRAM class and 32 GB system RAM for x86. A recorded small-scene demonstration on a smaller GPU is not a replacement for that support matrix. Isaac Lab backends have separate requirements.

## 2. Make the software artifact reproducible

Record the Isaac Sim release, installation method, GPU/driver, OS, enabled extensions, scene dependencies, and launch arguments. For a container, retain the human-readable image tag **and the resolved digest**, with architecture/platform. Tags can move; a digest identifies particular registry content. Record both an image-index digest and platform-specific image digest if your tooling exposes that distinction.

[Docker's pull documentation](https://docs.docker.com/reference/cli/docker/image/pull/) explains digest-based references. Pinning an image does not pin remotely referenced assets, host drivers, or downloaded model weights; record those separately. Do not reuse a tutorial's old digest merely because it is reproducible. Choose a supported release, then record the artifact you actually used.

A launch that ends with code 137 is consistent with a forced kill, including an out-of-memory kill. It does not establish the cause by itself. Check container state such as `State.OOMKilled`, the configured memory limit, available host RAM, and relevant system logs. [Docker inspection](https://docs.docker.com/reference/cli/docker/inspect/) exposes container metadata. Save selected diagnostic fields rather than publishing an entire configuration containing credentials.

Separate cold startup from steady operation. Shader compilation, asset retrieval, caches, scene complexity, rendering, physics, and resource limits can affect timings. Warm up, repeat the same workload, and report the configuration. Avoid treating one machine's milliseconds as universal performance.

## 3. Read the scene as a composed document

A **prim** is a named scene element at a path. An **Xform** groups or transforms elements. A **reference** composes another asset into a scene; a **payload** allows that composition to be loadable/unloadable. Layers hold authored opinions, and the current edit target determines where an edit is saved.

For our workshop, a useful organization is:

```text
/World
  /Bench
  /Tray
    /Floor
    /WallLeft
    /WallRight
    /WallFront
    /WallBack
  /Cube
  /Arm
  /Camera
```

Start without the arm. Record stage `metersPerUnit`, `upAxis`, gravity, and the measured dimensions of the cube and tray. An asset's local coordinates and world coordinates differ when its parents transform it. A centimetre-authored prop referenced into a metre stage may need an explicit corrective transform. Follow [OpenUSD's stage-unit rules](https://openusd.org/release/api/group___usd_geom_linear_units__group.html); changing metadata is not the same as rescaling geometry.

Inspect `xformOpOrder` and the evaluated local/world transforms. Its ordering follows USD's transform-stack convention, so a slogan such as “translate last” is insufficient without specifying the convention. Check existing operations before adding more, and test the world position of one known point after your edit. [OpenUSD's Xformable reference](https://openusd.org/release/api/class_usd_geom_xformable.html) defines the ordering.

Keep vendor assets separate from scene overrides. Save your edits, close the stage, reopen it, and confirm they survive. Archive or version the dependency graph as well as the root scene; copying one USD file may leave referenced geometry or textures behind.

## 4. Make the cube land inside the tray

A visible mesh, a collision shape, and a dynamic rigid body have different jobs. Give the cube a suitable rigid-body/collision configuration, and make the bench and tray appropriate static colliders. Turn on collision visualization and inspect the actual geometry used for contact.

An open tray approximated by one convex hull can acquire an invisible lid. For this simple workshop, five box colliders preserve the cavity: a floor and four walls. Keep their dimensions consistent with the visible tray. Use supported decomposition or other collision representations for more complex assets; dynamic and static bodies do not support every representation identically. Follow [Isaac Sim's physics fundamentals](https://docs.isaacsim.omniverse.nvidia.com/latest/physics/simulation_fundamentals.html).

Drop the cube above the empty tray. Observe initial height, contact, settling, and reset. In a separate variant, replace the tray's collision geometry with a convex hull and predict the change. Save the debug view and measured final pose. Restore the baseline before adding a controller.

Visual roughness describes light response. Contact friction and restitution belong to the physics configuration. A metallic-looking tray has not thereby acquired a particular friction coefficient. Inspect the effective material bindings and contact settings on both contacting shapes. Change one physical parameter and measure its effect before concluding it was applied.

### Check mass and inertia

Mass is measured in kg; rotational inertia is measured in kg·m². For a uniform box with sides `a, b, c`, about its centre and principal axes:

```text
Ixx = m (b² + c²) / 12
Iyy = m (a² + c²) / 12
Izz = m (a² + b²) / 12
```

For an illustrative 0.06 kg cube with 0.05 m sides, each diagonal is `0.000025 kg·m²`. Compare an equivalent simulated body using matching geometry and assumptions. A compound gripper, off-centre load, or nonuniform link requires more than this box calculation. At fixed mass, scaling all lengths by ten scales inertia by one hundred.

## 5. Build one joint before assembling an arm

Use the installed release's joint/articulation tutorial to connect an anchored base and one rigid link with a revolute joint. Inspect body relationships, joint frames and axis, articulation configuration, limits, target, drive type, and force/torque limit. Start with a bounded small motion in an isolated scene.

Compare the commanded target with measured joint position and velocity. USD angular properties use degrees; ROS joint positions use radians. Verify wrapper/API units at each boundary instead of assuming every Python interface uses the same convention. Incorrect scaling can produce plausible motion at the wrong rate.

A force drive can be understood as position/velocity error feeding stiffness and damping, subject to limits. Acceleration drives and different joint types have different parameter meanings. Gains interact with inertia and integration settings. Record units and change one setting at a time; do not copy another robot's gain or torque limit.

Then return to the supported Franka workflow. Look up joints by name, verify the base/tool/camera frames, and preserve the baseline before substituting a custom model. The one-joint scene is a learning fixture, not a validated replacement robot.

## 6. Know what each camera value means

Record camera prim, resolution, intrinsics, optical-frame convention, clipping range, measurement units, annotator, and timestamps. Depth along the optical axis and Euclidean distance along a pixel ray are different measurements. Either can reconstruct a point with the matching formula.

For an undistorted pinhole camera in an optical frame with positive forward `Z`:

```text
ray = [(u-cx)/fx, (v-cy)/fy, 1]
point_from_Z = Z × ray
point_from_range = range × ray / length(ray)
```

Use the sensor's documented frame conversion before treating this as a USD world coordinate. Invalid depth, distortion, and missing returns require additional handling in a real pipeline. See the [annotator definitions](https://docs.omniverse.nvidia.com/kit/docs/omni_replicator/latest/source/extensions/omni.replicator.core/docs/API.html).

**API review, 25 October 2026:** current camera docs move older `isaacsim.sensors.camera` workflows toward `isaacsim.sensors.experimental.rtx`, including `RtxCamera` authoring and `CameraSensor` runtime acquisition. They document `tick_rate` as the replacement for older camera-helper frame skipping. Follow your installed release's [camera documentation](https://docs.isaacsim.omniverse.nvidia.com/latest/sensors/isaacsim_sensors_camera.html); keep the annotator meaning separate from the API spelling.

## 7. Measure simulation time and wall time separately

Give simulation stepping one explicit owner: the selected standalone loop or the application's supported timeline/extension workflow. Extra update calls, sleeps, callbacks, rendering, and graph scheduling can change when work happens. Verify simulation-time increments and pause/reset behavior in the installed API rather than inferring them from a method name.

```text
RTF = elapsed simulation seconds / elapsed monotonic wall seconds
velocity_in_simulation = position change / source simulation-time change
```

At RTF 0.5, a motion of 0.25 m per simulated second appears as 0.125 m per wall second. Both can be correct. Fewer sensor samples do not inherently change the physical motion; using the physics timestep as the interval between slower sensor samples corrupts the estimated velocity.

A headless process may still need offscreen rendering for cameras. Disabling rendering entirely is a different workload from generating camera observations without a visible window. Report physics-step rate, rendered frame rate, sensor rate, and RTF separately. See NVIDIA's [RTF tutorial](https://docs.isaacsim.omniverse.nvidia.com/latest/ros2_tutorials/tutorial_series/tutorial_ros2_rtf.html) and [ROS 2 clock guide](https://docs.isaacsim.omniverse.nvidia.com/latest/ros2_tutorials/tutorial_series/tutorial_ros2_clock.html).

Prefer simulator-side elapsed measurements for execution RTF. Estimating it from a remote observer's source/receipt intervals also includes transport and buffering effects. Label the measurement location and clock domain so a network stall is not mistaken for slower physics.

## 8. Run the laptop contract lab

```bash
python3 examples/sensor_contracts.py
python3 examples/sensor_contracts.py --scenario reset
```

The first command uses invented inputs to demonstrate two depth conventions and mismatched sampling intervals. It reports the same 3D point from matching `Z`/range measurements; misreading range as `Z` produces a 0.25 m point error in this example. It also reports RTF 0.5, a correct 0.25 m/s source-time velocity, and an incorrect 1.0 m/s estimate obtained by dividing a sensor displacement by the physics timestep.

The reset scenario deliberately exits with an error because simulation timestamps move backward. Start a new episode instead of joining that transition into a velocity estimate. Download the [standalone script]({{base}}/examples/sensor_contracts.py), or run it from your clone. It uses only Python's standard library and does not contact a simulator.

Save `sensor-contracts.md` with your predicted values, output, frames/units, and the effect of changing a rate or depth convention. Mark the arithmetic fixture separately from GPU execution evidence.

## 9. Inspect labels before generating a large dataset

Generate a small image set with RGB and one relevant annotation channel. Document class/instance mappings, pixel coordinates, visible versus full-object extent, occlusion rules, depth convention, frame identity, and seed. Overlay annotations on the corresponding RGB frame and check a cube that is fully visible, partially hidden, and outside the camera view.

Compare channels only after confirming they describe the same objects and extent. A floor label should not be counted as a cube-label error. Record the writer/annotator versions and inspect the actual files, not only the viewport.

Blur, exposure, and noise perturbations test chosen image variations. They do not establish a mathematical lower bound on real-world error or guarantee transfer. Compare with a meaningful baseline, then use independently held-out real observations when making a sim-to-real claim. Continue with the [evaluation guide](evaluation.md).

## Deliver a reproducible scene

Save `scene.md`, the scene and its dependency revisions, your host/renderer evidence, physics settings, sensor contract, clock measurements, and baseline/perturbed results. For the arm, define placement tolerance, release evidence, and a stability window before the trial. A cube briefly passing through the tray region has not necessarily been placed.

<details><summary>The viewport looks right and ROS messages arrive. What remains unproved?</summary><p>The selected render device, collision shape, units, dynamics, source clock, sensor meaning, and object outcome can each still be wrong. Validate each contract with a small controlled experiment and retain its evidence.</p></details>
