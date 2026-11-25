"""Small independent audits for V5 generators and SAT self-reduction."""

import pytest

from rcp_qi_research.structural import (
    STRATEGIES,
    benchmark_cases,
    partition_pysat,
    symmetric_pairs,
    xor_chain,
)


@pytest.mark.parametrize("seed", [3, 17, 20261126])
def test_xor_chain_solution_promises(seed: int) -> None:
    for variant, expected in (("unique", 1), ("multiple", 4), ("zero", 0)):
        problem = xor_chain(6, seed=seed, variant=variant)
        assert sum(problem.evaluate(x) for x in range(1 << problem.n)) == expected


def test_symmetric_pair_swap_invariance() -> None:
    problem = symmetric_pairs(2)
    for candidate in range(1 << problem.n):
        swapped = candidate ^ ((candidate & 1) ^ ((candidate >> 1) & 1)) * 3
        assert problem.evaluate(candidate) == problem.evaluate(swapped)


@pytest.mark.parametrize("seed", [5, 20261126])
def test_partition_strategies_match_exhaustive_audit(seed: int) -> None:
    for _, problem in benchmark_cases(seed).values():
        has_solution = any(problem.evaluate(x) for x in range(1 << problem.n))
        for strategy in STRATEGIES:
            row = partition_pysat(problem, strategy)
            assert row["solution_found"] == has_solution
            assert row["verified"]
            assert row["solver_calls"] == (problem.n + 1 if has_solution else 1)
