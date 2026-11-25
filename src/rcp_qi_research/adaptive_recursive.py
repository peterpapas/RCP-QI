"""Confidence-controlled recursive search with failed runs and restarts."""

import argparse
import json
from math import asin, ceil, log, sin, sqrt
from pathlib import Path
from time import perf_counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from qiskit_aer import AerSimulator
from scipy.stats import binomtest

from .problems import EqualityProblem, SearchProblem
from .search import SearchResult, _grover_iterations, _probe, grover_search


def repetitions_for_confidence(single_shot_success: float, confidence: float, decisions: int = 1) -> int:
    """Conservative per-decision budget via a union bound over decisions."""
    if not 0 < single_shot_success <= 1 or not 0 < confidence < 1 or decisions < 1:
        raise ValueError("invalid success probability, confidence, or decision count")
    if single_shot_success >= 1 - 1e-12:
        return 1
    miss_budget = (1 - confidence) / decisions
    return max(1, ceil(log(miss_budget) / log(1 - single_shot_success)))


def _single_shot_success(size: int, iterations: int) -> float:
    return sin((2 * iterations + 1) * asin(1 / sqrt(size))) ** 2


def adaptive_recursive_search(
    problem: SearchProblem,
    *,
    confidence: float = 0.95,
    max_restarts: int = 2,
    seed: int = 0,
) -> dict:
    """Run implicit-prefix partition probes; never inspect the true solution."""
    if not 0 < confidence < 1 or max_restarts < 0:
        raise ValueError("invalid confidence or restart limit")
    start = perf_counter()
    result = SearchResult("adaptive_rcp_qi")
    backend = AerSimulator(method="statevector")
    run_records = []
    worst_case_miss_bound = 0.0
    for run_index in range(max_restarts + 1):
        prefix: tuple[int, ...] = ()
        decisions = []
        run_miss_bound = 0.0
        for level in range(problem.n):
            left = (*prefix, 0)
            left_size = 2 ** (problem.n - level - 1)
            iterations = _grover_iterations(left_size)
            p_if_present = _single_shot_success(left_size, iterations)
            budget = repetitions_for_confidence(p_if_present, confidence, problem.n)
            before_shots = result.circuit_executions
            before_phase = result.quantum_oracle_calls
            selected_left = _probe(
                problem, left, budget, backend, seed + 100_003 * run_index + 1009 * level, result
            )
            selected = left if selected_left else (*prefix, 1)
            decisions.append(
                {
                    "level": level,
                    "prefix_before": "".join(map(str, prefix)),
                    "tested_left_prefix": "".join(map(str, left)),
                    "selected_prefix": "".join(map(str, selected)),
                    "selected_left": selected_left,
                    "left_partition_size": left_size,
                    "grover_iterations_per_shot": iterations,
                    "single_shot_detection_if_present": p_if_present,
                    "shot_budget": budget,
                    "actual_shots": result.circuit_executions - before_shots,
                    "phase_oracle_calls": result.quantum_oracle_calls - before_phase,
                    "miss_bound_if_present": (1 - p_if_present) ** budget,
                }
            )
            run_miss_bound += (1 - p_if_present) ** budget
            prefix = selected
        candidate = int("".join(map(str, prefix)), 2)
        result.verification_calls += 1
        verified = problem.evaluate(candidate)
        run_records.append(
            {
                "run_index": run_index,
                "candidate": candidate,
                "verified": verified,
                "decisions": decisions,
                "worst_case_union_miss_bound": run_miss_bound,
            }
        )
        worst_case_miss_bound = max(worst_case_miss_bound, run_miss_bound)
        if verified:
            result.success = True
            result.candidate = candidate
            break
        result.candidate = None
    result.elapsed_s = perf_counter() - start
    return {
        **result.as_record(),
        "confidence_target_per_run": confidence,
        "max_restarts": max_restarts,
        "runs_used": len(run_records),
        "failed_runs": sum(not run["verified"] for run in run_records),
        "restarts_used": len(run_records) - 1,
        "worst_case_union_miss_bound_per_run": worst_case_miss_bound,
        "run_records": run_records,
    }


def _audit_decisions(run: dict, n: int, target: int) -> tuple[int, int]:
    """Offline audit only; the search routine never receives target."""
    target_bits = format(target, f"0{n}b")
    evaluated = 0
    incorrect = 0
    for attempt in run["run_records"]:
        for decision in attempt["decisions"]:
            prefix = decision["prefix_before"]
            if not target_bits.startswith(prefix):
                decision["target_in_current_partition_audit"] = False
                decision["decision_correct_audit"] = None
                continue
            correct_left = target_bits[len(prefix)] == "0"
            correct = decision["selected_left"] == correct_left
            decision["target_in_current_partition_audit"] = True
            decision["decision_correct_audit"] = correct
            evaluated += 1
            incorrect += not correct
    return evaluated, incorrect


