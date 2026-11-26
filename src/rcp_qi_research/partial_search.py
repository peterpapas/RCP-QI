"""Post-publication control: established global/local/global partial search.

This implements the sequence in Korepin (quant-ph/0503238), Eq. (13), for
two equal blocks. Schedules depend on N and a requested confidence, never on
the marked address. It is a generic equality-oracle query control, not a SAT
algorithm or a new RCP-QI operator.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from math import asin, ceil, pi, sin, sqrt
from pathlib import Path
from time import perf_counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector

from .problems import EqualityProblem
from .search import _diffuse

THRESHOLDS = (0.90, 0.95, 0.99)


@dataclass(frozen=True)
class Schedule:
    global_before: int
    local: int
    final_global: int = 1

    @property
    def phase_oracle_calls(self) -> int:
        return self.global_before + self.local + self.final_global


def apply_partition_bit_only_reflection(circuit: QuantumCircuit, n: int) -> None:
    """Historical V3 control: reflect on the most significant qubit only."""
    _diffuse(circuit, [n - 1])


def apply_intra_block_diffusion(circuit: QuantumCircuit, n: int) -> None:
    """Direct-sum diffusion on the lower n-1 qubits of both halves."""
    if n < 2:
        raise ValueError("partial search requires at least two data qubits")
    _diffuse(circuit, list(range(n - 1)))


def apply_global_diffusion(circuit: QuantumCircuit, n: int) -> None:
    """Diffusion over every address qubit."""
    _diffuse(circuit, list(range(n)))


def build_partial_search_circuit(
    n: int, target: int, schedule: Schedule, *, measure_partition: bool = False
) -> QuantumCircuit:
    """Prepare uniform state, then apply G_global G_local^j2 G_global^j1.

    The equality target is encoded only in the benchmark oracle. The schedule
    does not inspect it. One full-register phase oracle is charged per step.
    """
    if n < 2 or not 0 <= target < 2**n or schedule.global_before < 0 or schedule.local < 0 or schedule.final_global != 1:
        raise ValueError("invalid partial-search arguments")
    circuit = QuantumCircuit(n, int(measure_partition))
    data = list(range(n))
    for qubit in data:
        circuit.h(qubit)
    oracle = EqualityProblem(n, target)
    for _ in range(schedule.global_before):
        oracle.phase_oracle(circuit, data)
        apply_global_diffusion(circuit, n)
    for _ in range(schedule.local):
        oracle.phase_oracle(circuit, data)
        apply_intra_block_diffusion(circuit, n)
    oracle.phase_oracle(circuit, data)
    apply_global_diffusion(circuit, n)
    if measure_partition:
        circuit.measure(n - 1, 0)
    return circuit


def analytic_probabilities(n: int, schedule: Schedule) -> tuple[float, float]:
    """Exact finite-N three-amplitude recurrence for this fixed sequence.

    Amplitudes are per basis state: target, other states in its half, and
    states in the other half. All states in each category stay symmetric.
    The global phase of Qiskit's diffuser is immaterial to probabilities.
    """
    if n < 2 or schedule.global_before < 0 or schedule.local < 0 or schedule.final_global != 1:
        raise ValueError("invalid analytic schedule")
    size = 2**n
    block = size // 2
    marked = same = other = 1 / sqrt(size)
    for _ in range(schedule.global_before):
        marked = -marked
        mean = (marked + (block - 1) * same + block * other) / size
        marked, same, other = 2 * mean - marked, 2 * mean - same, 2 * mean - other
    for _ in range(schedule.local):
        marked = -marked
        mean = (marked + (block - 1) * same) / block
        marked, same = 2 * mean - marked, 2 * mean - same
    marked = -marked
    mean = (marked + (block - 1) * same + block * other) / size
    marked, same = 2 * mean - marked, 2 * mean - same
    return marked**2 + (block - 1) * same**2, marked**2


def best_schedule(n: int, threshold: float, *, max_queries: int | None = None) -> tuple[Schedule, float]:
    """Minimum queries in the nonnegative global/local/final-global family.

    All integer pairs with smaller total cost are enumerated. The tie-breaker
    maximizes half probability, then minimizes initial global iterations.
    No marked-address data or circuit outcomes enter schedule selection.
    """
    if n < 2 or not 0.5 < threshold < 1:
        raise ValueError("invalid size or confidence threshold")
    bound = max_queries if max_queries is not None else ceil(pi * sqrt(2**n) / 4) + 3
    for calls in range(1, bound + 1):
        candidates = []
        for global_before in range(calls):
            schedule = Schedule(global_before, calls - 1 - global_before)
            probability, _ = analytic_probabilities(n, schedule)
            if probability + 1e-12 >= threshold:
                candidates.append((probability, -global_before, schedule))
        if candidates:
            probability, _, schedule = max(candidates, key=lambda row: row[:2])
            return schedule, probability
    raise RuntimeError(f"no schedule reaches {threshold} within {bound} calls")


def korepin_two_block_asymptotic_schedule(n: int) -> Schedule:
    """Rounded K=2 large-block schedule from Korepin (2005), Eq. (18).

    It has no initial global iterations and about pi/4*sqrt(N/2) local
    iterations, followed by one global iteration. Rounding is a finite-N
    implementation choice, not the paper's exact finite-N optimum.
    """
    if n < 2:
        raise ValueError("partial search requires at least two qubits")
    return Schedule(0, int(pi * sqrt(2 ** (n - 1)) / 4 + 0.5))


def full_grover_half_probability(n: int, iterations: int) -> float:
    """V2's analytic one-shot half probability, independently restated."""
    size = 2**n
    theta = asin(1 / sqrt(size))
    marked = sin((2 * iterations + 1) * theta) ** 2
    return (size - 2 + size * marked) / (2 * (size - 1))


