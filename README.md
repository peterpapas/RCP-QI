# RCP-QI research

An initial, reproducible investigation of **Recursive Complementary Partitioning with Quantum Interference (RCP-QI)**. RCP-QI is an **unproven hypothesis**, not an established quantum speedup. This package compares three explicit baselines on promised unique-solution problems:

1. Classical exhaustive search over `0, ..., 2^n - 1`.
2. Grover search over the full space, with measured and classically verified candidates.
3. Recursive partition search. At each bit, a measured Grover subroutine probes the left half; a verified hit selects left, otherwise the traversal selects right. The final leaf is verified. This is a concrete, costed interpretation of a partition-existence test, **not** a free coherent partition oracle. A hit already reveals a witness, so deliberately continuing the partition traversal is inefficient; the experiment keeps it to measure the proposed recursive structure.

## Reproduce

Requires Python 3.12 and [uv](https://docs.astral.sh/uv/). `uv.lock` fixes package versions.

```powershell
uv sync --python 3.12
uv run pytest
uv run rcp-qi-research --seed 20261125 --trials 4 --max-n 4 --repetitions 3
uv run jupyter lab notebooks
```

The experiment writes `results/initial.json` (metadata, raw trials, and aggregate success/resource metrics), `results/initial.csv` (raw trials), and `results/scaling.png`. Equality targets are spread across the search space and their order is seeded. The notebook reads and plots the generated data. `--output-dir` can direct outputs elsewhere.

## Mathematical model and accounting

The search space has size \(N=2^n\), with **exactly one** satisfying assignment. The phase oracle is \(O_f|x\rangle=(-1)^{f(x)}|x\rangle\). The equality oracle uses bit flips and a multi-controlled phase. The CNF oracle computes every clause into a work qubit, phases on all clauses being true, and uncomputes the work qubits. The sample CNF is an implication chain \(x_1 \land (\neg x_1\lor x_2) \land (\neg x_2\lor x_3)\), whose only solution is `111`. The algorithm is given the formula, **not** a precomputed list of solutions.

For a partition of size \(M\) with one solution, \(r\) Grover iterations give ideal single-shot success
\(p=\sin^2((2r+1)\arcsin(1/\sqrt M))\). We choose the nearest integer to \(\pi/(4\arcsin(1/\sqrt M))-1/2\), using only the unique-solution promise and partition size. With `t` independent measured attempts, detection probability is \(1-(1-p)^t\). An empty partition gives no verified hit. A missed hit can send RCP-QI down the wrong branch; there is no backtracking in this baseline. Multiple solutions and unknown counts need a different iteration schedule or counting method and are outside this first experiment.

Each actual circuit execution includes initial-state preparation, its Grover iterations, and measurement. A candidate check is a separate classical predicate evaluation. Results report `quantum_oracle_calls` (one phase oracle per Grover iteration), `verification_calls`, `classical_evaluations`, their sum `total_predicate_queries`, `circuit_executions`, `state_preparations`, `measurements`, circuit builds, total transpiled gate count, summed and maximum transpiled depth, and wall-clock time. Circuits are decomposed into Qiskit `u` and `cx` gates at optimization level 0 for a reproducible logical basis; measurement is also counted as an operation. The cost of preparing, constructing, transpiling, simulating, and verifying is included in observed elapsed time. Circuit builds are counted separately because compilation has no hardware-independent gate-equivalent cost. The JSON records both per-trial values and mean resources, empirical success probability, and 95% Wilson intervals.

Classical exhaustive search takes at most \(N\) predicate evaluations and averages \((N+1)/2\) for uniformly located unique solutions. Grover uses \(\Theta(\sqrt N)\) phase queries for constant success. Testing one half at each recursive level with Grover costs a geometric sum \(\sum_{j=1}^{n}O(\sqrt{N/2^j})=O(\sqrt N)\) phase queries for fixed repetitions, plus measurements and verification. This accounting offers **no asymptotic improvement over Grover**. A hypothetical constant-cost exact partition-existence oracle for arbitrary unstructured search would conceal the search cost and conflict with the standard black-box lower bound of \(\Omega(\sqrt N)\) quantum queries for bounded-error search [1, 2]. Any proposal that improves the bound must identify an additional structure or a different oracle model and include its implementation cost.

## Interpretation limits

- Aer statevector simulation is ideal and noiseless. Its classical runtime scales exponentially with qubit count and is **not** quantum execution time or evidence of hardware advantage.
- The `u`/`cx` counts omit device topology, native gates, routing, error correction, readout error, and fault-tolerant overhead. Transpiled depth is a circuit proxy, not physical latency.
- `total_predicate_queries` adds quantum phase calls and classical checks for transparency; they are not equal-cost operations. Compare the separate columns as well.
- The initial experiment covers only 2–4 qubit equality instances and one three-variable unique-solution CNF. Four trials per case give a smoke test, not a reliable scaling exponent. Larger instances, more formulas, noise models, and unknown-solution-count methods are future work.
- The equality target is embedded in the circuit generator. This is a standard toy marked-state oracle, but its construction is not a practical black-box database implementation; no hardware speedup follows from it.
- The partition decisions are measured and classical. Interference occurs inside each Grover probe, with no coherent interference across partition levels. A genuinely new coherent RCP-QI construction remains to be specified and costed.
- The CNF chain exposes structure that a specialized classical SAT solver could exploit. The classical comparator here is exhaustive search by design, not the strongest classical SAT baseline.

## Sources

1. Bennett, Bernstein, Brassard, and Vazirani, [*Strengths and Weaknesses of Quantum Computing*](https://arxiv.org/abs/quant-ph/9701001), SIAM Journal on Computing 26 (1997).
2. Zalka, [*Grover's quantum searching algorithm is optimal*](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.60.2746), Physical Review A 60 (1999).
3. [Qiskit documentation](https://quantum.cloud.ibm.com/docs/en/api/qiskit) and [Qiskit Aer documentation](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.AerSimulator.html) for circuit and simulator APIs.
