## Measurements become an interpretation

The robot does not receive “the warehouse.” It receives images, ranges, inertial readings, encoder counts, and other measurements. Perception turns some of them into geometric or semantic information.

Encoders report joint or wheel motion. An IMU measures acceleration and angular motion subject to bias and noise. Cameras measure image intensity. Depth sensors or lidar provide range information under their operating assumptions. Each modality has characteristic failure modes.

## Geometry before labels

A camera maps a three-dimensional scene into a two-dimensional image. Intrinsic calibration describes properties of that projection, including focal parameters and distortion. Extrinsic calibration describes the camera's relationship to another frame.

Stereo estimates depth from corresponding observations across cameras with known geometry. A poor correspondence, textureless area, or incorrect calibration can corrupt the estimate. RGB-D cameras offer depth through technology-specific mechanisms and limitations.

Classical perception includes filtering, feature extraction, matching, and geometric alignment. Learned architectures extract representations from data. Detection identifies object instances, while segmentation assigns labels or instances to image regions. A useful system may combine both classical and learned methods.

## Confidence is not physical truth

Our detector may label a cardboard box with a high score while the box's estimated pose is unsuitable for grasping. Classification score, geometric uncertainty, and task success are different quantities. A single confidence badge should not collapse them.

For a reliable investigation, preserve the model version, sensor identity, calibration version, frame, source timestamp, and relevant output. Retain imagery only with appropriate scope and permission; a warehouse camera can also record people and sensitive operations.

## Today's practice

Choose a box in a photograph. Describe which properties you could infer from a single RGB image and which would require calibration, additional views, depth, or other assumptions.

Then use PORA's object-detection notebook. Try a changed background or partially hidden object. Log false positives and misses separately. Explain why performance on a few photographs does not establish performance in the target warehouse.

## Checkpoint

<details><summary>Does an accurate object label provide a reliable grasp pose?</summary><p>No. Recognition and geometric pose estimation solve different problems. Grasping also depends on object shape, contact, reachability, and execution.</p></details>

## Go deeper

- [PORA: Camera Models and Calibration](https://porabook.com/book/camera-models/).
- [PORA: Stereo Vision](https://porabook.com/book/stereo-vision/).
- [PORA: Classical Perception](https://porabook.com/book/classical-perception/).
- [PORA: Deep Learning for Perception](https://porabook.com/book/deep-learning-perception/) and [Object Detection](https://porabook.com/book/object-detection/).
