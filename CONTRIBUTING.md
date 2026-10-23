# Contributing

Help make robotics easier to enter without weakening its technical foundations.

## Useful contributions

- Correct a concept with a primary source and a concrete example.
- Reproduce a ROS/Isaac exercise and share versions, hardware, commands, and results.
- Explain a failure case or improve a checkpoint.
- Improve accessibility, mobile reading, or the portable labs.
- Add a translation with clear attribution and a maintenance plan.

## Edit the source

Lessons are in `content/lessons/`. Supporting notes are in `content/pages/`.
The order and daily practice budgets live in `curriculum.json`. Site generation
is in `scripts/build.py`; generated `dist/` output is not committed.

Keep the original explanatory voice, practical exercises, checkpoints, and links
to primary sources. Explain assumptions and evidence limits. Do not promise
robotics expertise in 21 days or imply simulator results certify real hardware.
Keep ClawMetry mentions relevant, factual, and clear about proposed integrations.

Do not copy textbook passages, vendor diagrams, course videos, proprietary data,
or third-party code into this repository without appropriate rights and attribution.

## Validate

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
node --check assets/app.js
python scripts/build.py --base-path /physical-ai-for-software-engineers
python scripts/check_site.py --base-path /physical-ai-for-software-engineers
```

For a root-path local preview, build without `--base-path`, then serve `dist/`.
Check both narrow/mobile and desktop views for UI changes. For GPU instructions,
include the exact environment and distinguish documentation review from execution.

Open a pull request describing the change, why it helps readers, source evidence,
and what you tested. Updates publish through GitHub Actions after merging to main.

## Licensing contributions

Submit original text under CC BY 4.0 and original code under MIT. You retain your
copyright while granting those permissions. External work keeps its own license.
