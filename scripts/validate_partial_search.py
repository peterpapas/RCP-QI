"""Validate immutable post-publication partial-search artifacts and accounting."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from rcp_qi_research.partial_search import (
    Schedule,
    analytic_probabilities,
    best_schedule,
    full_grover_half_probability,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "results" / "corrections" / "partial_search_20261127"
ARTIFACTS = ("partial_search.json", "thresholds.csv", "accuracy_vs_queries.png")


def _digest(path: Path) -> dict:
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def validate(directory: Path) -> tuple[int, int, Path, dict]:
    report = json.loads((directory / "partial_search.json").read_text(encoding="utf-8"))
    if report["metadata"]["id"] != "POSTPUB-PARTIAL-SEARCH-20261127":
        raise ValueError("unexpected correction identifier")
    for item in report["thresholds"]:
        schedule = Schedule(item["global_before"], item["local"], item["final_global"])
        expected, actual = best_schedule(item["n"], item["threshold"])
        if schedule != expected or item["partial_calls"] != schedule.phase_oracle_calls or abs(item["partial_analytic_probability"] - actual) > 1e-10:
            raise ValueError("incorrect threshold schedule or accounting")
        first_v2 = next(r for r in range(item["N"]) if full_grover_half_probability(item["n"], r) + 1e-12 >= item["threshold"])
        if item["v2_full_grover_calls"] != first_v2:
            raise ValueError("incorrect V2 comparator")
    groups: dict[tuple[int, float], list[float]] = {}
    for row in report["rows"]:
        schedule = Schedule(row["global_before"], row["local"], row["final_global"])
        half, solution = analytic_probabilities(row["n"], schedule)
        if (row["phase_oracle_calls"] != schedule.phase_oracle_calls or row["state_preparations"] != 1
                or row["partition_measurements"] != 1 or row["verification_calls"] != 0 or row["shots"] != 0
                or row["ancillas"] != 0 or row["qubits"] != row["n"]
                or row["transpiled_gate_count_with_measurement"] <= 0 or row["transpiled_depth_with_measurement"] <= 0
                or abs(row["partition_probability_analytic"] - half) > 1e-10
                or abs(row["partition_probability_statevector"] - half) > 1e-10
                or abs(row["solution_probability_analytic"] - solution) > 1e-10
                or abs(row["solution_probability_statevector"] - solution) > 1e-10):
            raise ValueError("invalid statevector or resource row")
        groups.setdefault((row["n"], row["threshold"]), []).append(row["partition_probability_statevector"])
    if len(groups) != len(report["thresholds"]) or any(max(values) - min(values) > 1e-10 for values in groups.values()):
        raise ValueError("target-position independence failed")
    manifest_path = directory / "manifest.json"
    manifest = {"schema_version": 1, "id": report["metadata"]["id"],
                "scope": "New correction artifacts only; V1–V10 manifest and closeout inventory remain untouched.",
                "artifacts": {name: _digest(directory / name) for name in ARTIFACTS}}
    return len(report["thresholds"]), len(report["rows"]), manifest_path, manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT)
    parser.add_argument("--write-manifest", action="store_true", help="pin a new inventory once")
    args = parser.parse_args()
    schedules, rows, path, current = validate(args.output_dir)
    if args.write_manifest:
        if path.exists():
            raise FileExistsError(f"refusing to overwrite: {path}")
        path.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
    elif current != json.loads(path.read_text(encoding="utf-8")):
        raise ValueError("post-publication correction artifact hash mismatch")
    print(f"Validated {schedules} schedules, {rows} statevector rows, and {len(ARTIFACTS)} correction artifacts")


if __name__ == "__main__":
    main()
