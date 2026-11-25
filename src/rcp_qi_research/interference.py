"""Exact check of the one-Grover-iteration correct-half probability."""

import json
from pathlib import Path
from time import perf_counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from qiskit import transpile
from qiskit.quantum_info import Statevector

from .problems import EqualityProblem
from .search import build_grover_circuit


def analytic_correct_half_probability(n: int) -> float:
    """P = 1/2 + 4/N - 8/N² after one Grover iteration, N=2**n."""
    if n < 1:
        raise ValueError("n must be positive")
    size = 2**n
    return 0.5 + 4 / size - 8 / size**2


def run_one_iteration_experiment(output_dir: Path, *, max_n: int = 8) -> dict:
    if max_n < 2:
        raise ValueError("max_n must be at least 2")
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for n in range(2, max_n + 1):
        size = 2**n
        for target in (0, size - 1):
            start = perf_counter()
            measured, iterations = build_grover_circuit(EqualityProblem(n, target), iterations=1)
            bare = measured.remove_final_measurements(inplace=False)
            logical = transpile(bare, basis_gates=["u", "cx"], optimization_level=0)
            probabilities = Statevector.from_instruction(bare).probabilities()
            half = slice(0, size // 2) if target < size // 2 else slice(size // 2, size)
            rows.append(
                {
                    "n": n,
                    "N": size,
                    "target": target,
                    "correct_half": "left" if target < size // 2 else "right",
                    "analytic_probability": analytic_correct_half_probability(n),
                    "statevector_probability": float(sum(probabilities[half])),
                    "absolute_error": abs(float(sum(probabilities[half])) - analytic_correct_half_probability(n)),
                    "quantum_oracle_calls": iterations,
                    "circuit_builds": 1,
                    "qubits": n,
                    "ancillas": 0,
                    "gate_count_before_measurement": sum(logical.count_ops().values()),
                    "depth_before_measurement": logical.depth(),
                    "measurement_operations_if_sampled": n,
                    "statevector_evaluation_s": perf_counter() - start,
                }
            )

    result = {
        "description": "Exact, noiseless statevector check; no shots or physical measurements were performed.",
        "formula": "P(correct half) = 1/2 + 4/N - 8/N^2, N = 2^n",
        "rows": rows,
    }
    (output_dir / "one_iteration.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    right = [row for row in rows if row["correct_half"] == "right"]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot([row["N"] for row in right], [row["analytic_probability"] for row in right], label="analytic", linewidth=2)
    ax.scatter([row["N"] for row in right], [row["statevector_probability"] for row in right], label="statevector", zorder=3)
    ax.axhline(0.5, color="gray", linestyle="--", label="uninformed half")
    ax.set(xlabel="search-space size N", ylabel="P(correct half)", title="One Grover iteration")
    ax.set_xscale("log", base=2)
    ax.set_ylim(0.45, 1.05)
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "one_iteration.png", dpi=160)
    plt.close(fig)
    return result
