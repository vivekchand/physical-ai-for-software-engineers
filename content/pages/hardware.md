## Buy for the experiment you want to run

Start with our red-cube-to-tray task, then choose a robot that makes that experiment practical. You can learn the software and run the included models before buying an arm. For a first physical setup, my shortlist starts with a supported SO-101 teleoperation kit; a second arm can follow when bimanual work becomes the actual learning goal.

**Prices reviewed 23 October 2026, in USD.** These are dated supplier listings, not delivered quotations or an automatically updated feed. Shipping, destination taxes/VAT, import charges, accessories, compute, and model/API fees can change the total. No affiliate links are used.

## From the lowest listed budget upward

The table separates a parts package from a usable teleoperation kit. Prices are read from the linked supplier pages or their public product data. Recommendations in the final column are this guide's assessment; we have not physically tested or purchased these arms.

{{single_arm_table}}

The SO-101 variant links select the reviewed black package. Its page showed a generic sold-out label while its public product data reported available variants; confirm the selected package, stock, and destination delivery with the seller. Do not treat a parts-only “from $199” label as the assembled kit price. [Supplier variant data](https://shop.wowrobo.com/products/so-arm101-diy-kit-assembled-version-1.js).

PiPER's $1,999 figure was verified in its [manufacturer product data](https://global.agilex.ai/products/piper.js). Regional resellers and configured packages can differ. Confirm which PiPER variant and accessories you are comparing. MakerMods' current Maker Arm listing separately showed future-batch shipping; check lead time before planning a 21-day hardware schedule.

## Understand what “two arms” means

A **leader** is the device a person moves to demonstrate a motion. A **follower** is the robot executing that motion. A kit with one leader and one follower provides **one working manipulator**, not two arms performing a bimanual task together.

A bimanual teleoperation station commonly has two followers and two leaders: four arm-shaped devices, plus cameras, mounts, control interfaces, and a computer.

{{bimanual_table}}

For a two-PiPER configuration like the reference scene, request an itemized two-arm quote including grippers, mounting, communication adapters, cameras, power, and teleoperation equipment. Twice a single-arm price is an arm subtotal, not a complete station quotation.

## What I would buy at each stage

1. **Before any hardware:** run the portable arm lab and, with suitable compute, the official Isaac Sim manipulation example.
2. **First physical learning setup:** shortlist an assembled SO-101 leader/follower kit with camera, power, cables, and mounting explicitly included. Learn calibration, demonstrations, replay, and a small policy.
3. **When you need two working arms:** compare complete bimanual packages such as the Maker Arm Station full teleop setup with a configured PiPER/YAM alternative. Check task workspace and software support before choosing by price.
4. **When a project demands specific performance:** evaluate Metal Arm, Lite 6, xArm, or Franka against measured requirements, support, and the full setup cost. A higher price does not automatically improve the learning experience.

These are starter routes, not claims that a particular product is best for every reader or location.

## The full learning setup

Ask the seller to list the working arm(s), leader/controller, gripper, camera(s), mounts/clamps, power supplies, communication adapters, cables, and supported host OS. Separately budget the computer, any GPU training/inference, spare parts, and vendor service charges.

For an EU delivery, get a destination-specific total and clear VAT/import treatment. Avoid comparing a tax-inclusive European offer with a US-dollar arm-only number as if they were the same package. This guide does not calculate a landed EUR price from unverified assumptions.

## Match the model to the robot

- [LeRobot SO-101 instructions](https://huggingface.co/docs/lerobot/so101) are a practical starting point for the low-cost route. Calibration and recording come before policy evaluation.
- A published SDK or URDF is useful, but does not establish that a specific VLA checkpoint supports the delivered robot/firmware.
- Dream-1's reviewed introduction emphasizes bimanual parallel-gripper manipulation. A single SO-101 or single Franka is not automatically a matching configuration.
- The guide's two-link browser/Python model is educational geometry; it is not a hardware driver or a simulator model of any product in the table.

Read the Models field note for the observation/action contract you should check. Use a controlled, supervised workspace and the manufacturer's setup procedures when you move from simulation to physical equipment.

## Source and maintenance notes

The priced rows are generated from `data/hardware.json`, including review date, supplier URLs, package scope, and public product-data links where used. Update the data and explanations together when a supplier changes a package.

Primary starting points: [SO-101 documentation](https://huggingface.co/docs/lerobot/so101), [Seeed's alternative assembled-arm listing](https://www.seeedstudio.com/SO-101-Assembled-Kit-Pro-p-6691.html), [MakerMods](https://www.makermods.ai/), [AgileX PiPER](https://global.agilex.ai/products/piper), [I2RT docs](https://doc.i2rt.com/products/yam), [UFACTORY store](https://www.shop.ufactory.cc/), and [Franka](https://franka.de/franka-research-3). The Seeed listing is another supplier/package, not assumed equivalent to the WowRobo leader/follower bundle.
