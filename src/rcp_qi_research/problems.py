"""Classical predicates and their explicit reversible phase-oracle circuits."""

from dataclasses import dataclass
from typing import Protocol

from qiskit import QuantumCircuit


class SearchProblem(Protocol):
    n: int

    def evaluate(self, candidate: int) -> bool: ...

    def phase_oracle(self, circuit: QuantumCircuit, data: list[int]) -> None: ...


def _phase_on_all_ones(circuit: QuantumCircuit, controls: list[int]) -> None:
    if len(controls) == 1:
        circuit.z(controls[0])
    else:
        circuit.h(controls[-1])
        circuit.mcx(controls[:-1], controls[-1])
        circuit.h(controls[-1])


@dataclass(frozen=True)
class EqualityProblem:
    n: int
    target: int

    def __post_init__(self) -> None:
        if self.n < 1 or not 0 <= self.target < 2**self.n:
            raise ValueError("target must fit in at least one qubit")

    def evaluate(self, candidate: int) -> bool:
        return candidate == self.target

    def phase_oracle(self, circuit: QuantumCircuit, data: list[int]) -> None:
        zero_bits = [data[i] for i in range(self.n) if not (self.target >> i) & 1]
        for qubit in zero_bits:
            circuit.x(qubit)
        _phase_on_all_ones(circuit, data)
        for qubit in reversed(zero_bits):
            circuit.x(qubit)


@dataclass(frozen=True)
class CNFProblem:
    """DIMACS-style signed literals; each clause gets a clean work qubit."""

    n: int
    clauses: tuple[tuple[int, ...], ...]

    def __post_init__(self) -> None:
        if self.n < 1 or not self.clauses or any(not clause for clause in self.clauses):
            raise ValueError("CNF needs variables and nonempty clauses")
        for clause in self.clauses:
            if any(lit == 0 or abs(lit) > self.n for lit in clause):
                raise ValueError("literal index outside variable range")
            if len({abs(lit) for lit in clause}) != len(clause):
                raise ValueError("a variable may occur only once per clause")

    def evaluate(self, candidate: int) -> bool:
        return all(
            any(bool((candidate >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause)
            for clause in self.clauses
        )

    def phase_unsatisfied_clause(self, circuit: QuantumCircuit, data: list[int], clause_index: int) -> None:
        """Flip phase when one clause is false; no solution list is used."""
        clause = self.clauses[clause_index]
        positive = [data[lit - 1] for lit in clause if lit > 0]
        for qubit in positive:
            circuit.x(qubit)
        _phase_on_all_ones(circuit, [data[abs(lit) - 1] for lit in clause])
        for qubit in reversed(positive):
            circuit.x(qubit)

    def phase_oracle(self, circuit: QuantumCircuit, data: list[int]) -> None:
        work = list(range(self.n, self.n + len(self.clauses)))

        def compute_clause(clause: tuple[int, ...], ancilla: int) -> None:
            # Start at 1; toggle to 0 only on the unique falsifying assignment.
            circuit.x(ancilla)
            positive = [data[lit - 1] for lit in clause if lit > 0]
            for qubit in positive:
                circuit.x(qubit)
            controls = [data[abs(lit) - 1] for lit in clause]
            circuit.mcx(controls, ancilla)
            for qubit in reversed(positive):
                circuit.x(qubit)

        for clause, ancilla in zip(self.clauses, work, strict=True):
            compute_clause(clause, ancilla)
        _phase_on_all_ones(circuit, work)
        for clause, ancilla in reversed(list(zip(self.clauses, work, strict=True))):
            # Reversible uncomputation restores every work qubit to |0>.
            compute_clause(clause, ancilla)
