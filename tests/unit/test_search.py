import json

import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from rcp_qi_research import (
    CNFProblem,
    EqualityProblem,
    classical_exhaustive,
    grover_search,
    recursive_partition_search,
)
from rcp_qi_research.experiment import run_experiment
from rcp_qi_research.interference import analytic_correct_half_probability
from rcp_qi_research.search import build_grover_circuit


@pytest.mark.parametrize(
    "problem",
    [
        EqualityProblem(3, 5),
        CNFProblem(3, ((1,), (-1, 2), (-2, 3))),
        CNFProblem(2, ((1, 2), (-1, 2), (1, -2))),
    ],
)
def test_phase_oracle_matches_predicate_and_cleans_ancillas(problem):
    ancillas = len(problem.clauses) if isinstance(problem, CNFProblem) else 0
    for candidate in range(2**problem.n):
        circuit = QuantumCircuit(problem.n + ancillas)
        for bit in range(problem.n):
            if (candidate >> bit) & 1:
                circuit.x(bit)
        problem.phase_oracle(circuit, list(range(problem.n)))
        state = Statevector.from_instruction(circuit).data
        expected = -1 if problem.evaluate(candidate) else 1
        assert np.isclose(state[candidate], expected)
        assert np.isclose(np.linalg.norm(state), 1)


def test_partition_preparation_excludes_other_half():
    circuit, iterations = build_grover_circuit(EqualityProblem(3, 5), (1,))
    state = Statevector.from_instruction(circuit.remove_final_measurements(inplace=False))
    assert iterations == 1
    assert all(int(bits, 2) >= 4 for bits, probability in state.probabilities_dict().items() if probability > 1e-10)
    assert state.probabilities_dict()["101"] > 0.99


def test_baselines_count_real_calls_and_find_unique_solution():
    problem = EqualityProblem(3, 7)
    classical = classical_exhaustive(problem)
    grover = grover_search(problem, repetitions=3, seed=11)
    recursive = recursive_partition_search(problem, repetitions=3, seed=11)
    assert classical.success and classical.candidate == 7
    assert classical.classical_evaluations == 8
    assert grover.success and grover.candidate == 7
    assert grover.quantum_oracle_calls > 0
    assert grover.verification_calls == grover.measurements == grover.state_preparations == grover.circuit_executions
    assert recursive.success and recursive.candidate == 7
    assert recursive.circuit_builds == 3
    assert recursive.verification_calls == recursive.circuit_executions + 1
    assert recursive.gate_count_total > 0 and recursive.circuit_depth_total > 0


def test_cnf_search_uses_structured_oracle():
    problem = CNFProblem(3, ((1,), (-1, 2), (-2, 3)))
    assert [x for x in range(8) if problem.evaluate(x)] == [7]
    assert grover_search(problem, repetitions=3, seed=5).success
    assert recursive_partition_search(problem, repetitions=3, seed=5).success


def test_handover_sat_formula_has_unique_011_solution():
    problem = CNFProblem(3, ((1, 2), (-2, 3), (-1,), (3,)))
    assert [x for x in range(8) if problem.evaluate(x)] == [6]
    assert grover_search(problem, repetitions=3, seed=5).success


@pytest.mark.parametrize("n", [2, 3, 4, 5, 6])
def test_one_iteration_correct_half_formula(n):
    size = 2**n
    for target in (0, size - 1):
        circuit, iterations = build_grover_circuit(EqualityProblem(n, target), iterations=1)
        probabilities = Statevector.from_instruction(circuit.remove_final_measurements(inplace=False)).probabilities()
        correct_half = probabilities[: size // 2] if target == 0 else probabilities[size // 2 :]
        assert iterations == 1
        assert np.isclose(sum(correct_half), analytic_correct_half_probability(n))


def test_experiment_writes_serializable_resource_data(tmp_path):
    report = run_experiment(tmp_path, seed=7, trials=1, max_n=2, repetitions=2)
    saved = json.loads((tmp_path / "initial.json").read_text(encoding="utf-8"))
    assert len(saved["records"]) == len(report["records"]) == 9
    assert (tmp_path / "initial.csv").exists()
    assert (tmp_path / "scaling.png").exists()
    one_iteration = json.loads((tmp_path / "one_iteration.json").read_text(encoding="utf-8"))
    assert max(row["absolute_error"] for row in one_iteration["rows"]) < 1e-10
    assert (tmp_path / "one_iteration.png").exists()
