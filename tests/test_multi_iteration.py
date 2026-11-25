import json
from math import isclose

import pytest

from rcp_qi_research.interference import analytic_correct_half_probability
from rcp_qi_research.multi_iteration import (
    THRESHOLDS,
    correct_half_probability,
    run_benchmark,
    solution_probability,
    threshold_plan,
)


@pytest.mark.parametrize("n", range(2, 9))
def test_analytic_probabilities_and_v1_invariance(n):
    size = 2**n
    assert isclose(correct_half_probability(n, 0), 0.5, abs_tol=1e-12)
    assert isclose(correct_half_probability(n, 1), analytic_correct_half_probability(n), abs_tol=1e-12)
    for r in range(0, 2 * n + 1):
        solution = solution_probability(n, r)
        half = correct_half_probability(n, r)
        assert 0 <= solution <= 1 + 1e-12
        assert 0 <= half <= 1 + 1e-12
        assert isclose(half, (size - 2 + size * solution) / (2 * (size - 1)))


@pytest.mark.parametrize("method", ["partition_majority", "grover_verified"])
@pytest.mark.parametrize("threshold", THRESHOLDS)
def test_threshold_plan_accounts_for_all_calls(method, threshold):
    plan = threshold_plan(3, threshold, method)
    assert plan["achieved_accuracy"] >= threshold - 1e-12
    assert plan["phase_oracle_calls"] == plan["iterations_per_shot"] * plan["shots"]
    assert plan["total_predicate_calls"] == plan["phase_oracle_calls"] + plan["verification_calls"]
    if method == "partition_majority":
        assert plan["shots"] % 2 == 1
        assert plan["verification_calls"] == 0
    else:
        assert plan["verification_calls"] == plan["shots"]


def test_benchmark_verifies_multiple_targets_and_seeds(tmp_path):
    report = run_benchmark(tmp_path, min_n=2, max_n=3, seed=17, shots=32, sample_seeds=2)
    assert len(report["thresholds"]) == 2 * len(THRESHOLDS) * 2
    assert {row["target"] for row in report["validations"] if row["n"] == 2} == {0, 1, 2, 3}
    assert max(
        abs(row["analytic_correct_half_probability"] - row["statevector_correct_half_probability"])
        for row in report["validations"]
    ) < 1e-10
    assert max(
        abs(row["analytic_solution_probability"] - row["statevector_solution_probability"])
        for row in report["validations"]
    ) < 1e-10
    assert all(len(row["samples"]) == 2 for row in report["validations"])
    saved = json.loads((tmp_path / "phase2_multi_iteration.json").read_text(encoding="utf-8"))
    assert saved["metadata"]["seed"] == 17
    assert (tmp_path / "phase2_thresholds.csv").exists()
    assert (tmp_path / "phase2_accuracy_vs_queries.png").exists()
    assert (tmp_path / "phase2_threshold_costs.png").exists()
