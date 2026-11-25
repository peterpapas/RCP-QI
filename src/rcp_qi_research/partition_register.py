"""Controlled comparison of partition-local diffusion and label registers."""

import argparse
import json
from math import asin, pi, sqrt
from pathlib import Path
from time import perf_counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector, partial_trace

from .problems import EqualityProblem
from .search import _diffuse

VARIANTS = ("standard", "local_partition_diffuser", "oracle_only", "label_before", "label_after", "phase_kickback")


def build_variant(n: int, target: int, iterations: int, variant: str) -> QuantumCircuit:
    """All variants use the same verification phase oracle once per iteration."""
    if n < 2 or iterations < 0 or variant not in VARIANTS:
        raise ValueError("invalid n, iterations, or variant")
    extra = variant in ("label_before", "label_after", "phase_kickback")
    circuit = QuantumCircuit(n + int(extra))
    data = list(range(n))
    for qubit in data:
        circuit.h(qubit)
    if variant == "label_before":
        circuit.cx(n - 1, n)
    elif variant == "phase_kickback":
        circuit.x(n)
        circuit.h(n)
        circuit.cx(n - 1, n)

    oracle = EqualityProblem(n, target)
    for _ in range(iterations):
        oracle.phase_oracle(circuit, data)
        if variant == "local_partition_diffuser":
            _diffuse(circuit, [n - 1])
        elif variant != "oracle_only":
            _diffuse(circuit, data)
    if variant == "label_after":
        circuit.cx(n - 1, n)
    return circuit


def _trace_distance(left: np.ndarray, right: np.ndarray) -> float:
    return float(sum(abs(np.linalg.eigvalsh(left - right))) / 2)


def run_register_experiment(output_dir: Path, *, min_n: int = 2, max_n: int = 6) -> dict:
    if min_n < 2 or max_n < min_n:
        raise ValueError("invalid qubit range")
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    pairs = []
    for n in range(min_n, max_n + 1):
        size = 2**n
        theta = asin(1 / sqrt(size))
        near_peak = max(1, round(pi / (4 * theta) - 0.5))
        for r in sorted({0, 1, near_peak}):
            for variant in VARIANTS:
                reduced = {}
                for target in (0, size - 1):
                    start = perf_counter()
                    circuit = build_variant(n, target, r, variant)
                    state = Statevector.from_instruction(circuit)
                    probabilities = state.probabilities()
                    data_probabilities = np.zeros(size)
                    for basis, probability in enumerate(probabilities):
                        data_probabilities[basis % size] += probability
                    correct_half = data_probabilities[: size // 2] if target == 0 else data_probabilities[size // 2 :]
                    physical = transpile(circuit, basis_gates=["u", "cx"], optimization_level=0)
                    ancilla_density = None
                    ancilla_one = None
                    if circuit.num_qubits > n:
                        rho = partial_trace(state, list(range(n))).data
                        reduced[target] = rho
                        ancilla_density = [[(float(z.real), float(z.imag)) for z in line] for line in rho]
                        ancilla_one = float(rho[1, 1].real)
                    rows.append(
                        {
                            "n": n,
                            "N": size,
                            "iterations": r,
                            "variant": variant,
                            "target": target,
                            "correct_half_probability_from_data": float(sum(correct_half)),
                            "ancilla_one_probability": ancilla_one,
                            "ancilla_density_real_imag": ancilla_density,
                            "phase_oracle_calls": r,
                            "qubits": circuit.num_qubits,
                            "ancillas": circuit.num_qubits - n,
                            "gate_count_before_measurement": sum(physical.count_ops().values()),
                            "depth_before_measurement": physical.depth(),
                            "statevector_and_compilation_s": perf_counter() - start,
                        }
                    )
                if reduced:
                    pairs.append(
                        {
                            "n": n,
                            "N": size,
                            "iterations": r,
                            "variant": variant,
                            "left_vs_right_ancilla_trace_distance": _trace_distance(reduced[0], reduced[size - 1]),
                        }
                    )

    report = {
        "metadata": {
            "scope": "ideal statevector, equality oracle, no correct-partition prior",
            "variants": {
                "standard": "full data-register diffuser",
                "local_partition_diffuser": "diffuser on the most significant data qubit only",
                "oracle_only": "verification phase oracle without a diffuser",
                "label_before": "copy partition bit to ancilla before data-only Grover iterations",
                "label_after": "copy partition bit to ancilla after Grover iterations",
                "phase_kickback": "ancilla in |->, controlled-X from partition bit before Grover iterations",
            },
            "gate_basis": ["u", "cx"],
            "density_format": "each complex entry serialized as [real, imaginary]",
            "no_shots": True,
        },
        "rows": rows,
        "left_right_pairs": pairs,
    }
    (output_dir / "phase2_partition_register.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for variant in ("standard", "local_partition_diffuser", "oracle_only"):
        points = sorted(
            (row["N"], row["correct_half_probability_from_data"])
            for row in rows
            if row["variant"] == variant and row["target"] == 0 and row["iterations"] == 1
        )
        axes[0].plot(*zip(*points), marker="o", label=variant)
    axes[0].axhline(0.5, color="gray", linestyle="--")
    axes[0].set(xlabel="N", ylabel="P(correct half)", title="One oracle call, alternative diffusers")
    axes[0].set_xscale("log", base=2)
    axes[0].grid(alpha=0.2)
    axes[0].legend(fontsize=8)
    for variant in ("label_before", "label_after", "phase_kickback"):
        points = sorted(
            (row["N"], row["left_vs_right_ancilla_trace_distance"])
            for row in pairs if row["variant"] == variant and row["iterations"] == 1
        )
        axes[1].plot(*zip(*points), marker="o", label=variant)
    axes[1].set(xlabel="N", ylabel="trace distance", title="Distinguish target half from ancilla alone")
    axes[1].set_xscale("log", base=2)
    axes[1].set_ylim(-0.03, 1.03)
    axes[1].grid(alpha=0.2)
    axes[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(output_dir / "phase2_partition_register.png", dpi=160)
    plt.close(fig)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    parser.add_argument("--min-n", type=int, default=2)
    parser.add_argument("--max-n", type=int, default=6)
    args = parser.parse_args()
    report = run_register_experiment(args.output_dir, min_n=args.min_n, max_n=args.max_n)
    print(f"Saved {len(report['rows'])} circuit profiles and {len(report['left_right_pairs'])} trace distances")
    print(f"Outputs: {args.output_dir / 'phase2_partition_register.json'} and phase2_partition_register.png")


if __name__ == "__main__":
    main()