def run_recursive_benchmark(
    output_dir: Path,
    *,
    min_n: int = 2,
    max_n: int = 5,
    seed: int = 20261125,
    trials: int = 3,
    max_restarts: int = 2,
    confidences: tuple[float, ...] = (0.90, 0.95, 0.99),
) -> dict:
    if min_n < 2 or max_n < min_n or trials < 1:
        raise ValueError("invalid range or trials")
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    records = []
    for n in range(min_n, max_n + 1):
        size = 2**n
        targets = sorted({0, size - 1, int(rng.integers(0, size))})
        for target in targets:
            problem = EqualityProblem(n, target)
            for confidence in confidences:
                full_r = _grover_iterations(size)
                full_p = _single_shot_success(size, full_r)
                grover_repetitions = repetitions_for_confidence(full_p, confidence)
                for trial in range(trials):
                    run_seed = seed + 100_003 * n + 1009 * target + 37 * trial + int(confidence * 100)
                    recursive = adaptive_recursive_search(
                        problem, confidence=confidence, max_restarts=max_restarts, seed=run_seed
                    )
                    evaluated, incorrect = _audit_decisions(recursive, n, target)
                    recursive["audited_decisions"] = evaluated
                    recursive["incorrect_decisions_audit"] = incorrect
                    records.append(
                        {
                            "algorithm": "adaptive_rcp_qi",
                            "n": n,
                            "N": size,
                            "target_audit_only": target,
                            "confidence": confidence,
                            "trial": trial,
                            "seed": run_seed,
                            **recursive,
                        }
                    )
                    grover = grover_search(problem, repetitions=grover_repetitions, seed=run_seed)
                    records.append(
                        {
                            "n": n,
                            "N": size,
                            "target_audit_only": target,
                            "confidence": confidence,
                            "trial": trial,
                            "seed": run_seed,
                            "shot_budget": grover_repetitions,
                            **grover.as_record(),
                            "algorithm": "grover_with_confidence",
                        }
                    )

    summary = []
    for n in range(min_n, max_n + 1):
        for confidence in confidences:
            for algorithm in ("adaptive_rcp_qi", "grover_with_confidence"):
                group = [row for row in records if row["n"] == n and row["confidence"] == confidence and row["algorithm"] == algorithm]
                successes = sum(row["success"] for row in group)
                interval = binomtest(successes, len(group)).proportion_ci(confidence_level=0.95, method="wilson")
                summary.append(
                    {
                        "n": n,
                        "N": 2**n,
                        "confidence_target": confidence,
                        "algorithm": algorithm,
                        "trials": len(group),
                        "success_probability_empirical": successes / len(group),
                        "success_ci95_low": interval.low,
                        "success_ci95_high": interval.high,
                        "mean_total_predicate_queries": float(np.mean([row["total_predicate_queries"] for row in group])),
                        "mean_quantum_oracle_calls": float(np.mean([row["quantum_oracle_calls"] for row in group])),
                        "mean_verification_calls": float(np.mean([row["verification_calls"] for row in group])),
                        "mean_gate_count_total": float(np.mean([row["gate_count_total"] for row in group])),
                        "mean_depth_total": float(np.mean([row["circuit_depth_total"] for row in group])),
                        "mean_elapsed_s": float(np.mean([row["elapsed_s"] for row in group])),
                        "total_failed_runs": sum(row.get("failed_runs", 0) for row in group),
                        "total_incorrect_decisions_audit": sum(row.get("incorrect_decisions_audit", 0) for row in group),
                    }
                )

    report = {
        "metadata": {
            "seed": seed,
            "trials_per_target_confidence": trials,
            "max_restarts": max_restarts,
            "confidence_targets": confidences,
            "promise": "exactly one solution; no correct-branch information passed to algorithm",
            "confidence_rule": "union bound across levels; left-present detection miss only; final candidate verified",
            "audit": "target used after search solely to score decisions; not included in algorithm query costs",
            "backend": "ideal Aer statevector, one shot per execution",
            "gate_basis": ["u", "cx"],
        },
        "summary": summary,
        "records": records,
    }
    (output_dir / "phase2_recursive.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    colors = {0.90: "C0", 0.95: "C1", 0.99: "C2"}
    for confidence in confidences:
        for algorithm in ("adaptive_rcp_qi", "grover_with_confidence"):
            rows = [row for row in summary if row["confidence_target"] == confidence and row["algorithm"] == algorithm]
            ax.plot(
                [row["mean_total_predicate_queries"] for row in rows],
                [row["success_probability_empirical"] for row in rows],
                color=colors.get(confidence),
                linestyle="-" if algorithm == "adaptive_rcp_qi" else "--",
                marker="o" if algorithm == "adaptive_rcp_qi" else "s",
                label=f"{algorithm}, {confidence:.0%}",
            )
            for row in rows:
                ax.annotate(f"N={row['N']}", (row["mean_total_predicate_queries"], row["success_probability_empirical"]), fontsize=7)
    ax.set(xlabel="mean total predicate calls, including failed runs", ylabel="empirical final-solution accuracy", title="End-to-end accuracy versus query cost")
    ax.set_ylim(-0.04, 1.04)
    ax.grid(alpha=0.2)
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(output_dir / "phase2_recursive_accuracy.png", dpi=160)
    plt.close(fig)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    parser.add_argument("--min-n", type=int, default=2)
    parser.add_argument("--max-n", type=int, default=5)
    parser.add_argument("--seed", type=int, default=20261125)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--max-restarts", type=int, default=2)
    args = parser.parse_args()
    report = run_recursive_benchmark(
        args.output_dir,
        min_n=args.min_n,
        max_n=args.max_n,
        seed=args.seed,
        trials=args.trials,
        max_restarts=args.max_restarts,
    )
    for row in report["summary"]:
        print(
            f"N={row['N']:2} {row['confidence_target']:.0%} {row['algorithm']:22} "
            f"success={row['success_probability_empirical']:.2f} "
            f"queries={row['mean_total_predicate_queries']:.1f}"
        )
    print(f"Saved {args.output_dir / 'phase2_recursive.json'} and phase2_recursive_accuracy.png")


if __name__ == "__main__":
    main()
