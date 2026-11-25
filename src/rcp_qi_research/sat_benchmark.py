"""Clause-built SAT oracles, unit propagation, DPLL, and unknown-count Grover."""

import argparse
import json
from dataclasses import asdict, dataclass
from math import ceil, sqrt
from pathlib import Path
from time import perf_counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from qiskit import transpile
from qiskit_aer import AerSimulator

from .problems import CNFProblem
from .search import SearchResult, build_grover_circuit, classical_exhaustive


@dataclass
class ClassicalWork:
    literal_checks: int = 0
    propagation_assignments: int = 0
    dpll_nodes: int = 0
    dpll_branches: int = 0


def unit_propagate(problem: CNFProblem, assignment: dict[int, int], work: ClassicalWork) -> dict[int, int] | None:
    """Return propagated zero-indexed bit assignments, or None on conflict."""
    assignment = assignment.copy()
    while True:
        changed = False
        for clause in problem.clauses:
            satisfied = False
            unknown = []
            for lit in clause:
                work.literal_checks += 1
                bit = abs(lit) - 1
                if bit not in assignment:
                    unknown.append(lit)
                elif bool(assignment[bit]) == (lit > 0):
                    satisfied = True
                    break
            if satisfied:
                continue
            if not unknown:
                return None
            if len(unknown) == 1:
                lit = unknown[0]
                assignment[abs(lit) - 1] = int(lit > 0)
                work.propagation_assignments += 1
                changed = True
                break
        if not changed:
            return assignment


def dpll_search(problem: CNFProblem) -> dict:
    start = perf_counter()
    work = ClassicalWork()

    def recurse(partial: dict[int, int]) -> int | None:
        work.dpll_nodes += 1
        propagated = unit_propagate(problem, partial, work)
        if propagated is None:
            return None
        if len(propagated) == problem.n:
            candidate = sum(value << bit for bit, value in propagated.items())
            return candidate if problem.evaluate(candidate) else None
        bit = next(bit for bit in range(problem.n) if bit not in propagated)
        for value in (0, 1):
            work.dpll_branches += 1
            result = recurse({**propagated, bit: value})
            if result is not None:
                return result
        return None

    candidate = recurse({})
    return {
        "candidate": candidate,
        "solution_found": candidate is not None,
        "unsat_proven": candidate is None,
        **asdict(work),
        "elapsed_s": perf_counter() - start,
    }


def unknown_count_grover(
    problem: CNFProblem,
    *,
    seed: int,
    max_attempts: int = 12,
    use_unit_propagation: bool = False,
    phase_mode: str = "predicate",
) -> dict:
    """Increasing randomized Grover-iteration schedule; no solution count input."""
    if max_attempts < 1 or phase_mode not in ("predicate", "clause_parity"):
        raise ValueError("invalid attempt budget or phase mode")
    start = perf_counter()
    result = SearchResult("grover_unknown")
    work = ClassicalWork()
    fixed = unit_propagate(problem, {}, work) if use_unit_propagation else {}
    if fixed is None:
        result.elapsed_s = perf_counter() - start
        return {
            **result.as_record(),
            "proved_unsat_by_preprocessing": True,
            "fixed_variables": 0,
            "clause_phase_calls": 0,
            "preprocessing": asdict(work),
            "phase_mode": phase_mode,
        }
    if len(fixed) == problem.n:
        candidate = sum(value << bit for bit, value in fixed.items())
        result.verification_calls += 1
        result.success = problem.evaluate(candidate)
        result.candidate = candidate if result.success else None
        result.elapsed_s = perf_counter() - start
        return {
            **result.as_record(),
            "proved_unsat_by_preprocessing": False,
            "fixed_variables": len(fixed),
            "clause_phase_calls": 0,
            "preprocessing": asdict(work),
            "phase_mode": phase_mode,
        }

    rng = np.random.default_rng(seed)
    backend = AerSimulator(method="statevector")
    search_size = 2 ** (problem.n - len(fixed))
    m = 1.0
    clause_calls = 0
    for attempt in range(max_attempts):
        upper = max(1, ceil(m))
        iterations = int(rng.integers(0, upper))
        circuit, _ = build_grover_circuit(problem, iterations=iterations, fixed_bits=fixed, phase_mode=phase_mode)
        physical = transpile(circuit, basis_gates=["u", "cx"], optimization_level=0)
        sample = backend.run(physical, shots=1, seed_simulator=seed + 1009 * attempt).result().get_counts()
        candidate = int(next(iter(sample)), 2)
        result.circuit_builds += 1
        result.circuit_executions += 1
        result.state_preparations += 1
        result.measurements += 1
        result.verification_calls += 1
        result.gate_count_total += sum(physical.count_ops().values())
        result.circuit_depth_total += physical.depth()
        result.circuit_depth_max = max(result.circuit_depth_max, physical.depth())
        if phase_mode == "predicate":
            result.quantum_oracle_calls += iterations
        else:
            clause_calls += iterations * len(problem.clauses)
        if problem.evaluate(candidate):
            result.candidate = candidate
            result.success = True
            break
        m = min(1.4 * m, sqrt(search_size))
    result.elapsed_s = perf_counter() - start
    return {
        **result.as_record(),
        "proved_unsat_by_preprocessing": False,
        "fixed_variables": len(fixed),
        "clause_phase_calls": clause_calls,
        "preprocessing": asdict(work),
        "phase_mode": phase_mode,
    }


