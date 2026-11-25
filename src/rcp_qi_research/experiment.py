"""Seeded experiment and resource/success summaries."""

import argparse
import csv
import json
from importlib.metadata import version
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binomtest

from .interference import run_one_iteration_experiment
from .problems import CNFProblem, EqualityProblem
from .search import classical_exhaustive, grover_search, recursive_partition_search


def run_experiment(
    output_dir: Path, *, seed: int = 20261125, trials: int = 4, max_n: int = 4, repetitions: int = 3
) -> dict:
    if trials < 1 or max_n < 2 or repetitions < 1:
        raise ValueError("trials and repetitions must be positive; max_n must be at least 2")
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    cases = []
    for n in range(2, max_n + 1):
        # Stratify target positions to avoid a tiny sample clustering at one end.
        targets = [min(2**n - 1, int((trial + 0.5) * 2**n / trials)) for trial in range(trials)]
        for trial, target in enumerate(rng.permutation(targets)):
            cases.append((f"equality_n{n}", trial, EqualityProblem(n, int(target))))
    # An implication chain, not a truth table: x1 and x_i => x_(i+1).
    sat = CNFProblem(3, ((1,), (-1, 2), (-2, 3)))
    for trial in range(trials):
        cases.append(("cnf_chain_n3", trial, sat))
    # User-supplied example: (a OR b) AND (NOT b OR c) AND (NOT a) AND c.
    # Variable 1 is the least-significant bit, so abc=011 is integer 6.
    sat_handover = CNFProblem(3, ((1, 2), (-2, 3), (-1,), (3,)))
    for trial in range(trials):
        cases.append(("cnf_handover_n3", trial, sat_handover))

    records = []
    for index, (case, trial, problem) in enumerate(cases):
        run_seed = seed + 7919 * index
        for result in (
            classical_exhaustive(problem),
            grover_search(problem, repetitions=repetitions, seed=run_seed),
            recursive_partition_search(problem, repetitions=repetitions, seed=run_seed),
        ):
            records.append(
                {
                    "case": case,
                    "n": problem.n,
                    "N": 2**problem.n,
                    "trial": trial,
                    "instance": repr(problem),
                    "seed": run_seed,
                    **result.as_record(),
                }
            )

    groups = {}
    for record in records:
        groups.setdefault((record["case"], record["algorithm"]), []).append(record)
    summary = []
    for (case, algorithm), rows in groups.items():
        successes = sum(row["success"] for row in rows)
        interval = binomtest(successes, len(rows)).proportion_ci(confidence_level=0.95, method="wilson")
        summary.append(
            {
                "case": case,
                "algorithm": algorithm,
                "N": rows[0]["N"],
                "trials": len(rows),
                "success_probability_empirical": successes / len(rows),
                "success_ci95_low": interval.low,
                "success_ci95_high": interval.high,
                **{
                    f"mean_{key}": float(np.mean([row[key] for row in rows]))
                    for key in (
                        "total_predicate_queries",
                        "quantum_oracle_calls",
                        "verification_calls",
                        "circuit_executions",
                        "state_preparations",
                        "measurements",
                        "gate_count_total",
                        "circuit_depth_total",
                        "circuit_depth_max",
                        "elapsed_s",
                    )
                },
            }
        )

    metadata = {
        "seed": seed,
        "trials_per_case": trials,
        "max_n": max_n,
        "repetitions": repetitions,
        "versions": {name: version(name) for name in ("qiskit", "qiskit-aer", "numpy", "scipy", "matplotlib")},
        "backend": "AerSimulator(method='statevector'), ideal/noiseless, one shot per execution",
        "gate_basis": ["u", "cx"],
        "gate_metric": "sum of transpiled operations, including measurement, over actual executions",
        "depth_metric": "transpiled circuit depth; total sums depth over actual executions",
    }
    result = {"metadata": metadata, "summary": summary, "records": records}
    (output_dir / "initial.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    with (output_dir / "initial.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    for algorithm in ("classical", "grover", "rcp_qi"):
        points = sorted(
            (row["N"], row["mean_total_predicate_queries"])
            for row in summary
            if row["algorithm"] == algorithm and row["case"].startswith("equality")
        )
        ax.plot(*zip(*points), marker="o", label=algorithm)
    ns = np.array([2**n for n in range(2, max_n + 1)])
    ax.plot(ns, ns, linestyle="--", color="gray", alpha=0.6, label="N reference")
    ax.plot(ns, np.sqrt(ns), linestyle=":", color="black", alpha=0.6, label="sqrt(N) reference")
    ax.set(xlabel="search-space size N", ylabel="mean total predicate calls", title="Unique-solution search: measured resource use")
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "scaling.png", dpi=160)
    plt.close(fig)
    run_one_iteration_experiment(output_dir, max_n=max(8, max_n))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    parser.add_argument("--seed", type=int, default=20261125)
    parser.add_argument("--trials", type=int, default=4)
    parser.add_argument("--max-n", type=int, default=4)
    parser.add_argument("--repetitions", type=int, default=3)
    args = parser.parse_args()
    result = run_experiment(args.output_dir, seed=args.seed, trials=args.trials, max_n=args.max_n, repetitions=args.repetitions)
    for row in result["summary"]:
        print(
            f"{row['case']:16} {row['algorithm']:9} "
            f"success={row['success_probability_empirical']:.2f} "
            f"queries={row['mean_total_predicate_queries']:.2f} "
            f"time={row['mean_elapsed_s']:.4f}s"
        )
    print(f"Saved initial.json, initial.csv, scaling.png, one_iteration.json, and one_iteration.png in {args.output_dir}")


if __name__ == "__main__":
    main()
