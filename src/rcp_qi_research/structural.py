"""Deterministic SAT families and costed classical partition selectors for V5.

These selectors use classical formula structure. PySAT answers each existence
question; its calls must never be described as quantum partition oracles.
"""

from __future__ import annotations

import argparse
import json
import platform
from dataclasses import asdict, dataclass
from importlib.metadata import version
from itertools import combinations, product
from pathlib import Path
from time import perf_counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pysat.solvers import Solver

from .problems import CNFProblem
from .sat_benchmark import ClassicalWork, dpll_search, unit_propagate


def xor_constraint(variables: tuple[int, ...], parity: int) -> list[tuple[int, ...]]:
    """CNF excludes exactly the assignments with the wrong XOR parity."""
    return [
        tuple(-var if bit else var for var, bit in zip(variables, bits, strict=True))
        for bits in product((0, 1), repeat=len(variables))
        if sum(bits) % 2 != parity
    ]


def xor_chain(n: int, *, seed: int, variant: str) -> CNFProblem:
    if n < 3 or variant not in {"unique", "multiple", "zero"}:
        raise ValueError("invalid XOR chain")
    rng = np.random.default_rng(seed)
    hidden = [int(x) for x in rng.integers(0, 2, size=n)]
    clauses: list[tuple[int, ...]] = []
    for i in range(n - 2):
        variables = (i + 1, i + 2, i + 3)
        clauses.extend(xor_constraint(variables, sum(hidden[i : i + 3]) % 2))
    if variant != "multiple":
        clauses.extend((i + 1 if hidden[i] else -(i + 1),) for i in range(2))
    if variant == "zero":
        clauses.extend(xor_constraint((1, 2, 3), 1 - sum(hidden[:3]) % 2))
    return CNFProblem(n, tuple(clauses))


def two_sat_chain(n: int, *, variant: str) -> CNFProblem:
    if n < 2 or variant not in {"unique", "multiple", "zero"}:
        raise ValueError("invalid 2-SAT chain")
    clauses = [(-i, i + 1) for i in range(1, n)]
    if variant != "multiple":
        clauses.append((1,))
    if variant == "zero":
        clauses.append((-n,))
    return CNFProblem(n, tuple(clauses))


def random_three_sat(n: int, m: int, *, seed: int, planted: bool) -> CNFProblem:
    if n < 3 or m < 1:
        raise ValueError("3-SAT needs at least three variables and one clause")
    rng = np.random.default_rng(seed)
    hidden = [int(x) for x in rng.integers(0, 2, size=n)] if planted else None
    clauses: list[tuple[int, ...]] = []
    for _ in range(m):
        variables = sorted(int(v) for v in rng.choice(np.arange(1, n + 1), size=3, replace=False))
        while True:
            signs = [int(x) for x in rng.integers(0, 2, size=3)]
            clause = tuple(var if sign else -var for var, sign in zip(variables, signs, strict=True))
            if hidden is None or any((lit > 0) == bool(hidden[abs(lit) - 1]) for lit in clause):
                clauses.append(clause)
                break
    return CNFProblem(n, tuple(clauses))


def graph_coloring(vertices: int, colors: int, edges: tuple[tuple[int, int], ...]) -> CNFProblem:
    if vertices < 1 or colors < 2:
        raise ValueError("invalid coloring dimensions")
    clauses: list[tuple[int, ...]] = []
    for v in range(vertices):
        choices = tuple(v * colors + color + 1 for color in range(colors))
        clauses.append(choices)
        clauses.extend((-a, -b) for a, b in combinations(choices, 2))
    for u, v in edges:
        if not 0 <= u < v < vertices:
            raise ValueError("edges must use ordered distinct vertices")
        clauses.extend((-(u * colors + c + 1), -(v * colors + c + 1)) for c in range(colors))
    return CNFProblem(vertices * colors, tuple(clauses))


def symmetric_pairs(pairs: int) -> CNFProblem:
    if pairs < 1:
        raise ValueError("need at least one pair")
    clauses = []
    for i in range(pairs):
        a, b = 2 * i + 1, 2 * i + 2
        clauses.extend(((a, b), (-a, -b)))
    return CNFProblem(2 * pairs, tuple(clauses))


def benchmark_cases(seed: int) -> dict[str, tuple[str, CNFProblem]]:
    return {
        "xor_unique": ("XOR-SAT", xor_chain(6, seed=seed, variant="unique")),
        "xor_multiple": ("XOR-SAT", xor_chain(6, seed=seed, variant="multiple")),
        "xor_zero": ("XOR-SAT", xor_chain(6, seed=seed, variant="zero")),
        "two_sat_unique": ("2-SAT", two_sat_chain(8, variant="unique")),
        "two_sat_multiple": ("2-SAT", two_sat_chain(8, variant="multiple")),
        "two_sat_zero": ("2-SAT", two_sat_chain(8, variant="zero")),
        "planted_3sat": ("planted 3-SAT", random_three_sat(8, 34, seed=seed + 1, planted=True)),
        "random_3sat": ("random 3-SAT", random_three_sat(8, 34, seed=seed + 2, planted=False)),
        "color_triangle": ("3-coloring", graph_coloring(3, 3, ((0, 1), (0, 2), (1, 2)))),
        "color_k4_zero": ("3-coloring", graph_coloring(4, 3, tuple(combinations(range(4), 2)))),
        "symmetric": ("symmetric CNF", symmetric_pairs(4)),
    }


