"""Validate committed experiment provenance and core accounting invariants."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> dict:
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def validate() -> list[str]:
    manifest = load("manifest.json")
    errors = []
    for experiment in manifest["experiments"]:
        for relative in (*experiment["raw"], *experiment["figures"], *experiment.get("processed", [])):
            if not (ROOT / relative).is_file():
                errors.append(f"missing {relative}")
    for relative in manifest.get("processed", []):
        if not (ROOT / relative).is_file():
            errors.append(f"missing {relative}")

    initial = load("initial.json")
    for row in initial["records"]:
        counted = row["classical_evaluations"] + row["quantum_oracle_calls"] + row["verification_calls"]
        if row["total_predicate_queries"] != counted:
            errors.append("v1 query count mismatch")

    v1 = load("one_iteration.json")
    if max(row["absolute_error"] for row in v1["rows"]) > 1e-10:
        errors.append("v1 analytic/statevector mismatch")

    multi = load("phase2_multi_iteration.json")
    for row in multi["validations"]:
        if abs(row["analytic_correct_half_probability"] - row["statevector_correct_half_probability"]) > 1e-10:
            errors.append("v2 correct-half mismatch")
        if abs(row["analytic_solution_probability"] - row["statevector_solution_probability"]) > 1e-10:
            errors.append("v2 exact-solution mismatch")
        for sample in row["samples"]:
            if sample["phase_oracle_calls"] != row["iterations"] * sample["shots"]:
                errors.append("v2 sampled oracle cost mismatch")
    for row in multi["thresholds"]:
        if row["total_predicate_calls"] != row["phase_oracle_calls"] + row["verification_calls"]:
            errors.append("v2 threshold cost mismatch")

    sat = load("phase2_sat.json")
    for case in sat["cases"]:
        for row in case["quantum"]:
            if row["total_logical_oracle_and_verification_calls"] != row["total_predicate_queries"] + row["clause_phase_calls"]:
                errors.append("SAT clause-phase cost mismatch")
            if case["audit_solution_count"] == 0 and row["correct_outcome"] and not row["unsat_proven"]:
                errors.append("SAT unsat result lacks proof")

    structural = load("phase2_structural.json")
    for case in structural["cases"]:
        expected = case["audit_solution_count"] > 0
        if case["direct_pysat"]["solution_found"] != expected or not case["direct_pysat"]["verified"]:
            errors.append("V5 direct solver disagrees with offline audit")
        for row in case["partition_strategies"]:
            if row["solution_found"] != expected or not row["verified"]:
                errors.append("V5 partition disagrees with offline audit")
            if row["solver_calls"] != (case["n"] + 1 if expected else 1):
                errors.append("V5 partition SAT-call accounting mismatch")
            if row["verification_calls"] != int(expected):
                errors.append("V5 final-verification accounting mismatch")

    recursive = load("phase2_recursive.json")
    for row in recursive["records"]:
        if row["total_predicate_queries"] != row["classical_evaluations"] + row["quantum_oracle_calls"] + row["verification_calls"]:
            errors.append("recursive total query mismatch")
        if row["algorithm"] == "adaptive_rcp_qi" and row["failed_runs"] > row["runs_used"]:
            errors.append("recursive failed-run count mismatch")
    return errors


if __name__ == "__main__":
    issues = validate()
    if issues:
        raise SystemExit("\n".join(issues))
    print("Validated result manifest, v1/v2 probabilities, and V1-V6 resource accounting")
