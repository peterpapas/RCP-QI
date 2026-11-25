import json

from rcp_qi_research.adaptive_recursive import (
    adaptive_recursive_search,
    repetitions_for_confidence,
    run_recursive_benchmark,
)
from rcp_qi_research.problems import CNFProblem, EqualityProblem


def test_confidence_budget_and_successful_recursive_run():
    assert repetitions_for_confidence(0.5, 0.95, 3) == 6
    result = adaptive_recursive_search(EqualityProblem(3, 7), confidence=0.95, max_restarts=2, seed=4)
    assert result["success"] and result["candidate"] == 7
    assert result["runs_used"] == 1 and result["failed_runs"] == 0
    assert result["worst_case_union_miss_bound_per_run"] <= 0.05 + 1e-12
    assert result["verification_calls"] == result["circuit_executions"] + 1
    assert len(result["run_records"][0]["decisions"]) == 3


def test_failed_runs_restarts_and_costs_are_retained():
    impossible = CNFProblem(2, ((1,), (-1,)))
    result = adaptive_recursive_search(impossible, confidence=0.9, max_restarts=2, seed=1)
    assert not result["success"]
    assert result["candidate"] is None
    assert result["runs_used"] == 3 and result["failed_runs"] == 3
    assert result["restarts_used"] == 2
    assert result["verification_calls"] == result["circuit_executions"] + 3
    assert result["quantum_oracle_calls"] > 0


def test_recursive_benchmark_audits_decisions_without_using_target(tmp_path):
    report = run_recursive_benchmark(
        tmp_path, min_n=2, max_n=2, seed=5, trials=1, max_restarts=1, confidences=(0.9,)
    )
    assert (tmp_path / "phase2_recursive.json").exists()
    assert (tmp_path / "phase2_recursive_accuracy.png").exists()
    assert {row["algorithm"] for row in report["records"]} == {"adaptive_rcp_qi", "grover_with_confidence"}
    saved = json.loads((tmp_path / "phase2_recursive.json").read_text(encoding="utf-8"))
    assert len(saved["records"]) == len(report["records"])
    for row in report["records"]:
        if row["algorithm"] == "adaptive_rcp_qi":
            assert row["audited_decisions"] > 0
            assert row["total_predicate_queries"] == row["quantum_oracle_calls"] + row["verification_calls"]
    assert all(0 <= row["success_probability_empirical"] <= 1 for row in report["summary"])
