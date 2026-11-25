from math import isclose

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from rcp_qi_research.problems import CNFProblem
from rcp_qi_research.sat_benchmark import (
    ClassicalWork,
    _cases,
    dpll_search,
    run_sat_benchmark,
    unit_propagate,
    unknown_count_grover,
)
from rcp_qi_research.search import build_grover_circuit


def test_clause_specific_phase_matches_clause_falsification():
    problem = CNFProblem(3, ((1, -2, 3),))
    for candidate in range(8):
        circuit = QuantumCircuit(3)
        for bit in range(3):
            if (candidate >> bit) & 1:
                circuit.x(bit)
        problem.phase_unsatisfied_clause(circuit, [0, 1, 2], 0)
        amplitude = Statevector.from_instruction(circuit).data[candidate]
        expected = -1 if candidate == 2 else 1
        assert isclose(amplitude.real, expected, abs_tol=1e-10)


def test_unit_propagation_and_dpll_distinguish_sat_from_unsat():
    cases = _cases()
    assert unit_propagate(cases["unique_handover"], {}, ClassicalWork()) == {0: 0, 2: 1, 1: 1}
    assert unit_propagate(cases["zero_units"], {}, ClassicalWork()) is None
    expected_counts = {"unique_handover": 1, "unique_no_units": 1, "multiple": 4, "zero_units": 0, "zero_no_units": 0}
    for name, problem in cases.items():
        actual = sum(problem.evaluate(candidate) for candidate in range(2**problem.n))
        assert actual == expected_counts[name]
        result = dpll_search(problem)
        if actual:
            assert result["solution_found"] and problem.evaluate(result["candidate"])
        else:
            assert result["unsat_proven"]


def test_structure_aware_preparation_and_unknown_count_accounting():
    problem = _cases()["unique_handover"]
    circuit, r = build_grover_circuit(problem, fixed_bits={0: 0, 2: 1}, iterations=0)
    state = Statevector.from_instruction(circuit.remove_final_measurements(inplace=False))
    assert r == 0
    assert all((int(bits, 2) & 0b101) == 0b100 for bits, p in state.probabilities_dict().items() if p > 1e-10)
    result = unknown_count_grover(problem, seed=7, use_unit_propagation=True)
    assert result["success"] and result["candidate"] == 6
    assert result["fixed_variables"] == 3
    assert result["circuit_executions"] == 0
    assert result["preprocessing"]["literal_checks"] > 0


def test_sat_benchmark_reports_inconclusive_zero_solution_search(tmp_path):
    report = run_sat_benchmark(tmp_path, seed=3, trials=1, max_attempts=3)
    assert (tmp_path / "phase2_sat.json").exists()
    assert (tmp_path / "phase2_sat.png").exists()
    zero = next(case for case in report["cases"] if case["name"] == "zero_no_units")
    assert zero["dpll"]["unsat_proven"]
    for run in zero["quantum"]:
        assert not run["correct_outcome"]
        assert not run["unsat_proven"]
        assert run["total_logical_oracle_and_verification_calls"] == run["total_predicate_queries"] + run["clause_phase_calls"]
