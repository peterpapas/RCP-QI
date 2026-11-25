"""Matched classical baselines and bounded partition traversal for V5.1."""

from __future__ import annotations

import hashlib
from itertools import pairwise
from time import perf_counter

from pysat.solvers import Solver

from .problems import CNFProblem
from .sat_benchmark import dpll_search
from .structural import STRATEGIES, SelectionWork, _swap_symmetry, choose_variable
from .v51_generators import Instance

METHODS = ("direct_g4", "direct_cadical", "dpll", "xor_gauss", "two_sat_scc", "symmetry_break", *STRATEGIES)


def _model_candidate(model: list[int], n: int) -> int:
    return sum(1 << (lit - 1) for lit in model if 0 < lit <= n)


def _candidate_record(problem: CNFProblem, candidate: int | None) -> dict:
    if candidate is None:
        return {"witness_verified": None, "witness_sha256": None}
    payload = candidate.to_bytes((problem.n + 7) // 8, "little")
    return {"witness_verified": problem.evaluate(candidate), "witness_sha256": hashlib.sha256(payload).hexdigest()}


def direct_cdcl(instance: Instance, solver_name: str, extra_clauses: tuple[tuple[int, ...], ...] = ()) -> dict:
    start = perf_counter()
    problem = instance.problem
    with Solver(name=solver_name, bootstrap_with=(*problem.clauses, *extra_clauses)) as solver:
        construction_s = perf_counter() - start
        before = perf_counter()
        sat = solver.solve()
        solve_s = perf_counter() - before
        candidate = _model_candidate(solver.get_model(), problem.n) if sat else None
        stats = solver.accum_stats()
    return {"status": "sat" if sat else "unsat", "solver": solver_name, "solver_calls": 1, "construction_s": construction_s, "solve_s": solve_s, "elapsed_s": perf_counter() - start, "solver_stats": stats, "partition_depth": 0, "search_space_reduction_log2": 0, **_candidate_record(problem, candidate)}


def partition_cdcl(instance: Instance, strategy: str, *, max_depth: int | None = None) -> dict:
    if strategy not in STRATEGIES:
        raise ValueError(strategy)
    problem = instance.problem
    limit = min(problem.n, max_depth if max_depth is not None else problem.n)
    start = perf_counter()
    work = SelectionWork()
    with Solver(name="g4", bootstrap_with=problem.clauses) as solver:
        construction_s = perf_counter() - start
        solver_s = 0.0
        calls = 0

        def ask(assumptions: list[int]) -> bool:
            nonlocal solver_s, calls
            before = perf_counter()
            result = solver.solve(assumptions=assumptions)
            solver_s += perf_counter() - before
            calls += 1
            return result

        sat = ask([])
        assignment: dict[int, int] = {}
        if sat:
            while len(assignment) < limit:
                bit = choose_variable(problem, assignment, strategy, work)
                prefix = [v + 1 if assignment[v] else -(v + 1) for v in assignment]
                branch_sat = ask([*prefix, -(bit + 1)])
                assignment[bit] = 0 if branch_sat else 1
        stats = solver.accum_stats()
    if not sat:
        status = "unsat"
        candidate = None
    elif len(assignment) == problem.n:
        status = "sat"
        candidate = sum(value << bit for bit, value in assignment.items())
    else:
        status = "partial"
        candidate = None
    return {"status": status, "solver": "g4", "solver_calls": calls, "construction_s": construction_s, "solve_s": solver_s, "scoring_s": work.scoring_s, "scoring_literal_visits": work.residual_literal_visits + work.propagation_literal_checks, "symmetry_clause_scans": work.symmetry_clause_scans, "propagation_assignments": work.propagation_assignments, "elapsed_s": perf_counter() - start, "solver_stats": stats, "partition_depth": len(assignment), "search_space_reduction_log2": len(assignment), **_candidate_record(problem, candidate)}


def xor_gauss(instance: Instance) -> dict:
    """GF(2) elimination on the original parity equations, not the CNF expansion."""
    if not instance.xor_equations:
        raise ValueError("XOR equations are unavailable")
    start = perf_counter()
    basis: dict[int, tuple[int, int, int]] = {}
    xor_steps = 0
    inconsistent = False
    certificate: list[int] = []
    for equation_index, (mask, rhs) in enumerate(instance.xor_equations):
        provenance = 1 << equation_index
        while mask:
            pivot = mask.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = (mask, rhs, provenance)
                break
            row, value, row_provenance = basis[pivot]
            mask ^= row
            rhs ^= value
            provenance ^= row_provenance
            xor_steps += 1
        if mask == 0 and rhs:
            inconsistent = True
            certificate = [i for i in range(len(instance.xor_equations)) if (provenance >> i) & 1]
            break
    candidate = None
    if not inconsistent:
        candidate = 0
        for pivot in sorted(basis):
            mask, rhs, _ = basis[pivot]
            parity = ((mask & candidate).bit_count() & 1)
            if parity ^ rhs:
                candidate |= 1 << pivot
    check_mask = 0
    check_rhs = 0
    for index in certificate:
        mask, rhs = instance.xor_equations[index]
        check_mask ^= mask
        check_rhs ^= rhs
    certificate_checked = (check_mask == 0 and check_rhs == 1) if inconsistent else None
    return {"status": "unsat" if inconsistent else "sat", "solver": "GF2 elimination", "solver_calls": 0, "xor_steps": xor_steps, "rank": len(basis), "unsat_certificate_equation_indices": certificate if inconsistent else None, "unsat_certificate_checked": certificate_checked, "elapsed_s": perf_counter() - start, "partition_depth": 0, "search_space_reduction_log2": 0, **_candidate_record(instance.problem, candidate)}


def two_sat_scc(instance: Instance) -> dict:
    """Kosaraju implication-graph solver, O(n+m), with a checked witness."""
    problem = instance.problem
    if any(len(clause) > 2 for clause in problem.clauses):
        raise ValueError("not a 2-CNF")
    start = perf_counter()
    graph = [[] for _ in range(2 * problem.n)]
    reverse = [[] for _ in range(2 * problem.n)]

    def node(lit: int) -> int:
        return 2 * (abs(lit) - 1) + int(lit < 0)

    for clause in problem.clauses:
        a = clause[0]
        b = clause[-1]
        for src, dst in ((node(-a), node(b)), (node(-b), node(a))):
            graph[src].append(dst)
            reverse[dst].append(src)
    seen = [False] * len(graph)
    order = []
    for root in range(len(graph)):
        if seen[root]:
            continue
        seen[root] = True
        stack = [(root, 0)]
        while stack:
            v, index = stack[-1]
            if index < len(graph[v]):
                nxt = graph[v][index]
                stack[-1] = (v, index + 1)
                if not seen[nxt]:
                    seen[nxt] = True
                    stack.append((nxt, 0))
            else:
                order.append(v)
                stack.pop()
    comp = [-1] * len(graph)
    count = 0
    for root in reversed(order):
        if comp[root] != -1:
            continue
        stack = [root]
        comp[root] = count
        while stack:
            v = stack.pop()
            for nxt in reverse[v]:
                if comp[nxt] == -1:
                    comp[nxt] = count
                    stack.append(nxt)
        count += 1
    conflict_variable = next((i for i in range(problem.n) if comp[2 * i] == comp[2 * i + 1]), None)
    inconsistent = conflict_variable is not None
    candidate = None if inconsistent else sum(1 << i for i in range(problem.n) if comp[2 * i] > comp[2 * i + 1])

    def implication_path(source: int, target: int) -> list[int]:
        queue = [source]
        parent = {source: None}
        for current in queue:
            if current == target:
                break
            for nxt in graph[current]:
                if nxt not in parent:
                    parent[nxt] = current
                    queue.append(nxt)
        if target not in parent:
            raise AssertionError("SCC conflict lacks implication path")
        path = []
        current = target
        while current is not None:
            path.append(current)
            current = parent[current]
        return list(reversed(path))

    paths = None
    checked = None
    if conflict_variable is not None:
        positive, negative = 2 * conflict_variable, 2 * conflict_variable + 1
        paths = [implication_path(positive, negative), implication_path(negative, positive)]
        checked = all(all(b in graph[a] for a, b in pairwise(path)) for path in paths)
        checked = checked and paths[0][0] == positive and paths[0][-1] == negative and paths[1][0] == negative and paths[1][-1] == positive
    return {"status": "unsat" if inconsistent else "sat", "solver": "2SAT SCC", "solver_calls": 0, "implication_edges": sum(map(len, graph)), "components": count, "unsat_certificate_paths": paths, "unsat_certificate_checked": checked, "elapsed_s": perf_counter() - start, "partition_depth": 0, "search_space_reduction_log2": 0, **_candidate_record(problem, candidate)}


def symmetry_break(instance: Instance) -> dict:
    """Certify supplied swaps, then impose x_a <= x_b for each independent pair."""
    if not instance.symmetric_pairs:
        raise ValueError("no supplied symmetry generators")
    start = perf_counter()
    for a, b in instance.symmetric_pairs:
        if not _swap_symmetry(instance.problem, a, b):
            raise ValueError("uncertified variable swap")
    preparation_s = perf_counter() - start
    clauses = tuple((-(a + 1), b + 1) for a, b in instance.symmetric_pairs)
    result = direct_cdcl(instance, "g4", clauses)
    result["preprocessing_s"] = preparation_s
    result["certified_swaps"] = len(clauses)
    result["elapsed_s"] += preparation_s
    return result


def execute(instance: Instance, method: str, *, max_depth: int | None = None) -> dict:
    if method == "direct_g4":
        return direct_cdcl(instance, "g4")
    if method == "direct_cadical":
        return direct_cdcl(instance, "cadical195")
    if method == "dpll":
        row = dpll_search(instance.problem)
        return {"status": "sat" if row["solution_found"] else "unsat", "solver": "simple DPLL", "solver_calls": 0, "elapsed_s": row["elapsed_s"], "dpll_nodes": row["dpll_nodes"], "dpll_branches": row["dpll_branches"], "literal_checks": row["literal_checks"], "partition_depth": 0, "search_space_reduction_log2": 0, **_candidate_record(instance.problem, row["candidate"])}
    if method == "xor_gauss":
        return xor_gauss(instance)
    if method == "two_sat_scc":
        return two_sat_scc(instance)
    if method == "symmetry_break":
        return symmetry_break(instance)
    if method in STRATEGIES:
        return partition_cdcl(instance, method, max_depth=max_depth)
    raise ValueError(method)