def _residual(problem: CNFProblem, assignment: dict[int, int]) -> tuple[list[tuple[int, ...]], int]:
    remaining = []
    visits = 0
    for clause in problem.clauses:
        satisfied = False
        for lit in clause:
            visits += 1
            if abs(lit) - 1 in assignment and bool(assignment[abs(lit) - 1]) == (lit > 0):
                satisfied = True
                break
        if satisfied:
            continue
        residual = []
        for lit in clause:
            visits += 1
            if abs(lit) - 1 not in assignment:
                residual.append(lit)
        remaining.append(tuple(residual))
    return remaining, visits


def _swap_symmetry(problem: CNFProblem, a: int, b: int) -> bool:
    """Exact signed-variable swap test on a CNF clause multiset."""
    def swapped(lit: int) -> int:
        v = abs(lit) - 1
        return (1 if lit > 0 else -1) * (b + 1 if v == a else a + 1 if v == b else v + 1)

    normalized = sorted(tuple(sorted(clause)) for clause in problem.clauses)
    transformed = sorted(tuple(sorted(swapped(lit) for lit in clause)) for clause in problem.clauses)
    return normalized == transformed


@dataclass
class SelectionWork:
    scoring_s: float = 0.0
    residual_literal_visits: int = 0
    propagation_literal_checks: int = 0
    propagation_assignments: int = 0
    symmetry_clause_scans: int = 0


def choose_variable(problem: CNFProblem, assignment: dict[int, int], strategy: str, work: SelectionWork) -> int:
    start = perf_counter()
    free = [i for i in range(problem.n) if i not in assignment]
    if not free:
        raise ValueError("no free variables")
    if strategy == "prefix":
        chosen = free[0]
    elif strategy == "symmetry":
        scores = {v: 0 for v in free}
        for a, b in combinations(free, 2):
            work.symmetry_clause_scans += 2 * len(problem.clauses)
            if _swap_symmetry(problem, a, b):
                scores[a] += 1
                scores[b] += 1
        chosen = max(free, key=lambda v: (scores[v], -v))
    elif strategy == "propagation":
        scores = {}
        for v in free:
            effects = []
            for value in (0, 1):
                probe = ClassicalWork()
                result = unit_propagate(problem, {**assignment, v: value}, probe)
                work.propagation_literal_checks += probe.literal_checks
                work.propagation_assignments += probe.propagation_assignments
                effects.append(problem.n + 1 if result is None else len(result) - len(assignment))
            scores[v] = min(effects)
        chosen = max(free, key=lambda v: (scores[v], -v))
    elif strategy in {"occurrence", "connectivity", "residual", "jeroslow_wang"}:
        clauses, visits = _residual(problem, assignment)
        work.residual_literal_visits += visits + sum(len(c) for c in clauses)
        scores = {v: 0.0 for v in free}
        for clause in clauses:
            for lit in clause:
                v = abs(lit) - 1
                if strategy == "connectivity":
                    scores[v] += len(clause) - 1
                elif strategy == "jeroslow_wang":
                    scores[v] += 2.0 ** -len(clause)
                elif strategy == "residual":
                    scores[v] += 1.0 / len(clause)
                else:
                    scores[v] += 1
        chosen = max(free, key=lambda v: (scores[v], -v))
    else:
        raise ValueError(f"unknown strategy: {strategy}")
    work.scoring_s += perf_counter() - start
    return chosen


STRATEGIES = ("prefix", "occurrence", "connectivity", "propagation", "symmetry", "residual", "jeroslow_wang")


def direct_pysat(problem: CNFProblem) -> dict:
    start = perf_counter()
    with Solver(name="g4", bootstrap_with=problem.clauses) as solver:
        build_s = perf_counter() - start
        solve_start = perf_counter()
        exists = solver.solve()
        solve_s = perf_counter() - solve_start
        model = solver.get_model() if exists else None
        candidate = sum(1 << (abs(lit) - 1) for lit in model if lit > 0 and abs(lit) <= problem.n) if model else None
        stats = solver.accum_stats()
    return {"solution_found": exists, "candidate": candidate, "solver_calls": 1, "construction_s": build_s, "solver_s": solve_s, "elapsed_s": perf_counter() - start, "solver_stats": stats, "verified": candidate is None or problem.evaluate(candidate)}