def _cases() -> dict[str, CNFProblem]:
    return {
        "unique_handover": CNFProblem(3, ((1, 2), (-2, 3), (-1,), (3,))),
        "unique_no_units": CNFProblem(3, ((1, 2), (-1, 2), (1, -2), (-1, 3))),
        "multiple": CNFProblem(3, ((1, 2), (-1, 3))),
        "zero_units": CNFProblem(3, ((1,), (-1,))),
        "zero_no_units": CNFProblem(2, ((1, 2), (1, -2), (-1, 2), (-1, -2))),
    }


def run_sat_benchmark(
    output_dir: Path, *, seed: int = 20261125, trials: int = 4, max_attempts: int = 12
) -> dict:
    if trials < 1 or max_attempts < 1:
        raise ValueError("trials and attempt budget must be positive")
    output_dir.mkdir(parents=True, exist_ok=True)
    cases = []
    for index, (name, problem) in enumerate(_cases().items()):
        # Offline audit is used only to label outcomes, never to build or tune a circuit.
        audit_solutions = [x for x in range(2**problem.n) if problem.evaluate(x)]
        exhaustive = classical_exhaustive(problem)
        dpll = dpll_search(problem)
        quantum = []
        for trial in range(trials):
            run_seed = seed + 7919 * index + trial
            for label, propagate, mode in (
                ("grover_unknown", False, "predicate"),
                ("grover_with_unit_propagation", True, "predicate"),
                ("clause_parity_control", False, "clause_parity"),
            ):
                row = unknown_count_grover(
                    problem,
                    seed=run_seed,
                    max_attempts=max_attempts,
                    use_unit_propagation=propagate,
                    phase_mode=mode,
                )
                row["label"] = label
                row["trial"] = trial
                row["seed"] = run_seed
                row["solution_found"] = row["success"]
                row["unsat_proven"] = row["proved_unsat_by_preprocessing"]
                row["correct_outcome"] = row["solution_found"] if audit_solutions else row["unsat_proven"]
                row["total_logical_oracle_and_verification_calls"] = row["total_predicate_queries"] + row["clause_phase_calls"]
                quantum.append(row)
        cases.append(
            {
                "name": name,
                "n": problem.n,
                "clauses": problem.clauses,
                "audit_solution_count": len(audit_solutions),
                "audit_predicate_evaluations": 2**problem.n,
                "classical_exhaustive": exhaustive.as_record(),
                "dpll": dpll,
                "quantum": quantum,
            }
        )
    report = {
        "metadata": {
            "seed": seed,
            "trials": trials,
            "max_attempts": max_attempts,
            "oracle_source": "reversible clause circuit; no satisfying assignment embedded",
            "unknown_count_schedule": "random r in [0,ceil(m)), m starts at 1 and multiplies by 1.4 up to sqrt(remaining space)",
            "clause_parity_control": "phases odd numbers of violated clauses; not a SAT conjunction oracle",
            "zero_solution_rule": "no candidate after the shot budget is inconclusive, not a proof of UNSAT",
            "gate_basis": ["u", "cx"],
        },
        "cases": cases,
    }
    (output_dir / "phase2_sat.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    labels = [case["name"] for case in cases]
    positions = np.arange(len(cases))
    width = 0.24
    for offset, label in enumerate(("grover_unknown", "grover_with_unit_propagation", "clause_parity_control")):
        means = [np.mean([row["total_logical_oracle_and_verification_calls"] for row in case["quantum"] if row["label"] == label]) for case in cases]
        success = [np.mean([row["correct_outcome"] for row in case["quantum"] if row["label"] == label]) for case in cases]
        axes[0].bar(positions + (offset - 1) * width, means, width, label=label)
        axes[1].bar(positions + (offset - 1) * width, success, width, label=label)
    axes[0].set(ylabel="mean logical phase + verification calls", title="SAT logical call accounting")
    axes[1].set(ylabel="correct outcome fraction", title="No-candidate is not an UNSAT proof", ylim=(0, 1.05))
    for ax in axes:
        ax.set_xticks(positions, labels, rotation=25, ha="right")
        ax.grid(axis="y", alpha=0.2)
    axes[0].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(output_dir / "phase2_sat.png", dpi=160)
    plt.close(fig)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    parser.add_argument("--seed", type=int, default=20261125)
    parser.add_argument("--trials", type=int, default=4)
    parser.add_argument("--max-attempts", type=int, default=12)
    args = parser.parse_args()
    report = run_sat_benchmark(args.output_dir, seed=args.seed, trials=args.trials, max_attempts=args.max_attempts)
    for case in report["cases"]:
        print(
            f"{case['name']:18} solutions={case['audit_solution_count']} "
            f"DPLL nodes={case['dpll']['dpll_nodes']} "
            f"exhaustive calls={case['classical_exhaustive']['classical_evaluations']}"
        )
    print(f"Saved {args.output_dir / 'phase2_sat.json'} and phase2_sat.png")


if __name__ == "__main__":
    main()
