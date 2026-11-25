"""Three search baselines with explicit per-execution resource accounting."""

from dataclasses import asdict, dataclass
from math import asin, pi, sqrt
from time import perf_counter

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

from .problems import CNFProblem, SearchProblem


@dataclass
class SearchResult:
    algorithm: str
    candidate: int | None = None
    success: bool = False
    classical_evaluations: int = 0
    quantum_oracle_calls: int = 0
    verification_calls: int = 0
    circuit_builds: int = 0
    circuit_executions: int = 0
    state_preparations: int = 0
    measurements: int = 0
    gate_count_total: int = 0
    circuit_depth_total: int = 0
    circuit_depth_max: int = 0
    elapsed_s: float = 0.0

    @property
    def total_predicate_queries(self) -> int:
        return self.classical_evaluations + self.quantum_oracle_calls + self.verification_calls

    def as_record(self) -> dict:
        return {**asdict(self), "total_predicate_queries": self.total_predicate_queries}


def classical_exhaustive(problem: SearchProblem) -> SearchResult:
    start = perf_counter()
    result = SearchResult("classical")
    for candidate in range(2**problem.n):
        result.classical_evaluations += 1
        if problem.evaluate(candidate):
            result.candidate = candidate
            result.success = True
            break
    result.elapsed_s = perf_counter() - start
    return result


def _grover_iterations(space_size: int) -> int:
    """Nearest iteration count for a promised single marked state."""
    if space_size == 1:
        return 0
    theta = asin(1 / sqrt(space_size))
    return max(0, int(pi / (4 * theta) - 0.5 + 0.5))


def _diffuse(circuit: QuantumCircuit, free: list[int]) -> None:
    for qubit in free:
        circuit.h(qubit)
        circuit.x(qubit)
    if len(free) == 1:
        circuit.z(free[0])
    else:
        circuit.h(free[-1])
        circuit.mcx(free[:-1], free[-1])
        circuit.h(free[-1])
    for qubit in reversed(free):
        circuit.x(qubit)
        circuit.h(qubit)


def build_grover_circuit(
    problem: SearchProblem, prefix: tuple[int, ...] = (), *, iterations: int | None = None
) -> tuple[QuantumCircuit, int]:
    """Build one measured shot restricted to a fixed most-significant-bit prefix."""
    if len(prefix) > problem.n or any(bit not in (0, 1) for bit in prefix):
        raise ValueError("invalid partition prefix")
    ancillas = len(problem.clauses) if isinstance(problem, CNFProblem) else 0
    circuit = QuantumCircuit(problem.n + ancillas, problem.n)
    for offset, bit in enumerate(prefix):
        if bit:
            circuit.x(problem.n - 1 - offset)
    free = list(range(problem.n - len(prefix)))
    for qubit in free:
        circuit.h(qubit)
    if iterations is None:
        iterations = _grover_iterations(2 ** len(free))
    elif iterations < 0:
        raise ValueError("iterations must be nonnegative")
    for _ in range(iterations):
        problem.phase_oracle(circuit, list(range(problem.n)))
        _diffuse(circuit, free)
    circuit.measure(list(range(problem.n)), list(range(problem.n)))
    return circuit, iterations


def _probe(
    problem: SearchProblem,
    prefix: tuple[int, ...],
    repetitions: int,
    backend: AerSimulator,
    seed: int,
    result: SearchResult,
) -> bool:
    circuit, iterations = build_grover_circuit(problem, prefix)
    physical = transpile(circuit, basis_gates=["u", "cx"], optimization_level=0)
    result.circuit_builds += 1
    gates_per_shot = sum(physical.count_ops().values())
    depth_per_shot = physical.depth()
    for attempt in range(repetitions):
        sample = backend.run(physical, shots=1, seed_simulator=seed + attempt).result().get_counts()
        candidate = int(next(iter(sample)), 2)
        result.circuit_executions += 1
        result.state_preparations += 1
        result.measurements += 1
        result.quantum_oracle_calls += iterations
        result.verification_calls += 1
        result.gate_count_total += gates_per_shot
        result.circuit_depth_total += depth_per_shot
        result.circuit_depth_max = max(result.circuit_depth_max, depth_per_shot)
        if problem.evaluate(candidate):
            result.candidate = candidate
            return True
    return False


def grover_search(problem: SearchProblem, *, repetitions: int = 3, seed: int = 0) -> SearchResult:
    if repetitions < 1:
        raise ValueError("repetitions must be positive")
    start = perf_counter()
    result = SearchResult("grover")
    backend = AerSimulator(method="statevector")
    result.success = _probe(problem, (), repetitions, backend, seed, result)
    result.elapsed_s = perf_counter() - start
    return result


def recursive_partition_search(
    problem: SearchProblem, *, repetitions: int = 3, seed: int = 0
) -> SearchResult:
    """Use measured Grover tests to choose a half, then verify the final leaf.

    A witness found during a test is discarded so this remains a partition
    traversal. This is deliberately an upper-bound cost for this hypothesis;
    the witness could instead terminate search immediately.
    """
    if repetitions < 1:
        raise ValueError("repetitions must be positive")
    start = perf_counter()
    result = SearchResult("rcp_qi")
    backend = AerSimulator(method="statevector")
    prefix: tuple[int, ...] = ()
    for level in range(problem.n):
        left = (*prefix, 0)
        found_left = _probe(problem, left, repetitions, backend, seed + 1009 * level, result)
        prefix = left if found_left else (*prefix, 1)
    candidate = int("".join(map(str, prefix)), 2)
    result.verification_calls += 1
    result.success = problem.evaluate(candidate)
    result.candidate = candidate if result.success else None
    result.elapsed_s = perf_counter() - start
    return result
