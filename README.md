# RCP-QI research

> **SUSPENDED — PENDING NEW MATHEMATICAL INSIGHT.** V1–V10 are complete as an unpublished research archive. No V11 or quantum architecture development is authorised. The [executive summary](research/archive/RCPQI_EXECUTIVE_SUMMARY.md), [final research report](research/archive/RCPQI_FINAL_RESEARCH_REPORT.md), [theorem catalogue](research/archive/RCPQI_THEOREM_CATALOGUE.md), [negative-results catalogue](research/archive/RCPQI_NEGATIVE_RESULTS.md), [reproducibility audit](research/archive/RCPQI_REPRODUCIBILITY.md) and [restart protocol](research/archive/RCPQI_RESTART_PROTOCOL.md) are the independent-review entry points.

The project has **no proof of P = NP or P ≠ NP; no novel quantum computational advantage; no universal impossibility theorem for quantum SAT solving; and no independently established publishable mathematical novelty.** All validated restricted-model findings and experimental evidence are preserved.

An initial, reproducible investigation of **Recursive Complementary Partitioning with Quantum Interference (RCP-QI)**. RCP-QI is an **unproven hypothesis**, not an established quantum speedup. This package compares three explicit baselines on promised unique-solution problems:

**Historical programme:** V1's one-iteration formula is analytically derived and numerically validated; V2–V4 and V6 contain costed controls and negative results. V5.1 extends the **classical** structural benchmark to held-out 8–512-variable families and 1,024/2,048-variable tractable controls. Some adaptive strategies improve arbitrary prefix search on selected harder cases, but none show an advantage over direct modern SAT solving in these data. V7/V7.1 shift to [structural promise discovery](research/v7_1_structural_promise_discovery.md): conditional complement/quotient characterizations, partial-complement and algebraic-residual counterexamples, and original-source comparisons find no justified new quantum operator. Lean proves stated abstract properties, not a speedup or Qiskit correspondence. See the [V5.1 findings](research/v5_1_findings.md), [experiment registry](research/experiment_registry.md), [formal status](theory/formal_status.md), [literature review](research/literature_review.md), and [negative results](research/negative_results.md).

**V8 theory decision:** The [source audit and final report](research/v8/V8_FINAL_REPORT.md) examine the November 2026 VP–VNP claims as unaccepted research claims, reconstruct their arithmetic proof mechanisms and identify a formal-polynomial versus Boolean transfer barrier. No mathematically justified quantum operator or V8 experiment emerged. The primary recommendation is a scoped lower-bound/impossibility investigation, with V8 circuit implementation suspended.

**V9 theory decision:** The [V9 final report](research/v9/V9_FINAL_REPORT.md) defines an exact symbolic partition model and shows that a perfect-matching CNF produces the permanent as its full generating polynomial while each partition-existence decision is polynomial-time matching. Boolean-ideal equivalence prevents raw formal-expression measures from directly lower-bounding Boolean verifiers, and a standard adversary argument gives `Θ(√N)` black-box queries for a unique-marker half label. These are scoped findings; the VP–VNP claims remain conditional premises, and no new quantum operator is authorized. [Decision brief](research/v9/V9_DECISION_BRIEF.md).

**V10 research decision:** The [bounded theorem screen](research/v10/V10_FINAL_REPORT.md) selected two candidates: distributed unit-clause SAT reduces to known set disjointness, and original-clause-certified recursive elimination reduces to known tree-like resolution. Lean checks the Boolean reductions and certificate soundness; neither gives a general SAT/quantum lower bound or a novel operator. The [decision brief](research/v10/V10_DECISION_BRIEF.md) recommends suspending active RCP-QI development until a genuinely new, model-preserving mathematical insight is identified.

