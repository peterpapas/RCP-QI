"""Phase 2: costed multi-iteration Grover partition benchmark.

This module introduces no new oracle or diffusion operator. It measures how
the existing Grover circuit's correct-half probability relates to its exact
solution probability, including repeated measured decisions.
"""

import argparse
import csv
import json
from math import asin, ceil, pi, sin, sqrt
from pathlib import Path
from time import perf_counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from qiskit import transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from scipy.stats import binom

from .problems import EqualityProblem
from .search import build_grover_circuit

THRESHOLDS = (0.90, 0.95, 0.99)


def solution_probability(n: int, iterations: int) -> float:
    """One marked item in N=2**n, starting from a uniform state."""
    if n < 1 or iterations < 0:
        raise ValueError("n must be positive and iterations nonnegative")
    theta = asin(1 / sqrt(2**n))
    return sin((2 * iterations + 1) * theta) ** 2


def correct_half_probability(n: int, iterations: int) -> float:
    """Marked half contains one marked and N/2-1 symmetric unmarked items."""
    size = 2**n
    marked = solution_probability(n, iterations)
    return (size - 2 + size * marked) / (2 * (size - 1))


def _accuracy(method: str, n: int, iterations: int, shots: int) -> float:
    if method == "partition_majority":
        if shots % 2 != 1:
            raise ValueError("partition majority needs an odd number of shots")
        return float(binom.sf(shots // 2, shots, correct_half_probability(n, iterations)))
    if method == "grover_verified":
        p = solution_probability(n, iterations)
        return 1 - (1 - p) ** shots
    raise ValueError(method)


def _cost(method: str, iterations: int, shots: int) -> int:
    # Candidate verification is a separate classical predicate evaluation.
    return shots * (iterations + (method == "grover_verified"))


def threshold_plan(n: int, threshold: float, method: str, *, scan_factor: int = 4) -> dict:
    """Find the minimum cost within the specified fixed-r, identical-shot family.

    We first find a feasible one-shot r, yielding a finite upper bound B.
    Exhausting every r,t with cost <=B proves the reported minimum for this
    protocol family; no truncation of t can suppress a cheaper option.
    """
    if not 0.5 < threshold < 1 or scan_factor < 1:
        raise ValueError("threshold must be between 0.5 and 1; scan_factor positive")
    if method not in ("partition_majority", "grover_verified"):
        raise ValueError(method)
    max_r = scan_factor * 2**n
    first_single = next(
        (r for r in range(max_r + 1) if _accuracy(method, n, r, 1) >= threshold - 1e-12),
        None,
    )
    if first_single is None:
        raise RuntimeError(f"no one-shot {threshold} solution for n={n} by r={max_r}")
    upper_bound = _cost(method, first_single, 1)
    best = None
    for r in range(0 if method == "grover_verified" else 1, upper_bound + 1):
        per_shot = _cost(method, r, 1)
        if per_shot == 0 or per_shot > upper_bound:
            continue
        max_shots = upper_bound // per_shot
        shots_range = range(1, max_shots + 1, 2) if method == "partition_majority" else range(1, max_shots + 1)
        for shots in shots_range:
            accuracy = _accuracy(method, n, r, shots)
            if accuracy >= threshold - 1e-12:
                cost = _cost(method, r, shots)
                candidate = (cost, r * shots, shots, r, accuracy)
                if best is None or candidate < best:
                    best = candidate
                break
    assert best is not None
    cost, phase_calls, shots, iterations, accuracy = best
    return {
        "n": n,
        "N": 2**n,
        "threshold": threshold,
        "method": method,
        "single_shot_min_iterations": first_single,
        "iterations_per_shot": iterations,
        "shots": shots,
        "phase_oracle_calls": phase_calls,
        "verification_calls": shots if method == "grover_verified" else 0,
        "total_predicate_calls": cost,
        "achieved_accuracy": accuracy,
        "single_shot_scan_max_iterations": max_r,
        "minimum_certified_under_cost_bound": upper_bound,
    }


def _target_positions(n: int, rng: np.random.Generator) -> list[int]:
    size = 2**n
    positions = {0, size // 2 - 1, size // 2, size - 1}
    positions.add(int(rng.integers(0, size)))
    return sorted(positions)


def _validate_circuit(
    n: int, target: int, iterations: int, *, shots: int, seeds: tuple[int, ...]
) -> dict:
    start = perf_counter()
    measured, oracle_calls = build_grover_circuit(EqualityProblem(n, target), iterations=iterations)
    bare = measured.remove_final_measurements(inplace=False)
    state = Statevector.from_instruction(bare)
    probabilities = state.probabilities()
    size = 2**n
    correct_half = slice(0, size // 2) if target < size // 2 else slice(size // 2, size)
    exact_solution = float(probabilities[target])
    exact_half = float(sum(probabilities[correct_half]))
    physical = transpile(measured, basis_gates=["u", "cx"], optimization_level=0)
    backend = AerSimulator(method="statevector")
    samples = []
    for seed in seeds:
        counts = backend.run(physical, shots=shots, seed_simulator=seed).result().get_counts()
        correct_half_count = sum(
            count for bitstring, count in counts.items() if (int(bitstring, 2) < size // 2) == (target < size // 2)
        )
        solution_count = counts.get(format(target, f"0{n}b"), 0)
        samples.append(
            {
                "seed": seed,
                "shots": shots,
                "correct_half_count": correct_half_count,
                "solution_count": solution_count,
                "correct_half_frequency": correct_half_count / shots,
                "solution_frequency": solution_count / shots,
                "phase_oracle_calls": shots * oracle_calls,
                "state_preparations": shots,
                "measurements": shots,
            }
        )
    return {
        "n": n,
        "N": size,
        "target": target,
        "iterations": iterations,
        "analytic_correct_half_probability": correct_half_probability(n, iterations),
        "analytic_solution_probability": solution_probability(n, iterations),
        "statevector_correct_half_probability": exact_half,
        "statevector_solution_probability": exact_solution,
        "qubits": physical.num_qubits,
        "ancillas": 0,
        "gate_count_per_shot": sum(physical.count_ops().values()),
        "depth_per_shot": physical.depth(),
        "phase_oracle_calls_per_shot": oracle_calls,
        "circuit_builds": 1,
        "elapsed_simulator_and_compilation_s": perf_counter() - start,
        "samples": samples,
    }


def run_benchmark(
    output_dir: Path,
    *,
    min_n: int = 2,
    max_n: int = 8,
    seed: int = 20261125,
    shots: int = 256,
    sample_seeds: int = 2,
) -> dict:
    if min_n < 2 or max_n < min_n or shots < 1 or sample_seeds < 1:
        raise ValueError("invalid benchmark range, shots, or seeds")
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    curves = []
    thresholds = []
    validations = []
    for n in range(min_n, max_n + 1):
        size = 2**n
        theta = asin(1 / sqrt(size))
        first_lobe_end = ceil(pi / (2 * theta))
        for r in range(first_lobe_end + 1):
            curves.append(
                {
                    "n": n,
                    "N": size,
                    "iterations": r,
                    "phase_oracle_calls_per_shot": r,
                    "solution_probability": solution_probability(n, r),
                    "correct_half_probability": correct_half_probability(n, r),
                }
            )
        for threshold in THRESHOLDS:
            for method in ("partition_majority", "grover_verified"):
                thresholds.append(threshold_plan(n, threshold, method))

        near_peak = max(0, round(pi / (4 * theta) - 0.5))
        check_iterations = sorted({0, 1, near_peak, next(
            row["single_shot_min_iterations"] for row in thresholds
            if row["n"] == n and row["threshold"] == 0.99 and row["method"] == "partition_majority"
        )})
        for target in _target_positions(n, rng):
            for r in check_iterations:
                seeds = tuple(seed + 100_003 * n + 101 * target + 17 * r + i for i in range(sample_seeds))
                validations.append(_validate_circuit(n, target, r, shots=shots, seeds=seeds))

    report = {
        "metadata": {
            "seed": seed,
            "min_n": min_n,
            "max_n": max_n,
            "shots_per_validation_seed": shots,
            "sample_seeds": sample_seeds,
            "backend": "ideal Aer statevector; exact probabilities also from Qiskit Statevector",
            "gate_basis": ["u", "cx"],
            "threshold_protocols": {
                "partition_majority": "fixed r, odd independent shots, majority of measured partition bits; no candidate verification",
                "grover_verified": "fixed r, independent shots, accept any classically verified candidate; worst-case planned shot cost",
            },
            "scope": "unique marked equality oracle; no partition-specific operator or claimed speedup",
        },
        "curves": curves,
        "thresholds": thresholds,
        "validations": validations,
    }
    (output_dir / "phase2_multi_iteration.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    with (output_dir / "phase2_thresholds.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(thresholds[0]))
        writer.writeheader()
        writer.writerows(thresholds)

    selected_n = sorted({min_n, (min_n + max_n) // 2, max_n})
    fig, axes = plt.subplots(1, len(selected_n), figsize=(5 * len(selected_n), 4.2), squeeze=False)
    for ax, n in zip(axes[0], selected_n, strict=True):
        rows = [row for row in curves if row["n"] == n]
        xs = [row["iterations"] for row in rows]
        ax.plot(xs, [row["correct_half_probability"] for row in rows], label="correct half")
        ax.plot(xs, [row["solution_probability"] for row in rows], label="exact solution")
        checks = [row for row in validations if row["n"] == n and row["target"] == 0 and row["iterations"] <= xs[-1]]
        ax.scatter(
            [row["iterations"] for row in checks],
            [row["statevector_correct_half_probability"] for row in checks],
            color="C0", marker="x", zorder=3, label="half: statevector",
        )
        ax.scatter(
            [row["iterations"] for row in checks],
            [row["statevector_solution_probability"] for row in checks],
            color="C1", marker="x", zorder=3, label="solution: statevector",
        )
        for level in THRESHOLDS:
            ax.axhline(level, color="gray", linestyle=":", linewidth=0.7, alpha=0.55)
        ax.set(xlabel="phase-oracle calls per shot", ylabel="probability", title=f"N={2**n}")
        ax.set_ylim(0, 1.04)
        ax.grid(alpha=0.2)
    axes[0][0].legend()
    fig.tight_layout()
    fig.savefig(output_dir / "phase2_accuracy_vs_queries.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    for threshold in THRESHOLDS:
        for method in ("partition_majority", "grover_verified"):
            rows = [row for row in thresholds if row["threshold"] == threshold and row["method"] == method]
            ax.plot(
                [row["N"] for row in rows],
                [row["total_predicate_calls"] for row in rows],
                marker="o",
                linestyle="-" if method == "partition_majority" else "--",
                label=f"{method}, {threshold:.0%}",
            )
    ax.set(xlabel="N", ylabel="minimum total predicate calls", title="Fixed-r repeated-shot confidence cost")
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.grid(alpha=0.2)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(output_dir / "phase2_threshold_costs.png", dpi=160)
    plt.close(fig)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    parser.add_argument("--min-n", type=int, default=2)
    parser.add_argument("--max-n", type=int, default=8)
    parser.add_argument("--seed", type=int, default=20261125)
    parser.add_argument("--shots", type=int, default=256)
    parser.add_argument("--sample-seeds", type=int, default=2)
    args = parser.parse_args()
    report = run_benchmark(
        args.output_dir,
        min_n=args.min_n,
        max_n=args.max_n,
        seed=args.seed,
        shots=args.shots,
        sample_seeds=args.sample_seeds,
    )
    max_error = max(
        abs(row["analytic_correct_half_probability"] - row["statevector_correct_half_probability"])
        for row in report["validations"]
    )
    print(f"Validated {len(report['validations'])} circuits; max correct-half error {max_error:.3g}")
    for row in report["thresholds"]:
        print(
            f"N={row['N']:3} {row['threshold']:.0%} {row['method']:18} "
            f"r={row['iterations_per_shot']:3} shots={row['shots']:3} "
            f"phase={row['phase_oracle_calls']:4} total={row['total_predicate_calls']:4}"
        )
    print(f"Saved phase2_multi_iteration.json, phase2_thresholds.csv, and two plots in {args.output_dir}")


if __name__ == "__main__":
    main()
