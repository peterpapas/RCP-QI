"""Regression controls for the post-publication partial-search correction."""

from math import isclose, pi, sqrt

import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from rcp_qi_research.partial_search import (
    Schedule,
    analytic_probabilities,
    apply_global_diffusion,
    apply_intra_block_diffusion,
    apply_partition_bit_only_reflection,
    best_schedule,
    build_partial_search_circuit,
    full_grover_half_probability,
    korepin_two_block_asymptotic_schedule,
    run_comparison,
)


def test_diffusers_target_distinct_address_subspaces() -> None:
    support = []
    for operator in (apply_partition_bit_only_reflection, apply_intra_block_diffusion, apply_global_diffusion):
        circuit = QuantumCircuit(3)
        operator(circuit, 3)
        probabilities = Statevector.from_instruction(circuit).probabilities()
        support.append(set(np.flatnonzero(probabilities > 1e-12)))
    assert support[0] == {4}  # partition bit flips, lower bits stay zero
    assert support[1] == {0, 1, 2, 3}  # independent diffusion inside marked half
    assert support[2] == set(range(8))  # global diffusion reaches both halves


@pytest.mark.parametrize("n,schedule", [(4, Schedule(0, 1)), (6, Schedule(2, 1)), (8, Schedule(0, 6))])
def test_analytic_prediction_matches_circuits_for_multiple_targets(n: int, schedule: Schedule) -> None:
    size = 2**n
    expected_half, expected_solution = analytic_probabilities(n, schedule)
    for target in sorted({0, 1, size // 2 - 1, size // 2, size - 1}):
        circuit = build_partial_search_circuit(n, target, schedule)
        probabilities = Statevector.from_instruction(circuit).probabilities()
        begin = (target // (size // 2)) * (size // 2)
        assert isclose(sum(probabilities[begin:begin + size // 2]), expected_half, abs_tol=1e-11)
        assert isclose(probabilities[target], expected_solution, abs_tol=1e-11)
        measured = build_partial_search_circuit(n, target, schedule, measure_partition=True)
        assert measured.count_ops()["measure"] == 1
        assert schedule.phase_oracle_calls == schedule.global_before + schedule.local + 1


@pytest.mark.parametrize("threshold,partial_calls,v2_calls", [(0.90, 7, 9), (0.95, 8, 10), (0.99, 9, 11)])
def test_n256_thresholds_are_minimal_in_stated_schedule_family(
    threshold: float, partial_calls: int, v2_calls: int
) -> None:
    schedule, probability = best_schedule(8, threshold)
    assert schedule.phase_oracle_calls == partial_calls
    assert probability >= threshold
    assert all(
        analytic_probabilities(8, Schedule(g, q - 1 - g))[0] < threshold
        for q in range(1, partial_calls)
        for g in range(q)
    )
    assert next(r for r in range(20) if full_grover_half_probability(8, r) >= threshold) == v2_calls


def test_published_two_block_large_block_schedule_and_validation() -> None:
    schedule = korepin_two_block_asymptotic_schedule(12)
    assert schedule.global_before == 0
    assert schedule.local == int(pi * sqrt(2**11) / 4 + 0.5)
    with pytest.raises(ValueError):
        build_partial_search_circuit(4, 16, Schedule(0, 1))
    with pytest.raises(ValueError):
        best_schedule(8, 1.0)


def test_new_artifact_is_reproducible_and_not_overwritten(tmp_path) -> None:
    output = tmp_path / "correction"
    report = run_comparison(output, sizes=(4,))
    assert len(report["rows"]) == 15
    assert (output / "partial_search.json").exists()
    assert (output / "thresholds.csv").exists()
    assert (output / "accuracy_vs_queries.png").exists()
    assert max(abs(row["partition_probability_analytic"] - row["partition_probability_statevector"])
               for row in report["rows"]) < 1e-11
    with pytest.raises(FileExistsError):
        run_comparison(output, sizes=(4,))
