"""Build a small Pandas-derived cross-experiment table from raw results."""

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def build() -> Path:
    results = ROOT / "results"
    multi = json.loads((results / "phase2_multi_iteration.json").read_text(encoding="utf-8"))
    recursive = json.loads((results / "phase2_recursive.json").read_text(encoding="utf-8"))
    rows = [
        {
            "experiment": "V2-MULTI-ITERATION",
            "algorithm": row["method"],
            "N": row["N"],
            "target_confidence": row["threshold"],
            "accuracy": row["achieved_accuracy"],
            "total_predicate_calls": row["total_predicate_calls"],
            "phase_oracle_calls": row["phase_oracle_calls"],
            "measurement_shots": row["shots"],
        }
        for row in multi["thresholds"]
    ]
    rows.extend(
        {
            "experiment": "V6-RECURSIVE-BENCHMARK",
            "algorithm": row["algorithm"],
            "N": row["N"],
            "target_confidence": row["confidence_target"],
            "accuracy": row["success_probability_empirical"],
            "total_predicate_calls": row["mean_total_predicate_queries"],
            "phase_oracle_calls": row["mean_quantum_oracle_calls"],
            "measurement_shots": None,
        }
        for row in recursive["summary"]
    )
    output = results / "processed" / "phase2_summary.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output, index=False)
    return output


if __name__ == "__main__":
    print(build())