def build_full_grover_half_circuit(n: int, target: int, iterations: int) -> QuantumCircuit:
    """Matched V2 control: full-space Grover, then measure one half-label bit."""
    if n < 2 or not 0 <= target < 2**n or iterations < 0:
        raise ValueError("invalid Grover comparator")
    circuit = QuantumCircuit(n, 1)
    data = list(range(n))
    for qubit in data:
        circuit.h(qubit)
    oracle = EqualityProblem(n, target)
    for _ in range(iterations):
        oracle.phase_oracle(circuit, data)
        apply_global_diffusion(circuit, n)
    circuit.measure(n - 1, 0)
    return circuit


def run_comparison(output_dir: Path, *, sizes: tuple[int, ...] = (4, 6, 8, 9)) -> dict:
    """Write a new correction artifact without touching V1–V10 results."""
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"refusing to replace existing correction artifacts: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    thresholds = []
    for n in sizes:
        size = 2**n
        for threshold in THRESHOLDS:
            schedule, analytic = best_schedule(n, threshold)
            v2_calls = next(r for r in range(size) if full_grover_half_probability(n, r) + 1e-12 >= threshold)
            v2_physical = transpile(build_full_grover_half_circuit(n, 0, v2_calls), basis_gates=["u", "cx"], optimization_level=0)
            thresholds.append({"n": n, "N": size, "threshold": threshold, "partial_calls": schedule.phase_oracle_calls,
                               "global_before": schedule.global_before, "local": schedule.local, "final_global": 1,
                               "partial_analytic_probability": analytic, "v2_full_grover_calls": v2_calls,
                               "v2_gate_count_with_partition_measurement": sum(v2_physical.count_ops().values()),
                               "v2_depth_with_partition_measurement": v2_physical.depth()})
            targets = sorted({0, 1, size // 2 - 1, size // 2, size - 1})
            for target in targets:
                start = perf_counter()
                circuit = build_partial_search_circuit(n, target, schedule)
                build_s = perf_counter() - start
                start = perf_counter()
                state = Statevector.from_instruction(circuit)
                statevector_s = perf_counter() - start
                probabilities = state.probabilities()
                half = target // (size // 2)
                actual = float(np.sum(probabilities[half * (size // 2):(half + 1) * (size // 2)]))
                marked = float(probabilities[target])
                measured = build_partial_search_circuit(n, target, schedule, measure_partition=True)
                start = perf_counter()
                physical = transpile(measured, basis_gates=["u", "cx"], optimization_level=0)
                transpile_s = perf_counter() - start
                predicted, predicted_marked = analytic_probabilities(n, schedule)
                rows.append({"n": n, "N": size, "threshold": threshold, "target": target,
                             **asdict(schedule), "phase_oracle_calls": schedule.phase_oracle_calls,
                             "partition_probability_analytic": predicted, "partition_probability_statevector": actual,
                             "solution_probability_analytic": predicted_marked, "solution_probability_statevector": marked,
                             "qubits": circuit.num_qubits, "ancillas": 0, "state_preparations": 1,
                             "partition_measurements": 1, "shots": 0, "verification_calls": 0,
                             "transpiled_gate_count_with_measurement": sum(physical.count_ops().values()),
                             "transpiled_depth_with_measurement": physical.depth(),
                             "circuit_construction_s": build_s, "statevector_s": statevector_s,
                             "transpilation_s": transpile_s})
    report = {"metadata": {"id": "POSTPUB-PARTIAL-SEARCH-20261127", "model": "ideal equality phase oracle, unique marker, two balanced blocks",
                           "sequence": "global_before, local-in-each-block, one final global",
                           "schedule": "minimum query count within enumerated nonnegative integer schedules; threshold at least target",
                           "schedule_target_independent": True, "oracle_per_iteration": 1,
                           "simulator": "Qiskit Statevector; no hardware or sampled shots",
                           "gate_basis": ["u", "cx"], "transpile_optimization_level": 0,
                           "limitations": "equality-oracle target is an input to the test fixture; no explicit SAT circuit, noise or fault-tolerance cost"},
              "thresholds": thresholds, "rows": rows}
    (output_dir / "partial_search.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    with (output_dir / "thresholds.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(thresholds[0]))
        writer.writeheader()
        writer.writerows(thresholds)
    fig, axes = plt.subplots(2, 2, figsize=(10, 7), squeeze=False)
    for axis, n in zip(axes.flat, sizes):
        limit = max(row["v2_full_grover_calls"] for row in thresholds if row["n"] == n)
        calls = list(range(1, limit + 1))
        partial = [max(analytic_probabilities(n, Schedule(g, q - 1 - g))[0] for g in range(q)) for q in calls]
        v2 = [full_grover_half_probability(n, q) for q in calls]
        axis.plot(calls, partial, marker="o", markersize=3, label="best global/local/final global")
        axis.plot(calls, v2, marker="x", markersize=3, label="V2 full Grover")
        axis.set(xlabel="Phase-oracle calls", ylabel="Correct-half probability", title=f"N={2**n}", ylim=(0.45, 1.03))
        axis.grid(alpha=0.25)
    axes[0, 0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(output_dir / "accuracy_vs_queries.png", dpi=150)
    plt.close(fig)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("results/corrections/partial_search_20261127"))
    parser.add_argument("--sizes", type=int, nargs="+", default=[4, 6, 8, 9])
    args = parser.parse_args()
    report = run_comparison(args.output_dir, sizes=tuple(args.sizes))
    print(f"Saved {len(report['rows'])} exact statevector comparisons in {args.output_dir}")


if __name__ == "__main__":
    main()
