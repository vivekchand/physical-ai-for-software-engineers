#!/usr/bin/env python3
"""Summarize labeled trial records. The default fixture is invented, not robot evidence."""
import argparse
from collections import defaultdict
import json
import math
from pathlib import Path


def load_trials(path):
    rows = []
    with Path(path).open() as source:
        for number, line in enumerate(source, 1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Line {number}: invalid JSON") from exc
    return rows


def summarize(rows):
    """Keep attempts, unknowns, interventions, conditions and provenance distinct."""
    groups = defaultdict(list)
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("Each trial must be a JSON object")
        for name in ("attempt_id", "policy", "condition", "evidence"):
            if not isinstance(row.get(name), str) or not row[name].strip():
                raise ValueError(f"Each trial needs a nonempty {name}")
        if row["attempt_id"] in seen:
            raise ValueError(f"Duplicate attempt_id: {row['attempt_id']}")
        seen.add(row["attempt_id"])
        if row["evidence"] not in ("synthetic", "simulation", "hardware"):
            raise ValueError("Evidence must be synthetic, simulation, or hardware")
        if row.get("outcome") not in ("placed", "failed", "unconfirmed"):
            raise ValueError("Outcome must be placed, failed, or unconfirmed")
        if type(row.get("intervened")) is not bool:
            raise ValueError("intervened must be a JSON boolean")
        elapsed = row.get("elapsed_s")
        if type(elapsed) not in (int, float) or not math.isfinite(elapsed) or elapsed <= 0:
            raise ValueError("elapsed_s must be a positive finite number including recovery/reset")
        groups[(row["policy"], row["condition"], row["evidence"])].append(row)
    if not seen:
        raise ValueError("Provide at least one trial")

    results = []
    for (policy, condition, evidence), trials in sorted(groups.items()):
        attempts = len(trials)
        placed = sum(row["outcome"] == "placed" for row in trials)
        autonomous = sum(row["outcome"] == "placed" and not row["intervened"] for row in trials)
        interventions = sum(row["intervened"] for row in trials)
        elapsed = sum(row["elapsed_s"] for row in trials)
        if not math.isfinite(elapsed):
            raise ValueError("Total elapsed time must remain finite")
        results.append({
            "policy": policy, "condition": condition, "evidence": evidence,
            "attempts": attempts, "verified_placements": placed, "autonomous_verified": autonomous,
            "failed": sum(row["outcome"] == "failed" for row in trials),
            "unconfirmed": sum(row["outcome"] == "unconfirmed" for row in trials),
            "interventions": interventions, "elapsed_s": elapsed,
            "verified_placement_rate": placed / attempts,
            "autonomous_verified_rate": autonomous / attempts,
            "intervention_rate": interventions / attempts,
            "autonomous_verified_per_hour": autonomous / elapsed * 3600,
        })
    return {
        "schema": "physical-ai-trial-summary-v1", "trial_count": len(seen), "groups": results,
        "scope": "Summarizes supplied labels; does not execute or independently verify a policy, simulator, or robot.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path(__file__).parent / "data/policy_trials.jsonl")
    args = parser.parse_args()
    try:
        result = summarize(load_trials(args.input))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