1. Classical exhaustive search over `0, ..., 2^n - 1`.
2. Grover search over the full space, with measured and classically verified candidates.
3. Recursive partition search. At each bit, a measured Grover subroutine probes the left half; a verified hit selects left, otherwise the traversal selects right. The final leaf is verified. This is a concrete, costed interpretation of a partition-existence test, **not** a free coherent partition oracle. A hit already reveals a witness, so deliberately continuing the partition traversal is inefficient; the experiment keeps it to measure the proposed recursive structure.

## Objective and handover

The motivating question is whether quantum interference combined with the *internal constraint structure* of an NP-complete problem can eliminate entire partitions of an exponentially large solution space at a cost below generic unstructured search. The immediate objective is a rigorous experimental framework, not a claim about P vs NP. A polynomial-time quantum algorithm for NP-complete problems would show \(\mathrm{NP}\subseteq\mathrm{BQP}\); it would not, by itself, establish classical \(\mathrm{P}=\mathrm{NP}\).

The idea evolved as follows:

1. Pair individual candidates so exactly one in each pair is valid. Evaluating one would determine the other: \(f(a)\oplus f(b)=1\).
2. Arbitrary candidates cannot generally be paired this way without knowing their answers. Repeated elimination can also destroy the proposed pairwise complementarity.
3. Move complementarity to **disjoint, exhaustive partitions**. Under a unique-solution promise, exactly one of two halves contains the solution.
4. Recursively ask whether the left partition contains a solution, then retain that half or its complement. The central unsolved step is implementing this existence decision efficiently and reliably.
5. Investigate whether constraint-aware quantum interference can amplify the successful partition and suppress the other without hiding the work in an oracle.

Conceptually, with implicit partitions and a reliable existence procedure:

```python
def rcp_qi(space):
    if space.size == 1:
        return space.only_candidate
    left, right = space.halve()
    if quantum_exists(left):
        return rcp_qi(left)
    return rcp_qi(right)
```

This pseudocode assumes the initial space contains exactly one solution. A range or bit prefix represents a partition; it never materializes an exponential candidate list. The implemented baseline uses measured Grover probes and can make a wrong branch decision.

## Reproduce

