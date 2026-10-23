# Verification scope

## Automated

The repository's GitHub Actions workflow runs:

- Behavioral tests for the portable control, estimation, and mission examples.
- JavaScript syntax validation.
- The static build under the GitHub Pages project base path.
- Local destination/fragment validation across generated pages.
- Coverage checks for all 21 lessons, source links, checkpoints, and search entries.

The tests verify bounded commands and baseline tracking, delay effects, seeded
filter behavior, synthetic event identity, cancellation versus motion evidence,
unconfirmed disconnects, duplicate requests, and preservation of existing output.

## Source-reviewed reference exercises

The ROS 2 and NVIDIA instructions link to official documentation. The initial
review date is 23 October 2026. Product references include Isaac Sim 6.2 GA,
Isaac Lab v3.0.0, Isaac ROS release-5.0 docs, and GR00T N1.7. Individual compatibility
and artifact availability must be checked for the user's environment.

These source reviews are not execution evidence for GPU training, ROS middleware,
Isaac bridges, Jetson deployment, or physical robot behavior. Contributors can add
reproduction reports with exact hardware, versions, commands, logs, and limitations.

## Reproduction report template

```text
Date:
Guide commit:
Lesson:
Route (CPU / ROS / GPU / hardware):
OS and hardware:
Drivers and product versions:
Physics backend and renderer:
Exact commands:
Expected result:
Observed result:
Evidence artifacts:
Unexecuted steps:
Known limitations:
```

Never publish credentials, proprietary scenes, personal data, or recordings without
permission. A successful simulation or software acknowledgment does not certify a
physical machine or establish a safety-rated intervention.