def partition_pysat(problem: CNFProblem, strategy: str) -> dict:
    """Classical SAT self-reduction with explicit existence calls and scoring work."""
    start = perf_counter()
    work = SelectionWork()
    with Solver(name="g4", bootstrap_with=problem.clauses) as solver:
        construction_s = perf_counter() - start
        solver_s = 0.0
        calls = 0

        def ask(assumptions: list[int]) -> bool:
            nonlocal calls, solver_s
            before = perf_counter()
            answer = solver.solve(assumptions=assumptions)
            solver_s += perf_counter() - before
            calls += 1
            return answer

        exists = ask([])
        assignment: dict[int, int] = {}
        if exists:
            while len(assignment) < problem.n:
                v = choose_variable(problem, assignment, strategy, work)
                assumptions = [i + 1 if assignment[i] else -(i + 1) for i in sorted(assignment)]
                keep_zero = ask([*assumptions, -(v + 1)])
                assignment[v] = 0 if keep_zero else 1
        candidate = sum(value << bit for bit, value in assignment.items()) if exists else None
        stats = solver.accum_stats()
    verified = candidate is None or problem.evaluate(candidate)
    return {"strategy": strategy, "solution_found": exists, "candidate": candidate, "verified": verified, "solver_calls": calls, "construction_s": construction_s, "solver_s": solver_s, "scoring": asdict(work), "solver_stats": stats, "elapsed_s": perf_counter() - start, "verification_calls": int(exists)}


def run_structural_benchmark(output_dir: Path, *, seed: int = 20261126, seed_count: int = 3) -> dict:
    if seed_count < 1:
        raise ValueError("seed_count must be positive")
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for run_seed in range(seed, seed + seed_count):
        for name, (family, problem) in benchmark_cases(run_seed).items():
            audit = sum(problem.evaluate(x) for x in range(1 << problem.n))
            direct = direct_pysat(problem)
            dpll = dpll_search(problem)
            strategies = [partition_pysat(problem, strategy) for strategy in STRATEGIES]
            if not direct["verified"] or any(not row["verified"] or row["solution_found"] != bool(audit) for row in strategies):
                raise AssertionError(f"incorrect outcome on {name} seed={run_seed}")
            rows.append({"name": name, "family": family, "seed": run_seed, "n": problem.n, "clauses": len(problem.clauses), "audit_solution_count": audit, "audit_predicate_evaluations": 1 << problem.n, "direct_pysat": direct, "dpll": dpll, "partition_strategies": strategies})
    report = {"metadata": {"seed": seed, "seed_count": seed_count, "python_version": platform.python_version(), "python_sat_version": version("python-sat"), "numpy_version": np.__version__, "solver": "PySAT Glucose4", "oracle": "classical PySAT solve under assumptions", "quantum_operator": None, "quantum_oracle_calls": 0, "cost_scope": "SAT calls, solver internal stats, scorer scans and propagation, construction and wall time; audit counts excluded from algorithm costs", "plot_scope": "first seed only; all seeds retained in JSON"}, "cases": rows}
    (output_dir / "phase2_structural.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    plotted = rows[: len(benchmark_cases(seed))]
    fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True)
    x = np.arange(len(plotted))
    width = 0.11
    for i, strategy in enumerate(("direct", *STRATEGIES)):
        selected = [case["direct_pysat"] if strategy == "direct" else next(row for row in case["partition_strategies"] if row["strategy"] == strategy) for case in plotted]
        for ax, key in zip(axes, ("solver_calls", "decisions"), strict=True):
            values = [row["solver_calls"] if key == "solver_calls" else row["solver_stats"]["decisions"] for row in selected]
            ax.bar(x + (i - 3.5) * width, values, width, label=strategy)
    axes[0].set(ylabel="classical SAT existence calls", title="V5 first seed: direct solver vs partition self-reduction")
    axes[1].set(ylabel="Glucose4 internal decisions (all SAT calls)")
    axes[1].set_xticks(x, [row["name"] for row in plotted], rotation=35, ha="right")
    axes[0].legend(ncol=4, fontsize=8)
    for ax in axes:
        ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    fig.savefig(output_dir / "phase2_structural.png", dpi=160)
    plt.close(fig)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    parser.add_argument("--seed", type=int, default=20261126)
    parser.add_argument("--seed-count", type=int, default=3)
    args = parser.parse_args()
    report = run_structural_benchmark(args.output_dir, seed=args.seed, seed_count=args.seed_count)
    for case in report["cases"]:
        print(f"{case['name']:20} solutions={case['audit_solution_count']:3} direct decisions={case['direct_pysat']['solver_stats']['decisions']:4}")
    print(f"Saved {args.output_dir / 'phase2_structural.json'}")


if __name__ == "__main__":
    main()