Requires Python 3.12 and [uv](https://docs.astral.sh/uv/). `uv.lock` fixes package versions.

```powershell
uv sync --python 3.12
uv run pytest
uv run rcp-qi-research --seed 20261125 --trials 4 --max-n 4 --repetitions 3
uv run rcp-qi-phase2 --min-n 2 --max-n 8 --seed 20261125 --shots 256 --sample-seeds 2
uv run rcp-qi-register --min-n 2 --max-n 6
uv run rcp-qi-sat --seed 20261125 --trials 4 --max-attempts 12
uv run rcp-qi-recursive --min-n 2 --max-n 5 --seed 20261125 --trials 3 --max-restarts 2
uv run rcp-qi-structural --seed 20261126 --seed-count 3
uv run python scripts/validate_v51.py --run-dir results/raw/v5_1_heldout_20261126
uv run ruff check src tests scripts
uv run python scripts/validate_results.py
uv run python scripts/build_processed_summary.py
uv run jupyter lab notebooks
```

The experiment writes `results/initial.json` (metadata, raw trials, and aggregate success/resource metrics), `results/initial.csv` (raw trials), and `results/scaling.png`. It also writes `results/one_iteration.json` and `results/one_iteration.png` to check the exact correct-half probability after one Grover iteration. Equality targets are spread across the search space and their order is seeded. The notebook reads and plots the generated data. `--output-dir` can direct outputs elsewhere.

The separate Phase 2 command preserves those v1 artifacts. It writes `results/phase2_multi_iteration.json`, `results/phase2_thresholds.csv`, `results/phase2_accuracy_vs_queries.png`, and `results/phase2_threshold_costs.png`.

### Formal verification environment

Install [Elan](https://lean-lang.org/install/manual/), then use the pinned Lean 4.36.0 project:

```powershell
cd formal/lean
lake build
lake env lean RCPQI/AxiomAudit.lean
```

The first proofs use Lean's bundled library, so Mathlib is not needed yet. On this Windows workspace, Elan was installed without changing PATH; use `~/.elan/bin/lake.exe` if `lake` is not found. The [Lean README](formal/lean/README.md) and [formal status table](theory/formal_status.md) identify precisely what is proven and what remains open.

## Mathematical model and accounting

The search space has size \(N=2^n\), with **exactly one** satisfying assignment in the current experiments. Candidate verification is \(f(x)\in\{0,1\}\). Partition existence is \(G(S)=\bigvee_{x\in S}f(x)\); for disjoint, exhaustive halves \(A,B\), the unique-solution promise gives \(G(A)\oplus G(B)=1\). Starting from a uniform superposition, the phase oracle is \(U_f|x\rangle=(-1)^{f(x)}|x\rangle\). The desired future construction would transfer information about \(G(S)\) to a partition register through interference while accounting for all its operations.

The equality oracle uses bit flips and a multi-controlled phase. The CNF oracle computes every clause into a work qubit, phases on all clauses being true, and uncomputes the work qubits. The first sample CNF is an implication chain \(x_1 \land (\neg x_1\lor x_2) \land (\neg x_2\lor x_3)\), whose only solution is `111`. The handover's second sample is \((a\lor b)\land(\neg b\lor c)\land\neg a\land c\), with unique assignment \(abc=011\). In the package, `a` is variable 1 and the least-significant bit, so this assignment is integer `6` and Qiskit's displayed bitstring is `110`. The algorithm is given each formula, **not** a precomputed list of solutions.

### One-iteration interference check

For a unique marked solution in a uniform state, one full Grover iteration gives the marked basis state amplitude \((3-4/N)/\sqrt N\) and each unmarked amplitude \((1-4/N)/\sqrt N\), up to a common global phase. The half containing the solution therefore has probability

\[
P(\text{correct half}) = \frac12 + \frac4N - \frac8{N^2}.
\]

This is `1` for \(N=4\), then approaches `1/2` as \(N\) grows. `one_iteration.json` compares that formula with exact, noiseless Qiskit statevector probabilities for targets in both halves over \(N=4,8,\ldots,256\). It records the circuit's oracle call, qubits, gate count, depth, and simulation time. This is an exact probability calculation, **not** a shot-based hardware measurement or a partition-existence algorithm.

For a partition of size \(M\) with one solution, \(r\) Grover iterations give ideal single-shot success
\(p=\sin^2((2r+1)\arcsin(1/\sqrt M))\). We choose the nearest integer to \(\pi/(4\arcsin(1/\sqrt M))-1/2\), using only the unique-solution promise and partition size. With `t` independent measured attempts, detection probability is \(1-(1-p)^t\). An empty partition gives no verified hit. A missed hit can send RCP-QI down the wrong branch; there is no backtracking in this baseline. Multiple solutions and unknown counts need a different iteration schedule or counting method and are outside this first experiment.

Each actual circuit execution includes initial-state preparation, its Grover iterations, and measurement. A candidate check is a separate classical predicate evaluation. Results report `quantum_oracle_calls` (one phase oracle per Grover iteration), `verification_calls`, `classical_evaluations`, their sum `total_predicate_queries`, `circuit_executions`, `state_preparations`, `measurements`, circuit builds, total transpiled gate count, summed and maximum transpiled depth, and wall-clock time. Circuits are decomposed into Qiskit `u` and `cx` gates at optimization level 0 for a reproducible logical basis; measurement is also counted as an operation. The cost of preparing, constructing, transpiling, simulating, and verifying is included in observed elapsed time. Circuit builds are counted separately because compilation has no hardware-independent gate-equivalent cost. The JSON records both per-trial values and mean resources, empirical success probability, and 95% Wilson intervals.

Classical exhaustive search takes at most \(N=2^n\) predicate evaluations and averages \((N+1)/2\) for uniformly located unique solutions. Grover uses \(\Theta(\sqrt N)=\Theta(2^{n/2})\) phase queries for constant success. RCP-QI makes \(n\) partition decisions, but **decision count is not runtime**. If \(C(k)\) is the full cost of deciding a partition with \(2^k\) candidates, including quantum operations, state preparation, measurements, verification, and error-control repetitions, then \(T(n)=\sum_{k=1}^{n}C(k)\). A polynomial \(C(k)\) would imply a polynomial sum, but such a generic partition-existence procedure is exactly what remains unproved.

Testing one half at each recursive level with Grover costs a geometric sum \(\sum_{j=1}^{n}O(\sqrt{N/2^j})=O(\sqrt N)\) phase queries for fixed repetitions, plus measurements and verification. This implementation therefore offers **no asymptotic improvement over Grover**. A hypothetical constant-cost exact partition-existence oracle for arbitrary unstructured search would conceal the search cost and conflict with the standard black-box lower bound of \(\Omega(\sqrt N)\) quantum queries for bounded-error search [1, 2]. Any proposal that improves the bound must identify exploitable structure or a different oracle model and include its implementation cost.

## Theoretical obstacles

- Recursive partitioning and SAT self-reduction are established ideas. Any potential novelty must lie in the quantum partition decision and its cost.
- A superposition does not make all candidate answers simultaneously readable. Deutsch's algorithm distinguishes constant from balanced one-bit functions under its promise, but does not reveal which of two candidates is true when the outputs differ.
- The unique-solution complement rule fails on zero-solution and multiple-solution spaces. Those cases need explicit treatment, including false positives, false negatives, and confidence control.
- An ideal partition oracle is useful as a conceptual control, never as evidence of a speedup. The promising direction is to exploit internal constraint structure rather than treat verification as an unstructured black box.

## Experimental roadmap

| Version | Investigation | Status |
| --- | --- | --- |
| v0 | Ideal partition oracle as a conceptual control | Documented only; not used as a performance result |
| v1 | Standard phase oracle and one-iteration interference | Implemented and checked analytically/numerically |
| v2 | Multi-iteration and partition-specific amplification controls | Multi-iteration benchmark and local-diffuser negative control completed |
| v3 | Entangled partition registers | Initial before/after and kickback controls completed; no advantage shown |
| v4 | Constraint-aware quantum interference | Clause-built SAT and unit-propagation controls completed; useful operator remains open |
| v5 | Adaptive partitioning from mathematical structure | Seven classical strategies and direct PySAT control benchmarked; a justified quantum operator remains open |
| v5.1 | Extended structural partitioning | Held-out classical scaling through 512 variables, larger tractable controls, timeout-aware comparisons and public SAT stress cases completed; no direct-CDCL crossover observed |
| v6 | End-to-end recursive benchmarking | Initial confidence/restart benchmark completed |
| v7 | Structural complementarity | Transformation and quotient characterizations, counterexamples, verified literature and Lean proofs; no justified V8 operator |
| v7.1 | Structural promise discovery | Partial complementarity, affine/nonlinear residual, MQ and oracle-promise screen completed; V8 remains suspended |
| v8 | Algebraic complexity and transfer audit | Public VP–VNP claims authenticated but not independently accepted; formal-to-Boolean transfer barrier and scoped Lean counterexample; decision D |
| v9 | Boolean-ideal and query-transfer audit | Permanent-generating CNF versus easy matching decision; Boolean-invariant screen and black-box half-label bound; no circuit or general SAT lower bound; decision D |
| v10 | Boolean-invariant and proof-complexity screen | Distributed unit CNF/disjointness and conflict-tree/resolution reductions; Lean soundness; no original theorem or new circuit; active development suspended |

V5/V5.1 compare prefix, occurrence, connectivity, propagation lookahead, symmetry scoring, residual score, and Jeroslow–Wang branching with direct Glucose4/CaDiCaL, DPLL and dedicated tractable-family algorithms. The partition-existence calls are **classical PySAT calls**. V5.1 found a limited branch-choice gain over prefix on 256-variable random 3-SAT, but no observed gain over direct CDCL. The [protocol](experiments/v5_1_extended/README.md) and [findings](research/v5_1_findings.md) give reproducible commands, full costs and limits. Future work needs more independent hard instances and a property-derived quantum operator compared with matched quantum backtracking and Grover costs. Negative results remain part of the record.

V7 challenges the recursive architecture itself. A supplied total validity-complementing map already produces a witness with one classical verifier call; a supplied validity-preserving quotient yields the same existence answer and query access on quotient representatives. Certifying semantic validity preservation for even a supplied bit flip can encode UNSAT. The [mathematical review](research/v7_mathematical_review.md) separates those conditional results from open questions about finding useful structure in explicit SAT instances. No speculative circuit was added.

V7.1 extends that screen to [partial complementarity and structural promises](research/v7_1_structural_promise_discovery.md). A locally complementing region with an accessible point is also classically one-query sufficient; flipping an individual constraint can leave arbitrary 3-SAT difficulty. Simon, Shor and hidden-shift algorithms rely on stronger oracle promises, while affine elimination and bounded-width hypergraph structure already have classical uses. V8 remains suspended until a concrete promise passes the full operator cost gate.

**Central question:** Can an NP-complete problem's internal constraints be encoded into a quantum interference operator that reliably decides whether a partition contains a satisfying assignment without exponential computational cost?

## Phase 2: multi-iteration benchmark

This first Phase 2 increment uses the **same full-space Grover operator** as v1. It sweeps the number \(r\) of phase-oracle calls, without introducing a new partition operator. For one marked state, let \(\theta=\arcsin(1/\sqrt N)\). The exact solution probability after \(r\) iterations is

\[
P_{\mathrm{sol}}(r)=\sin^2((2r+1)\theta).
\]

All \(N-1\) unmarked basis states have equal probability \((1-P_{\mathrm{sol}})/(N-1)\). Hence the half containing the marked item has

\[
P_{\mathrm{half}}(r)=P_{\mathrm{sol}}(r)+\left(\frac N2-1\right)\frac{1-P_{\mathrm{sol}}(r)}{N-1}
=\frac{N-2+N P_{\mathrm{sol}}(r)}{2(N-1)}.
\]

At \(r=1\), this reduces to the validated v1 formula. To reach a fixed one-shot correct-half probability \(q>1/2\), the same symmetric circuit needs \(P_{\mathrm{sol}}\ge 2q-1+2(1-q)/N\). A constant-confidence partition decision therefore requires substantial exact-solution amplification and \(\Theta(\sqrt N)\) generic phase queries. Repeating **only the partition-bit measurement** after one iteration starts with bias \(P_{\mathrm{half}}-1/2=4/N-8/N^2\); independent majority sampling needs \(\Theta(N^2)\) shots for a fixed confidence above 1/2. Each such shot repeats the state preparation, oracle, diffuser, and measurement.

The benchmark reports the first single-shot iteration count for 90%, 95%, and 99% confidence. It also minimizes total calls within two precisely defined fixed-iteration protocols: odd-shot majority of partition bits, and independent Grover samples followed by classical candidate verification, accepting any verified candidate. For Grover, the reported total includes one classical verification call per planned shot. The minimization starts from a feasible one-shot cost bound, then exhaustively checks all lower-cost iteration/shot combinations; the single-shot search uses \(r\le4N\). It does not optimize adaptive stopping or arbitrary quantum algorithms.

| \(N\) | Threshold | Partition majority: phase / total calls | Grover verified: phase / total calls |
| ---: | ---: | ---: | ---: |
| 256 | 90% | 9 / 9 | 10 / 11 |
| 256 | 95% | 10 / 10 | 11 / 12 |
| 256 | 99% | 11 / 11 | 12 / 13 |

These are **different tasks**: selecting one half versus producing a verified solution. Completing a recursive search requires further partition decisions, error control, and final verification. The small query-count difference above is not an algorithmic speedup. The cost curves remain consistent with generic Grover scaling. This is a negative result for the idea that full-space Grover interference alone exposes a cheap partition-existence decision.

The saved Phase 2 run covers \(N=4\) through \(256\), multiple marked positions including both half boundaries, and two seeded 256-shot samples per selected circuit. Exact statevector probabilities agree with the analytic values to roughly \(6\times10^{-14}\). Seeded frequencies fluctuate around those probabilities. Each validation records logical phase calls, state preparations, measurements, qubit count, transpiled `u`/`cx` gates and depth per shot, and simulator/compilation time. Repeated-shot resource totals follow from the per-shot counts and the recorded shot count. Simulator time is not quantum runtime.

### Partition-specific operators and an explicit register

`results/phase2_partition_register.json` and its plot compare the standard full diffuser, a diffuser on only the partition bit, and an oracle-only control. The local diffuser leaves \(P(\text{correct half})=1/2\) in every tested setting (\(N=4\)–\(64\), zero, one, and near-peak iteration counts). This is a negative result: a cheaper, partition-local reflection does not amplify the correct half. The oracle-only control likewise changes phase without changing measurement probabilities.

Three ancilla variants expose what the register does and does not reveal. Copying the partition bit **after** Grover gives an ancilla with left/right-target trace distance \(|2P_{\mathrm{half}}-1|\), exactly the existing measurement bias. Copying it **before** data-only Grover leaves the ancilla's reduced density matrix unchanged: \(\mathrm{Tr}_{D}[(U_D\otimes I)\rho(U_D^\dagger\otimes I)]=\mathrm{Tr}_{D}\rho\). A \(|-\rangle\) ancilla used for partition-bit phase kickback also has zero left/right-target trace distance on its own. Reduced density matrices, partition probabilities, oracle calls, qubits, transpiled gates, and depth are saved per circuit. The extra qubit can change Qiskit's multi-control synthesis and gate count, so gate comparisons must include qubit requirements and not be read as a free improvement.

### Structured SAT and recursive completion

`results/phase2_sat.json` compares clause-built reversible CNF oracles with exhaustive search, unit propagation, and a small DPLL implementation. It includes unique-, multiple-, and zero-solution formulas. The quantum baseline uses a seeded, increasing randomized Grover-iteration schedule; it does not receive the solution count. Constraint-aware preparation fixes only variables proven by unit propagation and records literal inspections. A clause-parity phase circuit is an explicit negative control: phasing each violated clause separately marks odd violation parity, **not** the CNF conjunction. Its calls are recorded separately from complete verification-oracle calls, with transpiled gates also reported. On the simple handover formula, unit propagation alone fixes all three variables; that is classical work, not quantum advantage. DPLL solves the five tiny benchmark cases in one to three nodes. On an unsatisfiable formula without unit clauses, a bounded quantum run reports **inconclusive**, while DPLL proves unsatisfiability.

`results/phase2_recursive.json` and its accuracy-versus-query plot contain a confidence-controlled, implicit-prefix traversal. For each possible left-present decision, the shot budget makes its ideal miss probability at most \((1-c)/n\) for a requested per-run confidence \(c\); summing those bounds gives a conservative run-level bound. Every measured probe, candidate verification, failed run, and restart is charged. The true target is used only in an offline decision audit, never in branch selection. The seeded 2–5 qubit experiment had one failed first run and one wrong partition decision, recovered by restart. Its mean total predicate calls exceeded the full-space Grover baseline in every reported group. The small sample and ideal simulator do not establish a general performance ratio. The 99% Grover group at \(N=32\) observed one rare failed shot among nine trials despite its 99.9% ideal single-shot probability; the JSON retains the failure and Wilson intervals.

These controls do not establish useful constraint-aware quantum interference. The remaining open task is an operator whose advantage survives complete oracle, gate, measurement, preprocessing, and end-to-end accounting.

## Repository architecture and research status

Working Python modules remain in `src/rcp_qi_research` to preserve imports and CLI commands. `core/partitions.py` adds a reusable implicit bit-prefix partition. The top-level `experiments/` entries identify implemented protocols; `benchmarks/` documents instances and runners. `results/manifest.json` indexes immutable flat raw files, and `results/processed/` contains a derived Pandas table. `theory/` holds derivations, limitations, and the formal-status table; `formal/lean/` holds machine-checked theorems. `research/` tracks the journal, hypotheses, experiment registry, and negative findings. `paper/` contains an unpublished LaTeX draft. [Architecture details](docs/architecture.md) explain why the existing package and result paths were retained.

The pinned Lean build proves unique-solution partition complementarity, preservation under a reliable existence decision, structural termination and decision count, conditional bitstring correctness, and a cost-sum bound **conditional on a bounded partition-oracle cost**. The V1 and V2 probability formulas remain analytical derivations with statevector checks, not Lean theorems. No efficient partition-existence oracle, polynomial-time NP-complete algorithm, or Lean-to-Qiskit correspondence has been proved.

Python and Lean checks run in separate GitHub Actions workflows. `uv run python scripts/validate_results.py` checks the committed result schema and accounting invariants; it does not re-execute every expensive experiment. The [paper draft](paper/README.md) is not a publication or preprint. `CITATION.cff` uses the author name already present in `pyproject.toml` and contains no DOI. No final license has been selected; public release, external disclosure, and licensing remain subject to author approval.
The [resource accounting contract](docs/resource_accounting.md) defines each cost field and its comparison limits.

## Interpretation limits

- Aer statevector simulation is ideal and noiseless. Its classical runtime scales exponentially with qubit count and is **not** quantum execution time or evidence of hardware advantage.
- The `u`/`cx` counts omit device topology, native gates, routing, error correction, readout error, and fault-tolerant overhead. Transpiled depth is a circuit proxy, not physical latency.
- `total_predicate_queries` adds quantum phase calls and classical checks for transparency; they are not equal-cost operations. Compare the separate columns as well.
- The initial experiment covers only 2–4 qubit equality instances and two three-variable unique-solution CNFs. Four trials per case give a smoke test, not a reliable scaling exponent. Larger instances, more formulas, noise models, and unknown-solution-count methods are future work.
- The equality target is embedded in the circuit generator. This is a standard toy marked-state oracle, but its construction is not a practical black-box database implementation; no hardware speedup follows from it.
- The partition decisions are measured and classical. Interference occurs inside each Grover probe, with no coherent interference across partition levels. A genuinely new coherent RCP-QI construction remains to be specified and costed.
- The CNF chain exposes structure that a specialized classical SAT solver could exploit. The classical comparator here is exhaustive search by design, not the strongest classical SAT baseline.

## Sources

1. Bennett, Bernstein, Brassard, and Vazirani, [*Strengths and Weaknesses of Quantum Computing*](https://arxiv.org/abs/quant-ph/9701001), SIAM Journal on Computing 26 (1997).
2. Zalka, [*Grover's quantum searching algorithm is optimal*](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.60.2746), Physical Review A 60 (1999).
3. [Qiskit documentation](https://quantum.cloud.ibm.com/docs/en/api/qiskit) and [Qiskit Aer documentation](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.AerSimulator.html) for circuit and simulator APIs.
4. Grover, [*A fast quantum mechanical algorithm for database search*](https://arxiv.org/abs/quant-ph/9605043), STOC (1996).
5. Brassard, Høyer, Mosca, and Tapp, [*Quantum Amplitude Amplification and Estimation*](https://arxiv.org/abs/quant-ph/0005055), Contemporary Mathematics 305 (2002).
