"""Validate V5.1 raw completeness, witnesses, accounting and family promises."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def expected_status(case: dict) -> str | None:
    family, level = case["family"], case["level"]
    if family == "planted_3sat" or family == "symmetry":
        return "sat"
    if family in {"xor", "two_sat"}:
        return "unsat" if level == "zero" else "sat"
    if family == "pigeonhole" or (family == "coloring" and level == "unsat_k4"):
        return "unsat"
    if family == "coloring" and level == "sparse":
        return "sat"
    return None


def validate(run_dir: Path) -> list[str]:
    config = json.loads((run_dir / "config.json").read_text(encoding="utf-8"))
    cases = read_jsonl(run_dir / "instances.jsonl")
    rows = read_jsonl(run_dir / "runs.jsonl")
    errors = []
    by_case = {case["instance_id"]: case for case in cases}
    if len(by_case) != len(cases):
        errors.append("duplicate instance ID")
    seen = set()
    for row in rows:
        key = (row["instance_id"], row["method"])
        if key in seen:
            errors.append(f"duplicate method record {key}")
        seen.add(key)
        if row["instance_id"] not in by_case:
            errors.append(f"unknown instance {key}")
            continue
        case = by_case[row["instance_id"]]
        if row["method"] not in case["methods"]:
            errors.append(f"unplanned method {key}")
        if row["budget_s"] != config["timeout_s"] or row["memory_budget_mb"] != config["memory_mb"]:
            errors.append(f"budget mismatch {key}")
        if row["completed"] != (row["status"] in {"sat", "unsat"}):
            errors.append(f"completion mismatch {key}")
        if row["status"] == "sat" and row.get("witness_verified") is not True:
            errors.append(f"unverified SAT witness {key}")
        if row["completed"] and expected_status(case) not in {None, row["status"]}:
            errors.append(f"generator promise mismatch {key}")
        if row["completed"] and row.get("partition_depth", 0) > case["actual_n"]:
            errors.append(f"partition depth overflow {key}")
        if row["method"] in {"prefix", "occurrence", "connectivity", "propagation", "symmetry", "residual", "jeroslow_wang"} and row["completed"]:
            if row["solver_calls"] != row["partition_depth"] + 1:
                errors.append(f"partition call accounting mismatch {key}")
            if row["status"] == "sat" and row["partition_depth"] != case["actual_n"]:
                errors.append(f"premature partition success {key}")
            if row["search_space_reduction_log2"] != row["partition_depth"]:
                errors.append(f"reduction accounting mismatch {key}")
    planned = {(case["instance_id"], method) for case in cases for method in case["methods"]}
    for key in planned - seen:
        errors.append(f"missing method record {key}")
    for case in cases:
        statuses = {row["status"] for row in rows if row["instance_id"] == case["instance_id"] and row["completed"]}
        if len(statuses) > 1:
            errors.append(f"completed solvers disagree on {case['instance_id']}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    args = parser.parse_args()
    errors = validate(args.run_dir)
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Validated {args.run_dir}")


if __name__ == "__main__":
    main()
